# 数字生命（统一 AstrBot 插件）

单插件版本 `0.6.0-alpha.2`。一个 Star、一套生命周期、一个控制台，复用现有
原生输入、记忆引擎、记忆基座和输出模块。本版是 M00–M03 的可运行落地骨架，
**不是 v0.6.0-rc.1，也不宣称旧插件全部能力已迁移**。

## 模式

| 模式 | 行为 |
|---|---|
| `OFF` | 不采集、不观察；控制台仍可查看/维护已有数据 |
| `COLLECT` | 采集私聊历史、后台判别与整理；不注入模型请求 |
| `ASSIST` | 在 COLLECT 基础上，把预算内证据作为临时内容块注入当前请求 |

只有 `allowed_sender_ids` 中明确列出的私聊用户会被采集；留空表示不采集任何用户，
不会默认接管所有私聊。`ASSIST` 默认关闭，必须在配置中显式选择。

## 配置

在 AstrBot 插件配置页填写：

- `mode`：`OFF` / `COLLECT` / `ASSIST`
- `allowed_sender_ids`：逗号分隔的用户 ID
- `judge_provider_id`：AstrBot provider ID；留空只入队、不建档
- `memory_budget_tokens`：注入预算，默认 512
- `judge_timeout_seconds` / `judge_budget_chars`
- `tick_seconds` / `tick_limit` / `retry_every`
- `console_read_only`：只读控制台

兼容环境变量：`SHADOW_JUDGE_PROVIDER`、`SHADOW_JUDGE_PROVIDER_ID`、
`SHADOW_MEMORY_BUDGET`、`SHADOW_HOST_TOTAL_TOKENS`、`SHADOW_CONSOLE_READONLY`、
`DIGITAL_LIFE_ALLOWED_SENDERS`。插件配置优先。

示例：

```powershell
$env:SHADOW_JUDGE_PROVIDER = 'astrbot'
$env:SHADOW_JUDGE_PROVIDER_ID = '<provider id>'
$env:DIGITAL_LIFE_ALLOWED_SENDERS = '123456789'
# 注入只由 mode=ASSIST 开启，不存在单独的 SHADOW_OUTPUT_MODE 开关
```

`tiktoken` 用于精确 token 预算；未安装时输出为空而不是估算注入。

## 控制台

WebUI → 插件 → **数字生命（统一插件）** → **数字生命控制台**。
路由为 `/astrbot_plugin_digital_life/console/*`，复用原控制台页面、查询与备份/
恢复副本能力。`SHADOW_CONSOLE_READONLY=1` 或配置 `console_read_only=true` 时禁用写操作。

## 数据

默认数据目录：

```text
<AstrBot>/data/plugin_data/astrbot_plugin_digital_life/
  shadow.sqlite3
  native_input_journal.sqlite3
  shadow_events.jsonl
  backups/
  restores/
```

如果新目录不存在、而旧 `astrbot_plugin_memory_shadow/` 存在，本版继续使用旧目录，
避免静默生成空库；状态面板会标记 `legacy_data_dir=true`。这是数据接续，不是旧基座
`manual_test_memory.sqlite3` 的迁移。

若检测到旧 shadow 插件模块仍活动，或数据目录已被另一个统一实例锁定，插件只进入
只读诊断状态（`blocked-legacy` / `blocked-locked`），不启动 pump、不采集、不注入。
同一目录的排他锁在进程内和跨进程都生效；显式 `judge_provider_id=""` 会关闭判别器，
不会回退到旧环境变量。

## 本版边界

已完成（M00–M03 的主体）：

- 单插件包、单 Star、单生命周期、单控制台、单注入入口；
- 模式与用户范围配置、兼容环境变量、状态 API；
- 自包含 `memory_engine` / `memory_output` / `v1_5_consolidator` /
  `astrbot_memory_input` / `dlm_console`；
- 复用已验证的输入、判别、输出、R03–R05 退出保证。

尚未完成，不能称为 RC：

- 旧基座 `manual_test_memory.sqlite3` 到新引擎的正式迁移清单/冲突处理；
- 实时追加契约（当前仍读取宿主完整历史快照）；
- 备份/恢复的停写、切换和启动恢复状态机；
- 旧插件偏好排序、短指代、主动聊天等兼容能力；
- 真实 AstrBot/NapCatQQ、真实模型质量与 72h 运行验收。

控制台里对旧基座库的删除只走既有 `dlm_console` 管理路径，不会自动同步新引擎事件。

## 构建

```powershell
python tools/build_unified_plugin.py
```

产物：

```text
dist/astrbot_plugin_digital_life-0.6.0-alpha.2.zip
dist/astrbot_plugin_digital_life-0.6.0-alpha.2.sha256
dist/RELEASE_UNIFIED.json
```

安装：AstrBot WebUI → 插件 → 上传 zip。发布包自包含，不需要 `DIGITAL_LIFE_DEV`。
