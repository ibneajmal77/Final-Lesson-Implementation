# Atlas AI Platform - Model Routing And Provider Examples

## 1. Purpose

This document makes the model gateway concrete.

The model gateway decides which model/provider to use for each use case, how much cost is allowed, whether reasoning is enabled, whether prompt caching is supported, whether sensitive data may be sent, and which fallback route is allowed.

The JSON examples in this document are bootstrap configuration examples. They use readable keys such as `provider_key`, `route_key`, and `fallback_route_key`. `provider_key` means `model_providers.name`. The database schema stores provider selection as `model_providers.id`, route identity as `model_routes.route_key`, and fallback identity as `model_routes.fallback_route_id` after the config loader resolves them.

## 2. Provider Registry Examples

### 2.1 Managed LLM Provider

```json
{
  "name": "openai_primary",
  "provider_type": "openai_compatible",
  "base_url": "https://api.openai.com/v1",
  "status": "active",
  "capabilities": {
    "supports_chat": true,
    "supports_structured_output": true,
    "supports_streaming": true,
    "supports_tool_calling": true,
    "supports_prompt_caching": true,
    "supports_batch_api": true,
    "supports_reasoning_controls": true,
    "supports_embeddings": true,
    "supports_image_generation": true,
    "supports_audio_input": true,
    "supports_audio_output": true
  },
  "data_policy": {
    "restricted_data_allowed": false,
    "training_usage_allowed": false,
    "region": "provider_default",
    "retention": "provider_policy"
  }
}
```

### 2.2 Enterprise Private Provider

```json
{
  "name": "azure_private_llm",
  "provider_type": "azure_openai",
  "base_url": "https://tenant-resource.openai.azure.com",
  "status": "active",
  "capabilities": {
    "supports_chat": true,
    "supports_structured_output": true,
    "supports_streaming": true,
    "supports_prompt_caching": true,
    "supports_embeddings": true,
    "supports_reasoning_controls": false
  },
  "data_policy": {
    "restricted_data_allowed": true,
    "training_usage_allowed": false,
    "region": "tenant_region",
    "retention": "enterprise_contract"
  }
}
```

### 2.3 Local Open Model Provider

```json
{
  "name": "local_vllm",
  "provider_type": "local_vllm",
  "base_url": "http://model-server:8000/v1",
  "status": "active",
  "capabilities": {
    "supports_chat": true,
    "supports_structured_output": false,
    "supports_streaming": true,
    "supports_prompt_caching": false,
    "supports_embeddings": false,
    "supports_tool_calling": false
  },
  "data_policy": {
    "restricted_data_allowed": true,
    "training_usage_allowed": false,
    "region": "private_network",
    "retention": "self_managed"
  }
}
```

## 3. Route Examples

### 3.1 Cheap Classifier Route

Use case:

```text
intent classification, ticket classification, safety precheck labels
```

Route:

```json
{
  "route_key": "classification_primary",
  "use_case": "classification",
  "provider_key": "openai_primary",
  "model_name": "cheap-fast-model",
  "priority": 1,
  "max_input_tokens": 2000,
  "max_output_tokens": 300,
  "temperature": 0.0,
  "timeout_seconds": 8,
  "reasoning_enabled": false,
  "prompt_caching_enabled": false,
  "restricted_data_allowed": false,
  "fallback_route_key": "classification_private"
}
```

Why:

- Classification should be cheap, fast, deterministic, and schema-validated.
- Reasoning mode is usually unnecessary.

### 3.2 RAG Answer Route

Use case:

```text
grounded answers over private documents
```

Route:

```json
{
  "route_key": "rag_answer_primary",
  "use_case": "rag_answer",
  "provider_key": "openai_primary",
  "model_name": "high-quality-chat-model",
  "priority": 1,
  "max_input_tokens": 24000,
  "max_output_tokens": 1800,
  "temperature": 0.2,
  "timeout_seconds": 30,
  "reasoning_enabled": false,
  "prompt_caching_enabled": true,
  "cacheable_prefix_min_tokens": 1024,
  "restricted_data_allowed": false,
  "fallback_route_key": "rag_answer_private"
}
```

