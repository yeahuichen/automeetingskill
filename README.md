# AutoMeeting 自动化会议纪要技能使用说明书

`.automeetingskill` 是专为**软件研发部产品周例会**定制的端到端会议纪要全自动工作流工具包。通过结合本地 FFmpeg 音频处理、多模态大模型转录、信息结构化提取以及 OpenPyXL 电子表格引擎，实现从“会议音频”到“官方标准 Excel 纪要”的秒级全自动交付。

---

## 一、 目录结构一览

```text
c:\job-project\会议纪要\.automeetingskill\
├── SKILL.md                          # Antigravity AI Agent 专用技能定义与行为规范
├── README.md                         # 本使用说明文档
├── scripts/                          # 核心自动化执行脚本库
│   ├── audio_cutter.py               # FFmpeg 无损音频分片切片工具（-c copy 秒级切片）
│   ├── audio_recorder.py             # 本地麦克风录音工具（DirectShow 音频捕获）
│   ├── fill_excel_minutes.py         # 官方 Excel 纪要模板安全无损回填工具
│   └── auto_meeting_pipeline.py      # 端到端全流程一键调度流水线
└── templates/                        # 官方标准模板库
    └── 软件研发部产品周例会会议纪要（标准空白模板）.xlsx
```

---

## 二、 两种使用方式

### 方式一：直接与 AI Agent 对话交互（推荐，无需手动敲命令）

日常使用中，您无需手动运行脚本，直接在聊天窗口对 AI Agent 发出自然语言指令即可触发：

#### 场景 1：处理已有例会录音文件

> **用户**：“请处理当前目录下的 `2026年10月19日 15点07分.mp3`，切片转录并填入本周的 Excel 纪要表中。”
> 
> **Agent 行为**：
> 
> 1. 自动调用 `audio_cutter.py` 完成无损切片；
> 2. 依次读取音频切片，转写并标记各发言人（园园、业辉、程鹏、冠星、海玲、达文、芮迪）；
> 3. 提炼各组员工作汇报、会议决议及待办事项；
> 4. 自动调用 `fill_excel_minutes.py` 写入目标 Excel 表格，交付最终文件。

#### 场景 2：让 Agent 自动录制会议

> **用户**：“帮我录制接下来 45 分钟的例会，并在录制结束后自动生成会议纪要和 Excel。”
> 
> **Agent 行为**：
> 
> 1. 自动后台唤起 `audio_recorder.py` 进行麦克风静默录制；
> 2. 定时结束或手动停止后，自动切片并生成纪要。

#### 场景 3：根据已有的决议文本补充回填待办项

> **用户**：“以当前 Excel 表中的会议决议为准，帮我提取所有待办项并填好表格。”
> 
> **Agent 行为**：
> 
> 1. 读取 Excel 中 A11 单元格的决议文本；
> 2. 结构化提炼待办事项（序号、待办项、提出人、责任人、预计关闭时间、备注）；
> 3. 不编造任何未知信息，规范回填并格式化保存。

---

### 方式二：通过命令行（CLI）独立运行脚本

如果您希望脱离聊天窗口独立在终端批处理，可以使用 Python 命令行运行：

#### 1. 快速无损音频切片

```powershell
python .automeetingskill/scripts/audio_cutter.py -i "2026年10月19日 15点07分.mp3" -t 120
```

- `-i / --input`：音频文件路径
- `-t / --segment-time`：每段切片时长（单位：秒，默认 120 秒）
- 切片文件将自动生成于 `[文件名]_切片/` 目录下。

#### 2. 本地麦克风录音

```powershell
# 查看所有音频录制设备
python .automeetingskill/scripts/audio_recorder.py --list-devices

# 录制 3600 秒（1小时）音频
python .automeetingskill/scripts/audio_recorder.py -o "今日例会.mp3" -t 3600
```

#### 3. 将待办项 JSON 回填至标准 Excel 模板

```powershell
python .automeetingskill/scripts/fill_excel_minutes.py -x "软件研发部产品周例会会议纪要（2026.10.20）.xlsx" -d "tasks.json"
```

#### 4. 一键端到端流水线

```powershell
python .automeetingskill/scripts/auto_meeting_pipeline.py -a "2026年10月19日 15点07分.mp3" -x "软件研发部产品周例会会议纪要（2026.10.20）.xlsx"
```

---

## 三、 Excel 模板填报规范与技术保障

回填工具严格遵循贵司《软件研发部产品周例会会议纪要》模板格式要求，具备以下防护特性：

1. **结构完整性保障**：绝不改动第 1~14 行的固有排版、元数据表头与单元格合并关系。
2. **合并单元格兼容**：待办事项的“待办项/未决事宜”列自动按行执行 `B:C` 列合并。
3. **边框与字体一致**：
   - 表格外框自动施加中粗线（`medium`），内部单元格施加细线（`thin`）；
   - 字体统一为原版 `微软雅黑 10pt`；
   - 序号、提出人、责任人、关闭时间居中对齐，待办事项与备注左对齐并开启自动换行。
4. **真实性原则**：凡决议中未明确提及提出人、预计关闭时间或无额外说明的字段，程序严格保持留空，绝不臆造。

---

## 四、 环境依赖

- **Python**：3.8+（当前运行环境为 Python 3.10）
- **依赖库**：`openpyxl`（处理 Excel）
- **多媒体组件**：`ffmpeg.exe`（脚本内置多路径自动探测机制，无需额外配置环境变量）
