#!/usr/bin/env python3
"""
实时监控 Android 触控事件
用法: python3 event_monitor.py [event_device]
例子: python3 event_monitor.py /dev/input/event1
"""

import subprocess
import sys
import re

def monitor_events(event_device='/dev/input/event1'):
    """
    实时显示触控事件
    """
    print(f'监控设备: {event_device}')
    print('按 Ctrl+C 停止监控')
    print('\n事件格式: [DEVICE] [TYPE] [CODE] [VALUE]')
    print('=' * 60)
    
    cmd = f'adb shell getevent -l {event_device}'
    
    try:
        process = subprocess.Popen(
            cmd,
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            universal_newlines=True,
            bufsize=1
        )
        
        event_count = 0
        touch_down = False
        
        for line in process.stdout:
            line = line.strip()
            if not line:
                continue
            
            # 解析事件
            if 'BTN_TOUCH' in line and 'DOWN' in line:
                touch_down = True
                print(f'\n✓ 触摸开始')
            elif 'BTN_TOUCH' in line and 'UP' in line:
                touch_down = False
                print(f'✓ 触摸结束\n')
            elif 'ABS_MT_POSITION_X' in line:
                # 提取 X 坐标
                match = re.search(r'(\d+)', line)
                if match:
                    x = match.group(1)
                    print(f'  X: {x}', end=' ')
            elif 'ABS_MT_POSITION_Y' in line:
                # 提取 Y 坐标
                match = re.search(r'(\d+)', line)
                if match:
                    y = match.group(1)
                    print(f'Y: {y}')
            else:
                print(f'{line}')
            
            event_count += 1
        
    except KeyboardInterrupt:
        print('\n\n监控已停止')
        process.terminate()
    except Exception as e:
        print(f'错误: {e}')
        sys.exit(1)

def main():
    if len(sys.argv) > 1:
        if sys.argv[1] in ['-h', '--help']:
            print('用法: python3 event_monitor.py [event_device]')
            print('例子:')
            print('  python3 event_monitor.py /dev/input/event0')
            print('  python3 event_monitor.py /dev/input/event1')
            sys.exit(0)
        event_device = sys.argv[1]
    else:
        event_device = '/dev/input/event1'
    
    monitor_events(event_device)

if __name__ == '__main__':
    main()
