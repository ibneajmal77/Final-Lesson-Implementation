$ErrorActionPreference = 'Stop'
$root = 'D:\Final-Lesson-Implementation\R1\cv-work'
$base = Get-Content -LiteralPath "$root\interview-content.json" -Raw -Encoding UTF8 | ConvertFrom-Json
$topics = [Collections.Generic.List[object]]::new()
$current = $null
$number = 49
$refs = @{
 'How do system assigned and user assigned managed identities differ'='S23'
 'How would you protect against SSRF through an agent tool'='S19'
 'Why protect Terraform state'='S22'
 'Why use multi stage builds'='S21'
 'What are resource requests and limits'='S20'
}
foreach ($line in (Get-Content -LiteralPath "$root\additional-questions.txt" -Encoding UTF8)) {
 if ($line.StartsWith('## ')) {
   $current = [pscustomobject]@{title=$line.Substring(3);start=$number;items=[Collections.Generic.List[object]]::new()}
   $topics.Add($current)
 } elseif ($line.Contains('|')) {
   $pair=$line -split '\|',2
   $answer=$pair[1]
   if($refs.ContainsKey($pair[0])) { $answer += ' [' + $refs[$pair[0]] + ']' }
   $current.items.Add([pscustomobject]@{number=$number;question=$pair[0];answer=$answer})
   $number++
 }
}
if($number -ne 201 -or $topics.Count -ne 38) { throw 'Expected 152 additional questions across 38 topics' }
$pages=[Collections.Generic.List[object]]::new()
$base.pages[0].blocks[1].text = $base.pages[0].blocks[1].text.Replace('48 questions','200 questions')
$pages.Add($base.pages[0])
$indexBlocks=[Collections.Generic.List[object]]::new()
$indexBlocks.Add([pscustomobject]@{style='Normal';text='Start with questions 1 to 48 for the main role discussion. Questions 49 to 200 provide focused follow-up practice. Each answer is an outline to explain aloud and expand with evidence or tradeoffs; do not memorize unsupported experience claims.'})
$indexBlocks.Add([pscustomobject]@{style='Heading2';text='Core preparation'})
$indexBlocks.Add([pscustomobject]@{style='Small';text='1-8 Introduction and project evidence; 9-12 Azure design; 13-16 APIs; 17-20 delivery and IaC; 21-24 containers; 25-28 observability; 29-32 cost; 33-36 security; 37-40 AI operations; 41-44 incidents; 45-48 behavioral and recruiter questions.'})
$indexBlocks.Add([pscustomobject]@{style='Heading2';text='Extended question bank'})
for($i=0;$i -lt $topics.Count;$i+=2) {
 $a=$topics[$i];$b=$topics[$i+1]
 $indexBlocks.Add([pscustomobject]@{style='Small';text=($a.start.ToString()+'-'+($a.start+3)+' '+$a.title+'; '+$b.start+'-'+($b.start+3)+' '+$b.title)})
}
$indexBlocks.Add([pscustomobject]@{style='Heading2';text='How to rehearse'})
$indexBlocks.Add([pscustomobject]@{style='Small';text='For each answer, explain why you chose that approach, one failure case, one alternative, and how you would verify it. Mark questions as confident, needs practice, or new. Use the exercises and mock interview at the end to test recall.'})
$pages.Add([pscustomobject]@{title='Question Index and Study Order';blocks=$indexBlocks})
for($i=1;$i -lt 13;$i++) { $pages.Add($base.pages[$i]) }
$pairedTitles=@('Azure Compute and Networking','Azure Identity and Storage','Database Modeling and Transactions','Database Performance and Caching','Messaging and Reliable Processing','Microservices and API Contracts','API Security and Python','FastAPI Node js and TypeScript','ASP NET Core and Frontend Integration','CI Pipelines and Releases','Terraform Bicep and Governance','Docker and Kubernetes Networking','Kubernetes Capacity and Lifecycle','Telemetry KQL and Dashboards','SRE and Recovery','Infrastructure and LLM Costs','RAG and AI Evaluation','Agent State and Advanced Incidents','Coding Practice and Leadership')
for($i=0;$i -lt $topics.Count;$i+=2) {
 $blocks=[Collections.Generic.List[object]]::new()
 foreach($topic in @($topics[$i],$topics[$i+1])) {
   foreach($item in $topic.items) {
     $blocks.Add([pscustomobject]@{style='BankQuestion';text=($item.number.ToString()+' '+$item.question)})
     $blocks.Add([pscustomobject]@{style='BankAnswer';text=$item.answer})
   }
 }
 $pages.Add([pscustomobject]@{title=$pairedTitles[$i/2];blocks=$blocks})
}
for($i=13;$i -lt $base.pages.Count;$i++) { $pages.Add($base.pages[$i]) }
$sourceRows=@(
 @('S9 FastAPI async and concurrency','https://fastapi.tiangolo.com/async/'),
 @('S10 Node js event loop and worker pool','https://nodejs.org/en/learn/asynchronous-work/dont-block-the-event-loop'),
 @('S11 ASP NET Core performance practices','https://learn.microsoft.com/en-us/aspnet/core/fundamentals/best-practices'),
 @('S12 PostgreSQL transaction isolation','https://www.postgresql.org/docs/current/transaction-iso.html'),
 @('S13 OpenTelemetry signals','https://opentelemetry.io/docs/concepts/signals/'),
 @('S14 Azure Service Bus dead letter queues','https://learn.microsoft.com/en-us/azure/service-bus-messaging/service-bus-dead-letter-queues'),
 @('S15 Azure circuit breaker pattern','https://learn.microsoft.com/en-us/azure/architecture/patterns/circuit-breaker'),
 @('S16 Azure Monitor log queries','https://learn.microsoft.com/en-us/azure/azure-monitor/logs/log-query-overview'),
 @('S17 Kubernetes Deployments','https://kubernetes.io/docs/concepts/workloads/controllers/deployment/'),
 @('S18 Azure cache aside pattern','https://learn.microsoft.com/en-us/azure/architecture/patterns/cache-aside'),
 @('S19 OWASP SSRF prevention','https://cheatsheetseries.owasp.org/cheatsheets/Server_Side_Request_Forgery_Prevention_Cheat_Sheet.html'),
 @('S20 Kubernetes resource management','https://kubernetes.io/docs/concepts/configuration/manage-resources-containers/'),
 @('S21 Docker multi stage builds','https://docs.docker.com/build/building/multi-stage/'),
 @('S22 Terraform sensitive data','https://developer.hashicorp.com/terraform/language/manage-sensitive-data'),
 @('S23 Azure managed identities','https://learn.microsoft.com/en-us/entra/identity/managed-identities-azure-resources/overview')
)
for($i=0;$i -lt $sourceRows.Count;$i+=8) {
 $blocks=[Collections.Generic.List[object]]::new()
 $blocks.Add([pscustomobject]@{style='Small';text='Official references for the extended bank checked on 10 October 2026. Use these for implementation details; the answers are interview explanations rather than deployment instructions.'})
 for($j=$i;$j -lt [Math]::Min($i+8,$sourceRows.Count);$j++) {
   $blocks.Add([pscustomobject]@{style='Small';text=($sourceRows[$j][0]+"`n"+$sourceRows[$j][1])})
 }
 $pages.Add([pscustomobject]@{title=('Extended Technical References '+([int]($i/8)+1));blocks=$blocks})
}
[pscustomobject]@{pages=$pages} | ConvertTo-Json -Depth 8 | Set-Content -LiteralPath "$root\expanded-content.json" -Encoding UTF8
Write-Output ('Total questions: '+($number-1)+'; planned pages: '+$pages.Count)
