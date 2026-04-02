"""
extract_frames.py — YOLOv8 数据集视频抽帧脚本
使用方法：修改下方 videos 列表中的配置，然后运行 python extract_frames.py
执行后请删除此文件。
"""

import cv2
from pathlib import Path

# ============================================================
# 配置区 — 修改这里 ===========================================
# ============================================================

# 目标图片输出根目录（images 上一层）
ROOT_DIR = Path(r"e:\2026-3-25\ecar\yolo\dataset\images")

TRAIN_DIR = ROOT_DIR / "train"
VAL_DIR   = ROOT_DIR / "val"

# 视频列表：path=视频路径, prefix=文件名前缀（英文）, target=train或val, count=目标抽取数量
videos = [
    {"path": r"e:\2026-3-25\ecar\yolo\data_test\Anumber.mp4", "prefix": "Anumber", "target": "val",   "count": 1000},
    {"path": r"e:\2026-3-25\ecar\yolo\data_test\black.mp4",  "prefix": "black",   "target": "train", "count": 900},
    {"path": r"e:\2026-3-25\ecar\yolo\data_test\blue.mp4",   "prefix": "blue",    "target": "train", "count": 900},
    {"path": r"e:\2026-3-25\ecar\yolo\data_test\yellow.mp4", "prefix": "yellow",  "target": "train", "count": 900},
]

# ============================================================
# 执行区 — 无需修改 ===========================================
# ============================================================

def clean_dirs():
    """清空目标目录"""
    for d in [TRAIN_DIR, VAL_DIR]:
        for f in d.glob("*"):
            if f.is_file():
                f.unlink()
    print("  目标目录已清空")


def extract(video_path: str, prefix: str, target: str, count: int):
    """从单个视频抽取指定数量的帧"""
    cap = cv2.VideoCapture(video_path)
    total = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    interval = max(1, total // count)
    cap.release()

    out_dir = TRAIN_DIR if target == "train" else VAL_DIR

    cap = cv2.VideoCapture(video_path)
    frame_idx = 0
    saved = 0
    expected = total // interval

    while True:
        ret, frame = cap.read()
        if not ret:
            break
        if frame_idx % interval == 0:
            fname = f"{prefix}_{saved + 1:05d}.jpg"
            cv2.imwrite(str(out_dir / fname), frame)
            saved += 1
            bar_len = 30
            filled = int(bar_len * saved / expected)
            bar = "#" * filled + "-" * (bar_len - filled)
            print(f"\r  [{bar}] {saved}/{expected} 帧  ", end="", flush=True)
        frame_idx += 1

    cap.release()
    print()
    print(f"  {prefix}: 完成，保存 {saved} 张到 images/{target}/")
    return saved


def main():
    clean_dirs()

    print("\n开始抽帧...")
    total = 0
    for v in videos:
        total += extract(v["path"], v["prefix"], v["target"], v["count"])

    print(f"\n全部完成，共抽取 {total} 张图片")


if __name__ == "__main__":
    main()
