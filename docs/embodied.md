# Embodied intelligence: decision, control, and physical feedback

[Home](../README.md) · [中文](embodied_zh.md)

Robot decisions must survive contact, motion, delay, and partial observation. A gripper moving toward a target does not prove the object moved; a command completing does not prove the task progressed. Jev's role should be located relative to perception, prediction, control, and feedback.

## Decision interfaces and representative systems

Embodied applications span waypoint selection, skill evaluation, local motion, and action reuse. NavJev, Nav Arena, Stacker, jev-libero, EmbodiedJev, RoboJEV, and RoboICL illustrate how these decision interfaces connect perception, prediction, and control.

### Seven core cases

| Case | Decision interface | Physical or algorithmic support | Evidence boundary |
| --- | --- | --- | --- |
| [NavJev](https://arxiv.org/abs/2609.34969) | Waypoint or stop from action-centered descriptions | Visual frontend and navigation candidates | Reported 100-task simulation comparison; limited real trials |
| [Nav Arena](https://research.dimensional.org/system-one-navigation/) | Direction, turn, stop, completion, target | Structured geometry and a navigation stack | Different complete systems; separate evaluation sets |
| [Code Owns the Simulation](https://arxiv.org/abs/2610.01834) | Language-conditioned skill choice | Programmed skills and known physics simulation | Skill granularity and control assistance change together |
| [jev-libero](https://github.com/Dimweaker/jev-libero) | Intent → family → atomic input | 27 atomic inputs, branch simulation, geometry | Passing examples, not a full benchmark score |
| [EmbodiedJev](https://github.com/FBddcz/embodied-jev) | Local direction and gripper choice | Visual planner, RGB-D processing, servo control | Small development runs, including failures |
| [RoboJEV](https://github.com/lykycy123/RoboJEV) | Intent → XYZ and gripper | MuJoCo state, kinematics, action checks | Rules outperform Jev in the reported aggregate |
| [RoboICL substudy](https://arxiv.org/html/2609.34261v1#S4.SS5) | Reuse action suffix or regenerate | A separate action generator and execution trace | Two development tasks, five layouts each |

## Read the measurements at their original scope

These are **author-reported results from the cited sources**, not new results produced by this repository.

| Case | Selected result | What must remain attached to the claim |
| --- | --- | --- |
| NavJev | 27/100 successes; GPT-4o 14/100 and Qwen 25/100 | Same provided interface; LLM baselines without reasoning |
| Nav Arena | Short-range subset: Jev 32/45, $0.055 per run | Systems use different software; separate from the 327-task main evaluation |
| Stacker study | Skill selection 9/20; direct torque selection 0/20; new instructions 22/40 | Different action abstraction/control support; original-task rule baseline 8/20 |
| RoboJEV | Jev 43/50; rules 48/50 | Five simulation tasks; not a real-robot result |
| RoboICL: Align Blocks | Generator calls 181 → 121; success 3/5 → 2/5 | Fewer calls accompany fewer completed tasks |
| RoboICL: General Pickup | Generator calls 116 → 60; success 4/5 → 5/5 | Small development sample; include gate cost and action count |

EmbodiedJev's [reviewed LIBERO development comparison](https://github.com/FBddcz/embodied-jev/blob/main/docs/results/libero-vision/RESULTS.md) reports a faster successful drawer run with the hybrid policy, but an unsuccessful microwave run under its budget. Demonstrations using cached plans or other execution protocols should be evaluated separately from that comparison.

## Connection to the three loops of closed-loop VLA

| Loop | Where Jev could enter | Evidence in this collection |
| --- | --- | --- |
| Execution | Decide whether to continue, re-observe, or regenerate | RoboICL action reuse; local-control cases |
| Prediction | Select among candidate outcomes, or decide whether to request prediction | Known-simulator examples; learned-model gating remains a proposal |
| Learning | Use accumulated outcomes to update a policy, critic, model, or interface | An open direction; inference-time Jev calls alone are not parameter updates |

See [Awesome Closed-Loop VLA](https://github.com/ZJU-OmniAI/Awesome-Closed-Loop-VLA) for execution, prediction, and learning, and [Awesome World Model](https://github.com/ZJU-OmniAI/Awesome-World-Model) for world-model concepts and resources.

There are two distinct prediction interfaces. **After prediction**, Jev can select among simulated candidates, but cannot recover the compute already spent generating them. **Before prediction**, a gate may save calls if there is a still-valid plan to execute. Test these two questions separately.

A learned latent predictor such as [V-JEPA 2-AC](https://arxiv.org/abs/2506.09985) introduces an additional interface: predicted features must become task-relevant information that the selector can consume. This paper does not establish an existing Jev integration.

## Three proposed experiments

### 1. Execution correction

Use a fixed pick-and-place task, generator, controller, and perception stack. Apply reproducible slippage, target motion, or occlusion. Compare fixed execution lengths, rule monitoring, a fast structured LLM, and Jev choosing continue / observe / replan.

Cross **ordinary versus observation-verified feedback** with **rules versus Jev**. This separates improvements in feedback from improvements in the selector. Measure full success, recovery, stale-action duration, unnecessary replanning, wall time, and total cost on held-out perturbations.

### 2. Active observation

Use similar objects with task-relevant differences and repeatable occlusion. Fix the detector and candidate viewpoints. Compare a fixed viewing sequence, visibility/uncertainty heuristics, a structured LLM, and Jev selecting the next observation.

Measure correct target selection and final task success under the same observation budget, including extra motion and time. Additional views cannot recover an attribute the frontend never estimates.

### 3. Selective prediction

Freeze candidate actions and the post-prediction ranking method. Compare never predict, always predict, geometric triggering, and Jev triggering. Start with a known simulator to isolate scheduling, then separately test a learned predictor.

Report success/risk together with total compute and wall time. The prediction horizon must cover the executed action horizon. Simulator scheduling gains do not establish learned world-model reliability.

## Useful failure distinctions

- **State failure:** relevant attributes are omitted or observations are stale.
- **Candidate failure:** none of the supplied actions can solve the situation.
- **Decision failure:** a worse available option is selected.
- **Execution failure:** a valid intent cannot be realized under dynamics or constraints.
- **Evaluation failure:** the success check or predicted reward is wrong.

Log these separately before attributing the entire outcome to the model. Keep simulator truth used for scoring separate from the information exposed to the decision maker.

[Evaluation guide](evaluation.md) · [Roadmap](roadmap.md)
