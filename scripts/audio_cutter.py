# -*- coding: utf-8 -*-
"""
音频快速无损分段切片工具
使用 FFmpeg 流拷贝（-c copy）秒级完成音频分片，音质零损耗。
"""

import os
import sys
import shutil
import argparse
import subprocess

KNOWN_FFMPEG_PATHS = [
    r"C:\Users\yeahu\Downloads\OneVideoCutter\bin\ffmpeg.exe",
    r"C:\Users\yeahu\Downloads\ffmpeg-master-latest-win64-gpl-shared\bin\ffmpeg.exe",
]

def find_ffmpeg():
    # 1. 检查环境变量 PATH
    ffmpeg_bin = shutil.which("ffmpeg")
    if ffmpeg_bin:
        return ffmpeg_bin
    
    # 2. 检查常见已安装路径
    for path in KNOWN_FFMPEG_PATHS:
        if os.path.isfile(path):
            return path
            
    # 3. 常见系统默认目录
    common_roots = [r"C:\Program Files\ffmpeg\bin\ffmpeg.exe", r"C:\ffmpeg\bin\ffmpeg.exe"]
    for path in common_roots:
        if os.path.isfile(path):
            return path
            
    raise FileNotFoundError("未在系统或已知路径中找到 ffmpeg.exe，请确认已安装或将其加入 PATH。")

def cut_audio(input_file, segment_time=120, output_dir=None):
    ffmpeg_exe = find_ffmpeg()
    
    input_file = os.path.abspath(input_file)
    if not os.path.isfile(input_file):
        raise FileNotFoundError(f"输入音频文件不存在: {input_file}")
        
    base_name = os.path.splitext(os.path.basename(input_file))[0]
    ext = os.path.splitext(input_file)[1]
    
    if not output_dir:
        output_dir = os.path.join(os.path.dirname(input_file), f"{base_name}_切片")
        
    os.makedirs(output_dir, exist_ok=True)
    
    output_pattern = os.path.join(output_dir, f"{base_name}_%02d{ext}")
    
    cmd = [
        ffmpeg_exe,
        "-y",
        "-i", input_file,
        "-f", "segment",
        "-segment_time", str(segment_time),
        "-c", "copy",
        output_pattern
    ]
    
    print(f"[AutoMeeting] 正在调用 FFmpeg 进行无损切片 (每 {segment_time} 秒一段)...")
    print(f"[AutoMeeting] 命令: {' '.join(cmd)}")
    
    res = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, encoding="utf-8", errors="ignore")
    if res.returncode != 0:
        raise RuntimeError(f"FFmpeg 切片失败: {res.stderr}")
        
    segments = sorted([
        os.path.join(output_dir, f) for f in os.listdir(output_dir)
        if f.startswith(f"{base_name}_") and f.endswith(ext)
    ])
    
    print(f"[AutoMeeting] 切片完成！共生成 {len(segments)} 个音频片段。")
    print(f"[AutoMeeting] 输出目录: {output_dir}")
    return segments

def main():
    parser = argparse.ArgumentParser(description="音频自动无损分片切片工具")
    parser.add_argument("-i", "--input", required=True, help="输入音频文件路径 (MP3/M4A/WAV 等)")
    parser.add_argument("-t", "--segment-time", type=int, default=120, help="每段切片时长（秒），默认 120 秒")
    parser.add_argument("-o", "--output-dir", default=None, help="输出切片目录，默认在音频同级创建目录")
    
    args = parser.parse_args()
    try:
        segments = cut_audio(args.input, args.segment_time, args.output_dir)
        for s in segments:
            print(f"  - {os.path.basename(s)} ({os.path.getsize(s) // 1024} KB)")
    except Exception as e:
        print(f"错误: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
