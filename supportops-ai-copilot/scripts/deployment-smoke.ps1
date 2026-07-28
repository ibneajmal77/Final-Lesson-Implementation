# ============================================================================
# FILE: scripts/deployment-smoke.ps1
#
# THINK OF THIS FILE AS: the final dress rehearsal after a deployment, proving
# that the cast and backstage machinery can perform one complete scene together.
#
# A "smoke test" is a quick, broad check for obvious breakage. This one does
# more than ask whether the API process is alive: it creates disposable support
# data and walks it through the same API, database, Redis queue, worker, review,
# and reporting path that an agent uses. Unit tests can prove each piece works
# alone; this script proves the deployed pieces can actually find one another.
#
# WHERE IT SITS IN THE REQUEST AND DATA FLOW:
#   operator runs this script after Docker Compose or staging has started
#     -> optional supportops_api.seed creates the local demo tenant
#       -> GET /ready confirms PostgreSQL and Redis can both be reached
#         -> POST /policies creates an AI instruction as a lead
#           -> POST /tickets creates a synthetic customer request as an agent
#             -> POST /analyze saves an AI-run row and queues its ID in Redis
#               -> apps/worker/supportops_worker/jobs.py produces a draft
#                 -> this script polls GET /analysis until that work finishes
#                   -> POST /reviews records a human approval
#                     -> GET /metrics/* proves review and cost reporting can read it
#
# THE HUMAN SAFETY BOUNDARY: an AI recommendation is never treated as sent just
# because analysis succeeded. This script separately records an "approved"
# review through routes/approvals.py. The project has no customer-delivery
# endpoint, so even this automated approval only tests the audit trail; it does
# not send the synthetic reply to anybody.
#
# WHO USES IT / WHAT LIVES HERE: docs/stage-16-local-deployment.md runs it
# against docker-compose.yml; docs/stage-17-staging-deployment.md runs it with
# staging-specific IDs and -SkipSeed. tests/deployment/test_local_deployment_files.py
# checks that this workflow continues to cover every important endpoint.
# ============================================================================
# CmdletBinding turns this script into an "advanced" PowerShell command. That
# enables standard command-line behavior such as named parameters and common
# flags, while `param` below declares this script's own inputs and defaults.
[CmdletBinding()]
param(
    # Everything before an endpoint path. Override this for staging; leaving it
    # unchanged targets the host port published by docker-compose.yml.
    [string]$ApiBaseUrl = "http://127.0.0.1:8765",
    # Every database lookup is restricted to this company ID. The local seed in
    # apps/api/supportops_api/seed.py creates `tenant_demo`.
    [string]$TenantId = "tenant_demo",
    # The identities placed in request headers. dependencies.py currently
    # trusts these values rather than checking a user table, so this verifies
    # role handling and tenant isolation but NOT real login/authentication.
    [string]$AgentUserId = "user_demo_agent",
    [string]$LeadUserId = "user_demo_lead",
    # One shared upper limit for API startup and the queued analysis. A larger
    # staging value allows for slower networks and a real hosted AI provider.
    [int]$TimeoutSeconds = 90,
    # A `switch` is false when omitted and true when its name is present. Staging
    # uses -SkipSeed because its tenant and users should already exist there.
    [switch]$SkipSeed
)

# Most PowerShell command errors are "non-terminating": they print an error but
# let the next line run. `Stop` promotes them to terminating errors so a broken
# request cannot drift onward and finish with a misleading success report.
# Native programs such as `docker` have version-dependent error handling, and
# this script does not explicitly inspect `$LASTEXITCODE`; the HTTP workflow is
# checked strictly, but the seed command is a small remaining weak spot.
$ErrorActionPreference = "Stop"

# Builds the small identity card attached to every protected API request.
# PowerShell functions have their own `param` block; the values supplied after
# `New-Headers` below are bound to these two names before the body runs.
function New-Headers {
    param(
        [string]$UserId,
        [string]$Role
    )

    # A hashtable is a key/value map. Invoke-RestMethod turns these entries into
    # HTTP headers, and get_current_actor in dependencies.py turns them back into
    # an Actor. `$TenantId` comes from the script-level parameter above, so every
    # request in this run stays inside the same tenant's data.
    return @{
        "X-Tenant-Id" = $TenantId
        "X-User-Id" = $UserId
        "X-Role" = $Role
    }
}

