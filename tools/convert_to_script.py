#!/usr/bin/env python3
"""
将录制的原始手势数据转换为可执行的 Shell 脚本
用法: python3 convert_to_script.py <输入文件> <输出脚本>
例子: python3 convert_to_script.py gesture_raw.txt replay.sh
"""

import sys
import re
from collections import defaultdict

def parse_gesture_data(input_file):
    """
    解析 getevent 输出的原始数据
    返回: (事件列表, 总时长)
    """
    events = []
    prev_time = 0
    
    with open(input_file, 'r') as f:
        for line in f:
            line = line.strip()
            # 跳过注释行和空行
            if not line or line.startswith('#'):
                continue
            
            parts = line.split()
            if len(parts) >= 4:
                try:
                    timestamp = int(parts[0])  # 毫秒
                    event_type = parts[1]
                    code = parts[2]
                    value = parts[3]
                    
                    # 计算延迟
                    delay = timestamp - prev_time
                    prev_time = timestamp
                    
                    events.append({
                        'time': timestamp,
                        'delay': delay,
                        'type': event_type,
                        'code': code,
                        'value': value
                    })
                except ValueError:
                    continue
    
    total_duration = prev_time / 1000.0  # 转换为秒
    return events, total_duration

def generate_shell_script(events, total_duration, output_file, event_device='/dev/input/event1'):
    """
    生成可执行的 Shell 脚本
    """
    with open(output_file, 'w') as f:
        # 写入脚本头
        f.write('#!/bin/bash\n')
        f.write(f'# Gesture Replay Script\n')
        f.write(f'# Auto-generated replay script\n')
        f.write(f'# Event device: {event_device}\n')
        f.write(f'# Total duration: {total_duration:.2f}s\n')
        f.write(f'# Total events: {len(events)}\n')
        f.write(f'\n')
        f.write(f'DEVICE="${{1:-{event_device}}}"\n')
        f.write(f'LOOP="${{2:-1}}"\n')
        f.write(f'\n')
        f.write(f'if [ ! -c "$DEVICE" ]; then\n')
        f.write(f'    echo "Error: $DEVICE not found"\n')
        f.write(f'    exit 1\n')
        f.write(f'fi\n')
        f.write(f'\n')
        f.write(f'for ((i=1; i<=LOOP; i++)); do\n')
        f.write(f'    echo "Playing loop $i/$LOOP"\n')
        f.write(f'\n')
        
        # 写入事件
        prev_delay = 0
        for event in events:
            delay_sec = event['delay'] / 1000.0
            
            # 如果延迟大于 10ms，添加 sleep 命令
            if delay_sec > 0.01:
                f.write(f'    sleep {delay_sec:.3f}  # {event["delay"]}ms\n')
            
            # 写入 sendevent 命令
            f.write(f'    sendevent $DEVICE {event["type"]} {event["code"]} {event["value"]}\n')
        
        f.write(f'\n')
        f.write(f'    if [ $i -lt $LOOP ]; then\n')
        f.write(f'        echo "Waiting before next loop..."\n')
        f.write(f'        sleep 2\n')
        f.write(f'    fi\n')
        f.write(f'done\n')
        f.write(f'\n')
        f.write(f'echo "Replay complete!"\n')
    
    # 给脚本执行权限
    import os
    os.chmod(output_file, 0o755)
    print(f'✓ 脚本已生成: {output_file}')
    print(f'  事件数: {len(events)}')
    print(f'  总时长: {total_duration:.2f}s')
    print(f'  设备: {event_device}')

def main():
    if len(sys.argv) < 3:
        print('用法: python3 convert_to_script.py <输入文件> <输出脚本> [event_device]')
        print('例子: python3 convert_to_script.py gesture_raw.txt replay.sh /dev/input/event1')
        sys.exit(1)
    
    input_file = sys.argv[1]
    output_file = sys.argv[2]
    event_device = sys.argv[3] if len(sys.argv) > 3 else '/dev/input/event1'
    
    try:
        print(f'正在解析: {input_file}...')
        events, total_duration = parse_gesture_data(input_file)
        
        if not events:
            print('错误: 没有找到有效的事件数据')
            sys.exit(1)
        
        print(f'找到 {len(events)} 个事件')
        print(f'正在生成脚本...')
        generate_shell_script(events, total_duration, output_file, event_device)
        print('\n完成！')
        print(f'下一步: adb push {output_file} /data/local/tmp/')
        
    except FileNotFoundError:
        print(f'错误: 文件 {input_file} 不存在')
        sys.exit(1)
    except Exception as e:
        print(f'错误: {e}')
        sys.exit(1)

if __name__ == '__main__':
    main()
