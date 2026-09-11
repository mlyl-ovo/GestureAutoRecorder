#!/bin/bash
# Android 手势录制脚本
# 使用 getevent 捕获原始触控事件
# 用法: adb shell bash /data/local/tmp/record_gesture.sh

# 配置
EVENT_DEVICE="${1:-/dev/input/event1}"  # 触控设备，默认 event1
OUTPUT_FILE="/data/local/tmp/gesture_raw.txt"

echo "================================="
echo "Android 手势录制工具"
echo "================================="
echo ""
echo "触控设备: $EVENT_DEVICE"
echo "输出文件: $OUTPUT_FILE"
echo ""
echo "开始录制手势..."
echo "请在手机上进行你想要录制的操作"
echo "按 Ctrl+C 停止录制"
echo ""

# 清空输出文件
> $OUTPUT_FILE

# 记录开始时间
START_TIME=$(date +%s%N)
echo "# Gesture Recording" > $OUTPUT_FILE
echo "# Start Time: $(date)" >> $OUTPUT_FILE
echo "# Event Device: $EVENT_DEVICE" >> $OUTPUT_FILE
echo "# Format: timestamp event_type code value" >> $OUTPUT_FILE
echo "#" >> $OUTPUT_FILE

# 捕获事件并记录
getevent $EVENT_DEVICE | while IFS=' ' read -r dev type code value; do
    CURRENT_TIME=$(date +%s%N)
    ELAPSED=$((($CURRENT_TIME - $START_TIME) / 1000000))  # 转换为毫秒
    echo "$ELAPSED $type $code $value" >> $OUTPUT_FILE
done

echo ""
echo "录制完成！"
echo "结果已保存到: $OUTPUT_FILE"
echo ""
echo "使用以下命令下载录制文件:"
echo "  adb pull $OUTPUT_FILE ./"
