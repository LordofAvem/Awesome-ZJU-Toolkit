# Auto Check-in Monitor：自动检测签到

> 基于 Playwright 自动化引擎的网页监控工具。通过实时扫描课堂列表页面，检测特定的签到关键字（如“雷达点名”），并触发多端联合提醒。

---

## 核心功能
自动化仿真：使用 Chromium 内核加载真实网页，自动处理页面刷新与 DOM 渲染。

联合提醒机制：

- Windows 声音：调用 winsound 发出系统级蜂鸣警告。

- 顶层弹窗：通过 tkinter 强制置顶显示消息框，确保不会错过视觉提醒。

- iOS Bark 推送：支持一键推送到 iPhone，即使你暂时离开座位，手机也能收到通知。

稳定监控模式：内置异常处理与断线重试逻辑，确保长时运行不崩溃。

## 环境依赖
除了根目录的 requirements.txt，该脚本额外需要浏览器驱动支持。执行以下命令配置环境：
```Bash
pip install -r requirements.txt
playwright install chromium
```
## 配置指南
在运行脚本前，请根据实际情况修改 `main.py` 顶部的配置：

KEYWORDS：添加你课程中常见的签到词（例如：数字点名、雷达点名）。

BARK_KEY：填入你 iOS Bark App 提供的 Key，若不需要手机推送可留空。

REFRESH_INTERVAL：默认每 5 秒刷新一次（建议不要设置太快，以防被系统封禁）。

## 使用步骤
启动程序：

```Bash
python main.py
```
人工干预：
程序会自动打开浏览器。由于学校系统通常需要统一身份认证（ZJU），请在弹出的浏览器窗口中手动完成登录。

开始监控：
登录成功并跳转到点名列表页后，回到命令行按 回车(Enter)，脚本即进入自动监控状态。

## ⚠️ 注意事项
环境限制：winsound 和 tkinter 弹窗主要针对 Windows 环境优化。

检测延迟：经多次使用测试，Bark推送一般会晚于Windows本地推送5s左右。