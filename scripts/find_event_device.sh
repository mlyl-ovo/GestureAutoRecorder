#!/bin/bash
# 自动查找触控设备的事件号
# 输出结果格式: /dev/input/eventX

echo "扫描触控设备..."
echo ""

# 查找 touchscreen 设备
for device in /proc/bus/input/devices; do
    if [ -f "$device" ]; then
        cat "$device" | grep -A 5 "Name.*[Tt]ouch\|Name.*[Ss]creen" | grep "Handlers" | grep -oE "event[0-9]+"
    fi
done

# 如果上面没找到，尝试直接列出所有 event 设备
echo ""
echo "所有输入设备:"
ls -la /dev/input/event* 2>/dev/null || echo "未找到事件设备"

echo ""
echo "使用以下命令测试触控事件:"
echo "  adb shell getevent /dev/input/event0"
echo "  adb shell getevent /dev/input/event1"
echo ""
echo "在列出的设备中选择能响应触屏操作的那个"
