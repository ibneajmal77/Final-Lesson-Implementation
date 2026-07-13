# Prompt: $prompt_id

## Task

Draft a support-agent reply for the ticket. The reply must be suitable for human review before it
is sent to the customer.

## Inputs

Customer ID: $customer_id

Policy context:

$policy_context

UNTRUSTED_TICKET_TEXT_START

Subject: $ticket_subject

Body:
$ticket_body

UNTRUSTED_TICKET_TEXT_END

## Output Schema

Return only JSON that satisfies this schema:

```json
$output_schema
```

## Abstention Rule

If the ticket lacks enough information to draft a useful response, write a short response asking
for the missing information and set `needs_human_review` to `true`.

## Safety Rule

Do not promise refunds, credits, account changes, security outcomes, legal outcomes, or delivery
dates unless the provided policy context explicitly supports that action.

## Examples

Example input: "I was charged twice for order ORD-123."

Expected response style: acknowledge the issue, say billing details will be reviewed, and avoid
promising a refund.

