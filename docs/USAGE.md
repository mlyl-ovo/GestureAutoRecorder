# 使用教程

## 概述

本教程将指导你完成以下流程：
1. 🎬 **录制**手势操作
2. 🔄 **转换**为可执行脚本
3. ▶️ **回放**手势操作

## 完整流程

### 第一步：查找触控设备

首先，需要确定你的手机使用的是哪个事件设备。

```bash
# 查看所有输入设备
adb shell cat /proc/bus/input/devices

# 或使用脚本查找
adb push scripts/find_event_device.sh /data/local/tmp/
adb shell bash /data/local/tmp/find_event_device.sh
```

输出示例：
```
N: Name="ilitek_ts"
H: Handlers=mouse0 event1
```

这里的 `event1` 就是我们需要的设备号。记下来，后续会用到。

### 第二步：录制手势

#### 使用脚本录制（推荐）

```bash
# 1. 将录制脚本推送到设备
adb push scripts/record_gesture.sh /data/local/tmp/

# 2. 执行录制脚本（指定正确的 event 号，这里以 event1 为例）
adb shell bash /data/local/tmp/record_gesture.sh /dev/input/event1

# 此时手机开始录制
# 进行你想要的游戏操作（移动、攻击、释放技能等）
# 完成后按 Ctrl+C 停止录制
```

输出示例：
```
=================================
Android 手势录制工具
=================================

触控设备: /dev/input/event1
输出文件: /data/local/tmp/gesture_raw.txt

开始录制手势...
请在手机上进行你想要的操作
按 Ctrl+C 停止录制
```

#### 手动使用 getevent 录制（高级）

```bash
# 直接使用 getevent 查看事件
adb shell getevent /dev/input/event1

# 将输出重定向到文件
adb shell getevent /dev/input/event1 > gesture_raw.txt
```

### 第三步：下载录制文件

```bash
# 将录制的原始数据从设备拉到电脑
adb pull /data/local/tmp/gesture_raw.txt ./

# 查看录制内容
cat gesture_raw.txt
```

输出示例：
```
# Gesture Recording
# Start Time: 2024-01-15 14:30:45
# Event Device: /dev/input/event1
# Format: timestamp event_type code value
#
0 0033 0035 0540
0 0033 0036 0960
0 0014 014a 0001
0 0000 0000 0000
500 0033 0036 0950
1000 0033 0035 0545
...
```

### 第四步：转换为脚本

```bash
# 使用 Python 工具将原始数据转换为可执行脚本
python3 tools/convert_to_script.py gesture_raw.txt replay_gesture.sh /dev/input/event1

# 输出类似于:
# ✓ 脚本已生成: replay_gesture.sh
#   事件数: 247
#   总时长: 15.23s
#   设备: /dev/input/event1
```

生成的脚本格式：

```bash
#!/bin/bash
# Gesture Replay Script
# Auto-generated replay script
# Event device: /dev/input/event1
# Total duration: 15.23s
# Total events: 247

DEVICE="${1:-/dev/input/event1}"
LOOP="${2:-1}"

if [ ! -c "$DEVICE" ]; then
    echo "Error: $DEVICE not found"
    exit 1
fi

for ((i=1; i<=LOOP; i++)); do
    echo "Playing loop $i/$LOOP"
    
    sleep 0.050
    sendevent $DEVICE 0033 0035 0540
    sendevent $DEVICE 0033 0036 0960
    ...
    
    if [ $i -lt $LOOP ]; then
        echo "Waiting before next loop..."
        sleep 2
    fi
done

echo "Replay complete!"
```

### 第五步：推送脚本到设备

```bash
# 推送脚本
adb push replay_gesture.sh /data/local/tmp/

# 给予执行权限
adb shell chmod +x /data/local/tmp/replay_gesture.sh

# 验证脚本
adb shell ls -la /data/local/tmp/replay_gesture.sh
```

### 第六步：测试回放

```bash
# 打开游戏（或你想要自动化的应用）
# 然后在电脑上执行：

adb shell /data/local/tmp/replay_gesture.sh

# 或指定参数：
# 参数1: 事件设备（可选，默认 /dev/input/event1）
# 参数2: 循环次数（可选，默认 1）

adb shell /data/local/tmp/replay_gesture.sh /dev/input/event1 1
```

### 第七步：后台运行（断开 ADB）

**核心功能**：一旦推送到设备，脚本可以在没有 ADB 连接的情况下运行！

