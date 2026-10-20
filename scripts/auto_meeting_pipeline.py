# -*- coding: utf-8 -*-
"""
端到端自动例会流水线调度器
整合：录音 -> 无损切片 -> 格式化数据 -> 回填标准 Excel
"""

import os
import sys
import argparse
from audio_cutter import cut_audio
from audio_recorder import record_audio
from fill_excel_minutes import fill_minutes_excel

def run_pipeline(audio_path=None, record_duration=None, excel_template=None, segment_time=120):
    print("=" * 60)
    print(" [AutoMeeting] 智能会议自动化全流程调度开始")
    print("=" * 60)
    
    # 阶段 1: 录音 / 获取音频
    if not audio_path:
        audio_path = "会议录音_auto.mp3"
        print(f"[阶段 1/3] 启动实时录音 (预计录制: {record_duration or '手动中断'} 秒)...")
        record_audio(audio_path, duration=record_duration)
    else:
        print(f"[阶段 1/3] 使用已有音频文件: {audio_path}")
        
    # 阶段 2: 快速分段切片
    print(f"\n[阶段 2/3] 执行音频无损分片切片 (每段 {segment_time} 秒)...")
    segments = cut_audio(audio_path, segment_time=segment_time)
    print(f"[AutoMeeting] 切片完成，已就绪供大模型转录识别: 共 {len(segments)} 段。")
    
    # 阶段 3: 检查 Excel 模板
    if excel_template and os.path.isfile(excel_template):
        print(f"\n[阶段 3/3] 目标纪要模板已定位: {excel_template}")
        print("[AutoMeeting] 提示: 切片已就绪，AI Agent 可依次读取切片并提取待办项调用 fill_excel_minutes.py 完成最终回填。")
    else:
        print("\n[阶段 3/3] 未指定模板或仅需音频处理，切片流水线已圆满完成。")
        
    print("=" * 60)
    print(" [AutoMeeting] 流程处理完毕！")
    print("=" * 60)

def main():
    parser = argparse.ArgumentParser(description="AutoMeeting 端到端会议自动化流水线")
    parser.add_argument("-a", "--audio", default=None, help="已有会议录音文件路径")
    parser.add_argument("-r", "--record", type=int, default=None, help="录音时长（秒），若不提供已有音频则以此参数开启录制")
    parser.add_argument("-t", "--segment-time", type=int, default=120, help="切片长度（默认 120 秒）")
    parser.add_argument("-x", "--excel", default=None, help="目标 Excel 纪要模板路径")
    
    args = parser.parse_args()
    try:
        run_pipeline(
            audio_path=args.audio,
            record_duration=args.record,
            excel_template=args.excel,
            segment_time=args.segment_time
        )
    except Exception as e:
        print(f"执行出错: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