# One wrapper for all JSON API calls. Keeping URL construction, headers, and
# body conversion here means every workflow step below behaves consistently.
function Invoke-SupportOpsJson {
    param(
        [string]$Method,
        [string]$Path,
        [hashtable]$Headers,
        # `$null` is PowerShell's "no value" marker. GET requests omit Body;
        # POST requests that need JSON pass a hashtable for it.
        [object]$Body = $null
    )

    # Build the arguments as data first. The quoted URI expands both variables,
    # turning, for example, the base URL plus `/tickets` into one address.
    $parameters = @{
        Method = $Method
        Uri = "$ApiBaseUrl$Path"
        Headers = $Headers
    }
    # Only requests with a body receive JSON and a JSON content type. `-Depth 10`
    # preserves nested objects such as the ticket's metadata; PowerShell's small
    # default depth can otherwise replace deeper values with incomplete text.
    if ($null -ne $Body) {
        $parameters.Body = ($Body | ConvertTo-Json -Depth 10)
        $parameters.ContentType = "application/json"
    }

    # `@parameters` is "splatting": each hashtable entry becomes a named
    # argument to Invoke-RestMethod. That cmdlet also parses the JSON response
    # into a PowerShell object, which is why later code can write `$ticket.id`.
    # With ErrorActionPreference set to Stop, an HTTP 4xx/5xx response aborts
    # the smoke test instead of being mistaken for useful data.
    return Invoke-RestMethod @parameters
}

# Waits for useful service, not merely a listening process. routes/health.py's
# GET /ready checks BOTH PostgreSQL and Redis, so continuing past this function
# means the later database writes and queue hand-off have a chance to work.
function Wait-ForReady {
    # Capture an absolute deadline once. Recomputing "now plus timeout" inside
    # the loop would move the finish line forever and could create an endless wait.
    $deadline = (Get-Date).AddSeconds($TimeoutSeconds)
    # `do ... while` always makes at least one attempt, even when the timeout is
    # zero. That gives an already-ready API a fair immediate check.
    do {
        try {
            $ready = Invoke-RestMethod -Method Get -Uri "$ApiBaseUrl/ready"
            # Checking the JSON field as well as the HTTP success code documents
            # the contract and protects against an accidentally optimistic route.
            if ($ready.status -eq "ready") {
                return
            }
        } catch {
            # Refused connections and readiness's expected HTTP 503 land here
            # while containers are still starting. Ignore them and retry.
            # There is also an unconditional sleep below, so this error path
            # waits about four seconds rather than two; harmless, but uneven.
            Start-Sleep -Seconds 2
        }
        # Polling means asking repeatedly at a modest interval. The pause avoids
        # hammering a service that is already busy starting its dependencies.
        Start-Sleep -Seconds 2
    } while ((Get-Date) -lt $deadline)

    # `throw` creates a terminating error. The deployment is not usable if its
    # dependencies never became ready, so no later workflow step should run.
    throw "API did not become ready within $TimeoutSeconds seconds."
}

# Local Docker starts with empty tables, so create the fixed demo company and
# agent unless the caller explicitly opted out. `-not` flips the switch value.
# The seed module is idempotent, meaning repeated runs leave the same starting
# rows rather than creating duplicates; see apps/api/supportops_api/seed.py.
if (-not $SkipSeed) {
    # `docker compose exec` runs inside the already-running API container, where
    # the package and container-only database address are available. `-T` turns
    # off an interactive terminal, which prevents an automation script from
    # waiting for keyboard input. The pipe displays the seed module's message.
    #
    # This happens BEFORE the readiness loop, so it assumes the API container
    # and database have started. The documented workflow runs this script only
    # after `docker compose up`; Wait-ForReady cannot rescue an earlier seed
    # failure. Use -SkipSeed for staging, whose data is managed separately.
    docker compose exec -T api python -m supportops_api.seed | Write-Host
}

# From here onward all checks use HTTP, so the same workflow can target local
# Docker or a remote staging URL without knowing where its containers live.
Wait-ForReady