#### 方案 1：使用 nohup 后台运行

```bash
# 推送脚本到设备
adb push replay_gesture.sh /data/local/tmp/
adb shell chmod +x /data/local/tmp/replay_gesture.sh

# 使用 nohup 在后台运行（即使断开 ADB 也继续运行）
adb shell nohup /data/local/tmp/replay_gesture.sh > /data/local/tmp/replay.log 2>&1 &

# 断开 ADB 连接（脚本继续运行）
adb disconnect

# 查看运行日志（可选）
adb shell tail -f /data/local/tmp/replay.log
```

#### 方案 2：在设备 Terminal 中运行

1. 在手机上安装 **Termux** 或其他 Terminal 应用
2. 打开 Terminal
3. 执行脚本：
   ```bash
   bash /data/local/tmp/replay_gesture.sh
   ```
4. 断开 ADB 连接，脚本继续运行

#### 方案 3：创建启动脚本（高级）

```bash
# 创建一个启动脚本，让脚本在后台持续运行
cat > /data/local/tmp/start_replay.sh << 'EOF'
#!/bin/bash
# 后台运行脚本 3 次循环
nohup /data/local/tmp/replay_gesture.sh /dev/input/event1 3 > /data/local/tmp/replay.log 2>&1 &
echo $! > /data/local/tmp/replay.pid
EOF

adb shell chmod +x /data/local/tmp/start_replay.sh
adb shell /data/local/tmp/start_replay.sh
```

## 常用命令参考

| 操作 | 命令 |
|------|------|
| 查看录制结果 | `adb pull /data/local/tmp/gesture_raw.txt ./` |
| 转换脚本 | `python3 tools/convert_to_script.py input.txt output.sh` |
| 推送脚本 | `adb push replay_gesture.sh /data/local/tmp/` |
| 直接运行 | `adb shell /data/local/tmp/replay_gesture.sh` |
| 后台运行 | `adb shell nohup /data/local/tmp/replay_gesture.sh &` |
| 查看日志 | `adb shell tail -f /data/local/tmp/replay.log` |
| 停止运行 | `adb shell pkill -f replay_gesture` |
| 查看进程 | `adb shell ps \| grep replay` |
| 权限检查 | `adb shell ls -la /data/local/tmp/replay_gesture.sh` |

## 游戏场景示例

### 原神 - 自动打怪循环

```bash
# 1. 录制步骤：
#    - 靠近怪物
#    - 点击攻击
#    - 释放大招
#    - 走开

adb push scripts/record_gesture.sh /data/local/tmp/
adb shell bash /data/local/tmp/record_gesture.sh /dev/input/event1
# [进行上述操作]
# Ctrl+C 停止

# 2. 转换脚本
adb pull /data/local/tmp/gesture_raw.txt ./
python3 tools/convert_to_script.py gesture_raw.txt genshin_farm.sh

# 3. 推送并运行
adb push genshin_farm.sh /data/local/tmp/
adb shell chmod +x /data/local/tmp/genshin_farm.sh
adb shell nohup /data/local/tmp/genshin_farm.sh /dev/input/event1 10 &
# 脚本将自动循环 10 次
```

### 王者荣耀 - 英雄连招

```bash
# 1. 录制英雄连招（按住方向键移动 + 依次点击技能）
adb shell bash /data/local/tmp/record_gesture.sh /dev/input/event1
# [进行连招操作]

# 2. 转换并运行
adb pull /data/local/tmp/gesture_raw.txt ./
python3 tools/convert_to_script.py gesture_raw.txt king_combo.sh
adb push king_combo.sh /data/local/tmp/
adb shell nohup /data/local/tmp/king_combo.sh /dev/input/event1 5 &
```

## 脚本参数

生成的脚本支持以下参数：

```bash
# 基本用法
/data/local/tmp/replay_gesture.sh [DEVICE] [LOOPS]

# 参数说明
DEVICE   - 触控设备路径，默认 /dev/input/event1
LOOPS    - 循环次数，默认 1

# 示例
/data/local/tmp/replay_gesture.sh                          # 运行 1 次
/data/local/tmp/replay_gesture.sh /dev/input/event1        # 指定设备
/data/local/tmp/replay_gesture.sh /dev/input/event1 5      # 循环 5 次
```

## 下一步

- 查看 [脚本格式说明](EVENT_FORMAT.md) 了解如何手动编辑脚本
- 查看 [故障排查](TROUBLESHOOTING.md) 解决常见问题
