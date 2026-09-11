# 事件格式说明

## getevent 原始格式

`getevent` 输出的原始格式为：
```
[设备] [事件类型] [事件代码] [值]
```

### 事件类型编码

| 代码 | 含义 | 说明 |
|------|------|------|
| 0001 | EV_KEY | 按键/按钮事件 |
| 0003 | EV_ABS | 绝对坐标事件 |
| 0000 | EV_SYN | 同步事件（标记事件结束） |
| 0002 | EV_REL | 相对运动事件 |

### 常见事件代码

#### 绝对坐标事件 (EV_ABS = 0003)

| 代码 | 代码(hex) | 含义 |
|------|-----------|------|
| 57 | 0x39 | ABS_MT_TRACKING_ID - 触控点 ID |
| 53 | 0x35 | ABS_MT_POSITION_X - X 坐标 |
| 54 | 0x36 | ABS_MT_POSITION_Y - Y 坐标 |
| 88 | 0x58 | ABS_MT_PRESSURE - 压力值 |
| 84 | 0x54 | ABS_MT_TOUCH_MAJOR - 触点宽度 |

#### 按键事件 (EV_KEY = 0001)

| 代码 | 代码(hex) | 含义 |
|------|-----------|------|
| 330 | 0x14a | BTN_TOUCH - 触摸按钮 |
| 158 | 0x9e | BTN_BACK - 返回键 |

#### 同步事件 (EV_SYN = 0000)

| 代码 | 代码(hex) | 含义 | 值 |
|------|-----------|------|-----|
| 0 | 0x00 | SYN_REPORT | 0 |

## 录制文件格式

转换工具生成的 shell 脚本格式：

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
    
    # 事件 1: 按下触点
    sleep 0.050
    sendevent $DEVICE 3 57 0              # 设置触点 ID 为 0
    sendevent $DEVICE 3 53 540            # 设置 X = 540
    sendevent $DEVICE 3 54 960            # 设置 Y = 960
    sendevent $DEVICE 0 0 0               # 同步
    
    # 延迟 0.5 秒
    sleep 0.500
    
    # 事件 2: 移动触点
    sendevent $DEVICE 3 53 545            # 更新 X
    sendevent $DEVICE 3 54 955            # 更新 Y
    sendevent $DEVICE 0 0 0               # 同步
    
    # 延迟
    sleep 0.100
    
    # 事件 3: 释放触点
    sendevent $DEVICE 3 57 -1             # 触点 ID 设为 -1（释放）
    sendevent $DEVICE 0 0 0               # 同步
    
    if [ $i -lt $LOOP ]; then
        echo "Waiting before next loop..."
        sleep 2
    fi
done

echo "Replay complete!"
```

## 常见操作对应的事件序列

### 1. 单点点击

```bash
# 按下（在坐标 540, 960）
sendevent /dev/input/event1 3 57 0      # 触点 ID = 0
sendevent /dev/input/event1 3 53 540    # X 坐标
sendevent /dev/input/event1 3 54 960    # Y 坐标
sendevent /dev/input/event1 0 0 0       # 同步

# 延迟 50ms
sleep 0.05

# 释放
sendevent /dev/input/event1 3 57 -1     # 触点 ID = -1（释放）
sendevent /dev/input/event1 0 0 0       # 同步
```

### 2. 滑动（从 A 点到 B 点）

```bash
# 按下 A 点 (100, 200)
sendevent /dev/input/event1 3 57 0
sendevent /dev/input/event1 3 53 100
sendevent /dev/input/event1 3 54 200
sendevent /dev/input/event1 0 0 0

# 移动到 B 点 (500, 600)，中间多个中间点
sleep 0.05
sendevent /dev/input/event1 3 53 200
sendevent /dev/input/event1 3 54 300
sendevent /dev/input/event1 0 0 0

sleep 0.05
sendevent /dev/input/event1 3 53 300
sendevent /dev/input/event1 3 54 400
sendevent /dev/input/event1 0 0 0

sleep 0.05
sendevent /dev/input/event1 3 53 500
sendevent /dev/input/event1 3 54 600
sendevent /dev/input/event1 0 0 0

# 释放
sleep 0.05
sendevent /dev/input/event1 3 57 -1
sendevent /dev/input/event1 0 0 0
```

### 3. 长按（持续按住）

```bash
# 按下
sendevent /dev/input/event1 3 57 0
sendevent /dev/input/event1 3 53 540
sendevent /dev/input/event1 3 54 960
sendevent /dev/input/event1 0 0 0

# 持续 2 秒
sleep 2.0

# 释放
sendevent /dev/input/event1 3 57 -1
sendevent /dev/input/event1 0 0 0
```

### 4. 多点触控（两个手指）

```bash
# 手指 1 按下
sendevent /dev/input/event1 3 57 0      # 手指 1 ID
sendevent /dev/input/event1 3 53 200    # 手指 1 X
sendevent /dev/input/event1 3 54 300    # 手指 1 Y
sendevent /dev/input/event1 0 0 0       # 同步

