# YOLOv8 常用命令速查

## 安装

```bash
pip install ultralytics
```

## 训练

```bash
yolo detect train data=data.yaml model=yolov8n.pt epochs=100 imgsz=640 device=0
```

### 从上次中断处继续

```bash
yolo detect train data=data.yaml model=yolov8n.pt epochs=100 resume=True
```

## 验证

```bash
yolo detect val data=data.yaml model=runs/detect/train/weights/best.pt
```

### 指定验证图片

```bash
yolo detect val data=data.yaml model=runs/detect/train/weights/best.pt source=images/val/
```

## 推理/预测

```bash
yolo detect predict model=runs/detect/train/weights/best.pt source=test.jpg
```

### 推理视频

```bash
yolo detect predict model=runs/detect/train/weights/best.pt source=test.mp4
```

### 推理目录（批量）

```bash
yolo detect predict model=runs/detect/train/weights/best.pt source=images/test/
```

### 保存结果到指定目录

```bash
yolo detect predict model=runs/detect/train/weights/best.pt source=test.jpg project=runs/detect name=predict_output
```

## 导出模型

| 格式 | 命令 | 说明 |
|------|------|------|
| ONNX | `yolo export model=best.pt format=onnx` | 跨平台，推荐 |
| TorchScript | `yolo export model=best.pt format=torchscript` | PyTorch 原生 |
| TensorRT | `yolo export model=best.pt format=engine` | GPU 加速（需 TensorRT） |
| CoreML | `yolo export model=best.pt format=coreml` | iOS/macOS |
| TFLite | `yolo export model=best.pt format=tflite` | 移动端/嵌入式 |

## 导出并推理 ONNX

```bash
# 导出
yolo export model=best.pt format=onnx

# 使用 ONNX 推理（需要 onnxruntime）
from ultralytics import RTDETR
model = RTDETR('best.onnx')
results = model('test.jpg')
```

## 模型信息

```bash
yolo inspect
```

## 查看训练结果

训练完成后，主要结果文件：

```
runs/detect/{project}/{name}/
├── weights/
│   ├── best.pt          # 最佳权重（mAP 最高）
│   └── last.pt          # 最后权重
├── results.csv          # 训练日志（CSV 格式）
├── results.png          # 训练曲线图
├── args.yaml            # 训练参数
└── train*.jpg           # 训练集样本可视化
```

## 绘制训练曲线

```python
from ultralytics.utils.plots import plot_results
plot_results('runs/detect/train/results.csv')
```

## 常用参数汇总

| 命令 | 常用参数 |
|------|---------|
| train | `data`, `model`, `epochs`, `imgsz`, `batch`, `device`, `patience`, `project`, `name`, `resume` |
| val | `data`, `model`, `source`, `imgsz`, `conf`, `iou` |
| predict | `model`, `source`, `conf`, `iou`, `project`, `name`, `save`, `view` |
| export | `model`, `format`, `imgsz`, `half`（FP16 量化） |

## Python API

```python
from ultralytics import YOLO

# 加载模型
model = YOLO('yolov8n.pt')

# 训练
results = model.train(data='data.yaml', epochs=100, imgsz=640)

# 验证
results = model.val(data='data.yaml')

# 推理
results = model.predict('test.jpg', conf=0.25)

# 导出
model.export(format='onnx')
```