Why:

- RAG often has a stable instruction prefix and large dynamic context.
- Prompt caching may help when prompts have repeated policy/tool instructions.
- If tenant policy blocks external providers, route to private model.

### 3.3 Embedding Route

Use case:

```text
query embeddings and document chunk embeddings
```

Route:

```json
{
  "route_key": "embedding_primary",
  "use_case": "embedding",
  "provider_key": "openai_primary",
  "model_name": "embedding-model-large",
  "priority": 1,
  "max_input_tokens": 8192,
  "max_output_tokens": 0,
  "embedding_dimension": 1536,
  "batch_enabled": true,
  "max_batch_items": 2048,
  "timeout_seconds": 60,
  "restricted_data_allowed": false,
  "fallback_route_key": "embedding_private"
}
```

Why:

- Embeddings should batch offline chunk processing.
- Embedding model changes require reindexing and evaluation.

### 3.4 Judge Route

Use case:

```text
LLM-as-judge scoring for evals
```

Route:

```json
{
  "route_key": "llm_judge_primary",
  "use_case": "llm_judge",
  "provider_key": "openai_primary",
  "model_name": "judge-capable-model",
  "priority": 1,
  "max_input_tokens": 12000,
  "max_output_tokens": 1200,
  "temperature": 0.0,
  "timeout_seconds": 30,
  "reasoning_enabled": true,
  "reasoning_effort": "medium",
  "reasoning_budget_tokens": 2000,
  "prompt_caching_enabled": true,
  "restricted_data_allowed": false
}
```

Why:

- Judging needs consistency and a rubric.
- Reasoning can help but must be measured and budgeted.

### 3.5 Reasoning Agent Planner Route

Use case:

```text
complex agent planning and verification
```

Route:

```json
{
  "route_key": "agent_planning_complex_primary",
  "use_case": "agent_planning_complex",
  "provider_key": "openai_primary",
  "model_name": "reasoning-model",
  "priority": 1,
  "max_input_tokens": 16000,
  "max_output_tokens": 2000,
  "temperature": 0.0,
  "timeout_seconds": 45,
  "reasoning_enabled": true,
  "reasoning_effort": "high",
  "reasoning_budget_tokens": 4000,
  "max_cost_usd": 0.75,
  "prompt_caching_enabled": true,
  "restricted_data_allowed": false
}
```

Why:

- Use only for difficult planning.
- Do not use this route for simple classification or summarization.

### 3.6 Private Restricted Data Route

Use case:

```text
sensitive tenant documents, confidential tickets, regulated data
```

Route:

```json
{
  "route_key": "rag_answer_private",
  "use_case": "rag_answer",
  "provider_key": "azure_private_llm",
  "model_name": "private-chat-model",
  "priority": 2,
  "max_input_tokens": 16000,
  "max_output_tokens": 1600,
  "temperature": 0.2,
  "timeout_seconds": 35,
  "reasoning_enabled": false,
  "prompt_caching_enabled": true,
  "restricted_data_allowed": true,
  "fallback_route_key": null
}
```

Why:

- Some tenants must not send sensitive content to public/provider-default routes.
- Fallback should not silently downgrade to less private provider.

The `use_case` here is `rag_answer`, not `rag_answer_private`. Data sensitivity is a **filter**, not a different use case: the caller asks for a grounded answer and does not know whether the tenant is restricted. A private route registered under its own `use_case` would never be a candidate for any real request, `rag_answer_primary` could never fall back to it, and a restricted-data request would find no compliant route at all. `use_case` describes what the caller wants; `restricted_data_allowed` and `priority` describe who may serve it. Priority 2 means this route loses to the primary for unrestricted requests and wins when the data-policy filter removes the primary.