# Build two identity cards once and reuse them. policies.py permits only lead or
# admin roles to write AI instructions; ordinary ticket work uses the agent.
$agentHeaders = New-Headers -UserId $AgentUserId -Role "agent"
$leadHeaders = New-Headers -UserId $LeadUserId -Role "lead"
# Ticket external IDs must be unique within a tenant. Including the current
# second keeps normal successive smoke runs from returning an older ticket via
# routes/tickets.py's duplicate-request protection. Two runs launched in the
# same second can still collide, so this is convenient rather than foolproof.
$externalId = "smoke-$(Get-Date -Format yyyyMMddHHmmss)"

# STEP 1: create a company policy as a lead. routes/policies.py stores this text;
# the worker later gathers the tenant's policies and includes them in the AI's
# instructions. The response becomes an object, and its generated ID is kept
# for the final receipt.
#
# PowerShell's trailing backtick continues one command onto the next line. The
# `@{ ... }` body is another hashtable, converted to JSON by the wrapper.
#
# Honest limitation: this script does not delete its synthetic policy or ticket.
# Repeated runs accumulate rows, and policies have no expiry here, so use a
# dedicated smoke tenant or clean it periodically; this matters especially with a real model,
# where repeated policy text increases prompt size and cost.
$policy = Invoke-SupportOpsJson `
    -Method Post `
    -Path "/policies" `
    -Headers $leadHeaders `
    -Body @{
        name = "Smoke refund policy $externalId"
        content = "Agents must verify duplicate charges before promising refunds."
    }

# STEP 2: create the synthetic customer request. Its billing words deliberately
# match the local/staging pilot category in docker-compose.yml and
# infra/staging/env.example, so POST /analyze is allowed through the pilot gate.
$ticket = Invoke-SupportOpsJson `
    -Method Post `
    -Path "/tickets" `
    -Headers $agentHeaders `
    -Body @{
        external_id = $externalId
        channel = "api"
        subject = "Charged twice"
        body = "I was charged twice for order ORD-123."
        customer_id = "customer-smoke"
        # The nested metadata marks this row as test data for anyone inspecting
        # packages/db/supportops_db/models.py or querying the deployment database.
        metadata = @{source = "deployment-smoke"}
    }

# STEP 3: request the asynchronous analysis path in routes/tickets.py. The API
# commits an AIRun "job sheet", places ONLY its ID on Redis, and returns HTTP
# 202 Accepted immediately. apps/worker/supportops_worker/jobs.py later reads
# the ticket and policy from PostgreSQL, calls the configured model, saves a
# recommendation and changes this run's status.
$run = Invoke-SupportOpsJson `
    -Method Post `
    -Path "/tickets/$($ticket.id)/analyze" `
    -Headers $agentHeaders

# Give the background half its own deadline. `$null` is a clear "not seen yet"
# marker; it will be replaced by the matching run returned from the API.
$deadline = (Get-Date).AddSeconds($TimeoutSeconds)
$completedRun = $null
# STEP 4: poll for completion. The queue deliberately makes analysis a separate
# transaction and process, so the first HTTP response cannot contain the final
# answer. Polling is the simple alternative: ask periodically until a terminal
# state appears or the fixed deadline passes.
while ((Get-Date) -lt $deadline) {
    # GET /analysis returns the ticket's ENTIRE run history, not just the job
    # created above. This matters after several smoke tests against one tenant.
    $runs = Invoke-SupportOpsJson `
        -Method Get `
        -Path "/tickets/$($ticket.id)/analysis" `
        -Headers $agentHeaders
    # A PowerShell pipeline passes each returned run through Where-Object. `$_`
    # means "the current item"; only the run ID received from POST /analyze is
    # retained. Select-Object takes one result defensively, even though IDs are
    # unique in packages/db/supportops_db/models.py.
    $completedRun = $runs | Where-Object { $_.id -eq $run.id } | Select-Object -First 1
    # These are the three terminal states driven by worker/jobs.py:
    #   succeeded - the model produced a usable draft
    #   abstained - the model safely declined because it was not confident
    #   failed    - configuration, queue, data, or provider work failed
    # `-and` requires both sides to be true; `-in` asks whether one value appears
    # in the supplied list. Pending and running deliberately keep polling.
    if ($completedRun -and $completedRun.status -in @("succeeded", "abstained", "failed")) {
        break
    }
    # Two seconds is responsive enough for a person without flooding the API or
    # database with tight-loop status reads.
    Start-Sleep -Seconds 2
}

