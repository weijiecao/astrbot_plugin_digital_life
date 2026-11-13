# 统一插件落地状态（v0.6.0-alpha.1）

日期：2026-11-13。基线：`8fce7a5eafb838bc082deb631fb242bc5adba6b9`。
本文件记录单插件融合的实际进度，不替代验收报告。

| 里程碑 | 状态 | 说明 |
|---|---|---|
| M00 冻结基线 | 完成 | 以 v0.5.1 的 shared 模块与退出修复为输入 |
| M01 包形态 | 完成 | 唯一 ZIP 顶层 `astrbot_plugin_digital_life/`；一个 Star |
| M02 配置 | 完成（首版） | `mode`、`allowed_sender_ids`、provider、预算、调度、只读；`_conf_schema.json` |
| M03 服务/生命周期 | 部分 | 复用 shadow 主链路；单 pump、单注入、R03–R05 退出保证；尚未拆成独立 application service |
| M04 实时追加 | 未完成 | 仍读取宿主完整历史快照；实时追加契约待做 |
| M05 输出 | 完成 | 单 `on_llm_request`；仅 ASSIST 注入；预算复验沿用 |
| M06 迁移 | 未完成 | 自动接续 shadow 数据目录；旧基座 `manual_test_memory.sqlite3` 正式迁移未做 |
| M07 恢复切换 | 未完成 | 控制台仍备份/恢复到副本，未实现在线停写切换状态机 |
| M08 统一 UI | 部分 | 单控制台路由与状态 API；页面仍复用 dlm_console 查询组件 |
| M09 目标环境验收 | 未完成 | 未启动真实 AstrBot/NapCatQQ，未做重启/升级/恢复全链路 |
| M10 测试 | 部分 | 配置、单包结构、自包含导入、OFF 生命周期、状态路由 6 项 |
| M11 发布 | 本文件对应 alpha | 不发布 rc.1，不宣称旧插件能力等价 |

## 已验证

```powershell
python -m unittest discover -s tests -t . -v
```

- 6 项通过；
- 单包根目录、metadata 无 BOM、自包含导入；
- `OFF` 不启动 pump、生命周期 `RUNNING -> CLOSED`；
- 控制台注册 `/astrbot_plugin_digital_life/console/status`。

## 明确未完成

- 旧基座身份映射、迁移清单/冲突处理、断点续跑；
- 原话撤回/删除的跨库失效链；
- 备份停写、校验、切换、启动恢复；
- 偏好排序、短指代、主动聊天等旧插件能力；
- 真实环境全链路、模型质量与 72h 运行。

因此当前版本只能作为 alpha 安装候选，不能按工程方案的 `v0.6.0-rc.1` 验收。
