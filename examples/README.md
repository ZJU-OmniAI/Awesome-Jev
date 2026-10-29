# An illustrative decision request / 示意判断请求

[English home](../README.md) · [中文首页](../README_zh.md)

The [JSON example](decision_request.json) illustrates a shared state with Choice, Score, and Noul questions. The facts and observation ID are invented for explanation; there is no recorded model response or claimed experiment. The example does not make an API call.

The block remains on the table while the gripper rises. A useful decision must distinguish robot motion from verified object progress. The application would validate a selected action against the newest observation before execution. The three questions are independent; the Choice answer does not consume the Score or Noul answer from this batch.

`jev-latest` is convenient for illustration. Actual experiments should pin and record the requested and returned model versions, SDK version, provider, full question definitions, and observation timing. Check the [current quick start](https://docs.typesafe.ai/introduction/quickstart) for authentication and request syntax.

这个 JSON 说明如何在同一状态下提出 Choice、Score、Noul 问题。事实与观察编号均为教学示例，没有模型返回值，也不代表实测。机械臂抬起而物体未跟随，用来说明机器人运动与物体进展的区别。

执行前应根据最新观察校验动作；同批三题独立求值，Choice 不读取本批 Score 或 Noul 的答案。真实实验需固定并记录模型请求名、实际返回版本、SDK、服务渠道、完整问题定义与观测时序。

## Multimodal request / 多模态请求

The [multimodal JSON](multimodal_request.json) illustrates Jev 1.14 image input with Choice, Score, Noul, and Box in the same request. It is a multipart request body: attach your PNG/JPEG as the part named `scene-photo`, and send the JSON as the first part named `request` with content type `application/json`. Enable `TypeSafe-Danger-Zone-Images: true` and use the authentication described by the [official Images guide](https://docs.typesafe.ai/go/images). The repository does not send this request or bundle a photograph.

The UUID-style asset reference appears once in state; questions refer to `photo`. A returned Box is not proof of target presence. The application must evaluate `mug_visible` and decide whether to use the box after the response arrives. The thresholds and downstream robot behavior are intentionally unspecified: no task calibration or controller is supplied.

[多模态 JSON](multimodal_request.json)展示同图四类问题。它是 multipart 请求的 JSON 部分：第一部分命名为 `request`，类型为 `application/json`；图片文件部分命名为 `scene-photo`，并加上图像开关请求头。图像格式、尺寸和认证以[官方文档](https://docs.typesafe.ai/go/images)为准。该文件是示例，不会发送请求，也没有附图或虚构响应。

应用在收到响应后结合 `mug_visible` 判断是否采用 Box；同批问题不互相读取答案。阈值和机器人执行方式需要按实际任务验证。

## Demonstration records / 演示记录

[Demonstration records](../data/demo-records.json) contain transcribed question and response examples. They illustrate response fields and candidate design, and are separate from the illustrative request files above. See [data notes](../data/README.md) for their scope.

[演示记录](../data/demo-records.json)保留问题与响应的转录，用于说明接口字段和候选设计，与上面的示意请求分别记录。使用范围见[数据说明](../data/README.md)。
