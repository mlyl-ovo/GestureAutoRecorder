# 详细安装指南

## 前置要求

### 1. Android 手机环境
- **系统版本**: Android 13 或更高
- **Root 状态**: 已 root（推荐使用 Magisk）
- **连接方式**: USB 连接到电脑，ADB 可用

### 2. PC 环境
- **ADB**: Android Debug Bridge
- **Python 3**: 用于脚本转换工具
- **Shell 环境**: Bash 或其他 Shell

## 步骤 1：配置 ADB

### Linux / macOS

```bash
# 安装 ADB
# macOS
brew install android-platform-tools

# Linux (Ubuntu/Debian)
sudo apt-get install android-tools-adb

# 验证安装
adb version
```

### Windows

1. 下载 Android SDK Platform Tools: https://developer.android.com/studio/releases/platform-tools
2. 解压到任意文件夹
3. 将文件夹路径加入系统环境变量 `PATH`
4. 打开 CMD 验证:
   ```cmd
   adb version
   ```

## 步骤 2：启用手机的开发者选项

1. 打开 **设置** → **关于手机**
2. 连续点击 **Build 版本号** 7 次
3. 返回设置，找到 **开发者选项**
4. 启用 **USB 调试**
5. 启用 **USB 调试（安全设置）**（如果有）

## 步骤 3：连接手机到 ADB

```bash
# 用 USB 连接手机到电脑
# 手机会弹出"允许 USB 调试"的对话框，点击"允许"

# 验证连接
adb devices

# 输出类似于:
# List of attached devices
# xxxxxxxxxxxxxxxx    device
```

如果看到 `device`，说明连接成功。

## 步骤 4：Root 权限设置（Magisk 示例）

### 检查 Root 状态

```bash
adb shell su -c "whoami"
# 如果返回 root，说明已获得 root 权限
```

### 使用 Magisk Root（Android 13+）

1. 下载 Magisk 应用: https://github.com/topjohnwu/Magisk/releases
2. 从恢复模式或启动模式安装（具体步骤因设备而异）
3. 重启手机
4. 打开 Magisk 应用，确认已获得 root 权限

## 步骤 5：验证环境

```bash
# 检查 ADB 连接
adb shell echo "ADB OK"

# 检查 Root 权限
adb shell su -c "id"

# 检查 getevent 和 sendevent 命令是否可用
adb shell which getevent
adb shell which sendevent

# 查找触控设备
adb shell cat /proc/bus/input/devices | grep -i touch
```

如果上述命令都能正常执行，环境配置完成！

## 常见问题

### Q: ADB 无法识别设备
**A**: 
- 确认 USB 调试已启用
- 尝试 `adb kill-server` 后重新连接
- 更新 ADB: `adb version`
- 在手机上重新授予调试权限

### Q: Root 权限无法获取
**A**:
- 确认已安装 Magisk 或其他 Root 工具
- 使用 `adb shell su` 测试权限
- 某些品牌手机（如三星）可能需要特殊处理

### Q: getevent/sendevent 命令不存在
**A**:
- 这两个工具通常预装在 Android 中
- 如果缺失，可以从其他设备提取或使用替代工具
- 确保使用 root 用户运行脚本

## 下一步

配置完成后，查看 [使用教程](USAGE.md) 了解如何录制和回放手势。
