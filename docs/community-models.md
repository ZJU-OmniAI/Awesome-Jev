# Community implementations: where decision scores come from

[Home](../README.md) · [Foundations](foundations.md) · [中文](community-models_zh.md)

OpenJev, Visual Jev, NanoJev, and CLM implement related candidate-decision interfaces with different models, training objectives, and probability readouts. This guide compares their public implementations; they do not establish TypeSafe Jev’s internal architecture.

## Two implementation routes

| Project | Source of option scores | Additional training | Scope |
| --- | --- | --- | --- |
| [OpenJev](https://github.com/razorback16/openjev) | Existing LM head; candidate-token logprobs at answer slots | Default path uses existing weights | Reviewed fixed-commit DiffusionGemma path; multiple slots do not guarantee one computation |
| [Visual Jev](https://github.com/guanxuyu-sv/Visual-Jev) | Qwen3-VL LM head; candidate logits at each `Answer:` position | Answer-SFT LoRA in the language tower; vision tower frozen | Released quickstart supports Choice with 2–16 options, not the official four-type API |
| [NanoJev](https://github.com/TianyuCodings/NanoJev) | Qwen3-0.6B with a shared decision head | Released model jointly trains backbone and head | Training and demonstrations cover four games, not a universal replacement |
| [CLM](https://github.com/Contrastive-LM/CLM) | Separate state/action projections, dot products, softmax | Frozen Qwen3-8B; train projection heads and logit scale | Reviewed encoder takes text; vision/multimodality remains on the roadmap |

Training, computation sharing, and image support are separate dimensions. Normalized option scores do not establish calibration. Matching interface names do not guarantee identical fields or confidence definitions.

## OpenJev: reading existing candidate probabilities

At the [reviewed engine.py commit](https://github.com/razorback16/openjev/blob/b4339c640f5331ef75098637d1be2c787715ee88/openjev/engine.py), prompts define single-token labels such as A/B/C. The diffusion answer template reserves positions for those labels; the engine reads logprobs and normalizes them over legal candidates. The default deployment uses DiffusionGemma-26B-A4B-it without additional task training.

A teaching example assigns vocabulary probabilities A=0.02, B=0.16, C=0.02, yielding 10% / 80% / 10% after candidate normalization. That 80% is relative to the supplied set, not an established real-world correctness rate. These are hypothetical numbers illustrating normalization, not measurements.

The diffusion path can read multiple answer positions in one block, but groups large question sets and may average additional reads when entropy is high. Bidirectional reads also do not establish statistical independence between answer slots. Autoregressive models can read next-token candidate probabilities and batch separate questions too. This implementation's entropy-based confidence must be evaluated separately from TypeSafe's statistic.

## Visual Jev: separate training from execution gains

The [paper](https://arxiv.org/abs/2609.25845) and [code](https://github.com/guanxuyu-sv/Visual-Jev) use Qwen3-VL-4B-Instruct. Image and public-text prefixes are cached, independent question suffixes run as a batch, and the existing LM head produces candidate distributions. The original model already supports probability readout; LoRA improves decisions on the evaluated tasks.

The [released model card](https://huggingface.co/guanxuyu/visual-jev-4b-answer-sft) records a frozen vision tower, language-layer LoRA with `r=16, α=32, dropout=0.05`, and 33,030,144 trainable parameters. Supervision comes from GQA and SNLI-VE training splits: 3,000 steps at batch size 8 gives roughly 24,000 cumulative sample slots, not 24,000 unique records. TextVQA and TallyQA were not used in this post-training. The author’s training notes report about 40 minutes for 4B on one RTX 5090.

| Author-reported result | Value | Interpretation |
| --- | --- | --- |
| Equal-weight four-task accuracy | 70.6% → 76.1% | Gains mainly on trained GQA/SNLI-VE families; not an official Jev score |
| 32 questions/image, independent serial → shared-prefix batch | 50.7 → 5.7 ms/question, about 8.9× throughput | 5.7 is about 182 ms for the batch divided by 32, not single-request latency |
| 32 questions/image, batch without prefix sharing | 19.3 ms/question | Separates batching from prefix reuse |
| One question, independent → shared path | 48.1 → 82.9 ms | Sharing adds overhead at this workload |
| Peak memory with 32 questions | 8.40 → 10.10 GiB | Higher throughput uses more memory |

These are warm RTX 5090 measurements starting from an in-memory decoded image. They include preprocessing, transfer, and execution, but exclude disk, network, decoding, and serving queues. They cannot be divided directly into official API network latency. With fixed weights, sharing does not change training state; better trained accuracy does not itself prove better calibration.

## NanoJev: a game decision head

The `unified-games-v1` release selects checkpoint step 400 from the `hard_lr1e5` run. Maze, Snake, ViZDoom Basic, and Predict Position provide 10,898 stored training questions; 10,893 pass target-validity filtering. Training uses complete-question cross entropy, backbone learning rate `1e-5`, and head learning rate `1e-4`.

The selected checkpoint does not mean the entire research effort used only 400 steps. Separate selected gameplay replays from complete evaluation. See the [project's dataset and model description](https://github.com/TianyuCodings/NanoJev#dataset-scale-and-model).

## CLM: contrastive alignment of states and candidates

A frozen Qwen3-8B encodes state and action text through their respective projection heads. Bidirectional InfoNCE pulls correct pairs together and separates mismatches. Inference scores embeddings and normalizes with softmax. States and candidates can be cached independently; new candidates do not require a new fixed-class output layer.

The author's [data recipe](https://github.com/Contrastive-LM/CLM#data-recipe) reports about 60 million Q&A pairs, 30 million synthetic hard negatives, and one million agent trajectories, with 40% Q&A replay and 60% trajectories in the final stage. Pairs, negatives, and multistep trajectories are different units and cannot be summed as 91 million unique training examples. Game screenshots illustrate the task, not direct image input to the published text encoder.

The author's [zero-shot evaluation](https://github.com/Contrastive-LM/CLM#zero-shot-evaluation):

| Task | Latency CLM / Jev (ms) | Success CLM / Jev |
| --- | --- | --- |
| T-Rex | 16.5 / 149.8 | 5/5 / 5/5 |
| BFCL v4 tool calling | 76.8 / 125.5 | 95.2% / 99.2% |
| WikiRacing | 79.8 / 225 | 26/30 / 30/30 |
| Super Mario | 33.5 / 132.6 | 5/5 / 5/5 |

CLM has lower reported latency in these settings, with lower tool-calling and WikiRacing success. The figure does not supply complete hardware, version, and uncertainty information; five-trial game results cannot establish general performance.

Separate DeepSWE / Terminal-Bench verifier experiments select among solutions generated by other models on only 38/30 held-out tasks. They are not standalone CLM coding results or full benchmark scores. README examples and playground screenshots are different records too, and should not be merged into a single response.

[Official multimodal interface](multimodal.md) · [Evaluation](evaluation.md)
