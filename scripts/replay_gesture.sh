#!/system/bin/sh
# Android 手势回放脚本 - 兼容 Android sh 环境
# 使用 sendevent 注入触控事件
# 用法: adb shell sh /data/local/tmp/replay_gesture.sh [DEVICE] [LOOPS]
# 例: adb shell sh /data/local/tmp/replay_gesture.sh /dev/input/event5 1

# 配置
EVENT_DEVICE="${1:-/dev/input/event5}"  # 触控设备
LOOP_COUNT="${2:-1}"  # 循环次数

echo "================================="
echo "Android 手势回放工具"
echo "================================="
echo "事件设备: $EVENT_DEVICE"
echo "循环次数: $LOOP_COUNT"
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
i=1
while [ $i -le $LOOP_COUNT ]; do
    echo "第 $i/$LOOP_COUNT 次回放"
    
    # 这里插入实际的 sendevent 命令
    # 格式: sendevent /dev/input/event5 TYPE CODE VALUE
    # 例如点击屏幕中心 (540, 960):
    # sendevent $EVENT_DEVICE 3 57 0
    # sendevent $EVENT_DEVICE 3 53 540
    # sendevent $EVENT_DEVICE 3 54 960
    # sendevent $EVENT_DEVICE 0 0 0
    # sleep 0.5
    # sendevent $EVENT_DEVICE 3 57 -1
    # sendevent $EVENT_DEVICE 0 0 0
    
    echo "本次回放完成"
    
    if [ $i -lt $LOOP_COUNT ]; then
        echo "等待 2 秒后进行下一次回放..."
        sleep 2
    fi
    
    i=$((i + 1))
done

echo ""
echo "所有回放完成！"
