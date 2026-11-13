# 数字生命 AstrBot 组合插件

本仓库把数字生命系统的两个 AstrBot 插件放在一起维护：

| 插件 | 作用 | 版本 |
|---|---|---|
| `astrbot_plugin_digital_memory_store` | 数字记忆基座：原话入库、有界召回、未确认上下文、WebUI panel | 1.0.19 |
| `astrbot_plugin_memory_shadow` | 原生输入、影子记忆引擎、可选临时注入、内嵌控制台 | 0.5.1 |

两个插件独立安装、共享同一个 AstrBot 实例；`memory_shadow` 的发布 zip 自包含
`memory_engine`、`memory_output`、`v1_5_consolidator`、`astrbot_memory_input`
和 `dlm_console`，安装时不需要额外的 `dev` 目录。

## 安装

从本仓库 Releases 下载：

- `astrbot_plugin_digital_memory_store-1.0.19.zip`
- `astrbot_plugin_memory_shadow-0.5.1.zip`
- `SHA256SUMS.txt`

在 AstrBot WebUI 的插件页上传 zip，或解压到 `<AstrBot>/data/plugins/`。两个插件
都需要在插件页启用。

`memory_shadow` 需要 `tiktoken`（用于精确 token 预算）；如果 AstrBot 环境没有，
先安装：

```powershell
python -m pip install tiktoken==0.14.0
```

## 配置 memory_shadow

```powershell
$env:ASTRBOT_ROOT = 'C:\path\to\AstrBot\instance'
$env:SHADOW_JUDGE_PROVIDER = 'astrbot'   # none / mock / astrbot / openai
$env:SHADOW_JUDGE_PROVIDER_ID = '<id>'   # astrbot 模式必填

# 可选：开启临时记忆注入（默认 off）
$env:SHADOW_OUTPUT_MODE = 'inject'
$env:SHADOW_MEMORY_BUDGET = '512'

# 可选：控制台只读
$env:SHADOW_CONSOLE_READONLY = '1'
```

没有配置判别器时插件只入队、不建档；注入默认关闭。开启后只修改
`ProviderRequest.extra_user_content_parts`，记忆块是临时内容，不写入持久化历史，
`prompt` / `system_prompt` / `contexts` 与回复不变。

打开控制台：WebUI → 插件 → **Memory Engine Shadow** → 视图 **数字记忆控制台**。

## 从源码运行

仓库中的 `astrbot_plugin_memory_shadow` 是薄插件；源码调试时把依赖目录指过去：

```powershell
$env:DIGITAL_LIFE_DEV = '<repo>/shared'
```

发布 zip 不需要这个变量。

## 构建

```powershell
python tools/build_plugins.py
```

输出在 `dist/`：

- 两个插件 zip；
- `SHA256SUMS.txt`；
- `RELEASE.json`（版本、文件数、SHA-256）。

## 目录

```text
astrbot_plugin_digital_memory_store/   基座插件（自包含）
astrbot_plugin_memory_shadow/          影子插件源码（薄）
shared/                                影子插件打包时内置的引擎/输入/输出/控制台
tools/build_plugins.py                 构建脚本
```

## 边界

- 仍是隔离验收版本，不代表已完成真实 AstrBot/NapCatQQ 长期运行、真实模型质量或
  生产发布；
- 控制台由 AstrBot WebUI 鉴权保护；`SHADOW_CONSOLE_READONLY=1` 可禁用写操作；
- 记忆注入默认关闭，开启后请自行承担请求变化与模型效果风险。

## License

MIT，见 `LICENSE`。
