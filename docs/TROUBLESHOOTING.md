# 故障排查

## 常见问题

### 问题 1："sendevent: not found"

**原因**：
- sendevent 命令不可用
- 没有 root 权限
- 设备上没有此工具

**解决方案**：
```bash
# 确认 root 权限
adb shell su -c "whoami"
# 应该返回 root

# 确认 sendevent 存在
adb shell which sendevent

# 如果不存在，尝试使用完整路径
adb shell /system/xbin/sendevent /dev/input/event1 ...

# 或使用 input 命令（某些设备可用）
adb shell input tap 540 960
```

### 问题 2："No such file or directory: /dev/input/event1"

**原因**：
- 使用了错误的事件设备号
- 触控设备在不同位置

**解决方案**：
```bash
# 重新查找触控设备
adb shell cat /proc/bus/input/devices | grep -i -A 2 "touch\|screen"

# 尝试所有可能的 event 设备
for i in {0..9}; do
    echo "Testing event$i:"
    adb shell getevent /dev/input/event$i &
    PID=$!
    sleep 1
    touch your phone screen
    sleep 1
    kill $PID
done
```

### 问题 3：回放后没有任何反应

**原因**：
- 事件设备号错误
- 脚本中的坐标超出屏幕范围
- sendevent 命令执行失败

**排查步骤**：
```bash
# 1. 验证脚本是否执行
adb shell bash -x /data/local/tmp/replay_gesture.sh 2>&1 | head -20

# 2. 手动测试 sendevent
# 获取屏幕分辨率
adb shell wm size
# 输出: Physical size: 1080x2340

# 尝试点击屏幕中心
adb shell su -c "sendevent /dev/input/event1 3 57 0"
adb shell su -c "sendevent /dev/input/event1 3 53 540"
adb shell su -c "sendevent /dev/input/event1 3 54 1170"
adb shell su -c "sendevent /dev/input/event1 0 0 0"

# 3. 查看运行日志
adb shell cat /data/local/tmp/replay.log
```

### 问题 4：录制文件为空或包含垃圾数据

**原因**：
- 录制脚本有问题
- 触控设备号错误
- getevent 命令失败

**解决方案**：
```bash
# 使用 -l 参数查看可读的事件名称
adb shell getevent -l /dev/input/event1

# 手动录制并重定向到文件
adb shell getevent /dev/input/event1 > /data/local/tmp/test.txt &
# [在手机上进行操作]
# Ctrl+C 停止

# 检查文件内容
adb pull /data/local/tmp/test.txt ./
cat test.txt | head -20
```

### 问题 5："Permission denied" 或 "root required"

**原因**：
- 没有 root 权限
- sendevent 需要 root 权限

**解决方案**：
```bash
# 确认 root 权限
adb shell su -c "id"
# 应该显示 uid=0 (root) gid=0 (root)

# 使用 su -c 运行脚本
adb shell su -c "/data/local/tmp/replay_gesture.sh /dev/input/event1 1"

# 或在脚本中添加 su
cat > /data/local/tmp/replay_with_su.sh << 'EOF'
#!/bin/bash
su -c "/data/local/tmp/replay_gesture.sh /dev/input/event1 1"
EOF
```

### 问题 6：回放坐标不正确

**原因**：
- 录制和回放时屏幕方向不同
- 屏幕分辨率改变
- 不同 Android 版本的坐标系统差异

**解决方案**：
```bash
# 查看屏幕分辨率
adb shell wm size

# 确保录制和回放时分辨率相同
# 如需适配多分辨率，可在脚本中添加转换

# 手动调整坐标
python3 tools/gesture_editor.py replay_gesture.sh
# 选择修改坐标选项
```

### 问题 7：多点触控不工作

**原因**：
- 设备不支持多点触控
- event 设备类型不对
- sendevent 不支持多点

**排查步骤**：
```bash
# 查看设备是否支持多点
adb shell cat /proc/bus/input/devices | grep -i "ABS_MT"

# 查看最大触控点数
adb shell grep -r "BTN_TOUCH" /proc/bus/input/

# 手动测试两点触控
adb shell su -c "
sendevent /dev/input/event1 3 57 0     # 触点 1 ID
sendevent /dev/input/event1 3 53 100   # 触点 1 X
sendevent /dev/input/event1 3 54 100   # 触点 1 Y
sendevent /dev/input/event1 0 0 0      # 同步

sendevent /dev/input/event1 3 57 1     # 触点 2 ID
sendevent /dev/input/event1 3 53 500   # 触点 2 X
sendevent /dev/input/event1 3 54 500   # 触点 2 Y
sendevent /dev/input/event1 0 0 0      # 同步
"
```

## 调试技巧

### 启用调试输出

```bash
# 使用 bash -x 查看脚本执行过程
adb shell bash -x /data/local/tmp/replay_gesture.sh 2>&1 | tee debug.log

# 或在脚本中添加 set -x
echo 'set -x' | cat - /data/local/tmp/replay_gesture.sh > temp && mv temp /data/local/tmp/replay_gesture.sh
```

### 实时监控事件

```bash
# 启动事件监控
python3 tools/event_monitor.py /dev/input/event1

# 在手机上进行操作，观察输出
```

### 逐步调试脚本

```bash
# 运行脚本的前几行
adb shell su -c "sendevent /dev/input/event1 3 57 0"
adb shell su -c "sendevent /dev/input/event1 3 53 540"
adb shell su -c "sendevent /dev/input/event1 3 54 960"
adb shell su -c "sendevent /dev/input/event1 0 0 0"

# 观察手机屏幕是否有反应
```

## 性能优化

### 降低脚本延迟

```bash
# 编辑脚本，减小 sleep 命令的值
# 从 sleep 0.5 改为 sleep 0.1
sed -i 's/sleep 0\.5/sleep 0.1/g' /data/local/tmp/replay_gesture.sh
```

### 增加脚本执行速度

```bash
# 使用 Python 工具生成脚本时指定加速因子
python3 tools/convert_to_script.py gesture_raw.txt replay_fast.sh /dev/input/event1
# (需要修改工具以支持加速因子)
```

## 获取更多帮助

1. 查看 [使用教程](USAGE.md)
2. 查看 [事件格式说明](EVENT_FORMAT.md)
3. 在 GitHub 提交 Issue
4. 查看原始的 getevent/sendevent 文档
   ```bash
   adb shell getevent -h
   adb shell sendevent -h
   ```
