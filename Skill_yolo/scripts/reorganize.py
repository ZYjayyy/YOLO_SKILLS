"""
reorganize.py — train/val 数据集重组脚本
使用方法：修改下方配置后运行 python reorganize.py
执行后请删除此文件。
"""

from pathlib import Path
from collections import Counter

# ============================================================
# 配置区 =====================================================
# ============================================================

TRAIN_DIR = Path(r"e:\2026-3-25\ecar\yolo\dataset\images\train")
VAL_DIR   = Path(r"e:\2026-3-25\ecar\yolo\dataset\images\val")

# 每个 prefix 从 train 取多少张到 val（None 表示不动该 prefix）
VAL_PER_PREFIX = {
    "Anumber": 25,
    "black":   25,
    "blue":    25,
    "yellow":  25,
}

# ============================================================
# 执行区 =====================================================
# ============================================================

def reorganize():
    print("Step 1: 统计当前状态...")
    train_files = list(TRAIN_DIR.glob("*.jpg"))
    val_files   = list(VAL_DIR.glob("*.jpg"))
    print(f"  train/: {len(train_files)} 张")
    print(f"  val/:   {len(val_files)} 张")

    # Step 2: 合并 val -> train
    if val_files:
        print(f"\nStep 2: 将 val/ 中的 {len(val_files)} 张移到 train/...")
        for f in val_files:
            dst = TRAIN_DIR / f.name
            if dst.exists():
                dst.unlink()
            f.rename(dst)
        print("  完成")

    # Step 3: 取样到 val
    print(f"\nStep 3: 从 train 每种靶取样到 val/...")
    for prefix, count in VAL_PER_PREFIX.items():
        if count is None:
            continue
        src_files = sorted(TRAIN_DIR.glob(f"{prefix}_*.jpg"))
        moved = 0
        for f in src_files[:count]:
            dst = VAL_DIR / f.name
            if not dst.exists():
                f.rename(dst)
                moved += 1
        print(f"  {prefix}: 取 {moved} 张到 val/（共 {len(src_files)} 张原图）")

    # Step 4: 统计最终结果
    print("\n调整后：")
    for d, label in [(TRAIN_DIR, "train"), (VAL_DIR, "val")]:
        files = list(d.glob("*.jpg"))
        cnt = Counter(f.stem.split("_")[0] for f in files)
        print(f"  images/{label}/ 共 {len(files)} 张:")
        for k in sorted(cnt):
            print(f"    {k}: {cnt[k]} 张")


if __name__ == "__main__":
    reorganize()
