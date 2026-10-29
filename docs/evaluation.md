# Evaluation: isolate the decision, measure the system

[Home](../README.md) · [中文](evaluation_zh.md)

The evaluation unit is the task or episode. Repeated decisions within one task are useful diagnostic events but are not independent success trials. When the same scenes generate several task variants, keep that dependence visible in analysis.

## Match the comparison to the question

| Research question | Hold fixed | Change | Report |
| --- | --- | --- | --- |
| Is Jev a better selector? | State, candidates, executor, tasks | Rule / structured LLM / Jev | Decision errors and full-task outcome |
| Is the state representation better? | Selector, raw observations, tasks | Representation only | Lost facts, decision quality, end-to-end impact |
| Does gating save useful compute? | Generator, action permissions, evaluation | Fixed / rule / model gate | Success, calls, gate overhead, wall time |
| Is prediction useful? | Candidate set, selector, execution horizon | Predictor or prediction schedule | Outcome fidelity, success, risk, total compute |

If perception or control changes too, label the comparison as a system comparison. A system comparison is still useful; it answers a different question.

## Minimum reporting fields

| Group | Fields |
| --- | --- |
| Identity | Source commit, SDK, requested model, returned model, provider, run date |
| Task | Task definition, initial-state ID, seed, perturbation, success and stop criteria |
| Inputs | Observation time/version, state, candidate definitions, exposed ground truth |
| Decision | Selected option, available probabilities, threshold statistic, fallback, latency |
| Execution | Executed action, rejection, observed consequence, retries |
| Outcome | Success/failure, reason, episode duration, all calls, token usage and price basis |

Preserve failed and interrupted attempts. Distinguish a clean run from a continuation, a cached plan from online planning, and a controller action from an actual model decision. Report retries in both time and cost.

## Metrics by direction

**Foundations:** accuracy or task score, calibration error with the binning specified, Brier score where appropriate, selective risk versus coverage, latency distribution, and total usage.

**Agents:** final completion, invalid/stale targets, retries, critical-fact deletion, support errors, observation age, full-task time, and total cost including auxiliary models.

**Embodied AI:** full success, recovery after perturbation, object progress, contact loss, collisions, rejected actions, stale execution, wall time, and all perception/prediction/decision costs.

Prefer a success–cost or risk–compute curve to a single favorable threshold. Include strong rules and an inexpensive structured model, not only an expensive reasoning baseline.

## Image decisions and localization

Record original and submitted images, dimensions, orientation, crop coordinates, encoding/compression, reference placement, and activation headers. Hold option count and instructions fixed when possible. A comparison changing both provider endpoint and image encoding cannot attribute differences solely to model version.

Evaluate missing correct candidates, false premises, illegible details, outside-image facts, and temporal inference separately. Adding an abstention option changes the candidate definition; report coverage and error. For Box, report IoU, false boxes on absent targets, and false rejection/acceptance from Noul gating. Cluster repeated calls and multiple questions by image rather than treating answer counts as independent samples.

For systems such as Visual Jev, `ms/question` in a shared-image batch is batch duration divided by question count. Report batch latency, independent-request latency, throughput, cold/warm caches, and peak memory separately. Separate training accuracy gains from computation-sharing gains. See [multimodal cases](multimodal.md) and [community models](community-models.md).

## Timing and cost

For a sequential step, a useful accounting decomposition is:

```text
perception + state construction + prediction + decision + execution + verification
```

Asynchronous systems overlap stages. Measure wall-clock duration directly and report the critical path; do not sum overlapping intervals as elapsed time. Distinguish simulated time, API waiting, and video playback. If physics pauses during an API call, that run does not measure responses to a continuously moving world.

Record actual usage and the dated/provider-specific price basis. Report mock, cache, and free-credit behavior separately. A lower count of expensive requests does not by itself prove a faster or cheaper complete task.

## Splits and uncertainty

Choose prompts, thresholds, and budgets on development data. Freeze them for held-out tasks, layouts, websites, or perturbations. Use paired initial conditions when possible and report counts alongside percentages. Bootstrap at the independent unit, clustering by scene when needed. A five-layout development result should remain a five-layout development result.

## Simulator and world-model distinctions

Known-state branch simulation can isolate selection and scheduling. A learned world model must additionally be checked for action sensitivity, failure prediction, reward alignment, and error accumulation. Report those experiments separately. Ground truth used by the evaluator should not silently enter the selector's state.

[Research roadmap](roadmap.md) · [Source notes](source-notes.md)
