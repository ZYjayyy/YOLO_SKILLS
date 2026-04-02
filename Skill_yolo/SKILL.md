---
name: skill-yolo
description: YOLOv8 图像数据集制作完整工作流：视频抽帧、train/val 划分、目录重组、标注、模型训练、验证与部署。适用于使用 ecar/yolo 风格项目结构训练自定义目标检测模型时使用。
---

# Skill_yolo — YOLOv8 自定义数据集制作工作流

## 职责定位

本 Skill 覆盖从原始视频到 YOLOv8 可训练数据集的完整流程，包括：抽帧、目录重组、标注准备、模型训练与验证。

---

## 触发场景

用户提及以下任意关键词时激活本 Skill：
- YOLO、yolov8、yolov5、目标检测、目标识别
- 视频抽帧、抽帧、frame extraction
- train/val、数据集划分、数据集制作
- 标注、X-Anylabeling、labelme
- 模型训练、模型验证、模型导出
- ecar、data_test、dataset

---

## 核心流程

```
Step 1  →  视频抽帧（extract_frames）
Step 2  →  清理目标目录
Step 3  →  train/val 划分重组
Step 4  →  标注（X-Anylabeling / labelme）
Step 5  →  生成 data.yaml
Step 6  →  模型训练（yolo detect train）
Step 7  →  模型验证（yolo detect val）
Step 8  →  模型导出 / 推理
```

---

## Step 1 — 视频抽帧

### 视频配置规范

在 `scripts/extract_frames.py` 中定义视频列表数组，每个元素包含：

| 字段 | 类型 | 说明 |
|------|------|------|
| `path` | string | 视频绝对路径 |
| `prefix` | string | 输出文件名前缀（英文） |
| `target` | string | `"train"` 或 `"val"` |
| `count` | int | 目标抽取帧数 |

### 抽帧脚本标准

```
位置：{项目根}/extract_frames.py（临时脚本，执行后删除）
依赖：cv2（opencv-python）、pathlib
输出目录：dataset/images/{train|val}/
文件名格式：{prefix}_{序号:05d}.jpg
```

### 脚本要求

- 抽取前**清空目标目录**
- 计算采样间隔：`interval = max(1, total_frames // target_count)`
- 实时显示进度条（`\r` 覆盖打印，30 字符宽度）
- 终端实时输出每帧进度
- 完成后打印每个前缀的保存数量
- **执行后删除脚本文件**，不留残余

### 抽帧输出标准

```
✅ 完成：{prefix}: 共抽取 N 张图片到 images/{target}/
✅ 全部完成，共抽取 TOTAL 张图片
```

---

## Step 2 — 目录清理（每次抽帧前执行）

每次抽帧前必须清空目标目录，避免旧文件残留：

```python
for d in [train_dir, val_dir]:
    for f in d.glob("*"):
        if f.is_file():
            f.unlink()
```

---

## Step 3 — train/val 重组（可选）

当需要自定义划分比例时：

1. 移动 val 全部文件到 train（若重新划分）
2. 从 train 每个 prefix 取前 N 张（按文件名升序）复制到 val
3. 验证最终数量

> 重组方案需**先给用户确认**，获得同意后再执行。

---

## Step 4 — 标注

### X-Anylabeling 推荐配置

```
项目类型：image
标注格式：YOLO（txt，每类一行）
导出目录：dataset/labels/{train|val}/
```

### 标注流程

1. 在 X-Anylabeling 中新建项目
2. 导入 `dataset/images/` 目录
3. 导出时选择 **YOLO TXT** 格式
4. 将 `labels/` 对应放到 `images/` 同级的 `labels/` 目录

### 标注格式（YOLO TXT）

每行：`class_id x_center y_center width height`
- 坐标均为**归一化值**（0.0 ~ 1.0）
- 一个目标一行，多个目标多行
- 文件名与对应图片名一致（扩展名不同）

---

## Step 5 — data.yaml 模板

```yaml
path: {项目根}/ecar/yolo/dataset
train: images/train
val: images/val

nc: {类别数量}
names:
  0: {类别名1}
  1: {类别名2}
  2: {类别名3}
  3: {类别名4}
```

