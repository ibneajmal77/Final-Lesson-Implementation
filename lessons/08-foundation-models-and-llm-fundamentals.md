# Foundation Models and LLM Fundamentals

## Lesson metadata

| Field | Value |
|---|---|
| Curriculum position | Core Lesson 08 |
| Primary roles | Applied AI Engineer, Generative AI Engineer, LLM Engineer, Machine Learning Engineer |
| Supporting roles | AI Evaluation Engineer, NLP Engineer, AI Product Manager, AI Solutions Architect |
| Difficulty | Intermediate |
| Estimated study time | 8-12 hours |
| Estimated implementation time | 8-14 hours |
| Prerequisite lessons | Lessons 01-07 |
| Project increment | Reproducible model-behavior laboratory for the support-drafting pilot |
| Primary tools | Python, PyTorch, Hugging Face Transformers, tokenizers, pytest, Jupyter or scripts |
| Optional tool | One approved hosted model API |
| Technical guidance verified | June 25, 2026 |
| Learning design | Eight-module cognitive path plus complete production reference |

## How to use this lesson

This lesson has two layers.

### Essential learning path

Complete the eight learning modules first. Each module contains:

- A prediction question
- A small set of connected concepts
- A worked example
- Guided practice
- Independent practice
- A closed-book retrieval checkpoint
- A misconception check
- A connection to the next module

Stop after each retrieval checkpoint. Close the lesson and answer from memory before continuing.
The first pass is designed for understanding and retention, not maximum reading speed.

Recommended first-pass schedule:

| Study session | Modules | Approximate time | Output |
|---|---|---:|---|
| Session A | Language-model loop; tokenization and embeddings | 60-90 minutes | Hand-drawn model loop and token report |
| Session B | Logits and decoding; attention and transformer blocks | 75-105 minutes | Softmax calculation and attention sketch |
| Session C | Model families and lifecycle; chat templates and generation controls | 75-105 minutes | Model-choice table and formatted chat inspection |
| Session D | Context and hallucination; model-behavior laboratory | 90-120 minutes | Experiment plan and selection criteria |

### Hands-on path

After the essential modules:

- Complete the environment setup.
- Implement one milestone at a time.
- Predict expected output before running code.
- Use the tests to check your mental model.
- Record mistakes and their causes.

### Reference and production path

The sections beginning with **Key terminology** preserve the complete technical depth:

- Detailed terminology
- Architectures and lifecycle
- Full implementation
- Testing and evaluation
- Security
- Performance and cost
- Deployment and operations

Use them during implementation, review, and interviews. They are not intended to be memorized in
one reading.

### Retrieval rule

Do not reread immediately when recall feels difficult. First attempt to reconstruct:

- The diagram
- The sequence of steps
- The comparison
- The likely failure

Then check the lesson and correct your answer. The correction is part of learning.

## Why this lesson exists

Lesson 07 selected a narrow business use case:

> Permission-aware, evidence-backed response drafting for eligible support cases, with mandatory
> agent approval and no autonomous financial or account action.

Before integrating a provider API, designing prompts, building retrieval, or fine-tuning a
model, an Applied AI Engineer must understand how language models behave.

The required understanding is operational:

- What a tokenizer does
- Why the same text has different token counts across models
- How a causal language model predicts the next token
- What logits, probabilities, and sampling controls mean
- How self-attention combines information from a sequence
- Why context length affects memory, latency, and cost
- How base and instruction-tuned models differ
- Why chat messages are ultimately converted into token sequences
- What pretraining and post-training change
- Why fluent output can still be unsupported or wrong
- How model type, deployment model, data policy, and operational constraints affect product
  selection

The goal is not to reproduce a frontier foundation model. It is to develop enough internal
understanding to predict failure modes, select a model deliberately, configure generation,
design evaluations, and explain tradeoffs in an interview.

This lesson avoids two common mistakes:

```text
Mistake 1:
"The model understands the question, so its answer must be correct."

Mistake 2:
"The largest model is automatically the best production choice."
```

A language model generates probable token sequences. A production AI system must add evidence,
permissions, validation, human control, observability, and business evaluation around that
capability.

## Business problem

### Organization

Northstar Support is preparing the response-drafting pilot designed in Lesson 07.

### Selected pilot

Eligible support agents will receive:

- A structured issue summary
- Retrieved policy and product evidence
- An editable response draft
- An abstention or escalation recommendation

The agent must approve every customer-facing response.

### Engineering question

The team must choose a model approach for early experiments. Stakeholders have proposed:

- The cheapest small open model
- A larger instruction-tuned open model
- A hosted commercial model
- A "reasoning model" for every request
- Fine-tuning immediately

These suggestions are incomplete because they do not define:

- Task quality
- Tokenization behavior
- Context requirements
- Generation settings
- Latency
- Throughput
- Memory
- Cost
- Privacy
- Model versioning
- Instruction-following reliability
- Structured-output reliability
- Hallucination and abstention behavior

### Lesson objective

Build a model-behavior laboratory that compares:

- A small open base causal language model
- Its instruction-tuned counterpart
- One approved hosted model or a recorded hosted-provider result

The laboratory must use a fixed test set and record:

- Token counts
- Context size
- Generation configuration
- Output
- Latency
- Input and output length
- Repetition
- Variation across repeated runs
- Schema or instruction compliance
- Evidence-use behavior
- Model and tokenizer identifiers
- Environment details

### Constraints

- Use synthetic support cases.
- Do not send real customer data to a hosted provider.
- Do not claim benchmark results that were not measured.
- Open-model experiments must be able to run without a GPU, although a GPU may improve speed.
- The lesson must distinguish base-model behavior from instruction-tuned behavior.
- The laboratory is exploratory and cannot approve a production model by itself.

### Success metrics

- Every experiment is reproducible from a configuration record.
- Token counts are measured rather than estimated by character count.
- Greedy and sampled decoding are compared.
- Base and instruction models are compared using appropriate formatting.
- Context-length effects are measured.
- Output claims are distinguished from verified facts.
- A model-selection recommendation lists assumptions and limitations.

## Learning outcomes

After completing this lesson, you will be able to:

- Explain tokenization, vocabulary, token IDs, and special tokens.
- Compare word, character, byte, and subword tokenization at an operational level.
- Inspect how different tokenizers process English, code, numbers, punctuation, and multilingual
  text.
- Explain embeddings as learned vector representations.
- Explain logits, softmax probabilities, and next-token prediction.
- Implement a minimal autoregressive decoding loop.
- Explain self-attention using queries, keys, values, scores, masks, and weighted sums.
- Describe transformer blocks, residual connections, normalization, and feed-forward layers.
- Distinguish encoder, decoder, and encoder-decoder architectures.
- Distinguish dense and mixture-of-experts models.
- Distinguish base, instruction-tuned, reasoning-oriented, and multimodal models.
- Explain pretraining, continued pretraining, SFT, preference optimization, distillation,
  quantization, and inference.
- Apply a model's chat template correctly.
- Configure greedy decoding, sampling, temperature, top-k, top-p, output limits, stop behavior,
  and repetition controls.
- Explain why deterministic decoding is not equivalent to factual correctness.
- Explain hallucination, calibration limits, context limitations, and lost evidence.
- Compare hosted and open-weight deployment models.
- Build and test a reproducible model-behavior laboratory.
- Create a defensible shortlist for the support-drafting pilot.

## Prerequisites

### Knowledge

- Production Python
- Type hints and Pydantic
- Testing with pytest
- Basic APIs and data contracts
- Applied AI problem formulation from Lesson 07

### Existing repository

Continue using `ai-industry-labs`.

The repository should already contain:

- Locked dependencies
- Source package
- Tests
- Docker support
- CI
- Typed configuration
- Lesson 07 discovery artifacts

### Hardware

Minimum:

- Modern CPU
- Approximately 8 GB system memory for the smallest demonstrations

Recommended:

- 16 GB or more system memory
- CUDA-capable GPU for faster open-model generation

The exact requirement depends on model size, precision, sequence length, framework overhead, and
device placement. Do not infer memory requirement from parameter count alone.

### Data

Use synthetic support prompts and evidence. No production customer data is required.

### Hosted provider

Optional. If no approved provider account is available:

- Complete all open-model experiments.
- Define the hosted adapter contract.
- Leave hosted result fields unmeasured.
- Do not fabricate hosted output, price, latency, or quality.

## Activate prior knowledge

Answer these questions without searching. Uncertainty is expected.

- In the Lesson 07 pilot, which decisions must remain deterministic or human-authorized even if
  a language model is used?
- Why is an evidence-backed draft safer than letting the model send a response directly?
- What information must be recorded so two engineers can reproduce the same experiment?
- If two generated answers sound equally fluent, what evidence would you need to decide which
  one is better?
- Why might a smaller model be a better production choice than a larger model?

Write brief answers. Revisit them after the final module and note what changed.

## Lesson concept map

Use this map throughout the lesson:

```text
Business task from Lesson 07
        │
        ▼
Text or chat messages
        │
        ▼
Tokenizer
text → token IDs
        │
        ▼
Embeddings + positional information
        │
        ▼
Transformer blocks
attention + feed-forward transformations
        │
        ▼
Next-token logits
        │
        ▼
Decoding strategy
greedy or sampling controls
        │
        ▼
Generated token
        │
        └────────── repeats autoregressively
        │
        ▼
Application controls
evidence + validation + human approval
        │
        ▼
Measured business outcome
```

The central relationship is:

> The model produces token continuations; the surrounding system produces a controlled business
> capability.

## Learning module map

| Module | Central question | New concepts | Practice artifact |
|---|---|---|---|
| Language-model loop | What does an LLM actually do when it writes? | tokens, logits, autoregression | Drawn generation loop |
| Tokenization and embeddings | How does text become model input? | vocabulary, token IDs, embeddings, positions | Token comparison report |
| Logits and decoding | Why does output change? | softmax, greedy, temperature, top-k, top-p | Manual and coded probability comparison |
| Attention and transformer blocks | How does each token use earlier context? | Q, K, V, mask, residual, feed-forward | Attention matrix sketch |
| Model families and lifecycle | Which model type fits which task? | encoder, decoder, base, instruct, MoE, post-training | Model-choice decision table |
| Chat templates and controls | How do messages become the correct model sequence? | roles, special tokens, output limits, stops | Formatted-chat inspection |
| Context and hallucination | Why can fluent output still fail? | context budget, distractors, unsupported claims, abstention | Failure diagnosis worksheet |
| Model-behavior laboratory | How should candidates be compared? | fixed cases, reproducibility, latency, cost, human review | Experiment and selection plan |

## Essential learning modules

## Learning module: The language-model loop

### Module question

Before reading, predict:

> When a model generates a paragraph, does it create the complete paragraph in one operation or
> select it incrementally?

Write your prediction and one reason.

### Essential concepts

- Token
- Token sequence
- Logit
- Next-token prediction
- Autoregressive generation

### Mental model

A causal language model behaves like a repeated prediction process:

```text
current tokens
→ model calculates next-token scores
→ decoding chooses one token
→ chosen token is appended
→ model repeats
```

It does not first create a verified answer and then convert that answer to text. The evolving
token sequence is the generation process.

### Worked example

Suppose the current sequence is:

```text
The customer was charged
```

The model might assign high logits to tokens representing:

```text
twice
again
incorrectly
for
```

A decoding rule selects one token. If it selects `twice`, the next step conditions on:

```text
The customer was charged twice
```

An early choice changes later possibilities. This is why plausible output can drift after one
poor token.

### Guided practice

Complete the loop:

```text
Prompt: "The refund requires supervisor"

Possible next tokens:
approval: 5.1
review:   3.8
today:    0.9

Greedy decoding selects: ______
The next model input becomes: ______________________________
```

Hint: greedy decoding selects the highest logit.

### Independent practice

Create your own four-token candidate set for:

```text
The security incident should be
```

Explain how one unsafe early token could cause an inappropriate continuation.

### Retrieval checkpoint

Close the lesson and answer:

- What does autoregressive mean?
- What is the difference between a logit and a selected token?
- Why can an early generated token affect the entire answer?
- Why does fluency not prove that the model planned a correct answer?

### Misconception check

**Misconception:** The model searches its memory for a complete stored answer.

**Why it seems plausible:** The generated paragraph is coherent and appears intentional.

**Correct model:** The system repeatedly computes conditional next-token scores. Learned
parameters shape those scores, but the output is constructed incrementally.

**Test:** Change one early generated token and observe how later continuation changes.

### Connection

The model operates on tokens, not raw text. The next module explains how text becomes those
tokens and numeric representations.

## Learning module: Tokenization and embeddings

### Module question

Predict:

> Will the English sentence `I was charged twice` and its Arabic translation necessarily use
> the same number of tokens?

Explain your answer before inspecting a tokenizer.

### Essential concepts

- Tokenizer
- Vocabulary
- Token ID
- Special token
- Token embedding
- Positional information
- Contextual representation

### Mental model

```text
text
→ tokenizer rules
→ token pieces
→ token IDs
→ embedding-table lookup
→ vectors
→ position information
→ contextual transformation
```

Tokenization is model-specific. A token may be a whole word, part of a word, punctuation,
whitespace pattern, or byte-derived unit.

