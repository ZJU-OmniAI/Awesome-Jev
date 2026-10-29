# Research roadmap

[Home](../README.md) · [中文](roadmap_zh.md)

The following research questions and experimental designs remain to be tested. Each study defines a specific question and controls that can reveal either positive or negative results.

## Track 1 — Model foundations

**Calibration under interface changes.** Hold labeled states fixed, then vary candidate count, label wording, class balance, and question type. Compare top probability, top-two margin, and API confidence using thresholds selected on separate validation data. Report risk–coverage curves and calibration rather than choosing one convenient threshold after testing.

**State sufficiency.** Remove or perturb task-relevant fields while keeping the decision maker fixed. Compare with rules and a structured LLM. Measure which missing facts cause errors and whether abstention or re-observation can identify those cases. This distinguishes state engineering from model improvement.

**Multimodal evidence and localization.** Hold original scenes and candidates fixed while comparing text state, images, crops, and combined inputs. Test missing correct options, false premises, illegible details, and outside-image facts separately, controlling candidate count. Evaluate Box with independent reference boxes and report both false rejection and false acceptance from presence gating, plus complete task outcomes.

**Training versus computation reuse.** On one visual backbone, separate original/LoRA weights from independent serial/batched/shared-prefix execution. Freeze weights to evaluate execution changes and fix execution to evaluate training. Report independent-request latency, batch throughput, and peak memory separately.

## Track 2 — Agent applications

**Evidence filtering.** Freeze a retrieved document set and separately evaluate topical relevance and claim support. Measure critical-evidence recall, false support, and final answer quality under equal budgets. The retriever and answer generator stay fixed.

**Context retention.** Compare recency truncation, summarization, and Jev retention on the same tool histories. Preserve call/result validity. Evaluate subsequent task completion, repeated tool work, and loss of paths, requirements, or unresolved errors, not only token reduction.

**Computation routing.** Compare always invoking the strong model, fixed rules, a small structured selector, and Jev. Freeze tools and fallback semantics. Record routing errors and all auxiliary costs on held-out tasks.

## Track 3 — Embodied intelligence

| Study | Fixed components | Intervention | Main outcomes |
| --- | --- | --- | --- |
| Execution correction | Perception, generator, controller, initial states | Reuse/observe/replan policy | Success, recovery, stale execution, total time/cost |
| Active observation | Detector, viewpoint candidates, motion planner | Next-view selector | Target accuracy, final success, observation and motion budget |
| Selective prediction | Action candidates, predictor, post-prediction ranking | Prediction trigger | Matched success/risk versus total compute |

The [embodied guide](embodied.md) expands the protocols. An initial simulator study can check experimental mechanics. Learned-predictor and real-robot claims require their own evaluations.

## A practical sequence

1. Publish the interface and evaluation protocol before collecting a comparison.
2. Run a small development set to expose logging, perception, and executor failures.
3. Freeze the configuration and evaluate held-out cases with paired initial conditions.
4. Publish all attempts, including failures and interrupted runs, with their protocol labels.
5. Add a finding to the resource index only at the scope supported by its evidence.

The first promising outcome need not be a model win: identifying the missing observation or a stronger rule baseline can also improve the system.
