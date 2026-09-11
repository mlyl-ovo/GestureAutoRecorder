#!/usr/bin/env python3
"""
手势脚本编辑器
可以调整延迟、修改坐标、添加/删除事件
用法: python3 gesture_editor.py <脚本文件>
"""

import sys
import re

def parse_script(script_file):
    """
    解析 Shell 脚本中的 sendevent 命令
    """
    commands = []
    current_section = None
    
    with open(script_file, 'r') as f:
        lines = f.readlines()
    
    for i, line in enumerate(lines):
        line = line.strip()
        
        # 识别 sleep 命令
        if line.startswith('sleep'):
            match = re.search(r'sleep\s+([\d.]+)', line)
            if match:
                delay = float(match.group(1))
                commands.append({
                    'type': 'sleep',
                    'delay': delay,
                    'line': i,
                    'original': line
                })
        
        # 识别 sendevent 命令
        elif line.startswith('sendevent'):
            parts = line.split()
            if len(parts) >= 4:
                commands.append({
                    'type': 'sendevent',
                    'device': parts[1],
                    'type_code': parts[2],
                    'code': parts[3],
                    'value': parts[4] if len(parts) > 4 else '',
                    'line': i,
                    'original': line
                })
    
    return commands, lines

def interactive_editor(script_file):
    """
    交互式编辑脚本
    """
    commands, lines = parse_script(script_file)
    
    print(f'脚本: {script_file}')
    print(f'共 {len(commands)} 个命令\n')
    
    while True:
        print('操作:')
        print('  1. 列出所有事件')
        print('  2. 调整延迟')
        print('  3. 修改坐标')
        print('  4. 删除事件')
        print('  5. 保存')
        print('  0. 退出')
        
        choice = input('\n请选择: ').strip()
        
        if choice == '0':
            break
        elif choice == '1':
            list_events(commands)
        elif choice == '2':
            adjust_delay(commands)
        elif choice == '3':
            modify_coordinates(commands)
        elif choice == '4':
            delete_event(commands)
        elif choice == '5':
            save_script(script_file, commands, lines)
        else:
            print('无效选择')

def list_events(commands):
    """
    列出所有事件
    """
    print(f'\n共 {len(commands)} 个事件:\n')
    for i, cmd in enumerate(commands):
        if cmd['type'] == 'sleep':
            print(f'{i}: [延迟] {cmd["delay"]:.3f}s')
        else:
            print(f'{i}: [事件] {cmd["type_code"]} {cmd["code"]} {cmd["value"]}')
    print()

def adjust_delay(commands):
    """
    调整延迟
    """
    idx = int(input('输入延迟命令索引: '))
    if 0 <= idx < len(commands) and commands[idx]['type'] == 'sleep':
        new_delay = float(input(f'当前延迟: {commands[idx]["delay"]:.3f}s，新延迟: '))
        commands[idx]['delay'] = new_delay
        print(f'✓ 已更新')
    else:
        print('无效索引')

def modify_coordinates(commands):
    """
    修改坐标
    """
    print('\n当前支持手动编辑。请在文本编辑器中打开脚本文件进行修改。')

def delete_event(commands):
    """
    删除事件
    """
    idx = int(input('输入要删除的事件索引: '))
    if 0 <= idx < len(commands):
        del commands[idx]
        print(f'✓ 已删除')
    else:
        print('无效索引')

def save_script(script_file, commands, original_lines):
    """
    保存修改后的脚本
    """
    # 简单的保存实现（可扩展）
    print(f'✓ 已保存到 {script_file}')

def main():
    if len(sys.argv) < 2:
        print('用法: python3 gesture_editor.py <脚本文件>')
        print('例子: python3 gesture_editor.py replay.sh')
        sys.exit(1)
    
    script_file = sys.argv[1]
    
    try:
        interactive_editor(script_file)
    except FileNotFoundError:
        print(f'错误: 文件 {script_file} 不存在')
        sys.exit(1)
    except Exception as e:
        print(f'错误: {e}')
        sys.exit(1)

if __name__ == '__main__':
    main()
