# References and evaluation sources / 参考资料与评测来源

The survey links directly to documentation, papers, code, and author-reported experiments. Quantitative results retain their original task scope, model versions, and measurement boundaries. Demonstration transcriptions illustrate interface behavior and candidate design; they are not independent benchmarks.

综述直接引用官方文档、论文、开源实现和作者实验。定量结果保留任务范围、模型版本与计时条件；演示转录用于说明接口和候选设计，不作为独立基准。

## Primary sources / 主要来源

| Claim group | Primary evidence |
| --- | --- |
| Interface and vendor timings/prices | [TypeSafe launch](https://typesafe.ai/blog/introducing-system-one-models-and-jev), [State](https://docs.typesafe.ai/concepts/state), [Confidence](https://docs.typesafe.ai/confidence) |
| Independent 37-dataset evaluation | [Paper](https://arxiv.org/abs/2609.37647) |
| Browser optimization timings | [Performance note](https://github.com/browser-use/jev-ultrafast/blob/main/docs/performance.md) |
| Desktop step accounting | [Step description](https://github.com/awlevin/typesafe-computer-use/blob/main/docs/how-a-step-works.md) |
| NavJev simulation comparison | [Paper](https://arxiv.org/abs/2609.34969) |
| Nav Arena main and short-range evaluations | [Author report](https://research.dimensional.org/system-one-navigation/) |
| Stacker skill versus torque results | [Paper §6](https://arxiv.org/html/2610.01834v1#S6) |
| RoboJEV aggregate results | [Project evaluation](https://github.com/lykycy123/RoboJEV/blob/main/docs/evaluation.md) |
| EmbodiedJev LIBERO development comparison | [Results and scope](https://github.com/FBddcz/embodied-jev/blob/main/docs/results/libero-vision/RESULTS.md) |
| RoboICL action reuse | [Paper §4.5](https://arxiv.org/html/2609.34261v1#S4.SS5) |
| Images and localization | [Images](https://docs.typesafe.ai/go/images), [Box](https://docs.typesafe.ai/go/box) |
| Visual Jev training and shared-prefix inference | [Paper](https://arxiv.org/abs/2609.25845), [code and model links](https://github.com/guanxuyu-sv/Visual-Jev) |
| Community COCO evaluation | [Author report](https://rohitghumare.com/blog/typesafe-870m-can-jev-see/) |
| Community candidate-decision models | [OpenJev](https://github.com/razorback16/openjev), [NanoJev](https://github.com/TianyuCodings/NanoJev), [CLM](https://github.com/Contrastive-LM/CLM) |

## Interpreting the results / 结果解读

Model latency, amortized batch cost, simulation time, and full-task wall-clock time measure different quantities. Compare selectors under shared states, candidates, and executors when isolating model effects. For complete-system comparisons, report perception, execution, recovery, and task success alongside model calls. See [evaluation](evaluation.md) / [评测方法](evaluation_zh.md).

`reviewed_on` and `source_snapshot` in the [resource catalog](../data/resources.json) identify documentation dates and known code versions. They are not experimental replication claims. Public repositories may change after the cited version.

## Related surveys / 相关综述

- [Awesome Closed-Loop VLA](https://github.com/ZJU-OmniAI/Awesome-Closed-Loop-VLA): execution, prediction, and learning loops in robot agents.
- [Awesome World Model](https://github.com/ZJU-OmniAI/Awesome-World-Model): world-model concepts, methods, and evaluation resources.

The overview diagrams are original. Linked third-party works retain their authorship and licensing.
