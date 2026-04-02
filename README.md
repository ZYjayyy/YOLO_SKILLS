# Skill_yolo

YOLOv8 自定义目标检测数据集工作流工具包，覆盖从视频抽帧到训练、验证、导出的完整流程。

## 功能概览

- 视频抽帧：按目标数量从视频均匀采样，生成 `images/train` 与 `images/val`。
- 数据重组：按前缀将 `train/val` 数据重新分配。
- 数据校验：检查图片与标签一一对应、标签格式与数值范围。
- 训练参考：提供 `data.yaml` 模板、目录模板、训练参数与常用命令。

## 目录结构

```text
Skill_yolo/
├── SKILL.md
├── README.md
├── assets/
│   ├── data.yaml.template
│   └── dataset_structure.template
├── references/
│   ├── data_yaml.md
│   ├── dataset_format.md
│   ├── training_params.md
│   └── yolo_commands.md
└── scripts/
    ├── extract_frames.py
    ├── reorganize.py
    └── verify_dataset.py
```

## 环境要求

- Python 3.9+
- OpenCV（抽帧脚本需要）
- Ultralytics YOLOv8（训练/验证/导出需要）

安装依赖：

```bash
pip install opencv-python ultralytics
```

## 快速开始

### 1) 准备数据目录

按模板创建标准目录（参考 `assets/dataset_structure.template`）：

```text
dataset/
├── images/
│   ├── train/
│   └── val/
└── labels/
    ├── train/
    └── val/
```

### 2) 视频抽帧

编辑 `scripts/extract_frames.py` 中的配置项：

- `ROOT_DIR`：数据集图片根目录（通常是 `.../dataset/images`）
- `videos`：每个视频的 `path/prefix/target/count`

运行：

```bash
python scripts/extract_frames.py
```

脚本会：

- 先清空目标目录
- 按间隔均匀抽帧
- 输出实时进度条
- 生成命名格式为 `{prefix}_{序号:05d}.jpg` 的图片

### 3) 重组 train/val（可选）

编辑 `scripts/reorganize.py` 中：

- `TRAIN_DIR`、`VAL_DIR`
- `VAL_PER_PREFIX`（每个前缀抽多少张进 `val`）

运行：

```bash
python scripts/reorganize.py
```

### 4) 标注

用 X-Anylabeling 或 Labelme 导出 YOLO TXT 标签，保证：

- 标签文件与图片同名
- 标签放入 `labels/train` 与 `labels/val`
- 每行格式：`class_id x_center y_center width height`
- 坐标均为 0~1 归一化值

### 5) 校验数据集

编辑 `scripts/verify_dataset.py` 中：

- `DATASET_ROOT`
- `EXPECTED_CLASSES`

运行：

```bash
python scripts/verify_dataset.py
```

### 6) 训练模型

先基于 `assets/data.yaml.template` 生成你的 `data.yaml`，再执行：

```bash
yolo detect train data=data.yaml model=yolov8n.pt epochs=100 imgsz=640 device=0
```

常用命令见 `references/yolo_commands.md`。

### 7) 验证与导出

验证：

```bash
yolo detect val data=data.yaml model=runs/detect/train/weights/best.pt
```

导出 ONNX：

```bash
yolo export model=runs/detect/train/weights/best.pt format=onnx
```

## 脚本说明

### scripts/extract_frames.py

用途：从视频均匀抽取指定数量帧到 `images/train` 或 `images/val`。

关键点：

- 自动清空输出目录
- 按 `interval = max(1, total_frames // count)` 采样
- 进度条显示当前抽帧进度

### scripts/reorganize.py

用途：将 `val` 合并回 `train` 后，按前缀重新抽样到 `val`。

适用：重新定义训练集/验证集比例时。

### scripts/verify_dataset.py

用途：做完整性检查与格式检查。

检查项包括：

- train/val 图片数量与按前缀统计
- 图片与标签是否一一对应
- 标签列数是否为 5
- `class_id` 是否越界
- 坐标是否在 `[0, 1]`

## 推荐工作流

1. 抽帧
2. 重组（可选）
3. 标注
4. 校验
5. 训练
6. 验证
7. 导出/部署

## 参考文档

- `references/data_yaml.md`：`data.yaml` 字段详解
- `references/dataset_format.md`：目录与标签格式规范
- `references/training_params.md`：训练参数建议
- `references/yolo_commands.md`：YOLO 命令速查

## 注意事项

- 建议前缀统一英文，避免空格与特殊字符。
- 每次重新抽帧前应清空目标目录，避免旧数据混入。
- `nc` 与 `names` 必须与实际标注类别严格一致。
- Windows 路径建议使用 `/`，减少转义问题。