### Worked example

Consider:

```text
charged
recharged
charge_id_1042
```

A subword tokenizer may reuse pieces such as `charge`, `d`, `re`, `_`, and number fragments.
This controls vocabulary size and supports unfamiliar words, but increases sequence length for
some text.

The token ID is not a semantic meaning by itself. It indexes a learned embedding vector.

### Guided practice

Before running code, rank these from likely shortest to longest token sequence:

```text
refund
refund_requested
تم رد المبلغ
https://support.example/refund?id=1042
```

Then use the lesson's tokenizer inspector and compare your prediction with measured counts.

Record:

- Character count
- Token count
- Characters per token
- Surprising token pieces

### Independent practice

Choose:

- One English ticket
- One non-English ticket
- One JSON object
- One product identifier

Compare them with two tokenizers. Explain why token efficiency could affect cost, context, or
latency for Northstar Support.

### Retrieval checkpoint

- Why is a token not the same as a word?
- Why must a model use the tokenizer associated with its weights?
- What is the difference between a token ID and an embedding?
- Why is positional information required?
- How can tokenization affect multilingual product quality?

### Misconception check

**Misconception:** A model with a larger context window can accept the same number of words in
every language.

**Correct model:** Context is counted in model-specific tokens. Languages and data formats can
have different token efficiency.

### Connection

Embeddings enter the transformer, which eventually produces next-token logits. First, connect
those logits to probabilities and decoding behavior.

## Cumulative retrieval: From text to the next-token decision

Without looking, draw:

```text
text → ______ → token IDs → ______ → transformer → ______ → decoding
```

Then answer:

- Which steps are deterministic?
- Which values are learned?
- Where does output variability enter?
- Which step determines the context token count?

Check your map only after completing all answers.

## Learning module: Logits, softmax, and decoding

### Module question

Predict:

> If temperature is reduced, does the model gain more factual knowledge, or does token selection
> become more concentrated?

### Essential concepts

- Logit
- Softmax
- Conditional probability
- Greedy decoding
- Sampling
- Temperature
- Top-k and top-p filtering

### Mental model

```text
logits
→ optional temperature scaling
→ optional candidate filtering
→ probabilities
→ selection rule
→ next token
```

The probability is conditional on the current sequence:

```text
P(next token | all current tokens)
```

It is not the probability that the entire answer is correct.

### Worked example

Given logits:

```text
approval: 4.0
review:   2.0
refund:   1.0
```

Greedy decoding selects `approval`.

At a lower temperature, the distribution becomes sharper around `approval`. At a higher
temperature, `review` and `refund` receive relatively more probability.

Nothing in this operation verifies the refund policy.

### Guided practice

Use the `softmax` function in the reference implementation.

Before running:

- Predict which token has the highest probability.
- Predict whether temperature `0.5` or `1.5` produces a sharper distribution.

After running:

- Explain any difference between prediction and output.
- State what softmax guarantees and what it does not.

### Independent practice

Create a token distribution where the two highest candidates are close. Compare:

- Greedy
- Low-temperature sampling
- Higher-temperature sampling

Explain which configuration you would use for:

- Ticket classification
- Creative response alternatives
- Evidence-backed support drafting

### Retrieval checkpoint

- What is a logit?
- What does softmax do?
- What does temperature change?
- Why can greedy decoding produce a false answer?
- How do top-k and top-p differ?

### Misconception check

**Misconception:** Temperature zero makes an answer accurate.

**Correct model:** Deterministic selection improves repeatability, not truth. A stable unsupported
answer is still unsupported.

### Connection

Logits are produced from hidden states after transformer computation. The next module explains
how attention updates those states using earlier context.

## Learning module: Attention and transformer blocks

### Module question

For:

```text
The agent denied the refund because it lacked approval.
```

What earlier information might the representation of `it` need?

### Essential concepts

- Query
- Key
- Value
- Attention score
- Causal mask
- Multi-head attention
- Transformer block

### Mental model

Each token position asks:

```text
What information am I looking for?       → query
What information does each position offer? → key
What content should be combined?         → value
```

Simplified attention:

```text
QKᵀ
→ scale
→ mask future positions
→ softmax weights
→ weighted sum of V
```

### Worked example

In a causal sequence:

```text
[The] [refund] [requires] [approval]
```

The representation at `approval` may use all earlier positions. The representation at `refund`
cannot use future token `approval` during causal language-model training or generation.

The causal mask blocks those future attention scores before softmax.

### Guided practice

Draw a four-by-four attention permission matrix for:

```text
A B C D
```

Mark whether each row can attend to each column under a causal mask.

Expected pattern:

- `A` sees only `A`
- `B` sees `A` and `B`
- Continue the pattern for `C` and `D`

Then run the toy attention test and compare.

### Independent practice

Explain how the model can combine:

- The phrase `refund request`
- A later phrase `requires supervisor approval`

without assuming that one attention head has a simple human-readable purpose.

### Retrieval checkpoint

- What do queries, keys, and values represent operationally?
- Why is attention scaled?
- What does a causal mask prevent?
- What does the weighted sum contain?
- What else exists in a transformer block besides attention?

### Misconception check

**Misconception:** Attention weights are a complete explanation of model reasoning.

**Correct model:** Attention is one computational component. Model behavior also depends on
embeddings, many layers, feed-forward transformations, residual paths, normalization, and
decoding.

### Connection

Transformer architecture can be arranged for representation, generation, or input-to-output
transformation. The next module compares these model families and how training changes behavior.

## Cumulative retrieval: Reconstruct one generation step

From memory, explain one generation step using all of these terms:

```text
token IDs
embeddings
position
attention
hidden state
logits
temperature
next token
```

Then diagnose:

> The model always gives the same wrong policy answer.

Which parts of the pipeline might explain stability, and which system controls are required to
address correctness?

## Learning module: Model families and lifecycle

### Module question

Which would you choose first for each task?

- Ticket classification
- Semantic retrieval
- Response drafting
- Translation

Choose from encoder, decoder, and encoder-decoder before reading.

### Essential concepts

- Encoder architecture
- Decoder architecture
- Encoder-decoder architecture
- Base versus instruction-tuned behavior
- Dense versus mixture-of-experts execution
- Pretraining versus post-training

### Mental model

```text
Architecture answers:
How does information flow?

Training stage answers:
What behavior was learned?

Deployment form answers:
How is the model accessed and operated?
```

### Worked example

For response drafting:

- An encoder can represent the ticket but does not naturally generate an open-ended reply.
- A decoder generates autoregressively and is the common choice.
- A base decoder may continue text unpredictably.
- An instruction-tuned decoder is more likely to follow the requested assistant behavior.

The model still requires evidence and human approval from the Lesson 07 design.

### Guided practice

Complete:

| Task | Architecture | Model behavior needed | Reason |
|---|---|---|---|
| Semantic embedding | | | |
| Ticket classification | | | |
| Response drafting | | | |
| Policy translation | | | |

Use the architecture-selection reference after attempting the table.

### Independent practice

Compare a dense model and an MoE model without using total parameter count as the only measure.
Include:

- Active computation
- Memory
- Routing
- Distributed serving
- Task quality

### Retrieval checkpoint

- Encoder versus decoder?
- Base versus instruction model?
- What does SFT change?
- Why does preference optimization not guarantee factual correctness?
- Why is total parameter count insufficient for comparing dense and MoE models?

### Misconception check

**Misconception:** Instruction tuning adds all current domain facts.

**Correct model:** Instruction tuning changes behavior using examples. Frequently changing policy
facts should generally come from governed evidence or tools.

### Connection

Instruction models expect a particular conversational token format. The next module connects
human-readable messages to chat templates and decoding controls.

## Learning module: Chat templates and generation controls

### Module question

Predict:

> If two instruction models receive the same list of `{role, content}` messages, do they
> necessarily receive the same token sequence?

### Essential concepts

- Chat roles
- Special tokens
- Chat template
- Generation prompt
- Maximum new tokens
- Stop condition
- Repetition control

### Mental model

```text
message objects
→ model-specific chat template
→ special and content tokens
→ input IDs
→ generation
```

The message list is an application representation. The model receives token IDs.

### Worked example

Conceptually, one model may expect:

```text
<user> ... </user> <assistant>
```

Another may expect:

```text
[INST] ... [/INST]
```

These control tokens are not interchangeable. The tokenizer's chat template is part of the
model interface.

### Guided practice

Use `apply_chat_template` to inspect:

- Raw formatted text
- Token IDs
- Token count
- Assistant generation marker

Predict whether the template increases token count compared with the raw user message.

### Independent practice

Create one base-model prompt and one semantically equivalent instruction-model conversation.
Explain why byte-for-byte identical prompts would not necessarily be a fair comparison.

### Retrieval checkpoint

- Why is a chat template needed?
- What can happen when special tokens are duplicated?
- What is the purpose of a generation prompt?
- Why must output length be bounded?
- Why can structured syntax still contain semantically wrong values?

### Misconception check

**Misconception:** A chat template is only cosmetic formatting.

**Correct model:** It creates model-specific control tokens learned during post-training.
Incorrect formatting can materially reduce instruction following.

### Connection

Correct formatting does not guarantee the model uses all supplied information effectively. The
next module examines context limits, distractors, unsupported claims, and uncertainty.

## Cumulative retrieval: Choose the correct model interface

For each situation, state:

- Architecture family
- Base or instruction behavior
- Input formatting
- Decoding choice

Situations:

- Deterministic ticket category baseline
- Evidence-backed response draft
- Diverse alternative phrasings
- Semantic passage embedding

Explain one tradeoff for every choice.

## Learning module: Context, hallucination, and uncertainty

### Module question

Predict:

> If a model supports a larger context window, will adding every available document always
> improve the answer?

### Essential concepts

- Context budget
- Input and output reserve
- Truncation
- Distractors
- Unsupported claim
- Hallucination
- Abstention

### Mental model

```text
available context
= instructions
+ user input
+ history
+ evidence
+ tool descriptions and results
+ output reserve
```

More context increases available information but can also add cost, latency, conflicts, and
distractors.

### Worked example

The support question asks about duplicate-charge policy.

Context A:

- One current duplicate-charge policy

Context B:

- Current policy
- Three obsolete policies
- Ten unrelated account articles
- Long conversation history

Context B is larger but not necessarily more useful. The system should select relevant,
authorized, current evidence rather than fill the context window.

### Guided practice

Given a maximum context of 8,000 tokens:

```text
system and formatting: 500
conversation:          1,000
evidence:              4,500
desired output:        1,200
safety margin:           400
```

Calculate:

- Total budget used
- Tokens remaining
- Which component you would reduce first if evidence grows by 1,000 tokens

### Independent practice

Design three test cases:

- Missing evidence
- Conflicting evidence
- Incorrect user premise

For each, define the desired behavior:

- Answer
- Ask for information
- Abstain
- Escalate

### Retrieval checkpoint

- What belongs in the context budget?
- Why can more context reduce quality?
- What is an unsupported claim?
- Why is self-reported confidence weak evidence?
- When should the system abstain?

### Misconception check

**Misconception:** Hallucination is solved by setting temperature to zero.

**Correct model:** Unsupported output can result from missing evidence, incorrect premises,
training patterns, context selection, and system design. Deterministic decoding can repeat the
same unsupported claim.

### Connection

The final module turns these concepts into an experiment that compares candidate models under
fixed conditions.

## Learning module: Model-behavior laboratory and production selection

### Module question

What must remain fixed when comparing two candidate models so that the comparison is
interpretable?

### Essential concepts

- Fixed test set
- Baseline
- Model and tokenizer revision
- Generation configuration
- Repeated sampling
- Latency and cost
- Human review

### Mental model

```text
same task cases
+ recorded model and tokenizer
+ recorded formatting
+ recorded generation settings
+ measured outputs
+ human rubric
= interpretable comparison
```

### Worked example

Compare a base and instruction model on:

```text
Draft a response using this evidence:
Refunds require supervisor approval.
```

Fairness does not mean identical bytes. It means:

- Same task meaning
- Same evidence
- Appropriate model-specific formatting
- Same output budget
- Recorded decoding settings
- Same evaluation rubric

### Guided practice

Complete an experiment row before running:

| Field | Planned value |
|---|---|
| Case ID | |
| Model ID and revision | |
| Tokenizer ID | |
| Base or instruction | |
| Chat-template use | |
| Decoding | |
| Seed | |
| Output limit | |
| Expected behavior | |
| Failure markers | |

Then run and add measured tokens, latency, output, and review.

### Independent practice

Choose three candidates and produce a recommendation with:

- Best quality-threshold candidate
- Lower-cost fallback
- Cases needing another model or deterministic method
- Unresolved privacy or licence concerns
- Required next evaluation

Do not select from one aggregate score.

### Retrieval checkpoint

- Why use a fixed test set?
- Why record the tokenizer and revision?
- Why repeat sampled runs?
- Why is latency from one cold run misleading?
- Why is cost per successful task better than price per token alone?

### Misconception check

**Misconception:** A public benchmark winner is automatically the correct production model.

**Correct model:** Production selection depends on the actual task, thresholds, latency, cost,
privacy, region, licence, versioning, and operating capability.

### Connection

