# Model foundations: from an interface to a reliable decision

[Home](../README.md) · [中文](foundations_zh.md)

Jev exposes typed judgments through a hosted API. Applications supply material and questions; answers include selections, scores, proposition probabilities, or target locations in images. This guide covers interface semantics, confidence, evaluation, and the relationship to community implementations.

TypeSafe's System One name borrows the idea of fast thinking; it is not a public architecture specification. The 2026-09-15 launch describes a dedicated architecture, parallel sampling, and RLCD, but does not release a complete training recipe or official model weights.

## State and independent questions

State may be text, an object, or an array. Include facts that can change the answer: task, current observation, available candidates, recent outcomes, and observation time. Separate those facts from the question instructions. All questions in one request see the same state and are evaluated independently ([State](https://docs.typesafe.ai/concepts/state)).

Batch independent judgments to avoid repeated round trips. If selecting an object changes the meaning of a subsequent action question, resolve the object first or define joint object–action candidates. Do not assume one answer in a batch becomes another question's input.

State can also reference images through `assets`; images may appear in `instructions` and `criteria`. Official documentation checked on 2026-10-27 states that **both Jev 1.13 and 1.14 accept images; Box requires 1.14**. Older cases' textual or structured observations describe their implementation, not the version's modality limit. See the [multimodal guide](multimodal.md) for activation and input limits.

## Four question types

| Primitive | Semantics | Good fit | Design risk |
| --- | --- | --- | --- |
| Choice | Selection and probabilities over defined options | Tool, route, target, action | The correct option may be missing |
| Score | Distribution over ordered levels; score is the expected level index | Progress, relevance, urgency | Levels may mix incompatible dimensions |
| Noul | Probability that a binary proposition is true | Retain evidence, condition met | A threshold may not transfer |
| Box (1.14, experimental) | One normalized bounding box and confidence | Locate an object or region in an image | Returns a box even for absent targets; needs a presence check |

For Score with zero-based levels, the documented expected score is `Σ i × pᵢ`. The distance between ordinal labels is a modeling choice: a score of 1.5 does not create an objectively measurable physical quantity. For Noul, the application defines any abstention band; there is no native third “unknown” answer.

See [Choice](https://docs.typesafe.ai/primitives/choice), [Score](https://docs.typesafe.ai/primitives/score), [Noul](https://docs.typesafe.ai/primitives/noul), and [Box](https://docs.typesafe.ai/go/box).

## Customer-message example

A customer-message example asks a department Choice, frustration Score, and urgency Noul about an English message reporting a Stripe connection failure for three days and lost sales. The demonstration records a 2026-10-27 response from `jev-1.14.0`: technical support probability `0.81`, Choice confidence `0.72`; frustration Score `1.0`, confidence `1.0`; urgency Noul `0.99`.

These transcribed single-call records illustrate the response structure; they are not an accuracy benchmark. Complete question definitions and transcribed responses appear in the [JSON records](../data/demo-records.json).

## Confidence is a distribution statistic

The documented Choice confidence for `n > 1` options is:

```text
confidence = (p_max - 1/n) / (1 - 1/n)
```

For three options and `p_max = 0.85`, it is `0.775`. The maximum probability, the top-two margin, and the API confidence are different statistics. Record which one a routing threshold uses.

Score confidence also considers distance from the most likely level. With modal level `m` and `n` levels, the documented formula is:

```text
D = (1/n) × Σ |i - (n-1)/2|
Score confidence = max(0, 1 - Σ pᵢ × |i-m| / D)
```

Noul returns no separate confidence field. Applications may derive `|2p-1|` as suggested in the documentation; this is a computed statistic, not another model answer. Validate Box confidence for localization rather than applying the Choice formula. Consult the [official definitions](https://docs.typesafe.ai/confidence) before sharing thresholds across types.

A concentrated distribution does not establish correctness. Evaluate calibration and selective prediction: as a system answers fewer, higher-confidence cases, what happens to error, coverage, fallback cost, and overall completion? Choose thresholds on validation data and freeze them before test evaluation.

## What is publicly known

The [launch article](https://typesafe.ai/blog/introducing-system-one-models-and-jev) describes a dedicated architecture, parallel sampling, and Reinforcement Learning for Calibrated Decisions (RLCD). These are vendor descriptions. They do not supply a complete independently reproducible architecture, training recipe, or open checkpoint. API behavior and application-level performance can be studied separately from those undisclosed details.

Type-constrained output prevents certain malformed answers; it does not guarantee the chosen label is factually or operationally correct. Modern generative LLMs also support structured outputs, so meaningful baselines should use comparable answer constraints.

## Two kinds of performance evidence

| Source | What is measured | How to interpret it |
| --- | --- | --- |
| TypeSafe launch workflow evaluation | Agreement with reference-model probabilities and workflow cost | Vendor-designed workflows; agreement is not universal ground-truth accuracy |
| [37-dataset evaluation](https://arxiv.org/abs/2609.37647) | Classification/scoring quality, calibration, selective prediction, API costs | Independent preprint; specific Jev version, fixed prompts, and specified baselines |

The independent paper reports Jev ahead of Qwen3.8-27B on 27 of 37 datasets, behind on nine, and tied on one. Eleven of the favorable comparisons have non-overlapping 95% bootstrap intervals. These counts describe that evaluation, not a guarantee on new tasks. The baseline uses constrained scoring without chain-of-thought.

The launch article reports 70–500 ms responses and September 2026 input pricing of $0.042 per million tokens. The independent study reports a mean client latency of 0.36 seconds under 32-way concurrency. Different environments, aggregation statistics, and workloads prevent a universal speedup calculation. Historical prices are not a current billing quote.

## From a judgment to an application

Further reading:

- [Images and Box](multimodal.md): official multimodal inputs, missing-candidate and insufficient-evidence examples, and a 48-image community COCO evaluation.
- [Community implementations](community-models.md): probability readout, training, and computation reuse in OpenJev, Visual Jev, NanoJev, and CLM, distinguished from the official API.

1. Define the target behavior and observable success criterion.
2. Construct state and candidates from information available at decision time.
3. Compare rules, a structured LLM, and Jev on the same inputs.
4. Validate any threshold and fallback policy independently.
5. Measure the complete task after executing decisions.

[Illustrative request](../examples/decision_request.json) · [Evaluation protocol](evaluation.md)
