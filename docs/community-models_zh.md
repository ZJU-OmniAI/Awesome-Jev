# 社区实现：Jev 风格的判断从哪里来

[首页](../README_zh.md) · [模型基础](foundations_zh.md) · [English](community-models.md)

OpenJev、Visual Jev、NanoJev 和 CLM 实现了相关的候选判断接口，但使用不同的模型、训练目标与概率读出方式。本节比较这些公开实现；它们的架构不等同于 TypeSafe 官方 Jev 的内部架构。

## 两类实现路线

| 项目 | 选项分数来自哪里 | 新增训练 | 适用范围 |
| --- | --- | --- | --- |
| [OpenJev](https://github.com/razorback16/openjev) | 原 LM head，在答案槽读取候选 token 的 logprob | 默认路径直接使用现成权重 | 这里审阅固定提交的 DiffusionGemma 路径；多位置读取不等于严格一次计算 |
| [Visual Jev](https://github.com/guanxuyu-sv/Visual-Jev) | Qwen3-VL 原 LM head，在各题 `Answer:` 位置读取候选 logits | 语言部分 answer-SFT LoRA，视觉编码器冻结 | 发布 quickstart 支持 Choice，2–16 个选项；不等同官方四类 API |
| [NanoJev](https://github.com/TianyuCodings/NanoJev) | Qwen3-0.6B 加共享决策头 | 当前发布版共同训练底座与头 | 四款游戏的专门训练与演示，不能外推为通用替代品 |
| [CLM](https://github.com/Contrastive-LM/CLM) | 状态与候选分别投影，点积打分后 softmax | 冻结 Qwen3-8B，训练两个投影头与 logit scale | 审阅版本提供文本编码；视觉/多模态仍列于路线图 |

是否新增训练、是否共享计算、是否支持图像，是三个独立维度。归一化候选分数本身不证明校准，接口名称相同也不意味着输出字段或 confidence 定义完全一致。

## OpenJev：读取现有候选概率

依据 [engine.py 固定提交](https://github.com/razorback16/openjev/blob/b4339c640f5331ef75098637d1be2c787715ee88/openjev/engine.py)，程序用 prompt 指定 A/B/C 等单 token 标签的含义，在扩散答案模板的预留位置读取 logprob，再在合法候选内归一化。默认部署使用 DiffusionGemma-26B-A4B-it，无需增加任务训练。

教学算例：若全词表概率中 A=0.02、B=0.16、C=0.02，则候选内分布为 10% / 80% / 10%。80% 是给定候选内的相对分数，不能直接写成真实正确率。这些数值是用于解释归一化的假设，不是实测。

扩散路径可在同一输出块读取多个答案位置；题目过多时分组，高熵时可追加读取再平均。双向读取也不证明不同答案槽在统计上完全独立。自回归模型同样可以读取下一 token 的候选概率并批处理问题。该实现使用熵定义 confidence，应与 TypeSafe 的统计量分开验证。

## Visual Jev：训练与推理优化分别看

[论文](https://arxiv.org/abs/2609.25845)与[代码](https://github.com/guanxuyu-sv/Visual-Jev)采用 Qwen3-VL-4B-Instruct：图片与公共文本前缀计算后缓存，各题后缀独立批处理，沿用原 LM head 输出候选分布。原模型已经能读取候选概率；LoRA 的作用是改善所测任务上的判断。

[发布模型卡](https://huggingface.co/guanxuyu/visual-jev-4b-answer-sft)记录：冻结视觉模块，语言线性层 LoRA `r=16, α=32, dropout=0.05`，训练参数 33,030,144；GQA 与 SNLI-VE 训练集提供监督，3,000 步、每批 8 条，约 24,000 个累计样本槽位，不是 24,000 条去重样本。TextVQA 与 TallyQA 未参与这次后训练。作者训练说明报告单张 RTX 5090 上 4B 约 40 分钟。

| 作者报告 | 结果 | 解读 |
| --- | --- | --- |
| 四任务等权平均准确率 | 70.6% → 76.1% | 增益主要来自参与训练的 GQA、SNLI-VE；不是官方 Jev 分数 |
| 同图 32 题，串行独立 → 共享前缀批处理 | 50.7 → 5.7 ms/题，约 8.9 倍吞吐 | 5.7 是整批约 182 ms 除以 32，不能当作单次请求延迟 |
| 同图 32 题，仅批处理、不共享前缀 | 19.3 ms/题 | 将批处理收益与前缀复用收益分开 |
| 只有 1 题时，独立 → 共享路径 | 48.1 → 82.9 ms | 共享路径反而增加开销 |
| 32 题峰值显存 | 8.40 → 10.10 GiB | 提速伴随更高显存 |

以上为 RTX 5090 的热启动测量，计时从内存中的解码图像开始，包含预处理、传输与执行，不包含磁盘、网络、解码或服务排队。不能与官方 API 网络延迟直接相除。固定模型权重时，执行共享不改变训练状态；训练准确率提高也不自动证明校准改善。

## NanoJev：游戏决策头

当前 `unified-games-v1` 对应 `hard_lr1e5` 训练的第 400 步 checkpoint。Maze、Snake、ViZDoom Basic、Predict Position 共存储 10,898 道训练题，其中 10,893 通过目标有效性过滤。训练使用完整问题的交叉熵，底座学习率 `1e-5`、头学习率 `1e-4`。

这是选定发布 checkpoint 的说明，不代表整个研究只训练了 400 步。游戏回放展示应与完整测试集评估分开。训练规模与版本来源：[项目说明](https://github.com/TianyuCodings/NanoJev#dataset-scale-and-model)。

## CLM：对比学习状态与候选

冻结的 Qwen3-8B 分别编码状态和动作文本，再经过各自投影头。双向 InfoNCE 拉近正确配对、拉远错误配对；推理时比较向量并用 softmax 得到候选分布。状态和候选可以独立缓存，新候选无需变成固定类别输出层。

作者的[数据配方](https://github.com/Contrastive-LM/CLM#data-recipe)包含约 6,000 万问答对、3,000 万合成困难负例和 100 万智能体轨迹；末阶段按 40% 问答回放、60% 轨迹混合。问答对、负例和多步轨迹的单位不同，不能相加成“9,100 万独立训练样本”。游戏截图表示任务，不证明当前文本编码器可直接输入图像。

作者的 [zero-shot 评测](https://github.com/Contrastive-LM/CLM#zero-shot-evaluation)：

| 任务 | 延迟 CLM / Jev（ms） | 成功 CLM / Jev |
| --- | --- | --- |
| T-Rex | 16.5 / 149.8 | 5/5 / 5/5 |
| BFCL v4 工具调用 | 76.8 / 125.5 | 95.2% / 99.2% |
| WikiRacing | 79.8 / 225 | 26/30 / 30/30 |
| Super Mario | 33.5 / 132.6 | 5/5 / 5/5 |

作者报告这些设置下 CLM 延迟更低，但工具调用与 WikiRacing 成功率也更低。图未给出全套硬件、版本和不确定性信息，5/5 的游戏结果尤其不能推广为普遍性能结论。

另有 DeepSWE / Terminal-Bench 的 verifier 实验：CLM 从其他模型生成的多个候选方案中择优，且仅用 38/30 项保留任务，不能写成 CLM 独立完成编码或完整基准成绩。README 示例与 playground 截图也是不同记录，不能拼成同一次调用。

[多模态官方接口](multimodal_zh.md) · [评测协议](evaluation_zh.md)
