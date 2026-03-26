# 🎓 Awesome ZJU Toolkit

> 一个基于 Python 的校园生活自动化工具集，旨在通过技术手段提升日常琐事处理效率。

---

## 🌟 项目简介
本项目集成针对校园环境设计的自动化脚本，涵盖 **自动检测签到** ， **校园跑路线GPX文件生成** 等功能。搭配其他工具可以实现简易的自动化。

## 📂 目录结构
```text
Awesome-ZJU-Toolkit/
├── README.md
├── Auto_Checkin_Monitor/  # 自动检测签到
│   ├── README.md
│   ├── requirements.txt
│   └── main.py
├── GPXroute/              # 校园跑路线GPX文件生成
│   ├── README.md
│   ├── requirements.txt
│   └── main.py
... (more tools coming soon)
```

## 🛠️ 核心功能概览

### 1. 自动检测签到 (`Auto_Checkin_Monitor/`)
* **功能**：实时轮询签到页面状态。
* **特性**：内置页面刷新失败检测，可稳定挂载后台。
* **扩展**：添加Bark推送功能，便于手机同步提醒。

### 2. 校园跑路线GPX文件生成 (`GPXroute/`)
* **功能**：基于标准 400m/200m 跑道几何建模。
* **特性**：支持 2D 旋转矩阵适配不同角度操场，内置高斯噪声模拟真实轨迹。
* **输出**：生成符合 Xcode 协议的 `.gpx` 轨迹文件及交互式 `.html` 地图预览。


## 📦 快速开始

### 环境安装
建议使用 Python 3.8+ 环境。

### 运行说明
每个子模块均包含独立的逻辑，进入对应目录执行命令：
```bash
pip install -r requirements.txt
```
详细参数配置请参考各模块内部注释或子目录说明。

## 🚷 施工项目

### Mark: 一站式DDL，个人目标，routine管理app
（开发中...）

## ⚠️ 免责声明
1. 本项目仅供 **算法研究** 与 **自动化测试** 交流使用。
2. 开发者不对因非法使用本项目工具而导致的任何校规处分或法律后果负责。
3. 请合理使用自动化工具，尊重教学管理秩序。

---
**Developed by FLEITI**
