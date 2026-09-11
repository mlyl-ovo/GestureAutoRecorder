#!/bin/bash
# Android 手势回放脚本模板
# 此脚本由 convert_to_script.py 自动生成
# 使用 sendevent 注入触控事件
# 用法: adb shell bash /data/local/tmp/replay_gesture.sh

# 配置
EVENT_DEVICE="${1:-/dev/input/event1}"  # 触控设备
LOOP_COUNT="${2:-1}"  # 循环次数
SPEED_FACTOR="${3:-1}"  # 速度因子 (0.5=半速, 2=双速)

echo "================================="
echo "Android 手势回放工具"
echo "================================="
echo "事件设备: $EVENT_DEVICE"
echo "循环次数: $LOOP_COUNT"
echo "速度因子: $SPEED_FACTOR"
echo ""
echo "开始回放..."
echo ""

# 检查 sendevent 是否可用
if ! command -v sendevent &> /dev/null; then
    echo "错误: sendevent 命令不可用"
    echo "请确保设备已 root，并使用 root 用户运行此脚本"
    exit 1
fi

# 检查事件设备是否存在
if [ ! -c "$EVENT_DEVICE" ]; then
    echo "错误: $EVENT_DEVICE 不存在"
    echo "请检查设备号是否正确"
    exit 1
fi

# 回放循环
for ((i=1; i<=LOOP_COUNT; i++)); do
    echo "第 $i/$LOOP_COUNT 次回放"
    
    # 这里插入实际的 sendevent 命令
    # 格式: sendevent /dev/input/eventX TYPE CODE VALUE
    # 例如点击屏幕中心 (540, 960):
    # sendevent /dev/input/event1 3 57 0     # 按下 (ABS_MT_TRACKING_ID)
    # sendevent /dev/input/event1 3 53 540   # 设置 X 坐标 (ABS_MT_POSITION_X)
    # sendevent /dev/input/event1 3 54 960   # 设置 Y 坐标 (ABS_MT_POSITION_Y)
    # sendevent /dev/input/event1 0 0 0      # 同步 (SYN_REPORT)
    # sleep 0.5                              # 延迟
    # sendevent /dev/input/event1 3 57 -1    # 释放
    # sendevent /dev/input/event1 0 0 0      # 同步
    
    echo "本次回放完成"
    
    if [ $i -lt $LOOP_COUNT ]; then
        echo "等待 2 秒后进行下一次回放..."
        sleep 2
    fi
done

echo ""
echo "所有回放完成！"
