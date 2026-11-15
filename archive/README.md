# 历史归档

本目录保存数字生命旧插件源码与旧构建脚本，仅作历史查阅，不参与当前构建、测试和发布。

```text
archive/
  plugins/
    astrbot_plugin_digital_memory_store/   数字记忆基座旧插件（1.0.19）
    astrbot_plugin_memory_shadow/          旧 shadow 插件（0.5.1 源码线）
  tools/
    build_plugins.py                       旧双插件构建脚本（路径基于旧仓库根）
```

当前版本只保留仓库根目录的 `astrbot_plugin_digital_life/`，由
`tools/build_unified_plugin.py` 构建。历史 ZIP 仍保留在 GitHub Releases，但不再作为
新部署入口。

旧 shadow 数据可由新插件自动接续；不要同时启用旧 shadow 与新统一插件。
