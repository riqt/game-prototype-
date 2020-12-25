import pygame
from pygame.locals import *
import sys
from tkinter import *
from tkinter import messagebox

SCR_RECT = Rect(0, 0, 1280, 720)

class Lyric(pygame.sprite.Sprite):
    def __init__(self, filename, x, y, vx, vy):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(filename).convert_alpha()
        colorkey = self.image.get_at((0,0))
        self.image.set_colorkey(colorkey, RLEACCEL)
        width = self.image.get_width()
        height = self.image.get_height()
        self.rect = Rect(x, y, width, height)
        self.vx = vx
        self.vy = vy
    def update(self):
        self.rect.move_ip(self.vx, self.vy)
        # 壁にぶつかったら跳ね返る
        if self.rect.left < 0 or self.rect.right > SCR_RECT.width:
            self.vx = -self.vx
        if self.rect.top < 0 or self.rect.bottom > SCR_RECT.height:
            self.vy = -self.vy
        # 画面からはみ出ないようにする
        self.rect = self.rect.clamp(SCR_RECT)

def judge(x, y, obj):
    if obj.rect.left < x < obj.rect.right and obj.rect.top < y < obj.rect.bottom:
        return 1
    else:
        return 0

def main():
    pygame.init()
    screen = pygame.display.set_mode(SCR_RECT.size)  # (SCR_RECT.size, FULLSCREEN)
    pygame.display.set_caption("Vocal_Lesson")

    # (座標, 速度)
    n = 5  # 曲数
    song = [[] for i in range(n)]
    song[0].append(Lyric("1_1.png", 0, 0, 2, 2))
    song[0].append(Lyric("1_2.png", 10, 10, 5, 5))
    song[0].append(Lyric("1_3.png", 320, 240, -2, 3))
    song[1].append(Lyric("1_1.png", 0, 0, 2, 2))
    print(dir(song[0][0]))

    # スプライトグループを作成してスプライトを追加
    group = []  # 初期化
    for i in range(len(song)):
        group.append(pygame.sprite.RenderUpdates())
        for j in range(len(song[i])):
            group[i].add(song[i][j])

    clock = pygame.time.Clock()

    fullscreen_flag = False

    miss_count = 0
    step = 0

    while True:
        clock.tick(60)  # 60fps

        screen.fill((0,0,255))

        for event in pygame.event.get():
            if event.type == MOUSEBUTTONDOWN and event.button == 1:
                x, y = pygame.mouse.get_pos()
                if judge(x, y, song[0][step]):
                    song[0][step].kill()
                    step += 1
                for i in range(step+1, len(song[0])):
                    if judge(x, y, song[0][i]):
                        miss_count += 1

        # スプライトグループを更新
        group[0].update()

        # スプライトグループを描画
        group[0].draw(screen)

        # 終了判定
        if len(song[0]) == step:
            Tk().wm_withdraw()
            messagebox.showinfo('','Game Clear')
            pygame.quit()
            sys.exit()
        elif miss_count > 3:
            Tk().wm_withdraw()
            messagebox.showinfo('','Game Over')
            pygame.quit()
            sys.exit()

        pygame.display.update()
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == KEYDOWN and event.key == K_F2:
                # F2キーでフルスクリーンモードへの切り替え
                fullscreen_flag = not fullscreen_flag
                if fullscreen_flag:
                    screen = pygame.display.set_mode(SCR_RECT.size, FULLSCREEN, 32)
                else:
                    screen = pygame.display.set_mode(SCR_RECT.size, 0, 32)


if __name__ == "__main__":
    main()