> 详细说明见 [references/data_yaml.md](references/data_yaml.md)

---

## Step 6 — 模型训练

### 标准训练命令

```bash
yolo detect train data={data_yaml路径} model={模型} epochs={轮数} imgsz={尺寸} device={设备}
```

### 推荐参数

| 参数 | 推荐值 | 说明 |
|------|--------|------|
| `model` | `yolov8n.pt` / `yolov8s.pt` | 优先用 n 测试流程，再换 s |
| `epochs` | 50~200 | 数据量少时用长一些 |
| `imgsz` | 640 | 默认 640 |
| `batch` | 16 | 显存不够则降 |
| `device` | `0`（GPU）或 `cpu` | 优先 GPU |
| `patience` | 20 | 早停轮数 |
| `project` | 自定义项目名 | 便于管理 |
| `name` | run 名称 | 便于管理 |

### 训练中终端输出

训练过程中会在终端显示：
- 当前 epoch 进度
- 损失指标（box_loss、cls_loss、dfI_loss）
- 验证指标（mAP50、mAP50-95）

---

## Step 7 — 模型验证

```bash
yolo detect val data={data_yaml路径} model={best_pt路径}
```

### 验证输出标准指标

```
Box(P):  Precision
Box(R):  Recall
mAP50:   mAP@IoU=0.50
mAP50-95: mAP@IoU=0.50:0.95（全范围）
```

---

## Step 8 — 模型导出与推理

### 导出

```bash
yolo export model={best_pt路径} format=onnx
```

### 推理

```bash
yolo detect predict model={best_pt路径} source={图片或视频路径}
```

---

## 目录结构标准

```
{项目根}/
├── ecar/yolo/
│   ├── data_test/          # 原始视频
│   │   ├── Anumber.mp4
│   │   ├── black.mp4
│   │   ├── blue.mp4
│   │   └── yellow.mp4
│   └── dataset/
│       ├── images/
│       │   ├── train/      # 训练图片
│       │   └── val/        # 验证图片
│       └── labels/
│           ├── train/     # 训练标签（标注后生成）
│           └── val/       # 验证标签（标注后生成）
├── extract_frames.py       # 临时抽帧脚本（执行后删除）
└── data.yaml               # 训练配置文件
```

---

## 输出标准

| 阶段 | 终端必须显示 | 说明 |
|------|-------------|------|
| 抽帧 | 进度条 + 每视频完成数 + 总数 | 实时刷新 |
| 重组 | 每步操作 + 最终统计 | 增减数量明确 |
| 训练 | epoch 进度 + 3大损失 + 2大mAP | 每 epoch 输出 |
| 验证 | Precision/Recall/mAP50/mAP50-95 | 最终汇总 |
| 导出 | 导出格式 + 文件路径 | 完成后提示 |

---

## 关键约束

1. **文件名前缀只用英文**，不混用中文
2. **每次抽帧前清空目录**，防止旧图残留
3. **脚本执行后删除**，不保留不必要的临时文件
4. **操作前先给方案**，用户确认后再执行
5. **所有对话开头喊"主人好"**
6. **使用专业终端进度条**（`\r` 覆盖打印，30 字符 `#` + `-`）
7. 标注文件与图片**一一对应**，缺一不可

---

## 参考文档

- [references/data_yaml.md](references/data_yaml.md) — data.yaml 完整字段说明
- [references/dataset_format.md](references/dataset_format.md) — YOLO 数据集目录结构与格式规范
- [references/training_params.md](references/training_params.md) — 训练参数详解与调优建议
- [references/yolo_commands.md](references/yolo_commands.md) — YOLOv8 常用命令速查

## 自动化脚本

- [scripts/extract_frames.py](scripts/extract_frames.py) — 视频抽帧（参数化模板）
- [scripts/reorganize.py](scripts/reorganize.py) — train/val 重组
- [scripts/verify_dataset.py](scripts/verify_dataset.py) — 数据集完整性校验

## 模板文件

- [assets/data.yaml.template](assets/data.yaml.template) — data.yaml 配置模板
- [assets/dataset_structure.template](assets/dataset_structure.template) — 目录结构模板