### 3.7 Private Fallback Routes For Classification And Embedding

The classification and embedding routes above name fallbacks. Those fallbacks are defined here, under the same rule as §3.6: same `use_case` as the route they serve, priority 2, `restricted_data_allowed: true`, and no onward fallback.

```json
{
  "route_key": "classification_private",
  "use_case": "classification",
  "provider_key": "azure_private_llm",
  "model_name": "private-chat-model",
  "priority": 2,
  "max_input_tokens": 2000,
  "max_output_tokens": 300,
  "temperature": 0.0,
  "timeout_seconds": 10,
  "reasoning_enabled": false,
  "prompt_caching_enabled": false,
  "restricted_data_allowed": true,
  "fallback_route_key": null
}
```

```json
{
  "route_key": "embedding_private",
  "use_case": "embedding",
  "provider_key": "azure_private_llm",
  "model_name": "private-embedding-model",
  "priority": 2,
  "max_input_tokens": 8192,
  "max_output_tokens": 0,
  "embedding_dimension": 1536,
  "batch_enabled": true,
  "max_batch_items": 1024,
  "timeout_seconds": 60,
  "restricted_data_allowed": true,
  "fallback_route_key": null
}
```

`embedding_private.embedding_dimension` **must** equal `embedding_primary.embedding_dimension`. Two embedding routes for one collection that produce different vector widths cannot share an index, and the failure appears at query time as a dimension mismatch rather than at configuration time. `max_batch_items` may differ between the two — that is a provider limit, not a correctness constraint.

Every `fallback_route_key` in this document now resolves to a route defined in this document. A configuration loader should validate that before writing routes, because a dangling fallback fails only on the day the primary provider is down.

### 3.8 Media Generation Route

Use case:

```text
text-to-image, image editing, video generation, audio generation
```

Route:

```json
{
  "route_key": "image_generation_primary",
  "use_case": "image_generation",
  "provider_key": "openai_primary",
  "model_name": "image-generation-model",
  "priority": 1,
  "max_input_tokens": 2000,
  "max_output_tokens": 0,
  "timeout_seconds": 120,
  "async_only": true,
  "cost_estimate_required": true,
  "restricted_data_allowed": false,
  "route_config": {
    "prompt_safety_required": true,
    "output_safety_required": true,
    "requires_provenance": true
  }
}
```

Why:

- Media generation can be slow and expensive.
- Run it as a job, not a blocking request.

## 4. Route Selection Algorithm

```text
receive model request
-> resolve tenant policy
-> resolve use_case
-> load active routes ordered by priority
-> filter routes by required capability
-> filter routes by data policy
-> filter routes by cost budget
-> select first route
-> resolve bootstrap `provider_key` to `provider_id` and `fallback_route_key` to `fallback_route_id`
-> if provider unavailable, apply fallback if policy allows
-> create ai_run record
-> execute provider call
-> store usage, cost, latency, cache tokens, reasoning tokens
```

## 5. Route Rejection Examples

### 5.1 Restricted Data On Public Route

```text
Request has restricted_data=true
Route restricted_data_allowed=false
Result: reject or route to private route
```

### 5.2 Reasoning Budget Too High

```text
Requested reasoning_budget_tokens=8000
Route max reasoning_budget_tokens=4000
Result: reject or reduce by policy
```

### 5.3 Provider Does Not Support Structured Output

```text
Use case requires structured output
Provider capability supports_structured_output=false
Result: select another route or fail before model call
```

## 6. Route Promotion Checklist

Before activating a new route:

```text
[ ] Provider capability verified
[ ] Tenant data policy reviewed
[ ] Cost estimate configured
[ ] Timeout configured
[ ] Fallback policy configured
[ ] Eval suite passes
[ ] Safety suite passes
[ ] Observability fields tested
[ ] Rollback route exists where appropriate
[ ] Model card updated
```
