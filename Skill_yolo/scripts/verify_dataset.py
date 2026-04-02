"""
verify_dataset.py — YOLO 数据集完整性校验脚本
使用方法：python verify_dataset.py
"""

from pathlib import Path
from collections import Counter

# ============================================================
# 配置区 =====================================================
# ============================================================

DATASET_ROOT = Path(r"e:\2026-3-25\ecar\yolo\dataset")

# 预期的类别（与 data.yaml 中的 names 对应）
EXPECTED_CLASSES = {
    "Anumber": 0,
    "black":   1,
    "blue":    2,
    "yellow":  3,
}

# ============================================================
# 执行区 =====================================================
# ============================================================

def verify():
    print("=" * 50)
    print("YOLO 数据集完整性校验")
    print("=" * 50)

    images_train = list((DATASET_ROOT / "images" / "train").glob("*.jpg"))
    images_val   = list((DATASET_ROOT / "images" / "val").glob("*.jpg"))
    labels_train = list((DATASET_ROOT / "labels" / "train").glob("*.txt"))
    labels_val   = list((DATASET_ROOT / "labels" / "val").glob("*.txt"))

    errors = []

    # 1. 图片统计
    print(f"\n[1] 图片统计")
    print(f"  train: {len(images_train)} 张")
    for k, v in sorted(Counter(f.stem.split("_")[0] for f in images_train).items()):
        print(f"    {k}: {v}")
    print(f"  val:   {len(images_val)} 张")
    for k, v in sorted(Counter(f.stem.split("_")[0] for f in images_val).items()):
        print(f"    {k}: {v}")

    # 2. 标签统计
    print(f"\n[2] 标签统计")
    print(f"  train: {len(labels_train)} 个")
    print(f"  val:   {len(labels_val)} 个")

    # 3. 图片-标签对应性
    print(f"\n[3] 图片-标签对应性检查")
    train_img_names = {f.stem for f in images_train}
    train_lbl_names = {f.stem for f in labels_train}
    val_img_names   = {f.stem for f in images_val}
    val_lbl_names   = {f.stem for f in labels_val}

    train_missing_labels = train_img_names - train_lbl_names
    val_missing_labels   = val_img_names   - val_lbl_names
    train_extra_labels   = train_lbl_names - train_img_names
    val_extra_labels     = val_lbl_names   - val_img_names

    if train_missing_labels:
        errors.append(f"train/ 中有 {len(train_missing_labels)} 张图片缺少标签: {list(train_missing_labels)[:5]}")
    if val_missing_labels:
        errors.append(f"val/ 中有 {len(val_missing_labels)} 张图片缺少标签: {list(val_missing_labels)[:5]}")
    if train_extra_labels:
        errors.append(f"train/ 中有 {len(train_extra_labels)} 个标签无对应图片: {list(train_extra_labels)[:5]}")
    if val_extra_labels:
        errors.append(f"val/ 中有 {len(val_extra_labels)} 个标签无对应图片: {list(val_extra_labels)[:5]}")

    # 4. 标签格式抽查（每部分取前 3 个）
    print(f"\n[4] 标签格式抽查（每类取 1 个）")
    checked_classes = set()
    for lbl in labels_train:
        cls_name = lbl.stem.split("_")[0]
        if cls_name in checked_classes:
            continue
        checked_classes.add(cls_name)
        lines = lbl.read_text().strip().splitlines()
        for line in lines[:1]:
            parts = line.split()
            if len(parts) != 5:
                errors.append(f"{lbl.name}: 格式错误，应为 5 列 (class x y w h)")
                continue
            try:
                cls_id = int(parts[0])
                coords = [float(p) for p in parts[1:]]
                if cls_id < 0 or cls_id >= len(EXPECTED_CLASSES):
                    errors.append(f"{lbl.name}: class_id {cls_id} 超出范围 (0~{len(EXPECTED_CLASSES)-1})")
                for c in coords:
                    if not (0.0 <= c <= 1.0):
                        errors.append(f"{lbl.name}: 坐标 {c} 超出 [0,1] 范围")
            except ValueError:
                errors.append(f"{lbl.name}: 含非数字值")

    # 5. 汇总
    print(f"\n[5] 汇总")
    if errors:
        print(f"  ❌ 发现 {len(errors)} 个问题：")
        for e in errors:
            print(f"    - {e}")
    else:
        print(f"  ✅ 校验通过，无错误")


if __name__ == "__main__":
    verify()