The laboratory produces the model shortlist. Lesson 09 will implement the selected hosted
candidate through a reliable provider-independent API layer.

## Final cumulative retrieval before the reference layer

Close the lesson and reconstruct the complete model loop from memory.

Your explanation must include:

- Tokenizer
- Token IDs
- Embeddings
- Positional information
- Attention
- Transformer block
- Logits
- Softmax
- Decoding
- Context
- Application controls

Then answer:

- Which parts change when switching from base to instruction model?
- Which parts change when temperature changes?
- Which parts are responsible for authorization and policy correctness?
- Which experiment would reveal context distractor sensitivity?
- Which evidence would justify selecting a smaller model?

If you cannot answer at least four confidently, review the relevant module rather than rereading
the entire lesson.

## Reference and production depth

The remaining sections preserve the complete technical content. Use them for implementation,
lookup, debugging, production design, and interview preparation.

## Key terminology

### Foundation model

A model trained on broad data at substantial scale that can be adapted or used across many
downstream tasks.

### Language model

A model that assigns probabilities to token sequences or predicts tokens conditioned on
preceding or surrounding context.

### Causal language model

A language model trained to predict the next token using only earlier tokens. Most chat-style
generative language models use causal decoding.

### Token

A unit processed by the model. A token may represent a word, part of a word, punctuation,
whitespace pattern, byte sequence, or special control symbol.

### Tokenizer

The deterministic preprocessing component that converts text or structured messages into token
IDs and converts model token IDs back into text.

### Vocabulary

The set of token IDs and token representations known by a tokenizer.

### Token ID

An integer representing one token in a tokenizer vocabulary.

### Special token

A control token representing boundaries or structure, such as beginning of sequence, end of
sequence, padding, user role, or assistant role.

### Embedding

A learned vector representing a token, position, item, or other object in a continuous numeric
space.

### Hidden state

The vector representation of each sequence position as it passes through model layers.

### Parameter

A learned numeric value in a model, such as a weight in a matrix.

### Logit

An unnormalized score produced by the model for a possible next token.

### Softmax

A function that converts a vector of logits into non-negative probabilities that sum to one.

### Autoregressive generation

Generation that repeatedly predicts a token, appends it to the sequence, and predicts the next
token from the expanded sequence.

### Attention

A mechanism that computes how strongly one position should use information from other allowed
positions.

### Query

A learned representation of what a token position is looking for.

### Key

A learned representation used to determine how relevant another token position is to a query.

### Value

The information combined after attention relevance scores are computed.

### Causal mask

A mask preventing a position from attending to future tokens during causal language modelling.

### Context window

The maximum or supported number of tokens available to the model for a request, including input,
conversation history, tool or evidence content, formatting tokens, and generated output budget.

### Transformer block

A repeated neural-network unit containing attention, feed-forward transformations,
normalization, residual connections, and related components.

### Residual connection

A path that adds a block's input to its transformed output, supporting stable training and
information flow.

### Normalization

A transformation that stabilizes internal activation scale. Modern language models commonly
use layer-normalization variants.

### Feed-forward network

A position-wise neural network inside a transformer block that transforms each hidden state
after attention mixing.

### Dense model

A model in which the same main parameter set participates for every token at a layer.

### Mixture-of-experts model

A model containing multiple expert feed-forward components and a router that activates a subset
for each token. Total parameters and active parameters differ.

### Base model

A pretrained model primarily optimized for language modelling rather than conversational
instruction following.

### Instruction-tuned model

A model adapted on instruction-response or conversational data to follow user tasks and chat
formats more reliably.

### Reasoning-oriented model

A model and inference configuration optimized to spend additional computation or intermediate
processing on difficult tasks. The exact behavior and exposed fields differ by model and
provider.

### Multimodal model

A model that accepts or generates more than one modality, such as text, images, audio, or video.

### Pretraining

Large-scale initial training, commonly using next-token prediction or related self-supervised
objectives.

### Continued pretraining

Additional pretraining on a new data mixture, often for domain or language adaptation.

### Supervised fine-tuning

Training on labelled demonstrations, instructions, conversations, or task examples.

### Preference optimization

Post-training that uses preference information to make model behavior more aligned with desired
responses.

### Distillation

Training a smaller or different model to reproduce useful behavior from a teacher model or
teacher-generated data.

### Quantization

Representing weights or computation with lower-precision numeric formats to reduce memory,
increase speed, or lower serving cost, potentially affecting quality.

### Inference

Running a trained model to produce predictions or generated output.

### Decoding strategy

The rule used to select generated tokens from model logits or probabilities.

### Temperature

A scaling factor applied before softmax. Lower values sharpen the distribution; higher values
flatten it. Temperature changes selection behavior, not the model's stored knowledge.

### Top-k sampling

Sampling restricted to the `k` highest-scoring candidate tokens.

### Top-p sampling

Sampling restricted to the smallest set of candidates whose cumulative probability reaches a
chosen threshold.

### Greedy decoding

Selecting the highest-scoring next token at every step.

### Beam search

Tracking multiple candidate sequences and retaining high-scoring continuations. It is useful for
some input-grounded sequence tasks but is not automatically the best choice for conversational
generation.

### Hallucination

A fluent output containing unsupported, fabricated, inconsistent, or incorrect claims. The term
does not imply that the model has human beliefs or perceptions.

### Perplexity

An intrinsic measure related to average token prediction likelihood. It can compare language
modelling behavior under controlled conditions, but it does not directly measure task
correctness, safety, usefulness, or business value.

## Mental model

A causal language model repeatedly performs:

```text
Existing token sequence
→ compute hidden representations
→ produce one logit per vocabulary token
→ convert or filter logits
→ select next token
→ append token
→ repeat
```

At a simplified level:

```text
text
→ tokenizer
→ token IDs
→ token and position representations
→ many transformer blocks
→ next-token logits
→ decoding strategy
→ next token ID
→ tokenizer decode
→ generated text
```

The model does not retrieve a sentence from a conventional database each time it answers.
Information learned during training is distributed across parameters, and generated output is
conditioned on the current token sequence.

This explains several important behaviors:

- Fluency can exist without correctness.
- A small prompt change can change the continuation.
- Repeated sampling can produce different outputs.
- The model may continue an incorrect premise.
- Current private policy is not reliably available unless supplied through context, tools, or
  adaptation.
- A deterministic token path can still produce a deterministic false answer.

## Architecture and data flow

### Model-behavior laboratory

```text
Fixed experiment cases
        │
        ▼
Experiment runner
        │
        ├── tokenizer inspection
        ├── base open model
        ├── instruction open model
        └── optional hosted adapter
        │
        ▼
Generation configuration
        │
        ├── greedy
        ├── low-temperature sampling
        └── broader sampling
        │
        ▼
Raw model output
        │
        ▼
Deterministic measurements
        ├── token counts
        ├── latency
        ├── output length
        ├── repetition
        └── instruction-marker checks
        │
        ▼
Human review
        ├── task relevance
        ├── unsupported claims
        ├── uncertainty
        └── support-pilot suitability
        │
        ▼
Versioned result records and selection report
```

### Trust boundaries

- Model repositories and code are external supply-chain inputs.
- `trust_remote_code=True` executes repository-provided Python and is prohibited unless reviewed
  and explicitly approved.
- Hosted providers process submitted content under their service terms and configuration.
- Model output is untrusted data.
- Downloaded weights and tokenizers require licence and provenance review.
- Synthetic test cases are safe for this laboratory; production customer data is not.

### State ownership

| State | Owner |
|---|---|
| Model shortlist | Applied AI and platform owners |
| Test cases | Evaluation owner and support-domain reviewers |
| Generation configurations | Engineering |
| Model and tokenizer identifiers | Experiment runner |
| Raw output | Experiment artifact store |
| Human review | Evaluation and domain reviewers |
| Production selection | Product, engineering, security, finance, and operations |

### Failure boundaries

- A model load failure must not produce a partial success record.
- An input exceeding the context budget must be rejected or intentionally truncated.
- Invalid chat formatting invalidates the comparison.
- Hosted-provider failure must be recorded as unavailable, not replaced with invented output.
- Unsupported output must be marked during review rather than corrected silently.

## Design decisions

### Use a small open model for mechanics

The laboratory should be runnable on broadly available hardware. A small model is sufficient to
inspect:

- Tokenization
- Chat templates
- Logits
- Generation settings
- Latency
- Context growth
- Base versus instruction behavior

Its quality is not representative of larger production models.

### Compare related base and instruction models

Using models from the same family makes the effect of instruction post-training easier to
observe. The lesson examples use configurable model identifiers, with defaults:

- `Qwen/Qwen2.5-0.5B`
- `Qwen/Qwen2.5-0.5B-Instruct`

Verify model licences, repository metadata, files, and organizational approval before download.
The model identifiers are defaults for a lab, not production recommendations.

### Keep hosted integration minimal

Lesson 09 implements production model APIs. This lesson defines an adapter contract and
experiment record so a hosted model can participate without duplicating retry, fallback,
streaming, authentication, or cost-attribution architecture.

### Use scripts as the source of truth

Jupyter is useful for exploration, but committed scripts, configuration, tests, and result files
provide better reproducibility.

### Do not rank models using one aggregate score

A model can be:

- Better at instruction following
- Worse at latency
- More expensive
- Restricted by data policy
- Better at multilingual input
- Worse at schema compliance

Use a decision matrix with task-specific thresholds and tradeoffs.

## Tooling

| Tool | Purpose | Why selected | Limitation | Alternative |
|---|---|---|---|---|
| PyTorch | Tensor operations, toy attention, and open-model execution | Foundation of much of the production LLM ecosystem | Hardware packaging and performance require platform-specific care | JAX for organizations standardized on its ecosystem |
| Hugging Face Transformers | Tokenizers, model loading, chat templates, and generation | Broad open-model support and inspectable APIs | Model repositories vary in quality, licence, and custom-code requirements | Provider SDK for hosted-only teams |
| Safetensors | Safer weight serialization format | Avoids loading arbitrary Python pickle objects for supported checkpoints | Does not establish model or data trustworthiness | Organization-approved artifact format |
| Accelerate | Large-model loading and device support | Integrates with Transformers and later distributed lessons | Not a substitute for serving or cluster orchestration | Native PyTorch device management for small models |
| YAML | Human-reviewable experiment configuration | Suitable for fixed cases and generation plans | Weak without schema validation | JSON or database configuration |
| JSON Lines | Appendable experiment output | One record per run and easy downstream analysis | Large artifacts need external storage and indexing | Parquet for larger analytical datasets |
| JupyterLab | Interactive inspection | Useful for tokens, logits, and plots | Notebook state is easy to lose and hard to operate | Committed Python scripts as the source of truth |
| Hosted model adapter | Optional third candidate | Exposes production-relevant capability without self-hosting | Provider behavior and policy can change | Additional approved open model |

## Model architecture families

### Encoder models

An encoder reads the input and creates contextual representations for all positions.

Common uses:

- Classification
- Token labelling
- Embeddings
- Reranking
- Retrieval

Encoder models are not usually used for open-ended autoregressive chat generation.

### Decoder models

A causal decoder predicts the next token from previous tokens.

Common uses:

- Text generation
- Chat
- Code generation
- Tool-call generation
- Autoregressive multimodal output

Most current general-purpose LLM applications use decoder-style models.

### Encoder-decoder models

An encoder represents the input, and a decoder generates output conditioned on the encoded
input.

Common uses:

- Translation
- Summarization
- Structured sequence transformation
- Some speech and vision-language tasks

### Architecture selection

| Task | Common architecture choice |
|---|---|
| Ticket category prediction | Encoder or classical ML |
| Semantic embedding | Encoder |
| Cross-encoder reranking | Encoder |
| Response drafting | Decoder |
| Translation | Encoder-decoder or decoder |
| Speech recognition | Encoder-decoder or specialized architecture |
| Multimodal chat | Multimodal decoder or combined encoder-decoder system |

Use the architecture that matches the task rather than forcing every problem through a chat
model.

## Dense and mixture-of-experts models

### Dense model

In a simplified dense transformer, every token passes through the same feed-forward parameter
set in each layer.

Advantages:

- Simpler routing behavior
- Predictable execution structure
- Broad tooling support

Costs:

- Increasing parameter count generally increases compute and memory requirements

### Mixture of experts

An MoE layer has multiple experts and a router that selects a subset for each token.

```text
hidden state
→ router scores
→ select top experts
→ expert computation
→ combine outputs
```

Potential advantages:

- Larger total model capacity without activating every parameter for every token

Operational concerns:

- Expert load balancing
- Communication overhead
- Distributed placement
- Active parameter count
- Memory for total weights
- Router behavior

Do not compare models only by total parameter count. Architecture, active parameters, training
data, post-training, precision, serving stack, and task fit all matter.

## Model lifecycle

```text
Data collection and filtering
→ pretraining
→ optional continued pretraining
→ supervised fine-tuning
→ preference or reinforcement-based post-training
→ evaluation
→ optional distillation or quantization
→ serving
→ monitoring and further adaptation
```

### Pretraining

The model learns broad statistical structure by predicting tokens from large data collections.
Pretraining creates capabilities but does not guarantee reliable instruction following.

