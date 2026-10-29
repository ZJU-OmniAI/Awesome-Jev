# Contributing / 贡献指南

Contributions should help readers understand a specific decision interface or assess a concrete claim. Negative results and corrections are welcome.

## Add a resource

1. Choose one primary track: `foundations`, `agents`, or `embodied`.
2. Add an entry to [data/resources.json](data/resources.json) with a unique ID, an original English/Chinese summary, a scope note in both languages, and a primary source URL.
3. Use the [evidence labels](data/README.md). Mark a mock, proposal, development run, or author-reported result accordingly.
4. Record the source version or snapshot when it matters. Do not replace a historical experiment's result with a later demo under different conditions.
5. Run the commands below and include the generated README changes in the same PR.

```bash
python3 scripts/update_catalog.py
python3 scripts/check_repository.py
```

Optional network audit:

```bash
python3 scripts/check_repository.py --online
```

Edit topic guides directly. Edit generated README tables through the JSON catalog. Prefer primary papers, official documentation, code, and raw experimental records over unsourced reposts. Do not copy third-party diagrams or large excerpts without permission under their licenses.

## Report a result

State what Jev receives and decides; identify the perception, candidate generator, planner, simulator, and executor. Include the model version, protocol, task/seed count, baselines, success definition, failures, total time/cost, and a public artifact or record. Distinguish your own reproduction from an author's result and separate mocks from online calls.

This repository does not require positive outcomes. A well-specified failure can be more useful than a selected successful video.

## 中文说明

新增资源时选择模型基础、Agent 应用或具身智能之一，在 `data/resources.json` 中提供双语原创摘要、来源和适用范围，再运行脚本同步首页。专题正文可直接编辑。

请明确资源属于官方资料、论文、项目、演示、设想或背景工作；模拟响应、开发集结果和作者报告应分别标注。结果类贡献需说明 Jev 输入与判断职责、其他模块分工、版本、协议、样本量、基线、成功标准、失败、总耗时与费用，并链接公开证据。

贡献的原创内容按本仓库 Apache-2.0 许可证发布；链接的第三方材料仍遵循原许可。
