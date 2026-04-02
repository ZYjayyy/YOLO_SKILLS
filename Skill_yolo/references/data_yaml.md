# data.yaml 完整字段说明

## 基础结构

```yaml
path: E:/2026-3-25/ecar/yolo/dataset   # 数据集根目录（绝对路径或相对路径）
train: images/train                    # 训练集图片相对路径（相对于 path）
val: images/val                        # 验证集图片相对路径（相对于 path）

nc: 4                                  # 类别数量（必须与 names 长度一致）
names:
  0: Anumber                           # 类别 0
  1: black                            # 类别 1
  2: blue                             # 类别 2
  3: yellow                           # 类别 3
```

## 字段详解

### path
- **类型**：字符串
- **说明**：数据集根目录的绝对路径或相对于运行命令的路径
- **注意**：Windows 路径用 `/` 分隔（Unix 风格），避免 `\` 导致转义问题

### train / val
- **类型**：字符串（相对路径）
- **说明**：相对于 `path` 的目录路径
- **要求**：目录内直接存放图片文件（.jpg/.png），不嵌套子文件夹

### nc
- **类型**：整数
- **说明**：类别总数
- **注意**：必须与 `names` 中的键数量一致

### names
- **类型**：字典（键为整数，值为字符串）
- **键**：类别 ID（从 0 开始，连续）
- **值**：类别名称（建议英文，无空格，避免特殊字符）
- **顺序**：类别 ID 的顺序必须与标注时的 class_id 一致

## 完整示例

```yaml
path: E:/project/ecar/yolo/dataset
train: images/train
val: images/val

nc: 4
names:
  0: Anumber
  1: black
  2: blue
  3: yellow
```

## 常见错误

| 错误 | 原因 | 解决方案 |
|------|------|---------|
| `Dataset not found` | path 路径错误 | 使用绝对路径或确认相对路径 |
| `Only one class` detected | nc 与实际类别不符 | 核对 names 数量 |
| `No labels found` | labels 目录缺失或路径不对 | 确认 labels 与 images 同级 |

## 多数据集融合写法

```yaml
path: E:/project/ecar/yolo/dataset
train:
  - dataset1/images/train
  - dataset2/images/train
val: images/val

nc: 4
names:
  0: Anumber
  1: black
  2: blue
  3: yellow
```