### Continued pretraining

The model receives additional language-modelling training on a new domain or language mixture.
It may improve domain familiarity but can introduce forgetting or distribution shifts.

### Supervised fine-tuning

The model trains on demonstrations:

```text
instruction or conversation
→ desired response
```

SFT improves target behavior and formatting but does not automatically provide current private
facts.

### Preference optimization

The model learns that some responses are preferred over others according to human, model, or
verifiable feedback.

### Distillation

A student learns from teacher outputs, labels, probabilities, or generated datasets. The aim may
be lower cost, lower latency, or targeted behavior.

### Quantization

Weights or computations use lower precision. This can reduce memory and increase throughput,
but quality and hardware compatibility must be measured.

### Inference

The model is loaded and serves requests. Inference engineering includes:

- Batching
- KV caching
- Quantization
- Parallelism
- Scheduling
- Latency and throughput
- Cost

Later lessons cover each adaptation and serving stage in depth.

## Tokens and tokenization

### Why tokenization matters

Tokenization affects:

- Context usage
- API billing where providers charge by tokens
- Latency
- Memory
- Truncation
- Multilingual efficiency
- Code and number handling
- Training sequence length
- Output limits

Characters and words are not reliable substitutes for token counts.

### Tokenization approaches

#### Word tokenization

Splits on words or word-like units.

Problem:

- Vocabulary becomes very large.
- Unknown words and spelling variants are difficult.

#### Character tokenization

Uses characters as tokens.

Advantage:

- Small vocabulary

Problem:

- Sequences become long.

#### Byte tokenization

Represents text as bytes or byte-derived units.

Advantage:

- Can represent arbitrary text

Problem:

- Raw byte sequences may be long; modern tokenizers usually merge frequent patterns.

#### Subword tokenization

Uses common words and reusable word fragments.

Advantages:

- Handles rare and novel words
- Controls vocabulary size
- Reduces sequence length compared with characters

Common algorithm families include BPE, WordPiece, and Unigram. Exact implementation and
pre-tokenization differ by tokenizer.

### Tokenization is model-specific

The model's embedding table corresponds to its tokenizer vocabulary. Do not substitute a
different tokenizer because it appears to produce fewer tokens.

### Special tokens and chat templates

Chat APIs commonly expose:

```python
[
    {"role": "system", "content": "..."},
    {"role": "user", "content": "..."},
]
```

The model receives a token sequence with model-specific control tokens.

The current Transformers documentation emphasizes that causal chat models still continue token
sequences, and that models can use different chat control tokens even when based on the same
pretrained model. Use the tokenizer's `apply_chat_template` method.

Incorrect chat formatting can significantly reduce quality.

## Embeddings

### Token embedding

Each token ID indexes a learned vector:

```text
token ID
→ embedding table lookup
→ vector
```

If hidden size is `d`, a sequence of `n` tokens begins as a matrix shaped approximately:

```text
n × d
```

### Positional information

Attention alone does not inherently encode sequence order. Models add or apply positional
information so that:

```text
"agent approved refund"
```

differs from:

```text
"refund approved agent"
```

Implementations may use learned positions, sinusoidal methods, rotary position embeddings, or
other schemes.

### Contextual representations

The same token can have different hidden states depending on context:

```text
"bank account"
"river bank"
```

The initial token embedding is transformed through attention and feed-forward layers into a
contextual representation.

### Token embeddings versus retrieval embeddings

Token embeddings are internal model representations. Retrieval embedding models produce
vectors designed for comparing sentences, passages, images, or other items. Lesson 12 covers
retrieval embeddings.

## Logits, softmax, and probabilities

For a vocabulary of size `V`, the model produces `V` next-token logits.

Given logits `z`, softmax is:

```text
p_i = exp(z_i) / sum_j exp(z_j)
```

For numerical stability, subtract the maximum logit before exponentiation.

### Minimal softmax

**`src/ai_industry_labs/model_lab/math_utils.py`**

```python
from collections.abc import Sequence
from math import exp


def softmax(logits: Sequence[float], temperature: float = 1.0) -> list[float]:
    if not logits:
        raise ValueError("logits must not be empty")
    if temperature <= 0:
        raise ValueError("temperature must be greater than zero")

    scaled = [value / temperature for value in logits]
    maximum = max(scaled)
    exponentials = [exp(value - maximum) for value in scaled]
    denominator = sum(exponentials)

    return [value / denominator for value in exponentials]
```

### Temperature effect

For logits:

```text
[4.0, 2.0, 1.0]
```

- Lower temperature makes the highest-scoring token more dominant.
- Higher temperature spreads probability across more candidates.

Temperature does not:

- Verify facts
- Add evidence
- Fix prompt injection
- Expand the model context
- Change model weights

### Probabilities are conditional

The next-token probability means:

```text
P(next token | current token sequence)
```

It is not a calibrated probability that the complete answer is correct.

## Autoregressive generation

### Minimal conceptual loop

```python
tokens = tokenizer.encode(prompt)

while not finished:
    logits = model(tokens)
    next_token_logits = logits[-1]
    next_token = decode_strategy(next_token_logits)
    tokens.append(next_token)

return tokenizer.decode(tokens)
```

Real implementations add:

- Batching
- KV caching
- Attention masks
- Stop conditions
- Length controls
- Sampling filters
- Device placement
- Mixed precision
- Distributed execution

### Exposure to earlier generated output

At every step, the model conditions on its own previous tokens. An early poor choice can change
later output.

### Stop behavior

Generation can stop because:

- End-of-sequence token is generated
- Maximum new tokens is reached
- Stop sequence is detected
- Structured decoder completes a schema
- Application cancels the request

Output limits are a safety, latency, and cost control.

## Self-attention

### Operational intuition

For each token position, attention asks:

> Which earlier or allowed positions contain information useful for updating this position?

Each hidden state is projected into:

- Query vector `Q`
- Key vector `K`
- Value vector `V`

Scaled dot-product attention is:

```text
Attention(Q, K, V) = softmax(QKᵀ / sqrt(d_k) + mask) V
```

### Steps

```text
hidden states
→ project to Q, K, V
→ compare queries with keys
→ scale scores
→ apply causal and padding masks
→ softmax to attention weights
→ weighted sum of values
```

### Why scale by square root of key dimension

Dot-product magnitude tends to grow with dimension. Scaling helps keep softmax inputs in a range
that supports stable gradients and useful probabilities.

### Causal mask

For tokens:

```text
[A, B, C, D]
```

position `C` may attend to `A`, `B`, and `C`, but not future position `D`.

### Multi-head attention

The model uses multiple attention heads with separate learned projections. Heads can represent
different patterns, but assigning a simple human meaning to every head is often unreliable.

### Toy attention implementation

**`src/ai_industry_labs/model_lab/attention_demo.py`**

```python
import math

import torch


def causal_attention(
    query: torch.Tensor,
    key: torch.Tensor,
    value: torch.Tensor,
) -> tuple[torch.Tensor, torch.Tensor]:
    if query.ndim != 2 or key.ndim != 2 or value.ndim != 2:
        raise ValueError("query, key, and value must be rank-2 tensors")
    if query.shape != key.shape or key.shape != value.shape:
        raise ValueError("query, key, and value shapes must match")

    sequence_length, key_dimension = query.shape
    scores = query @ key.transpose(0, 1)
    scores = scores / math.sqrt(key_dimension)

    causal_mask = torch.triu(
        torch.ones(sequence_length, sequence_length, dtype=torch.bool),
        diagonal=1,
    )
    scores = scores.masked_fill(causal_mask, float("-inf"))

    weights = torch.softmax(scores, dim=-1)
    output = weights @ value
    return output, weights
```

This demonstrates the mathematics, not an optimized production attention kernel.

## Transformer block

A simplified pre-normalization block:

```text
input
├── normalize
├── self-attention
├── add residual
├── normalize
├── feed-forward network
└── add residual
    ↓
output
```

Modern architectures vary:

- Normalization placement
- Activation
- Positional method
- Attention variants
- Grouped or multi-query attention
- Feed-forward form
- Expert routing
- Bias usage

Do not assume all models use the exact original transformer architecture.

## Context windows

### Context budget

The effective request budget includes:

```text
system instructions
+ user message
+ conversation history
+ retrieved evidence
+ tool descriptions
+ tool results
+ formatting and special tokens
+ output budget
≤ supported context
```

### Context overflow

When a request exceeds the model or provider limit:

- The application may reject it.
- Older content may be truncated.
- A framework may truncate silently.
- The provider may return an error.

Silent truncation can remove:

- System requirements
- User constraints
- Critical evidence
- Earlier approvals

Always measure token count before sending a request near the limit.

### Longer context is not free

Potential effects:

- More input processing
- Higher memory use
- Higher API cost
- Higher latency
- More irrelevant information
- Harder evidence selection
- Reduced attention to important content

The relationship is implementation-dependent. Do not claim a universal fixed scaling law for
all serving systems.

### Context capacity versus effective use

A model accepting a long input does not guarantee equal use of every relevant token. Evaluate
position, distractors, evidence volume, and question type.

### Output budget

Reserve enough tokens for the answer:

```text
maximum context
- input tokens
- safety margin
= maximum possible output tokens
```

## Base, instruction, reasoning, and multimodal models

### Base model behavior

A base model continues the prompt according to pretraining patterns.

Prompt:

```text
Customer: I was charged twice.
Support agent:
```

Possible behavior:

- Continue a dialogue
- Produce a fictional transcript
- Complete a document pattern
- Provide an answer

The behavior is less reliably aligned with explicit instructions.

### Instruction-tuned behavior

An instruction-tuned model has seen examples of tasks and assistant responses. It is more likely
to:

- Follow task wording
- Respect chat roles
- Produce requested structure
- Refuse some requests
- Use an assistant style

It can still hallucinate, ignore constraints, or fail schema requirements.

### Reasoning-oriented behavior

Reasoning-oriented models may use:

- Additional inference compute
- Internal or exposed reasoning fields
- Search or verification techniques
- Specialized post-training

Use them when task gains justify latency and cost. Do not use maximum reasoning effort for every
classification or extraction task.

Do not require a model to reveal hidden reasoning. Evaluate the answer, evidence, tool actions,
and verifiable intermediate artifacts.

### Multimodal behavior

Multimodal models can process combinations such as:

- Text and image
- Text and document pages
- Text and audio
- Text and video

Each modality adds:

- Preprocessing
- Token or feature cost
- Privacy concerns
- New failure modes
- Modality-specific evaluation

Lessons 26 and 27 cover multimodal and voice systems.

## Chat templates

### Why templates are required

A chat is converted into model-specific control tokens. Different instruction models may use
different representations for:

- System role
- User role
- Assistant role
- End of message
- Beginning and end of sequence

Use:

```python
tokenizer.apply_chat_template(
    messages,
    tokenize=True,
    add_generation_prompt=True,
    return_tensors="pt",
)
```

The current Transformers documentation recommends tokenizing through the template directly when
possible, avoiding duplicated special tokens.

### Training versus inference

For inference:

- `add_generation_prompt=True` may add the assistant-start marker when required.

For training:

- The full assistant answer is already present.
- `add_generation_prompt=False` is generally appropriate.

Model-specific behavior must be checked in the tokenizer documentation.

## Decoding strategies

### Greedy decoding

Configuration:

```text
do_sample = false
```

Use for:

- Reproducible baseline
- Short constrained tasks
- Debugging

Limitations:

- Can repeat
- Can choose a locally likely but globally poor continuation
- Deterministic false answers remain false

### Sampling

Configuration:

```text
do_sample = true
temperature > 0
```

Use for:

- Diversity
- Creative generation
- Exploring output variation

Production concerns:

- Reproducibility
- Quality variance
- More evaluation samples

### Top-k

Restricts candidates to the highest `k` logits before sampling.

### Top-p

Restricts candidates to a dynamic set covering cumulative probability `p`.

### Combining controls

Temperature, top-k, and top-p interact. Do not tune one in isolation and assume behavior
transfers across models and tasks.

### Beam search

Beam search maintains several candidate sequences. It is often more useful for input-grounded
tasks such as translation, transcription, or captioning than for free-form chat.

### Repetition controls

Frameworks may support:

- Repetition penalty
- No-repeat n-gram constraints
- Token suppression

Overly aggressive controls can damage valid repeated terms, identifiers, or structured output.

### Structured generation

Structured generation constrains output to a grammar or schema. It can improve syntactic
validity but does not guarantee semantic correctness.

Lesson 09 implements provider structured outputs; Lesson 10 covers prompt and context contracts.

## Hallucination and uncertainty

### Why unsupported output occurs

Possible causes:

- Training data contains conflicting or incorrect patterns.
- Prompt contains an incorrect premise.
- Required fact is absent from parameters and context.
- Evidence is irrelevant, stale, or too large.
- Decoding selects a plausible continuation.
- Instruction post-training rewards helpful-sounding answers.
- The model fails to represent uncertainty appropriately.

### Hallucination is a system property

Measure:

- Model behavior
- Prompt
- Context
- Retrieval
- Tools
- Validation
- Human review

The same model can have different unsupported-claim rates in different systems.

### Confidence limitations

Do not treat:

- Fluent wording
- Long explanations
- Token probability
- Self-reported confidence

as proof of answer correctness.

### Mitigations

- Use authoritative evidence
- Retrieve current private data
- Require citations
- Validate claims where possible
- Use tools for calculations and state
- Add abstention
- Use human review for consequential output
- Evaluate on realistic failure cases

### Calibration

Calibration asks whether stated or inferred confidence aligns with observed correctness. LLM
confidence requires task-specific measurement and may not transfer across prompts or domains.

## Hosted versus open-weight models

### Hosted model

Advantages:

- Fast access
- Managed scaling
- Strong capabilities
- Reduced infrastructure burden
- Rapid feature availability

Concerns:

- Data policy and regional processing
- Vendor dependency
- Model updates
- Rate limits
- Cost variability
- Limited weight access
- Provider-specific APIs

### Open-weight model

Advantages:

- Deployment control
- Private hosting options
- Adaptation
- Inspectable artifacts
- Provider portability

Concerns:

- Infrastructure ownership
- Security
- Capacity planning
- Model licence
- Evaluation
- Updates and patching

### Open source versus open weight

Access to weights does not necessarily imply:

- Open training data
- Open training code
- Unrestricted commercial use
- Full reproducibility

Read the licence and model card.

### Selection matrix

| Dimension | Hosted | Open weight |
|---|---|---|
| Time to first experiment | Usually faster | Requires download and runtime setup |
| Infrastructure ownership | Lower | Higher |
| Data-control options | Provider-dependent | Can be privately hosted |
| Fine-tuning control | Provider-dependent | Broad, subject to licence and compute |
| Scaling | Managed | Team-owned |
| Version stability | Provider policy | Team controls artifact |
| Cost model | Usage-based | Infrastructure plus operations |
| Offline use | Usually unavailable | Possible |

## Model-selection criteria

Evaluate:

- Task correctness
- Instruction following
- Structured-output compliance
- Evidence use
- Appropriate abstention
- Tool-use reliability
- Multilingual quality
- Context capacity
- Latency
- Throughput
- Cost per successful task
- Memory and hardware
- Data policy
- Region availability
- Model and licence terms
- Versioning
- Fine-tuning support
- Operational maturity

Do not select from:

- Parameter count alone
- One public leaderboard
- One impressive prompt
- Marketing category
- Lowest per-token price without quality

## Project structure

Add:

```text
ai-industry-labs/
├── model-lab/
│   ├── cases.yaml
│   ├── experiment-plan.yaml
│   ├── model-catalog.yaml
│   ├── results/
│   │   └── .gitkeep
│   └── selection-report.md
├── src/
│   └── ai_industry_labs/
│       └── model_lab/
│           ├── __init__.py
│           ├── attention_demo.py
│           ├── catalog.py
│           ├── cli.py
│           ├── generation.py
│           ├── math_utils.py
│           ├── metrics.py
│           ├── models.py
│           ├── open_model.py
│           └── tokenizer_inspector.py
└── tests/
    ├── test_attention_demo.py
    ├── test_generation.py
    ├── test_math_utils.py
    ├── test_model_lab_models.py
    └── test_tokenizer_inspector.py
```

## Environment setup

### Add dependencies

Continue in the `ai-industry-labs` repository.

```powershell
uv add "torch>=2.7,<3" "transformers>=5.12,<6" "accelerate>=1,<3" `
    "safetensors>=0.5,<1" "pyyaml>=6,<7"
uv add --dev "jupyterlab>=4,<5"
uv lock
uv sync --locked
```

The selected ranges reflect the official documentation verified for this lesson. The committed
lockfile records the exact environment. PyTorch installation can depend on operating system and
accelerator. Follow the official PyTorch selector when a CUDA-specific build is required.

### Verify

```powershell
uv run python -c "import torch, transformers; print(torch.__version__); print(transformers.__version__)"
uv run python -c "import torch; print('cuda', torch.cuda.is_available())"
```

### Model cache

Model downloads may be large. Configure an approved cache location where necessary:

```powershell
$env:HF_HOME = "D:\model-cache"
```

Do not commit the cache or model weights into the application repository.

### Authentication

Some model repositories require accepted terms or authentication. Use the official CLI and an
approved token store. Never put a model hub token in:

- Source code
- Notebook cells
- Git-tracked `.env`
- Docker image layers

### Security rule

Do not enable `trust_remote_code=True` for this lesson. Loading custom repository code executes
external Python in the environment.

## Data contract

### Experiment case

**`model-lab/cases.yaml`**

```yaml
cases:
  - id: "classification-routine"
    task: "classification"
    prompt: "Classify this ticket as billing, account, technical, or security: I was charged twice."
    expected_markers:
      - "billing"
    prohibited_markers:
      - "refund issued"
    max_new_tokens: 32

  - id: "draft-with-evidence"
    task: "drafting"
    prompt: |
      Evidence:
      - Duplicate charges must be reviewed before refund eligibility is confirmed.
      - Support agents cannot issue refunds without approval.

      Draft a concise response that acknowledges the issue and explains the next step.
    expected_markers:
      - "review"
      - "approval"
    prohibited_markers:
      - "I issued"
      - "refund completed"
    max_new_tokens: 120

  - id: "unsupported-policy"
    task: "abstention"
    prompt: |
      The customer asks whether an undocumented lifetime refund policy applies.
      No supporting policy is available. State what should happen next.
    expected_markers:
      - "escalat"
    prohibited_markers:
      - "lifetime refund is guaranteed"
    max_new_tokens: 80

  - id: "multilingual-tokenization"
    task: "tokenization"
    prompt: "The customer wrote: تم تحصيل الرسوم مرتين. Please summarize the issue."
    expected_markers: []
    prohibited_markers: []
    max_new_tokens: 64

  - id: "code-and-json"
    task: "structured"
    prompt: |
      Return a compact JSON object with keys category and requires_approval
      for this ticket: Customer requests a $500 refund.
    expected_markers:
      - "category"
      - "requires_approval"
    prohibited_markers: []
    max_new_tokens: 64
```

### Model catalog entry

```yaml
models:
  - id: "open-base-small"
    kind: "open"
    repository: "Qwen/Qwen2.5-0.5B"
    model_type: "base"
    approved_for_synthetic_data_only: true

  - id: "open-instruct-small"
    kind: "open"
    repository: "Qwen/Qwen2.5-0.5B-Instruct"
    model_type: "instruction"
    approved_for_synthetic_data_only: true

  - id: "hosted-candidate"
    kind: "hosted"
    repository: null
    model_type: "instruction"
    approved_for_synthetic_data_only: true
```

### Experiment configuration

```yaml
experiments:
  - name: "greedy"
    do_sample: false
    temperature: 1.0
    top_k: null
    top_p: 1.0
    repetitions: 1

  - name: "low-temperature-sampling"
    do_sample: true
    temperature: 0.3
    top_k: 50
    top_p: 0.9
    repetitions: 3

  - name: "broad-sampling"
    do_sample: true
    temperature: 0.9
    top_k: 50
    top_p: 0.95
    repetitions: 5
```

### Result record

Every run records:

| Field | Meaning |
|---|---|
| `run_id` | Unique experiment run |
| `case_id` | Fixed test case |
| `model_id` | Model catalog ID |
| `model_revision` | Revision if pinned |
| `tokenizer_id` | Tokenizer identifier |
| `generation` | Decoding configuration |
| `seed` | Random seed when sampling |
| `input_tokens` | Measured token count |
| `output_tokens` | Measured generated token count |
| `latency_ms` | End-to-end measured latency |
| `output_text` | Raw generated output |
| `expected_markers_found` | Deterministic marker results |
| `prohibited_markers_found` | Deterministic failure markers |
| `device` | CPU, CUDA, or other |
| `framework_versions` | PyTorch and Transformers versions |
| `error` | Failure category if generation failed |

### Validity rules

- Case IDs are unique.
- Model IDs are unique.
- Sampling repetitions are at least one.
- Temperature is positive.
- `top_p` is greater than zero and at most one.
- `top_k`, when supplied, is positive.
- `max_new_tokens` is bounded.
- Result records do not omit model and tokenizer identity.

## Establish the baseline

This lesson uses two baselines for different questions.

### Product baseline

The non-model baseline from Lesson 07 is:

```text
Improved policy search
+ approved response templates
+ manual agent review
```

The future LLM product must outperform that workflow on useful business metrics without
degrading policy error, reopen rate, privacy, or agent workload.

### Model-behavior baseline

The first model baseline is:

```text
small open base model
+ semantically equivalent raw prompt
+ greedy decoding
+ bounded output
```

This baseline reveals continuation behavior before instruction post-training and sampling are
introduced.

The second baseline is the related instruction model with:

```text
official chat template
+ greedy decoding
+ the same task meaning
+ the same output limit
```

### Baseline measurements

Record:

- Exact model and tokenizer revision
- Input and output token counts
- Load and request latency
- Required and prohibited markers
- Raw output
- Human review
- Hardware and framework versions

Do not publish an aggregate quality claim until the fixed cases are reviewed.

### Revision requirement

Exploratory runs may begin from a named repository revision such as `main`. Before the final
selection report:

- Resolve and record the exact repository commit.
- Re-run the selected experiments.
- Preserve the commit in the model catalog.

## Minimal implementation

### Package initialization

**`src/ai_industry_labs/model_lab/__init__.py`**

```python
"""Reproducible experiments for language-model behavior."""
```

### Typed experiment models

**`src/ai_industry_labs/model_lab/models.py`**

```python
from enum import StrEnum
from typing import Literal

from pydantic import BaseModel, Field, model_validator


class ModelKind(StrEnum):
    OPEN = "open"
    HOSTED = "hosted"


class ModelType(StrEnum):
    BASE = "base"
    INSTRUCTION = "instruction"
    REASONING = "reasoning"
    MULTIMODAL = "multimodal"


class ExperimentCase(BaseModel):
    id: str = Field(pattern=r"^[a-z0-9][a-z0-9-]*$")
    task: str = Field(min_length=3, max_length=80)
    prompt: str = Field(min_length=1, max_length=20000)
    expected_markers: list[str] = Field(default_factory=list)
    prohibited_markers: list[str] = Field(default_factory=list)
    max_new_tokens: int = Field(ge=1, le=512)


class ModelSpec(BaseModel):
    id: str = Field(pattern=r"^[a-z0-9][a-z0-9-]*$")
    kind: ModelKind
    repository: str | None = None
    revision: str | None = None
    model_type: ModelType
    approved_for_synthetic_data_only: bool = True

    @model_validator(mode="after")
    def require_repository_for_open_model(self) -> "ModelSpec":
        if self.kind is ModelKind.OPEN and not self.repository:
            raise ValueError("open models require a repository")
        return self


class GenerationSpec(BaseModel):
    name: str = Field(pattern=r"^[a-z0-9][a-z0-9-]*$")
    do_sample: bool
    temperature: float = Field(gt=0, le=2)
    top_k: int | None = Field(default=None, gt=0)
    top_p: float = Field(gt=0, le=1)
    repetitions: int = Field(ge=1, le=20)


class RunResult(BaseModel):
    run_id: str
    case_id: str
    model_id: str
    model_revision: str | None
    tokenizer_id: str
    generation_name: str
    seed: int | None
    input_tokens: int
    output_tokens: int
    latency_ms: float
    output_text: str
    expected_markers_found: dict[str, bool]
    prohibited_markers_found: dict[str, bool]
    device: str
    torch_version: str
    transformers_version: str
    status: Literal["ok", "error"]
    error: str | None = None
```

### Configuration loader

**`src/ai_industry_labs/model_lab/catalog.py`**

```python
from pathlib import Path

import yaml
from pydantic import BaseModel

from ai_industry_labs.model_lab.models import (
    ExperimentCase,
    GenerationSpec,
    ModelSpec,
)

def load_yaml(path: Path) -> dict[str, object]:
    with path.open(encoding="utf-8") as file:
        data = yaml.safe_load(file)
    if not isinstance(data, dict):
        raise ValueError(f"{path} must contain a YAML mapping")
    return data


def load_item_list(path: Path, *, key: str) -> list[object]:
    data = load_yaml(path)
    items = data.get(key)
    if not isinstance(items, list):
        raise ValueError(f"{path} must contain a list at key {key!r}")
    return items


def validate_unique_ids(items: list[BaseModel], *, field: str) -> None:
    values = [getattr(item, field) for item in items]
    if len(values) != len(set(values)):
        raise ValueError(f"duplicate {field} values are not allowed")


def load_cases(path: Path) -> list[ExperimentCase]:
    cases = [
        ExperimentCase.model_validate(item)
        for item in load_item_list(path, key="cases")
    ]
    validate_unique_ids(cases, field="id")
    return cases


def load_models(path: Path) -> list[ModelSpec]:
    models = [
        ModelSpec.model_validate(item)
        for item in load_item_list(path, key="models")
    ]
    validate_unique_ids(models, field="id")
    return models


def load_experiments(path: Path) -> list[GenerationSpec]:
    experiments = [
        GenerationSpec.model_validate(item)
        for item in load_item_list(path, key="experiments")
    ]
    validate_unique_ids(experiments, field="name")
    return experiments
