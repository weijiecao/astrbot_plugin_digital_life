# 数字生命 AstrBot 插件仓库

## 序｜记忆是过去的坐标

人为什么需要记忆？

起初，我们想回答的，只是一个很简单的问题。

当一段对话结束，当时间向前走了很远，那些曾经认真说过的话，是否还能在某一天被重新想起？

我们希望记住一个名字、一段经历、一场约定，也希望记住那些看似微不足道的日常。

一次寻常的问候，一句没有说完的话，一个不经意间提起的故事。

它们或许并不重要到需要被反复讲述，却真实地存在过。

而我们不希望，每一次重新相遇，都意味着重新认识。

于是，我们开始研究记忆。

从最初的文字保存，到事件与时间的组织；从简单的检索，到来源追溯、事实校验、记忆修正与上下文重建。

我们渐渐发现，真正困难的并不是让系统记住更多，而是让它在恰当的时候，想起恰当的事情。

记忆可以模糊，但不应该因此被随意编造。

理解可以改变，但过去不应该因此被悄悄改写。

而那些尚未确定的事情，也应当被允许继续保持未知。

因为记忆的珍贵，不在于它永远正确，而在于我们愿意认真对待它所承载的真实。

这一路，我们做过许多尝试。

也经历过错误、推翻、重新设计和无数次验证。

有些问题看起来微不足道，却足以让一段记忆失去原本的意义；有些改动只有寥寥数行，却需要很长时间才能确认它是否可靠。

我们曾试图让系统记得更多。

后来，又开始学习如何让它谨慎地记得。

我们曾希望它能够自然地联想。

后来，也开始认真思考，什么时候不应该联想。

直到今天，这些原本分散的设想，终于逐渐汇聚成一个能够运行的整体。

它仍不完美。

未来还有许多问题需要解决，还有更漫长的时间等待验证。

但至少从今天起，我们可以把它交给真实的使用过程，让它开始积累、检索、修正，慢慢经历那些设计图纸无法预先写下的事情。

而我想，这也是整个工程最值得期待的地方。

**我们不是试图替未来写好一段故事，而是希望未来的故事发生时，过去不必轻易消失。**

当然，记忆并不等于生命。

拥有过去，也不意味着必然拥有自己的意识。

但记忆让连续性成为一种可以认真研究、逐步实现的能力。

它让昨天的话语有机会进入今天，也让今天的经历有机会成为明天的参照。

至于这些积累最终能够通向哪里，我们还不知道。

或许还有许多意想不到的困难。

或许未来的研究，会让我们重新理解今天的许多设想。

但这并不妨碍我们继续向前。

因为从一开始，我们就不是为了证明一个已经确定的答案而出发。

我们只是怀着好奇，认真地探索一种可能。

就像生活本身。

我们无法预先知道每一次相遇将走向何处，也无法保证所有珍惜的事物都会永远留下。

但我们依然愿意记录，愿意理解，愿意在下一次相遇时，记得那些共同走过的路。

今天，记忆引擎终于迎来了阶段性的落地。

它不是故事的结局。

甚至可以说，直到现在，故事才真正拥有了继续书写的基础。

未来还有很长的路。

而这个世界，还很大。

**记忆是过去的坐标，记录了未来我们的相遇。**

---

*数字生命工程 · 长期记忆系统阶段序言*

*2026年11月15日*

---