# 手指 2 按下
sendevent /dev/input/event1 3 57 1      # 手指 2 ID（不同的 ID）
sendevent /dev/input/event1 3 53 800    # 手指 2 X
sendevent /dev/input/event1 3 54 300    # 手指 2 Y
sendevent /dev/input/event1 0 0 0       # 同步

# 两个手指同时移动（缩小）
sleep 0.1
sendevent /dev/input/event1 3 57 0      # 手指 1
sendevent /dev/input/event1 3 53 300    # 向中间移动
sendevent /dev/input/event1 3 54 400
sendevent /dev/input/event1 0 0 0

sendevent /dev/input/event1 3 57 1      # 手指 2
sendevent /dev/input/event1 3 53 700    # 向中间移动
sendevent /dev/input/event1 3 54 400
sendevent /dev/input/event1 0 0 0

# 手指 1 释放
sleep 0.1
sendevent /dev/input/event1 3 57 0
sendevent /dev/input/event1 3 53 300
sendevent /dev/input/event1 3 54 400
sendevent /dev/input/event1 3 57 -1    # 释放
sendevent /dev/input/event1 0 0 0

# 手指 2 释放
sendevent /dev/input/event1 3 57 1
sendevent /dev/input/event1 3 53 700
sendevent /dev/input/event1 3 54 400
sendevent /dev/input/event1 3 57 -1    # 释放
sendevent /dev/input/event1 0 0 0
```

## 手动编辑脚本

### 修改延迟时间

```bash
# 将所有 sleep 0.5 改为 sleep 0.2（加速）
sed -i 's/sleep 0\.5/sleep 0.2/g' replay_gesture.sh

# 将所有 sleep 改为原来的 2 倍（减速）
sed -i 's/sleep \([0-9.]*\)/sleep $(echo "\1 * 2" | bc)/g' replay_gesture.sh
```

### 修改坐标

```bash
# 将所有 X=540 改为 X=600（右移 60）
sed -i 's/53 540/53 600/g' replay_gesture.sh

# 将所有 Y=960 改为 Y=1000（下移 40）
sed -i 's/54 960/54 1000/g' replay_gesture.sh
```

### 调整循环次数

```bash
# 修改脚本的循环次数（在命令行指定）
/data/local/tmp/replay_gesture.sh /dev/input/event1 10  # 运行 10 次

# 或在脚本中修改默认值
sed -i 's/LOOP="${2:-1}"/LOOP="${2:-5}"/g' replay_gesture.sh  # 默认 5 次
```

## 获取屏幕分辨率和坐标系统

```bash
# 查看屏幕分辨率
adb shell wm size
# 输出: Physical size: 1080x2340

# 查看屏幕密度（DPI）
adb shell wm density
# 输出: Physical density: 420

# 获取触控坐标的最大范围
adb shell cat /proc/bus/input/devices | grep -A 10 "ABS_MT"
```

## 事件值说明

### sendevent 事件值（VALUE）

- **触点 ID (ABS_MT_TRACKING_ID)**: 
  - `0` 到 `N`: 有效的触点 ID
  - `-1`: 释放该触点（结束触摸）
  - 不同的手指应该有不同的 ID

- **坐标值 (ABS_MT_POSITION_X/Y)**:
  - `0` 到设备最大值（通常 1080 或 2160）
  - 根据屏幕分辨率和触控设备调整

- **压力值 (ABS_MT_PRESSURE)**:
  - `0`: 无压力（可选，某些设备忽略）
  - `1` 到 `N`: 压力大小（越大压力越强）

## 工具转换说明

### convert_to_script.py

该工具会：
1. 读取 `getevent` 的原始输出
2. 计算相邻事件间的延迟
3. 生成 `sendevent` 命令序列
4. 添加必要的 `sleep` 延迟
5. 生成可执行的 shell 脚本

### 转换过程

```
原始录制 (gesture_raw.txt)
    ↓
  [转换工具]
    ↓
可执行脚本 (replay_gesture.sh)
    ↓
  [推送到设备]
    ↓
[设备后台执行]
```

## 常见坐标参考

对于常见屏幕尺寸，常用坐标：

| 屏幕 | 分辨率 | 中心 | 左上 | 右下 |
|------|--------|------|------|------|
| 小屏 | 720×1280 | (360, 640) | (0, 0) | (720, 1280) |
| 普通 | 1080×1920 | (540, 960) | (0, 0) | (1080, 1920) |
| 大屏 | 1440×2560 | (720, 1280) | (0, 0) | (1440, 2560) |
| 高刷 | 1080×2340 | (540, 1170) | (0, 0) | (1080, 2340) |

