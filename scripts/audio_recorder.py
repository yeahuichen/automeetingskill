# -*- coding: utf-8 -*-
"""
本地会议录音工具
利用本地 FFmpeg 调用 DirectShow 音频输入设备，支持定时录制或手动停止。
"""

import os
import sys
import argparse
import subprocess
from audio_cutter import find_ffmpeg

def list_audio_devices():
    ffmpeg_exe = find_ffmpeg()
    cmd = [ffmpeg_exe, "-list_devices", "true", "-f", "dshow", "-i", "dummy"]
    res = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, encoding="utf-8", errors="ignore")
    output = res.stderr
    
    devices = []
    capture = False
    for line in output.splitlines():
        if "DirectShow audio devices" in line:
            capture = True
            continue
        if "DirectShow video devices" in line:
            capture = False
        if capture and "]" in line and '"' in line:
            parts = line.split('"')
            if len(parts) >= 2:
                dev_name = parts[1]
                if dev_name not in devices and not dev_name.startswith("@"):
                    devices.append(dev_name)
    return devices

def record_audio(output_file, duration=None, device_name=None):
    ffmpeg_exe = find_ffmpeg()
    
    devices = list_audio_devices()
    if not devices:
        print("[AutoMeeting] 警告: 未检测到 DirectShow 音频设备，尝试使用默认音频设备...")
        device_arg = "audio=virtual-audio-capturer"
    else:
        selected_dev = device_name if device_name else devices[0]
        print(f"[AutoMeeting] 使用音频输入设备: {selected_dev}")
        device_arg = f"audio={selected_dev}"
        
    os.makedirs(os.path.dirname(os.path.abspath(output_file)), exist_ok=True)
    
    cmd = [
        ffmpeg_exe,
        "-y",
        "-f", "dshow",
        "-i", device_arg,
        "-acodec", "libmp3lame",
        "-ab", "128k"
    ]
    
    if duration:
        cmd.extend(["-t", str(duration)])
        
    cmd.append(output_file)
    
    print(f"[AutoMeeting] 开始录音...")
    if duration:
        print(f"[AutoMeeting] 录音预定时长: {duration} 秒 (~{duration // 60} 分钟)")
    else:
        print(f"[AutoMeeting] 持续录音中，按 Ctrl+C 可停止录音...")
        
    print(f"[AutoMeeting] 输出文件: {output_file}")
    
    try:
        subprocess.run(cmd, check=True)
        print(f"[AutoMeeting] 录音完成并成功保存至: {output_file}")
    except KeyboardInterrupt:
        print(f"\n[AutoMeeting] 用户手动停止录音，文件已保存至: {output_file}")
    except subprocess.CalledProcessError as e:
        print(f"[AutoMeeting] 录音过程中断或出错: {e}", file=sys.stderr)

def main():
    parser = argparse.ArgumentParser(description="会议录音自动化工具")
    parser.add_argument("-o", "--output", default="会议录音.mp3", help="录音保存路径 (默认: 会议录音.mp3)")
    parser.add_argument("-t", "--duration", type=int, default=None, help="录音时长（秒），不填则持续录制至手动中断")
    parser.add_argument("-d", "--device", default=None, help="指定麦克风设备名称，不填则自动使用第一个设备")
    parser.add_argument("--list-devices", action="store_true", help="列出当前系统所有可用的音频输入设备")
    
    args = parser.parse_args()
    
    if args.list_devices:
        devices = list_audio_devices()
        print("当前系统检测到的音频输入设备:")
        for idx, dev in enumerate(devices, 1):
            print(f"  [{idx}] {dev}")
        return
        
    record_audio(args.output, args.duration, args.device)

if __name__ == "__main__":
    main()
