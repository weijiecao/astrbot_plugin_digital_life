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


本仓库只保留最新版单插件 `astrbot_plugin_digital_life`。旧 store / shadow 插件源码和
旧构建脚本已统一移入 `archive/`，仅作历史查阅，不再参与构建和发布。

| 插件 | 形态 | 版本 | 状态 |
|---|---|---|---|
| `astrbot_plugin_digital_life` | **单插件融合版**：一个 Star、一套生命周期、一个控制台 | 0.7.0-dev.2 | 开发版；迁移/实时追加/恢复/兼容适配已接入，真实宿主验收未完成 |

单插件版的发布 zip 自包含 `memory_engine`、`memory_output`、
`v1_5_consolidator`、`astrbot_memory_input`、`dlm_console`，安装时不需要额外的
`dev` 目录。

## 单插件版（主推）

`astrbot_plugin_digital_life` 把采集、后台判别、检索与输出收敛到一个 Star：

- 模式 `OFF` / `COLLECT` / `ASSIST`；
- 只有 `allowed_sender_ids` 明确列出的私聊用户会被采集，留空不采集任何用户；
- 只有 `ASSIST` 会把预算内证据作为临时内容块注入当前请求；
- 统一控制台：`/astrbot_plugin_digital_life/console/*`；
- 沿用 R03–R05 的退出、取消隔离与失败重试保证。

安装：从 Releases 下载 `astrbot_plugin_digital_life-0.7.0-dev.2.zip`，在 AstrBot
WebUI 插件页上传并启用。需要 `tiktoken`：

```powershell
python -m pip install tiktoken==0.14.0
```

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

### 数据与迁移边界

默认使用：

```text
<AstrBot>/data/plugin_data/astrbot_plugin_digital_life/
```

如果新目录不存在而旧 `astrbot_plugin_memory_shadow/` 存在，会继续使用旧目录并在
状态中标记 `legacy_data_dir`，避免静默生成空库。若检测到旧 shadow 插件模块仍活动，
或同一数据目录已被另一个统一实例占用，插件进入 `blocked-legacy` / `blocked-locked`
只读诊断状态，不启动 pump、不采集、不注入。旧基座
`manual_test_memory.sqlite3` 的正式迁移、实时追加契约、备份恢复切换、偏好排序/
短指代等兼容能力尚未完成，因此本版是 **alpha 骨架**，不能称为 `v0.6.0-rc.1`。

## 历史归档

旧版本已统一放入：

```text
archive/
  plugins/astrbot_plugin_digital_memory_store/   旧基座插件源码
  plugins/astrbot_plugin_memory_shadow/          旧 shadow 插件源码
  tools/build_plugins.py                         旧双插件构建脚本
```

历史 ZIP 仍可从 GitHub Releases 获取，但不再作为当前发布入口。新部署只使用
`astrbot_plugin_digital_life`。

## 从源码运行

仓库中的插件目录是薄源码，构建时把 `shared/` 复制进插件私有包空间。源码调试可设置：

```powershell
$env:DIGITAL_LIFE_DEV = '<repo>/shared'
```

发布 zip 不需要这个变量。

## 构建

```powershell
python tools/build_unified_plugin.py
```

输出在 `dist/`，包含 zip、`.sha256` 与 `RELEASE*.json`。清单文件数从最终 ZIP
统计，不使用源码目录预过滤计数。

## 验证

```powershell
python -m unittest discover -s tests -t . -v
```

覆盖统一配置/模式、单包根目录、自包含导入、OFF 生命周期与控制台状态路由。

## 边界

- 仍是隔离验收版本，不代表真实 AstrBot/NapCatQQ、真实模型质量或长期运行验收；
- 控制台由 AstrBot WebUI 鉴权保护；只读模式可禁用写操作；
- 记忆注入默认关闭，开启后请自行承担请求变化与模型效果风险；
- 单插件 alpha 未完成旧基座迁移、恢复切换和旧插件全部兼容能力，能力表见插件
  README。

## License

MIT，见 `LICENSE`。