# Distinguish three failures so an operator immediately knows where to look.
# A run missing from the list means the POST response and durable database view
# disagree, which should be impossible after routes/tickets.py commits the row.
if (-not $completedRun) {
    throw "Queued analysis run was not visible through the API."
}
# A recorded worker failure carries a stable error code plus diagnostic detail.
if ($completedRun.status -eq "failed") {
    throw "Queued analysis run failed: $($completedRun.error_code) $($completedRun.error_message)"
}
# If the ID was visible but remained pending/running, the worker may be stopped,
# Redis may not be delivering jobs, or a hosted provider may simply be too slow.
if ($completedRun.status -notin @("succeeded", "abstained")) {
    throw "Queued analysis run did not complete within $TimeoutSeconds seconds."
}

# STEP 5: fetch the saved draft. worker/jobs.py writes a recommendation even
# when the model abstains, because its explanation is still useful to a human.
# GET /recommendations returns every historical suggestion for this ticket.
$recommendations = Invoke-SupportOpsJson `
    -Method Get `
    -Path "/tickets/$($ticket.id)/recommendations" `
    -Headers $agentHeaders
# A fresh smoke ticket normally has exactly one recommendation. This takes the
# first rather than following `$completedRun.output_recommendation_id`; if two
# runs collide on the same second-based external ID, it could select an older
# draft. That is a genuine limitation of this lightweight deployment check.
$recommendation = $recommendations | Select-Object -First 1
if (-not $recommendation) {
    throw "No recommendation was saved for the smoke ticket."
}

# STEP 6: cross the human-review boundary explicitly. In the real console, a
# support agent reads the summary and suggested reply before choosing approved,
# edited, or rejected. Here the approval is automated because the purpose is to
# prove routes/approvals.py and repositories/approvals.py can save the decision.
# It is NOT evidence that a person judged the draft, and it still sends nothing
# to a customer; it only creates the permanent audit record.
$review = Invoke-SupportOpsJson `
    -Method Post `
    -Path "/tickets/$($ticket.id)/recommendations/$($recommendation.id)/reviews" `
    -Headers $agentHeaders `
    -Body @{decision = "approved"; notes = "Deployment smoke approval."}

# STEP 7: prove the reporting queries can read the newly populated tables.
# routes/metrics.py obtains these figures through tenant-filtered repositories:
# reviews reports human decisions; costs reports model usage recorded by the
# worker. The same agent identity may read both endpoints.
$reviewMetrics = Invoke-SupportOpsJson -Method Get -Path "/metrics/reviews" -Headers $agentHeaders
$costMetrics = Invoke-SupportOpsJson -Method Get -Path "/metrics/costs" -Headers $agentHeaders

# Build one tidy receipt instead of dumping every large API response.
# `[PSCustomObject]` turns this hashtable-shaped literal into an object with named
# properties, and ConvertTo-Json makes it easy for a person, log collector, or
# later automation to consume. IDs connect the output back to database rows.
#
# The two counters are tenant-wide totals, not counts scoped to this run. The
# script also prints rather than asserts their values, so it proves the metrics
# endpoints respond but does not rigorously prove this run changed each total.
[PSCustomObject]@{
    # Permanent row IDs from each major stage make failures traceable across the
    # policy, ticket, AI run, recommendation, and human-review tables.
    policy_id = $policy.id
    ticket_id = $ticket.id
    ai_run_id = $completedRun.id
    ai_run_status = $completedRun.status
    recommendation_id = $recommendation.id
    review_id = $review.id
    # Headline operational evidence: how many drafts this tenant has reviewed,
    # and how many recorded model calls it has made in total.
    reviewed_recommendations = $reviewMetrics.reviewed_recommendations
    cost_events = $costMetrics.total_events
} | ConvertTo-Json -Depth 10