```

### Tokenizer inspector

**`src/ai_industry_labs/model_lab/tokenizer_inspector.py`**

```python
from dataclasses import dataclass

from transformers import PreTrainedTokenizerBase


@dataclass(frozen=True)
class TokenRecord:
    position: int
    token_id: int
    token_text: str


@dataclass(frozen=True)
class TokenizationReport:
    tokenizer_id: str
    character_count: int
    token_count: int
    characters_per_token: float
    records: list[TokenRecord]


def inspect_text(
    tokenizer: PreTrainedTokenizerBase,
    *,
    tokenizer_id: str,
    text: str,
) -> TokenizationReport:
    token_ids = tokenizer.encode(text, add_special_tokens=False)
    tokens = tokenizer.convert_ids_to_tokens(token_ids)

    records = [
        TokenRecord(position=index, token_id=token_id, token_text=token)
        for index, (token_id, token) in enumerate(
            zip(token_ids, tokens, strict=True)
        )
    ]
    token_count = len(token_ids)
    characters_per_token = (
        len(text) / token_count if token_count > 0 else 0.0
    )

    return TokenizationReport(
        tokenizer_id=tokenizer_id,
        character_count=len(text),
        token_count=token_count,
        characters_per_token=characters_per_token,
        records=records,
    )
```

### Marker metrics

**`src/ai_industry_labs/model_lab/metrics.py`**

```python
import re


def marker_results(text: str, markers: list[str]) -> dict[str, bool]:
    normalized = text.casefold()
    return {
        marker: re.search(re.escape(marker.casefold()), normalized) is not None
        for marker in markers
    }


def repeated_ngram_fraction(text: str, *, n: int = 3) -> float:
    words = text.casefold().split()
    if n <= 0:
        raise ValueError("n must be positive")
    if len(words) < n:
        return 0.0

    ngrams = [tuple(words[index : index + n]) for index in range(len(words) - n + 1)]
    return 1 - (len(set(ngrams)) / len(ngrams))
```

Marker checks are weak quality signals. They do not replace semantic or human evaluation.

### Open-model loader

**`src/ai_industry_labs/model_lab/open_model.py`**

```python
from dataclasses import dataclass

import torch
from transformers import AutoModelForCausalLM, AutoTokenizer, PreTrainedModel
from transformers.tokenization_utils_base import PreTrainedTokenizerBase


@dataclass
class OpenModelBundle:
    model_id: str
    tokenizer_id: str
    tokenizer: PreTrainedTokenizerBase
    model: PreTrainedModel
    device: torch.device


def select_device() -> torch.device:
    if torch.cuda.is_available():
        return torch.device("cuda")
    if torch.backends.mps.is_available():
        return torch.device("mps")
    return torch.device("cpu")


def load_open_model(
    model_id: str,
    *,
    revision: str | None = None,
) -> OpenModelBundle:
    device = select_device()
    dtype = (
        torch.float16
        if device.type in {"cuda", "mps"}
        else torch.float32
    )
    tokenizer = AutoTokenizer.from_pretrained(
        model_id,
        revision=revision,
        trust_remote_code=False,
    )
    model = AutoModelForCausalLM.from_pretrained(
        model_id,
        revision=revision,
        trust_remote_code=False,
        dtype=dtype,
        low_cpu_mem_usage=True,
        use_safetensors=True,
    )
    model.to(device)
    model.eval()

    return OpenModelBundle(
        model_id=model_id,
        tokenizer_id=tokenizer.name_or_path,
        tokenizer=tokenizer,
        model=model,
        device=device,
    )
```

### Prompt formatting

**`src/ai_industry_labs/model_lab/generation.py`**

```python
from dataclasses import dataclass
from time import perf_counter

import torch
from transformers import PreTrainedModel
from transformers.tokenization_utils_base import PreTrainedTokenizerBase

from ai_industry_labs.model_lab.models import GenerationSpec


@dataclass(frozen=True)
class GenerationOutput:
    text: str
    input_tokens: int
    output_tokens: int
    latency_ms: float


def prepare_inputs(
    *,
    tokenizer: PreTrainedTokenizerBase,
    prompt: str,
    instruction_model: bool,
) -> dict[str, torch.Tensor]:
    if instruction_model and tokenizer.chat_template:
        messages = [{"role": "user", "content": prompt}]
        prepared = tokenizer.apply_chat_template(
            messages,
            tokenize=True,
            add_generation_prompt=True,
            return_tensors="pt",
            return_dict=True,
        )
        return dict(prepared)

    return dict(tokenizer(prompt, return_tensors="pt"))


def generate_text(
    *,
    model: PreTrainedModel,
    tokenizer: PreTrainedTokenizerBase,
    prompt: str,
    instruction_model: bool,
    generation: GenerationSpec,
    max_new_tokens: int,
    seed: int | None,
) -> GenerationOutput:
    if seed is not None:
        torch.manual_seed(seed)
        if torch.cuda.is_available():
            torch.cuda.manual_seed_all(seed)

    inputs = prepare_inputs(
        tokenizer=tokenizer,
        prompt=prompt,
        instruction_model=instruction_model,
    )
    device = next(model.parameters()).device
    inputs = {name: tensor.to(device) for name, tensor in inputs.items()}
    input_tokens = int(inputs["input_ids"].shape[-1])
    context_limit = getattr(model.config, "max_position_embeddings", None)
    if (
        isinstance(context_limit, int)
        and input_tokens + max_new_tokens > context_limit
    ):
        raise ValueError(
            "formatted input and output budget exceed model context limit"
        )

    pad_token_id = tokenizer.pad_token_id
    if pad_token_id is None:
        pad_token_id = tokenizer.eos_token_id
    if pad_token_id is None:
        raise ValueError("tokenizer requires a pad or end-of-sequence token")

    generation_arguments: dict[str, object] = {
        "max_new_tokens": max_new_tokens,
        "do_sample": generation.do_sample,
        "pad_token_id": pad_token_id,
    }
    if generation.do_sample:
        generation_arguments.update(
            {
                "temperature": generation.temperature,
                "top_p": generation.top_p,
            }
        )
        if generation.top_k is not None:
            generation_arguments["top_k"] = generation.top_k

    started = perf_counter()
    with torch.inference_mode():
        output_ids = model.generate(**inputs, **generation_arguments)
    latency_ms = (perf_counter() - started) * 1000

    generated_ids = output_ids[0, input_tokens:]
    text = tokenizer.decode(generated_ids, skip_special_tokens=True)

    return GenerationOutput(
        text=text,
        input_tokens=input_tokens,
        output_tokens=int(generated_ids.shape[-1]),
        latency_ms=latency_ms,
    )
```

Only pass sampling controls when sampling is enabled. This prevents misleading warnings and
keeps greedy runs explicit.

## Production implementation

### Experiment runner

The production-learning implementation adds:

- Model and tokenizer identity
- Config validation
- Repeatable seeds
- Error records
- Result persistence
- Environment versions
- Context checks
- Marker and repetition metrics
- No remote code execution

**`src/ai_industry_labs/model_lab/cli.py`**

```python
import argparse
import json
import platform
import uuid
from pathlib import Path

import torch
import transformers

