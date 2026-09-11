# GestureAutoRecorder 🎮

Android 手势录制与离线回放工具 - 基于 Shell 脚本的游戏自动化方案

**适用游戏**：原神、王者荣耀、鸣潮等所有触控类游戏

## ✨ 核心特性

- ✅ **设备端录制** - 直接在手机上用 `getevent` 捕获真实触控事件
- ✅ **离线回放** - 生成 `.sh` 脚本，断开 ADB 后台独立运行
- ✅ **多点并行** - 支持同时进行多个操作（如左手按住方向键 + 右手点技能）
- ✅ **精确时序** - 毫秒级的时间控制
- ✅ **易于编辑** - 脚本格式清晰，支持手动修改延迟和操作

## 🚀 快速开始

### 前置要求

- Android 13+ 手机，已 root（Magisk/SuperSU）
- 已通过 ADB 连接到电脑
- 手机已连接到电脑的 Shell 访问

### 第一步：获取设备信息

```bash
adb shell cat /proc/bus/input/devices
```

找到 touchscreen 对应的 event 号（通常是 `event0` 或 `event1`）

### 第二步：录制手势

```bash
# 1. 将录制脚本推送到设备
adb push scripts/record_gesture.sh /data/local/tmp/

# 2. 在设备上执行录制
adb shell chmod +x /data/local/tmp/record_gesture.sh
adb shell /data/local/tmp/record_gesture.sh

# 此时手机开始录制，进行你想要的游戏操作
# 完成后按 Ctrl+C 停止

# 3. 获取录制结果
adb pull /data/local/tmp/gesture_raw.txt ./
```

### 第三步：生成回放脚本

```bash
# 运行转换工具（需要 Python 3）
python3 tools/convert_to_script.py gesture_raw.txt output_gesture.sh

# 脚本已生成！可以预览
cat output_gesture.sh
```

### 第四步：推送并运行回放脚本

```bash
# 推送脚本到设备
adb push output_gesture.sh /data/local/tmp/

# 给予执行权限
adb shell chmod +x /data/local/tmp/output_gesture.sh

# 在设备上后台运行（断开 ADB 也继续运行）
adb shell nohup /data/local/tmp/output_gesture.sh > /data/local/tmp/replay.log 2>&1 &

# 或者直接在设备 Shell 运行
adb shell /data/local/tmp/output_gesture.sh
```

## 📁 项目结构

```
GestureAutoRecorder/
├── README.md                          # 本文件
├── scripts/
│   ├── record_gesture.sh             # 设备端录制脚本
│   ├── replay_gesture.sh             # 基础回放脚本（示例）
│   └── find_event_device.sh          # 自动查找触控设备
├── tools/
│   ├── convert_to_script.py          # 录制数据 → 可执行脚本
│   ├── event_monitor.py              # 实时查看触控事件
│   └── gesture_editor.py             # 脚本编辑工具
├── examples/
│   ├── genshin_farming.sh            # 原神自动刷怪示例
│   ├── king_honor_combo.sh           # 王者连招示例
│   └── wuthering_waves_explore.sh    # 鸣潮自动探图示例
└── docs/
    ├── SETUP.md                      # 详细安装指南
    ├── USAGE.md                      # 使用教程
    ├── TROUBLESHOOTING.md            # 故障排查
    └── EVENT_FORMAT.md               # 事件格式说明
```

## 📖 详细文档

- [安装指南](docs/SETUP.md) - root 和 ADB 环境配置
- [使用教程](docs/USAGE.md) - 完整的录制和回放步骤
- [脚本编辑](docs/EVENT_FORMAT.md) - 理解和修改脚本
- [故障排查](docs/TROUBLESHOOTING.md) - 常见问题解决

## 🎮 游戏场景示例

### 原神 - 自动打怪

```bash
# 录制内容：走到怪物位置 → 点击攻击 → 释放大招 → 走开
adb push examples/genshin_farming.sh /data/local/tmp/
adb shell /data/local/tmp/genshin_farming.sh
```

### 王者荣耀 - 英雄连招

```bash
# 录制内容：走位 → 一技能 → 二技能 → 大招 → 走位
adb push examples/king_honor_combo.sh /data/local/tmp/
adb shell /data/local/tmp/king_honor_combo.sh
```

## ⚙️ 原理说明

### 录制阶段
1. 使用 `getevent` 监听 `/dev/input/event*`
2. 捕获原始触控事件（按下、移动、释放）
3. 记录每个事件的时间戳和坐标

### 回放阶段
1. 读取录制的事件数据
2. 计算事件间的延迟
3. 使用 `sendevent` 注入到 `/dev/input/event*`
4. 支持循环、加速、减速回放

## 🔧 常用命令

```bash
# 查找触控设备
adb shell getevent -l | head -20

# 实时监控触控事件
adb shell getevent /dev/input/event1

# 后台运行脚本（断开 ADB 继续）
adb shell nohup /data/local/tmp/gesture.sh &

# 查看后台运行日志
adb shell tail -f /data/local/tmp/replay.log

# 停止正在运行的脚本
adb shell pkill -f gesture.sh
```

## ⚠️ 重要提示

1. **账号安全**
   - 不要在排名赛/竞技模式使用自动化
   - 容易被游戏检测并封号
   - 仅用于单机/闲置模式

2. **设备安全**
   - Root 可能影响系统稳定性
   - 长时间运行可能导致手机发热
   - 建议测试前备份重要数据

3. **精度问题**
   - 不同手机分辨率会影响坐标
   - 同一部手机、同一分辨率录制和回放最佳
   - 如需适配多分辨率，手动编辑脚本

## 📝 脚本格式示例

生成的脚本格式：

```bash
#!/bin/bash
# Gesture Replay Script
# Recorded on: 2024-01-15
# Event device: /dev/input/event1
# Duration: 15.3s

# 点击坐标 (540, 960) - 按下
sendevent /dev/input/event1 3 57 0
sendevent /dev/input/event1 3 53 540
sendevent /dev/input/event1 3 54 960
sendevent /dev/input/event1 0 0 0

# 延迟 0.5 秒
sleep 0.5

# 同一位置释放
sendevent /dev/input/event1 3 57 -1
sendevent /dev/input/event1 0 0 0

# 后续操作...
```

## 🐛 故障排查

**问题：脚本运行后没有反应**
- 检查 event 设备号是否正确
- 确认 sendevent 命令是否可用（root 用户）

**问题：坐标不对**
- 不同分辨率录制回放会有偏差
- 需在同一分辨率的设备上操作

**问题：多点触控不工作**
- 检查 event 设备支持的触控点数
- 某些老设备可能不支持多点

详见 [故障排查文档](docs/TROUBLESHOOTING.md)

## 🤝 贡献

欢迎提交 Issue 和 PR！

- 报告 Bug
- 提交新的游戏场景示例
- 改进脚本工具

## 📄 许可证

MIT License - 仅供学习和研究使用

## 联系方式

有问题？提交 Issue 或 Discussion！

---

**免责声明**：本项目仅供学习和研究使用。使用过程中产生的任何后果（包括账号封禁、设备损害等）由用户自行承担。
