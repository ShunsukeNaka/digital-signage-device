#!/usr/bin/env python3
import pygame
import sys
import glob
import time
import subprocess
import os

COUNT_FILE = "/home/tns0/service/count.txt"   # 周回数を書き込むファイル
def get_dir_num():
    num_path = "/home/tns0/service/datas/dirnum.txt"
    with open(num_path, "r") as f:
        data = f.read().replace("\n", "")
    return data


def load_and_scale_image(path, screen_size):
    """画像を読み込み、アスペクト比を保持して拡大縮小"""
    img = pygame.image.load(path)
    img_rect = img.get_rect()
    screen_w, screen_h = screen_size
    img_w, img_h = img_rect.size

    # 縦横比を保持したまま拡縮
    scale_ratio = min(screen_w / img_w, screen_h / img_h)
    new_w = int(img_w * scale_ratio)
    new_h = int(img_h * scale_ratio)
    img = pygame.transform.smoothscale(img, (new_w, new_h))
    return img

def play_video(path):
    """mpvで動画をフルスクリーン再生"""
    subprocess.run(["mpv", "--fs", "--no-terminal", path])

def read_count():
    """現在の周回数を取得。ファイルが無ければ0"""
    try:
        with open(COUNT_FILE) as f:
            return int(f.read().strip())
    except (FileNotFoundError, ValueError):
        return 0

def write_count(n):
    """周回数をファイルに書き込む"""
    with open(COUNT_FILE, "w") as f:
        f.write(str(n) + "\n")

def run_slideshow(image_interval=5):
	"""指定フォルダ内の画像・動画を順番に再生し、1周ごとに周回数を更新"""
	pygame.init()
	screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
	screen_size = screen.get_size()

	dir_num = get_dir_num()

	while True:
		# 画像と動画をまとめて取得
		content_folder = f"/home/tns0/service/content{dir_num}"  # コンテンツフォルダ
		images = glob.glob(os.path.join(content_folder, "*.jpg")) + \
		     glob.glob(os.path.join(content_folder, "*.png"))
		videos = glob.glob(os.path.join(content_folder, "*.mp4")) + \
		     glob.glob(os.path.join(content_folder, "*.mov")) + \
		     glob.glob(os.path.join(content_folder, "*.avi"))
		content_list = sorted(images + videos)
		if not content_list:
			print("コンテンツが見つかりません")
			return

		idx = 0
		clock = pygame.time.Clock()
		last_switch = time.time()
		lap_count = read_count()  # 既存の周回数からスタート

		while True:
			now_dir_num = get_dir_num()
			if dir_num == now_dir_num:
				None
			else:
				dir_num = now_dir_num
				break
			# イベント処理
			for event in pygame.event.get():
			    if event.type == pygame.QUIT:
			        pygame.quit(); sys.exit()
			    if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
			        pygame.quit(); sys.exit()

			current_file = content_list[idx]
			ext = os.path.splitext(current_file)[1].lower()

			if ext in [".jpg", ".png"]:
			    # 画像の場合
			    if time.time() - last_switch >= image_interval:
			        idx += 1
			        last_switch = time.time()
			elif ext in [".mp4", ".mov", ".avi"]:
			    # 動画の場合（ブロッキング）
			    play_video(current_file)
			    idx += 1
			    last_switch = time.time()
			else:
			    # 不明な拡張子はスキップ
			    idx += 1

			# 1周したらカウントアップ
			if idx >= len(content_list):
			    idx = 0
			    lap_count += 1
			    write_count(lap_count)
			    print(f"=== {lap_count} 周目終了 ===")

			# 画像を描画
			if ext in [".jpg", ".png"]:
			    screen.fill((0, 0, 0))
			    img = load_and_scale_image(current_file, screen_size)
			    img_rect = img.get_rect(center=(screen_size[0]//2, screen_size[1]//2))
			    screen.blit(img, img_rect)
			    pygame.display.flip()

			clock.tick(60)

if __name__ == "__main__":
    run_slideshow(3)
