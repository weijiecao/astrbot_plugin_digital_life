# 离线验收

`core/tests` 保留上一轮 alpha.6 审核使用的 137 项共享核心回归。`run_core_package.py` 强制模块路径位于指定解压包内；运行包不依赖本目录。新功能在 `tests/completion_suite.py` 验证。

执行 `python -m unittest discover -s tests -t . -v` 自动构建包、在隔离子进程执行核心与新增功能测试，并保留原有 20 项插件测试。两个子进程入口是包装器，统计独立用例时不要再重复计入包装器本身。

UI：`tests/console_dom_check.cjs` 用 jsdom 执行实际页面事件委托，借管道调用真实 ConsoleApi/ApplicationService，替换的是 AstrBot 宿主壳。它不等于真实浏览器布局或 AstrBot 登录会话验收。

可选 `tests/console_browser_check.py` 通过真实 Chromium 执行相同流程；当前工作环境禁止 Chromium 所需的 socket，故此项未通过。可在允许启动浏览器的开发环境安装 Playwright/aiohttp 后运行，不能把环境阻断记录改写成浏览器通过。