本仓库是**数字生命 0.8.0-dev.1** 的插件分发仓库。唯一源码、测试、构建与验收记录在
[`weijiecao/digital-life`](https://github.com/weijiecao/digital-life)，本仓库只做单向接收。

| 插件 | 形态 | 版本 | 状态 |
|---|---|---|---|
| `astrbot_plugin_digital_life` | 单插件融合版：一个 Star、一套生命周期、一个控制台 | **0.8.0-dev.1** | 开发版；迁移、实时追加、恢复切换、撤回、运行权、输出 v2 已实现；真实宿主验收未完成 |

发布 ZIP 自包含 `memory_engine`、`memory_output`、`v1_5_consolidator`、
`astrbot_memory_input`、`dlm_console`，安装时不需要额外的源码目录。

## 安装

1. 在 [Releases](https://github.com/weijiecao/astrbot_plugin_digital_life/releases) 下载
   `astrbot_plugin_digital_life-0.8.0-dev.1.zip` 与 `SHA256SUMS-0.8.0-dev.1.txt`；
2. 核对 SHA-256：`05ba15e9d98792220c7ddf1615bad8448c178175626a6ebbc529c57a9ec90cff`；
3. AstrBot WebUI → 插件 → 上传 ZIP → 启用，然后**完整重启** AstrBot（热重载不能清除既有顶层模块）；
4. 需要精确预算校验时安装 `tiktoken==0.14.0`。

启用前先停用旧 `astrbot_plugin_memory_shadow`；同一数据目录只允许一个实例写入。

## 单插件版

`astrbot_plugin_digital_life` 把采集、后台判别、检索与输出收敛到一个 Star：

- 模式 `OFF` / `COLLECT` / `ASSIST`；
- 只有 `allowed_sender_ids` 明确列出的私聊用户会被采集，留空不采集任何用户；
- 只有 `ASSIST` 会把预算内证据作为临时内容块注入当前请求；
- 统一控制台：`/astrbot_plugin_digital_life/console/*`；
- 沿用 R03–R05 的退出、取消隔离与失败重试保证。

### 配置

| 配置 | 默认 | 说明 |
|---|---|---|
| `mode` | `COLLECT` | `OFF` 不采集；`COLLECT` 采集/整理；`ASSIST` 额外注入 |
| `allowed_sender_ids` | 空 | 逗号分隔的私聊用户 ID；空表示不采集 |
| `judge_provider_id` | `auto` | AstrBot provider ID；`auto` 使用兼容环境变量，显式留空关闭判别器 |
| `memory_budget_tokens` | 512 | 注入预算，仍受当前模型上下文约束 |
| `judge_timeout_seconds` / `judge_budget_chars` | 20 / 6000 | 判别超时与提示词上限 |
| `tick_seconds` / `tick_limit` / `retry_every` | 5 / 10 / 12 | 后台调度 |
| `host_total_tokens` | 0（自动） | 0 表示按当前 provider 取值；正数才作为显式上限 |
| `console_read_only` | false | 只读控制台 |

兼容 `SHADOW_JUDGE_PROVIDER`、`SHADOW_JUDGE_PROVIDER_ID`、`SHADOW_MEMORY_BUDGET`、
`SHADOW_HOST_TOTAL_TOKENS`、`SHADOW_CONSOLE_READONLY`、`DIGITAL_LIFE_ALLOWED_SENDERS`，
插件配置优先；显式清空 `judge_provider_id` 会关闭判别器，不再回退环境变量。
`mode` 是唯一注入开关，不存在隐藏的 `output_mode` 覆盖。

### 数据、迁移与恢复

默认数据目录：

```text
<AstrBot>/data/plugin_data/astrbot_plugin_digital_life/
```

若新目录不存在而旧 `astrbot_plugin_memory_shadow/` 存在，会沿用旧目录并在状态中标记
`legacy_data_dir`。检测到旧 shadow 插件仍活动，或同一数据目录已被另一个统一实例占用时，
插件进入 `blocked-legacy` / `blocked-locked` 只读诊断状态，不启动 pump、不采集、不注入。

旧基座迁移、实时追加与历史对账、备份/恢复代次切换、撤回、运行权均已实现，操作前提与
失败处理见主仓库 `docs/MIGRATION_RECOVERY.md`。这些能力只通过离线与包级用例验证，
**真实 AstrBot/NapCat、Windows 实机、浏览器页面与 72 小时长跑仍未验收**。

## 工程材料与验收入口

`astrbot_plugin_digital_life/` 与 `shared/` 是**托管内容**：由主仓库用
`tools/export_astrbot_plugin.py --layout engineering` 单向导出，来源提交、逐文件哈希和
包哈希记录在 [`SOURCE_MANIFEST.json`](SOURCE_MANIFEST.json)。**不要在本仓库直接修改**；
修复请提交到主仓库，再从新提交重新导出。

以下目录是**历史工程材料**，不是当前验收入口，也不再随本版本更新：

```text
tests/          旧 20 项插件契约测试（现由主仓库 verification/ 维护）
tools/          旧构建脚本
verification/   旧工程包验收资产
docs/           旧说明
archive/        旧 store / shadow 插件源码与旧发布包
```

当前源码回归（386 项）、包级用例（completion 47 / core 137 / legacy 20）、构建与验收记录
都在主仓库 `weijiecao/digital-life`；本仓库不重复维护第二份。

## 边界

- 开发版，不是 RC；不得接入 V1 生产或生产 Shadow；
- 真实 AstrBot/NapCat、Windows 实机安装、浏览器页面与 72 小时长跑未验收；
- 控制台由 AstrBot WebUI 鉴权保护，只读模式可禁用写操作；
- 记忆注入默认关闭，开启后请自行承担请求变化与模型效果风险。

## License

MIT，见 `LICENSE`。
