import os
import sys
import pygame as pg
import random
import time


WIDTH, HEIGHT = 1100, 650
DELTA = {pg.K_UP:   ( 0,-5),
         pg.K_DOWN: ( 0,+5),
         pg.K_LEFT: (-5, 0),
         pg.K_RIGHT:(+5, 0),
         }

os.chdir(os.path.dirname(os.path.abspath(__file__)))

def check_bound(obj_rct: pg.rect) -> tuple[bool, bool]:
    """
    引数  ：こうかとん または 爆弾のRect
    戻り値：真理値タプル（横判定結果、縦判定結果）
    画面内ならTrue 画面外ならFalse
    """
    yoko,tate = True,True
    if obj_rct.left < 0 or WIDTH < obj_rct.right:
        yoko = False
    if obj_rct.top < 0 or HEIGHT < obj_rct.bottom:
        tate = False
    
    return yoko,tate
    
def gameover(screen):
    """
    ゲームオーバー時の処理
    引数:screen
    戻り値:無し
    背景をブラックアウト、GameOverの文字を中心に、その上に泣いているこうかとんの画像を配置
    """
    black= pg.Surface((WIDTH,HEIGHT))
    pg.draw.rect(black,(0,0,0),(0,0,WIDTH,HEIGHT))
    black.set_alpha(100)
    screen.blit(black,(0,0))
    cry_img = pg.transform.rotozoom(pg.image.load("fig/8.png"),0,1.2)
    cry_rct = cry_img.get_rect(center=(WIDTH//2,HEIGHT//2-50))
    screen.blit(cry_img,cry_rct)
    fonto = pg.font.Font(None,80)
    txt = fonto.render("GameOver",True,
                       (0,150,255))
    txt_rct = txt.get_rect()
    txt_rct.center = WIDTH//2,HEIGHT//2
    screen.blit(txt,txt_rct)
    pg.display.update()
    time.sleep(5)
    


def main():
    pg.display.set_caption("逃げろ！こうかとん")
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    bg_img = pg.image.load("fig/pg_bg.jpg")    
    kk_img = pg.transform.rotozoom(pg.image.load("fig/3.png"), 0, 0.9)
    kk_rct = kk_img.get_rect()
    kk_rct.center = 300, 200
    bb_img = pg.Surface((20, 20))
    pg.draw.circle(bb_img, (255, 0 ,0), (10, 10),10)
    bb_img.set_colorkey((0, 0, 0))
    bb_rct = bb_img.get_rect()
    bb_rct.centerx = random.randint(0, WIDTH)
    bb_rct.centery = random.randint(0, HEIGHT)
    vx , vy = +5, +5
    clock = pg.time.Clock()
    tmr = 0
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT: 
                return
        screen.blit(bg_img, [0, 0]) 
        

        key_lst = pg.key.get_pressed()
        sum_mv = [0, 0]

        # if key_lst[pg.K_UP]:
        #     sum_mv[1] -= 5
        # if key_lst[pg.K_DOWN]:
        #     sum_mv[1] += 5
        # if key_lst[pg.K_LEFT]:
        #     sum_mv[0] -= 5
        # if key_lst[pg.K_RIGHT]:
        #     sum_mv[0] += 5

        for key, tpl in DELTA.items():
            if key_lst[key]:
                sum_mv[0] += tpl[0] #横方向
                sum_mv[1] += tpl[1] #縦方向
            
        
        kk_rct.move_ip(sum_mv)
        if check_bound(kk_rct) != (True,True):
            kk_rct.move_ip(-sum_mv[0],-sum_mv[1])

        screen.blit(kk_img, kk_rct)
        bb_rct.move_ip(vx, vy)
        yoko,tate = check_bound(bb_rct)
        if not yoko:
            vx *= -1
        if not tate:
            vy *= -1
        screen.blit(bb_img, bb_rct)
        if kk_rct.colliderect(bb_rct) == True:
            gameover(screen)
            return
            
        pg.display.update()
        tmr += 1
        clock.tick(50)

if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()