from ai_industry_labs.model_lab.catalog import (
    load_cases,
    load_experiments,
    load_models,
)
from ai_industry_labs.model_lab.generation import generate_text
from ai_industry_labs.model_lab.metrics import (
    marker_results,
    repeated_ngram_fraction,
)
from ai_industry_labs.model_lab.open_model import load_open_model


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run open-model behavior experiments")
    parser.add_argument("--cases", type=Path, required=True)
    parser.add_argument("--models", type=Path, required=True)
    parser.add_argument("--experiments", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--model-id", required=True)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    cases = load_cases(args.cases)
    models = {item.id: item for item in load_models(args.models)}
    experiments = load_experiments(args.experiments)

    spec = models[args.model_id]
    if spec.kind.value != "open":
        raise ValueError("this runner handles open models only")
    if spec.repository is None:
        raise ValueError("open model repository is required")

    bundle = load_open_model(spec.repository, revision=spec.revision)

    args.output.parent.mkdir(parents=True, exist_ok=True)

    with args.output.open("w", encoding="utf-8") as file:
        for case in cases:
            for experiment in experiments:
                for repetition in range(experiment.repetitions):
                    seed = 1000 + repetition if experiment.do_sample else None
                    run_id = str(uuid.uuid4())

                    try:
                        output = generate_text(
                            model=bundle.model,
                            tokenizer=bundle.tokenizer,
                            prompt=case.prompt,
                            instruction_model=(
                                spec.model_type.value != "base"
                            ),
                            generation=experiment,
                            max_new_tokens=case.max_new_tokens,
                            seed=seed,
                        )
                        record = {
                            "run_id": run_id,
                            "case_id": case.id,
                            "model_id": spec.id,
                            "model_repository": spec.repository,
                            "model_revision": spec.revision,
                            "tokenizer_id": bundle.tokenizer_id,
                            "generation_name": experiment.name,
                            "seed": seed,
                            "input_tokens": output.input_tokens,
                            "output_tokens": output.output_tokens,
                            "latency_ms": output.latency_ms,
                            "output_text": output.text,
                            "expected_markers_found": marker_results(
                                output.text,
                                case.expected_markers,
                            ),
                            "prohibited_markers_found": marker_results(
                                output.text,
                                case.prohibited_markers,
                            ),
                            "repeated_trigram_fraction": repeated_ngram_fraction(
                                output.text
                            ),
                            "device": str(bundle.device),
                            "python_version": platform.python_version(),
                            "torch_version": torch.__version__,
                            "transformers_version": transformers.__version__,
                            "status": "ok",
                            "error": None,
                        }
                    except Exception as exc:
                        record = {
                            "run_id": run_id,
                            "case_id": case.id,
                            "model_id": spec.id,
                            "generation_name": experiment.name,
                            "seed": seed,
                            "status": "error",
                            "error": f"{type(exc).__name__}: {exc}",
                        }

                    file.write(json.dumps(record, ensure_ascii=False) + "\n")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
```

### Hosted model adapter contract

Do not implement provider-specific behavior here. Define:

**`src/ai_industry_labs/model_lab/hosted.py`**

```python
from typing import Protocol

from ai_industry_labs.model_lab.generation import GenerationOutput
from ai_industry_labs.model_lab.models import GenerationSpec


class HostedModelAdapter(Protocol):
    @property
    def model_id(self) -> str:
        raise NotImplementedError

    def count_input_tokens(self, prompt: str) -> int:
        raise NotImplementedError

    def generate(
        self,
        *,
        prompt: str,
        generation: GenerationSpec,
        max_new_tokens: int,
        seed: int | None,
    ) -> GenerationOutput:
        raise NotImplementedError
```

Lesson 09 will implement:

- Authentication
- Timeouts
- Retries
- Streaming
- Structured output
- Rate limits
- Fallback
- Cost attribution

### Result storage

Use JSON Lines:

- One independent record per run
- Streamable writes
- Easy recovery from partial experiments
- Easy loading into Polars, pandas, Spark, or a database

Do not commit large outputs or sensitive prompts to Git. Store experiment metadata in Git and
artifacts in an approved artifact store when results grow.

## Model-behavior experiments

### Tokenizer comparison

Inspect:

- Short English ticket
- Long policy paragraph
- Arabic or another supported language
- Product code
- JSON
- Whitespace and punctuation
- Repeated numbers
- URL

Record:

- Characters
- Tokens
- Characters per token
- Token pieces
- Special tokens

### Base versus instruction

Use equivalent content but model-appropriate formatting.

Compare:

- Direct task compliance
- Assistant-style response
- Output structure
- Continuation behavior
- Refusal or uncertainty

Do not feed a chat template to a base model and then claim a fair model-family comparison.

### Greedy versus sampling

For each:

- Run greedy once
- Run low-temperature sampling three times
- Run broader sampling five times

Measure:

- Variation
- Repetition
- Required and prohibited markers
- Length
- Latency

### Context growth

Create prompt versions with:

- No evidence
- One relevant evidence passage
- Relevant plus irrelevant passages
- Long repeated conversation history

Measure:

- Token count
- Latency
- Output behavior
- Use of relevant evidence
- Distractor sensitivity

Do not intentionally exceed machine memory. Use bounded cases.

### Incorrect premise

Prompt:

```text
The lifetime refund policy guarantees every customer a refund.
Explain how to issue it.
```

No such policy exists in the synthetic evidence.

Evaluate whether the model:

- Accepts the premise
- Questions it
- Asks for evidence
- Invents procedure

### Missing evidence

Evaluate whether the model:

- Abstains
- Escalates
- Produces unsupported detail

### Structured-output attempt

Prompt for JSON and measure syntactic validity. Do not infer that valid JSON is semantically
correct.

## Testing

### Math tests

**`tests/test_math_utils.py`**

```python
import pytest

from ai_industry_labs.model_lab.math_utils import softmax


def test_softmax_sums_to_one() -> None:
    probabilities = softmax([4.0, 2.0, 1.0])

    assert sum(probabilities) == pytest.approx(1.0)
    assert probabilities[0] > probabilities[1] > probabilities[2]


def test_lower_temperature_sharpens_distribution() -> None:
    low = softmax([4.0, 2.0, 1.0], temperature=0.5)
    high = softmax([4.0, 2.0, 1.0], temperature=1.5)

    assert low[0] > high[0]


@pytest.mark.parametrize("temperature", [0.0, -1.0])
def test_invalid_temperature_is_rejected(temperature: float) -> None:
    with pytest.raises(ValueError):
        softmax([1.0, 2.0], temperature=temperature)
```

### Attention tests

**`tests/test_attention_demo.py`**

```python
import torch

from ai_industry_labs.model_lab.attention_demo import causal_attention


def test_attention_shapes_and_probability_rows() -> None:
    query = torch.eye(3)
    key = torch.eye(3)
    value = torch.arange(9, dtype=torch.float32).reshape(3, 3)

    output, weights = causal_attention(query, key, value)

    assert output.shape == (3, 3)
    assert weights.shape == (3, 3)
    assert torch.allclose(weights.sum(dim=-1), torch.ones(3))


def test_causal_attention_blocks_future_positions() -> None:
    query = torch.eye(3)
    key = torch.eye(3)
    value = torch.eye(3)

    _, weights = causal_attention(query, key, value)

    assert weights[0, 1].item() == 0
    assert weights[0, 2].item() == 0
    assert weights[1, 2].item() == 0
```

### Configuration tests

**`tests/test_model_lab_models.py`**

```python
import pytest

from ai_industry_labs.model_lab.models import (
    GenerationSpec,
    ModelKind,
    ModelSpec,
    ModelType,
)


def test_open_model_requires_repository() -> None:
    with pytest.raises(ValueError):
        ModelSpec(
            id="missing-repository",
            kind=ModelKind.OPEN,
            repository=None,
            model_type=ModelType.BASE,
        )


def test_generation_limits_sampling_parameters() -> None:
    with pytest.raises(ValueError):
        GenerationSpec(
            name="invalid",
            do_sample=True,
            temperature=0.7,
            top_k=0,
            top_p=1.2,
            repetitions=1,
        )
```

### Tokenizer tests

Tokenizer tests may download artifacts. Mark them as integration tests and cache approved
artifacts in CI where appropriate.

**`tests/test_tokenizer_inspector.py`**

```python
from transformers import AutoTokenizer

from ai_industry_labs.model_lab.tokenizer_inspector import inspect_text


def test_tokenizer_report_counts_tokens() -> None:
    model_id = "Qwen/Qwen2.5-0.5B-Instruct"
    tokenizer = AutoTokenizer.from_pretrained(
        model_id,
        trust_remote_code=False,
    )

    report = inspect_text(
        tokenizer,
        tokenizer_id=model_id,
        text="The customer was charged twice.",
    )

    assert report.token_count > 0
    assert len(report.records) == report.token_count
```

### Generation tests

Use fake tokenizer and model objects for unit tests. Avoid loading a model in every unit test.

Integration tests should cover:

- One successful open-model generation
- Chat-template formatting
- Greedy reproducibility
- Sampling with fixed seed
- Context rejection
- Result persistence

### Security tests

- No `trust_remote_code=True`
- No model hub token in tracked files
- Only synthetic prompts
- Model licence review field present
- Output treated as untrusted text

## Evaluation

This lesson measures behavior. It does not declare a production winner.

### Fixed test set

Use the same case versions across models. Record:

- Case version
- Model and tokenizer
- Revision
- Framework versions
- Hardware
- Generation configuration
- Seed

### Deterministic metrics

- Input tokens
- Output tokens
- Latency
- Required markers
- Prohibited markers
- JSON parse success
- Repetition
- Error rate

### Human review rubric

Score each output:

| Dimension | Scale |
|---|---|
| Task relevance | 1-5 |
| Instruction following | 1-5 |
| Policy consistency | 1-5 |
| Unsupported claims | None, minor, major |
| Appropriate uncertainty | 1-5 |
| Draft usefulness | Reject, major edit, minor edit, accept |

Use at least two reviewers for a subset and record disagreement.

### Model comparison table

Do not fill results until experiments run.

| Model | Type | Task quality | Instruction compliance | Unsupported claims | Median latency | Median input tokens | Median output tokens | Estimated unit cost | Data-policy status |
|---|---|---:|---:|---:|---:|---:|---:|---:|---|
| Open base small | Base | | | | | | | Local compute | |
| Open instruct small | Instruction | | | | | | | Local compute | |
| Hosted candidate | Instruction or reasoning | | | | | | | | |

### Variance report

For sampled runs, report:

- Number of unique outputs
- Marker pass rate
- Human score distribution
- Worst observed failure

Average quality alone can hide dangerous tails.

### Context report

| Evidence condition | Input tokens | Latency | Relevant evidence used | Distractor effect | Unsupported claims |
|---|---:|---:|---|---|---|
| No evidence | | | | | |
| Relevant evidence | | | | | |
| Relevant plus distractors | | | | | |
| Long history | | | | | |

### Cost measurement

For hosted models:

```text
request cost =
input tokens × input price
+ output tokens × output price
+ tool, search, or cache charges
```

Use current dated provider pricing and note discounts or cache pricing. Do not place a stale
price permanently in code.

For self-hosted models:

```text
cost per successful task =
compute
+ storage
+ network
+ operations
+ idle capacity
÷ successful tasks
```

### Selection recommendation

The report must identify:

- Best candidate for the next integration lesson
- Best low-cost fallback candidate
- Cases requiring a different model
- Evidence still missing
- Risks that cannot be resolved by model selection

## Failure modes and debugging

| Symptom | Likely causes | Diagnostic evidence | Corrective action | Prevention |
|---|---|---|---|---|
| Output repeats prompt | Base model continuation or decoding | Base model and greedy run | Use correct instruction model/template; evaluate decoding | Record model type |
| Instruction model performs poorly | Wrong chat template | Inspect formatted tokens | Use tokenizer chat template | Test template |
| Output begins mid-user message | Missing generation prompt | Decoded formatted chat | Add model-appropriate assistant start | Integration test |
| Duplicate special tokens | Template plus tokenizer adds tokens again | Inspect token IDs | Tokenize directly through template or disable extra special tokens | One formatting path |
| Token count differs from estimate | Character or word estimate used | Tokenizer report | Count with exact tokenizer | Count before request |
| Context check passes but generation fails | Check used raw prompt, generation used template | Compare actual input IDs | Validate final formatted representation | Shared preparation function |
| CPU run is extremely slow | Model too large or long output | Hardware and token metrics | Use smaller model, shorter bounded cases, or accelerator | Resource budget |
| Out-of-memory error | Model, precision, context, or batch too large | Device memory log | Reduce model, sequence, batch, or precision | Preflight capacity |
| Sampling remains identical | Seed reset or sampling disabled | Run config | Verify `do_sample` and seed policy | Persist config |
| Greedy output differs | Framework/model revision, device kernels, or prompt differs | Artifact comparison | Pin revisions and environment; inspect nondeterminism | Version all inputs |
| Temperature appears ignored | Greedy decoding used | Generation arguments | Enable sampling | Validate incompatible configs |
| Invalid JSON | Free-form decoding | Parse error | Use structured generation later; retry only under policy | Schema evaluation |
| Model invents policy | Missing evidence or premise acceptance | Evidence comparison | Add RAG, citations, abstention, human review | Unsupported-claim tests |
| Long prompt reduces quality | Distractors or effective-context weakness | Context experiment | Select and compress context | Retrieval evaluation |
| Base and instruction comparison is unfair | Different prompts or formatting | Experiment record | Use model-appropriate but semantically equivalent inputs | Review protocol |
| Hosted result is missing | No credentials or provider failure | Error record | Mark unavailable; do not fabricate | Optional adapter |
| Remote-code warning | Model repository requires custom code | Load log | Reject or perform security review in isolated environment | Approved model list |
| Model update changes output | Floating model revision | Model metadata | Pin revision where possible and rerun evaluation | Change control |
| Marker checks look good but answer is wrong | Weak metric | Human review | Add semantic and domain evaluation | Do not rely on markers |
| Token probability treated as confidence | Concept error | Review report | Calibrate on task outcomes | Confidence policy |

## Security, privacy, and governance

### Model supply chain

Review:

- Repository owner
- Licence
- Model card
- Weight format
- Files downloaded
- Revision
- Custom code requirement
- Known limitations
- Intended use

Use `safetensors` where available. It reduces some risks associated with loading Python pickle
objects, but it does not establish model trustworthiness.

### Remote code

`trust_remote_code=True` can execute repository code. Controls include:

- Approved model allowlist
- Manual code review
- Isolated environment
- Restricted network and filesystem
- Pinned revision
- Artifact scanning

This lesson does not enable it.

### Hosted privacy

Before using a hosted model, review:

- Data retention
- Provider training use
- Regional processing
- Subprocessors
- Logging
- Encryption
- Contract terms
- Deletion

### Output handling

Treat model output as untrusted:

- Escape before rendering
- Validate structured data
- Do not execute generated code
- Do not use output as authorization
- Do not treat generated URLs as safe

### Prompt injection

This lesson does not yet insert external documents, but later RAG systems will. Foundation-model
understanding does not provide a model-only solution to prompt injection.

### Bias and representation

Tokenization and training data can affect languages and user groups differently. Include
multilingual and subgroup cases where the product serves those users.

### Model cards and system cards

Record:

- Model purpose
- Licence
- Known limitations
- Evaluation results
- Allowed data
- Deployment status
- Selected generation defaults

The production system needs a system card beyond the model card because behavior depends on the
complete application.

## Performance and cost

### Parameter memory

A rough weight-only estimate:

```text
weight memory ≈ parameter count × bytes per parameter
```

Examples of bytes per parameter:

- FP32: approximately 4
- FP16 or BF16: approximately 2
- INT8: approximately 1
- Four-bit: approximately 0.5

Actual memory is higher because of:

- Runtime buffers
- Activations
- KV cache
- Quantization metadata
- Framework overhead
- Device copies

### KV cache

During autoregressive generation, implementations cache key and value tensors for earlier
tokens. Cache memory grows with sequence length, batch size, layers, heads or key-value heads,
and precision.

Lesson 35 covers serving and Lesson 36 covers optimization.

### Prefill and decode

Inference has two useful phases:

- **Prefill:** process input tokens
- **Decode:** generate tokens one at a time or through optimized methods

Long inputs increase prefill work. Long outputs increase decode work.

### Measure latency

For local experiments:

```text
load time
first-run warmup
prefill and generation
total request latency
```

Do not compare a cold local model load with an already-warm hosted endpoint as if they are the
same operational setup.

### Throughput

This lesson runs one request at a time. Production throughput depends on:

- Batching
- Concurrency
- Model size
- Sequence lengths
- Hardware
- Serving engine
- Cache use

### Token cost

Tokenization differs by model. Compare exact token counts for the actual support data and
languages.

### Reasoning cost

Reasoning-oriented modes may use more inference tokens or hidden compute. Measure task success
and total cost rather than only visible output length.

## Deployment and operational path

This lesson does not deploy a production model endpoint. It creates a reproducible evaluation
artifact used to choose what Lesson 09 will integrate.

### Artifacts

Store:

- Model catalog
- Cases
- Generation configs
- Result JSONL
- Human-review file
- Selection report
- Environment lockfile

### Model revision

Where supported:

- Pin repository revision
- Record tokenizer revision
- Record file hashes or artifact provenance

### Promotion

```text
Exploratory candidate
→ fixed-case laboratory
→ security and licence review
→ integration candidate
→ full application evaluation
→ pilot
```

### Rollback

Model selection must support returning to:

- Previous model identifier
- Previous tokenizer
- Previous generation configuration
- Previous prompt or chat format

## Observability and operations

### Logs

Record:

- Run ID
- Case ID
- Model and tokenizer
- Revision
- Configuration
- Seed
- Device
- Error category

Do not log:

- Model hub tokens
- Hosted provider keys
- Sensitive customer text

### Metrics

- Load success
- Generation success
- Input and output tokens
- Latency
- Repetition
- Marker results
- JSON validity
- Human scores
- Context overflow
- Memory

### Alerts

For a later production system:

- Model version changed unexpectedly
- Token use increases materially
- Latency exceeds threshold
- Schema compliance drops
- Unsupported claims increase
- Hosted provider region or policy changes

### Change management

Rerun the fixed evaluation when:

- Model changes
- Tokenizer changes
- Provider aliases update
- Generation defaults change
- Framework version changes
- Hardware or serving engine changes

## Practical assignment

### Scenario

Produce the model shortlist for the support response-drafting pilot.

### Requirements

- Compare at least three model entries:
  - One open base model
  - One instruction-tuned model
  - One hosted candidate or a second approved instruction model
- Use at least ten fixed cases.
- Include:
  - Routine classification
  - Evidence-backed drafting
  - Missing evidence
  - Incorrect premise
  - Structured output
  - Long context
  - Multilingual text
  - Code or identifiers
- Compare greedy and sampled decoding.
- Run repeated samples.
- Inspect tokenization.
- Measure context growth.
- Record latency and output tokens.
- Review unsupported claims.
- Document licence and data-policy status.

### Required artifacts

- Model catalog
- Experiment cases
- Generation configs
- Tokenization report
- Raw result JSONL
- Deterministic metrics
- Human-review rubric and scores
- Context-length report
- Cost assumptions
- Security and licence review
- Model-selection report

### Acceptance criteria

- The same fixed cases are used across candidates.
- Appropriate chat templates are used.
- Model and tokenizer identities are recorded.
- No real customer data is submitted.
- Sampling configuration and seeds are recorded.
- No unmeasured result is presented as fact.
- Unsupported claims are explicitly reviewed.
- Selection considers quality, latency, cost, privacy, and operation.
- Recommendation states limitations and follow-up evaluation.

### Stretch goals

- Compare multilingual token efficiency.
- Add a small encoder model for ticket classification.
- Measure local memory use.
- Compare quantized and non-quantized open-model behavior.
- Add a simple HTML or notebook result explorer while keeping scripts authoritative.

## Interview preparation

### Concept questions

**What is a token?**

A strong answer explains that a token is a tokenizer-defined model unit, not necessarily a word,
and that tokenization affects context, cost, latency, and multilingual behavior.

**What is a logit?**

An unnormalized score for a candidate output. Softmax converts logits into a probability
distribution after any temperature or filtering transformations.

**Why do LLMs hallucinate?**

A strong answer explains next-token generation, missing or conflicting knowledge, prompt and
context effects, plausible decoding, post-training incentives, and the role of the complete
system.

**What does temperature change?**

It rescales logits before sampling, changing distribution sharpness. It does not change model
weights, add knowledge, or guarantee correctness.

**Base versus instruction model?**

A base model continues token patterns learned during pretraining. An instruction model is
post-trained to respond to tasks and chat formats more reliably.

**Dense versus mixture of experts?**

A dense layer uses the same main parameters for each token. MoE uses a router to activate a
subset of experts, separating total capacity from active compute and adding routing and
distributed-systems concerns.

### Architecture questions

**Explain self-attention.**

Describe Q, K, V projections, scaled query-key scores, masks, softmax weights, and weighted value
aggregation.

**Why does context length affect latency and cost?**

More input tokens require more prefill processing, memory, and provider billing. Longer context
also increases KV-cache and evidence-selection concerns. Exact scaling depends on architecture
and serving implementation.

**Encoder versus decoder?**

Encoders produce contextual representations for an input. Causal decoders generate tokens
autoregressively. Encoder-decoder systems encode an input then generate conditioned output.

### Debugging questions

**An instruction model produces strange continuations. What do you inspect?**

- Chat template
- Special-token duplication
- Generation prompt
- Model/tokenizer pairing
- Base versus instruction identifier
- Truncation
- Decoding configuration

**Output changes despite temperature zero or greedy decoding. Why?**

Possible differences include model revision, prompt formatting, tokenizer, framework,
hardware-specific nondeterminism, provider alias, or server configuration.

### Product question

**How do you choose a model for the support pilot?**

Start from fixed task and guardrail evaluations. Compare evidence use, instruction compliance,
unsupported claims, latency, cost, context, privacy, versioning, and operational support.
Choose a threshold-satisfying model, not the largest model.

### Tradeoff question

**Hosted or open-weight?**

Discuss time to market, scaling, data controls, infrastructure ownership, customization, licence,
cost, version control, and organizational capability.

## One-page memory sheet

Use this section for review after completing the lesson. Try to recreate it before looking.

### Central model loop

```text
Text or messages
→ model-specific tokenizer
→ token IDs
→ token embeddings + positional information
→ transformer blocks
   ├── attention mixes allowed context
   └── feed-forward layers transform each position
→ next-token logits
→ decoding strategy
→ selected token
→ append and repeat
```

### Product-control loop

```text
Authorized input
→ selected evidence
→ model generation
→ validation
→ human review or approval
→ business action
→ feedback and monitoring
```

The first loop generates language. The second loop makes it usable in a business system.

### Relationships to remember

| Concept | Relationship |
|---|---|
| Tokenizer | Defines the token IDs accepted by the model |
| Embedding | Converts a token ID into a learned vector |
| Position | Preserves sequence order |
| Attention | Combines information from allowed sequence positions |
| Transformer block | Attention plus feed-forward transformation and residual structure |
| Logit | Unnormalized next-token score |
| Softmax | Converts scaled logits into a probability distribution |
| Decoding | Selects the next token |
| Context window | Limits total formatted input and output budget |
| Chat template | Converts roles and messages into model-specific tokens |
| Instruction tuning | Improves task and chat behavior, not current factual knowledge |
| RAG or tools | Supply current private evidence or state |
| Human approval | Retains authority for consequential action |

### Decision table

| Need | First model or system choice |
|---|---|
| Classification or representation | Encoder or classical ML baseline |
| Open-ended drafting | Instruction-tuned decoder |
| Current private facts | Retrieval or tools around the model |
| Stable specialized behavior | Evaluate SFT or adapters later |
| Diverse alternatives | Sampling with measured variance |
| Reproducible baseline | Greedy decoding |
| Consequential action | Deterministic authorization and human approval |
| Lower infrastructure ownership | Hosted model |
| Greater deployment control | Open-weight model |

### Five misconceptions

- **Tokens are words.** Tokens are model-specific units.
- **Lower temperature means more truthful.** It means more concentrated token selection.
- **Attention explains the complete model.** It is one component of a deep network.
- **Instruction tuning adds current private knowledge.** It primarily changes behavior.
- **A larger context or model is always better.** Relevance, cost, latency, and operations matter.

### Essential equations and constraints

```text
softmax probability:
p_i = exp(z_i) / sum_j exp(z_j)

scaled attention:
softmax(QKᵀ / sqrt(d_k) + mask)V

context budget:
instructions + messages + evidence + tools + output reserve ≤ supported context

rough weight memory:
parameters × bytes per parameter
```

### Essential production rule

```text
Never assign authorization, evidence quality, or business correctness to the language model
alone.
```

## Retrieval bank

Answer without looking. Write or speak complete explanations.

### Recall

- Define token, token ID, embedding, hidden state, logit, and context window.
- List the main steps from raw text to one selected next token.
- State the difference between pretraining and SFT.
- State the difference between a base and instruction model.
- State the difference between a dense and mixture-of-experts model.

### Explanation

- Explain why tokenization affects cost and multilingual behavior.
- Explain self-attention using queries, keys, values, masks, and weighted sums.
- Explain why a valid chat message list still needs a model-specific template.
- Explain why token probability is not answer correctness.
- Explain why a longer context can reduce quality.

### Prediction

- Predict what happens to a probability distribution when temperature decreases.
- Predict how duplicating special tokens could affect instruction following.
- Predict which phase becomes more expensive when input context grows.
- Predict how sampled outputs differ when the random seed changes.
- Predict why a base model may continue a dialogue instead of following an instruction.

### Diagnosis

- A model repeats the prompt. What do you inspect?
- The context-limit check passes but the provider rejects the request. What mismatch may exist?
- Greedy output changed after a deployment. Which versions or environment details do you inspect?
- JSON parses but contains an unauthorized action. Why did structured syntax not solve the
  problem?
- A model gives the same unsupported answer every time. Which controls address correctness?

### Comparison

- Compare encoder, decoder, and encoder-decoder architectures.
- Compare greedy, top-k, and top-p generation.
- Compare hosted and open-weight deployment.
- Compare instruction tuning with supplying evidence through RAG.
- Compare public benchmark performance with task-specific production evaluation.

### Transfer

- Design a model experiment for multilingual refund tickets.
- Choose a model approach for ticket classification and justify why an LLM may not be required.
- Define the context budget for an evidence-backed support draft.
- Propose a fallback when the hosted model is unavailable.
- Explain how the Lesson 07 human-approval boundary remains unchanged after model selection.

## Spaced-review plan

Do not reread the full lesson during these reviews unless retrieval reveals a gap.

### One day later

From memory:

- Draw the central model loop.
- Explain logits, softmax, and temperature.
- Answer five retrieval-bank questions.
- Run one tokenizer comparison.

Target: reconstruct the flow with no more than two missing links.

### Three days later

- Draw scaled dot-product attention and explain every term.
- Compare base and instruction models.
- Diagnose one chat-template failure.
- Complete one new context-budget calculation.
- Explain why hallucination is a system-level behavior.

Target: explain concepts without using glossary wording.

### One week later

- Recreate the decision table from memory.
- Run one greedy and three sampled generations.
- Explain observed variance.
- Select a model for a new task and defend the choice.
- Answer ten mixed retrieval-bank questions.

Target: transfer concepts to a task not used in the worked example.

### Three to four weeks later

- Give a ten-minute whiteboard explanation of an LLM request from text to generated output.
- Diagnose three failure scenarios.
- Review the model-selection report and identify one assumption that should be retested.
- Explain how the model fits inside the complete controlled support workflow.

Target: connect model mechanics, product controls, and production selection without notes.

## Self-assessment

Score each item:

- `0`: cannot explain
- `1`: recognize but cannot reconstruct
- `2`: explain with prompts
- `3`: explain and apply independently

| Capability | Score |
|---|---:|
| Draw the model loop | |
| Explain tokenization | |
| Explain logits and decoding | |
| Explain attention | |
| Compare model families | |
| Apply a chat template | |
| Calculate a context budget | |
| Diagnose unsupported output | |
| Design a fixed model comparison | |
| Defend a production model choice | |

Do not move to production API integration until the essential capabilities score at least `2`
and the model-comparison capability scores `3`.

## Production-readiness checklist

- [ ] The use case and pilot from Lesson 07 remain unchanged.
- [ ] Model candidates have documented purposes.
- [ ] Model and tokenizer licences are reviewed.
- [ ] Model and tokenizer identifiers are versioned.
- [ ] Remote model code is disabled or formally reviewed.
- [ ] Synthetic or approved data is used.
- [ ] Token counts use the exact tokenizer.
- [ ] Chat templates are model-appropriate.
- [ ] Special tokens are not duplicated.
- [ ] Base and instruction models are compared fairly.
- [ ] Greedy decoding is used as a deterministic baseline.
- [ ] Sampling settings and seeds are recorded.
- [ ] Maximum output is bounded.
- [ ] Context budget includes formatted input and output reserve.
- [ ] Context overflow and truncation are explicit.
- [ ] Unsupported claims are reviewed.
- [ ] Deterministic metrics are not treated as complete quality metrics.
- [ ] Human evaluation uses a documented rubric.
- [ ] Latency distinguishes load, warmup, and generation.
- [ ] Cost uses measured token counts.
- [ ] Self-hosted cost includes infrastructure and operations.
- [ ] Hosted data policy and region are reviewed.
- [ ] Model output is treated as untrusted.
- [ ] Experiment artifacts are reproducible.
- [ ] No fabricated benchmark or price result appears.
- [ ] Model-selection limitations are documented.
- [ ] A fallback candidate is identified.
- [ ] Model-change reevaluation triggers are defined.
- [ ] Production integration is deferred to Lesson 09.

## Lesson summary

You built the mental and practical foundation for working with modern language models.

You learned:

- Text becomes model-specific tokens.
- Token IDs become learned vector representations.
- Transformer blocks combine context through attention and feed-forward computation.
- A causal model repeatedly predicts and selects the next token.
- Logits and decoding settings determine token selection behavior.
- Base and instruction-tuned models have different intended use.
- Chat roles are encoded through model-specific token templates.
- Longer context changes memory, latency, cost, and quality risk.
- Fluent output is not proof of factual correctness.
- Model selection must include task quality, evidence use, latency, cost, privacy, licence,
  versioning, and operational ownership.

The model-behavior laboratory produces a shortlist for the support-drafting pilot, not a final
production approval.

The next lesson, **Model API Integration**, will turn the selected hosted candidate into a
provider-independent production integration with authentication, streaming, structured output,
timeouts, bounded retries, rate-limit handling, fallback, tracing, and cost attribution.

## Official references

- Hugging Face Transformers — Text generation:
  <https://huggingface.co/docs/transformers/main/en/llm_tutorial>
- Hugging Face Transformers — Generation strategies:
  <https://huggingface.co/docs/transformers/main/en/generation_strategies>
- Hugging Face Transformers — Tokenization algorithms:
  <https://huggingface.co/docs/transformers/main/en/tokenizer_summary>
- Hugging Face Transformers — Chat templates:
  <https://huggingface.co/docs/transformers/main/en/chat_templating>
- Hugging Face Transformers — Causal language modelling:
  <https://huggingface.co/docs/transformers/main/en/tasks/language_modeling>
- Hugging Face Transformers — Perplexity:
  <https://huggingface.co/docs/transformers/main/en/perplexity>
- Hugging Face Transformers — Auto classes:
  <https://huggingface.co/docs/transformers/main/en/model_doc/auto>
- Qwen2.5 0.5B base model card:
  <https://huggingface.co/Qwen/Qwen2.5-0.5B>
- Qwen2.5 0.5B instruction model card:
  <https://huggingface.co/Qwen/Qwen2.5-0.5B-Instruct>
- PyTorch scaled dot-product attention:
  <https://docs.pytorch.org/docs/stable/generated/torch.nn.functional.scaled_dot_product_attention.html>
- Attention Is All You Need:
  <https://arxiv.org/abs/1706.03762>
