# 数字生命 AstrBot 插件仓库

本仓库包含数字生命系统的单插件融合版，以及过渡期的两个独立插件。

| 插件 | 形态 | 版本 | 状态 |
|---|---|---|---|
| `astrbot_plugin_digital_life` | **单插件融合版**：一个 Star、一套生命周期、一个控制台 | 0.6.0-alpha.5 | M00–M03 落地骨架，未完成迁移/恢复 |
| `astrbot_plugin_digital_memory_store` | 数字记忆基座（独立） | 1.0.19 | 过渡期兼容 |
| `astrbot_plugin_memory_shadow` | 原生输入 / 引擎 / 输出 / 控制台（独立） | 0.5.1 | 过渡期兼容 |

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

安装：从 Releases 下载 `astrbot_plugin_digital_life-0.6.0-alpha.5.zip`，在 AstrBot
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

## 旧双插件（过渡期）

Releases 中仍保留：

- `astrbot_plugin_digital_memory_store-1.0.19.zip`
- `astrbot_plugin_memory_shadow-0.5.1.zip`

两者可独立安装；配置见各自 README。新部署建议直接使用单插件版。

## 从源码运行

仓库中的插件目录是薄源码，构建时把 `shared/` 复制进插件私有包空间。源码调试可设置：

```powershell
$env:DIGITAL_LIFE_DEV = '<repo>/shared'
```

发布 zip 不需要这个变量。

## 构建

```powershell
python tools/build_unified_plugin.py   # 单插件版
python tools/build_plugins.py          # 过渡期两个独立插件
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
