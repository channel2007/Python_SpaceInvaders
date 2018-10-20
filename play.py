# encoding: utf-8
import random, sys, os, pygame
from pygame.locals import *
from drewEngine import *

#-------------------------------------------------------------------------
# 常數.
#-------------------------------------------------------------------------
# 顏色.
CONST_BLOCK     = (0,0,0)
CONST_WHITE     = (255,255,255)
CONST_RED       = (255, 0, 0)
CONST_GREEN     = (47, 248, 3)

# 玩家生命數.
COMST_PLAYER_LIFE = 2
# 玩家重生時間(1/1000).
COMST_PLAYER_REBIRTH_TIME = 1000
# 敵人移動速度.
CONST_ENEMY_SPEED = 300
# 敵人發射子彈時脈.
CONST_ENEMY_FIRE_TICK = 900
# 爆炸效果停留時間(1/1000).
CONST_BOOM_TIME = 200
# 飛碟出現時間.
CONST_UFO_TIME = 10000
# 增加隻數分數(每N分增加一隻).
CONST_ADD_1Up_SCORE = 2000

# FPS.
CONST_FPS = 60
# 敵人移動次數.
CONST_ENEMY_MOVE_NUMBER = 60

#-------------------------------------------------------------------------
# 像素陣列.
#-------------------------------------------------------------------------
# 玩家飛機.
CONST_AIRCRAFT_PIXEL = [
[7,21,22,23,36,37,38,46,47,48,49,50,51,52,53,54,55,56,57,58,60,61,62,63,64,65,66,67,68,69,70,71,72,73,74,75,76,77,78,79,80,81,82,83,84,85,86,87,88,89,90,91,92,93,94,95,96,97,98,99,100,101,102,103,104,105,106,107,108,109,110,111,112,113,114,115,116,117,118,119]]
# 玩家飛機-子彈.
CONST_AIRCRAFT_BULLET_PIXEL = [[0,1,2,3]]
# 敵人像素-1.
CONST_ENEMY_PIXEL_1 = [
[3,4,10,11,12,13,17,18,19,20,21,22,24,25,27,28,30,31,32,33,34,35,36,37,38,39,42,45,49,51,52,54,56,58,61,63],
[3,4,10,11,12,13,17,18,19,20,21,22,24,25,27,28,30,31,32,33,34,35,36,37,38,39,41,43,44,46,48,55,57,62]]
# 敵人像素-2.
CONST_ENEMY_PIXEL_2 = [
[2,8,11,14,18,21,22,24,25,26,27,28,29,30,32,33,34,35,37,38,39,41,42,43,44,45,46,47,48,49,50,51,52,53,54,56,57,58,59,60,61,62,63,64,68,74,78,86],
[2,8,14,18,24,25,26,27,28,29,30,34,35,37,38,39,41,42,44,45,46,47,48,49,50,51,52,53,54,55,57,58,59,60,61,62,63,65,66,68,74,76,80,81,83,84]]
# 敵人像素-3.
CONST_ENEMY_PIXEL_3 = [
[4,5,6,7,13,14,15,16,17,18,19,20,21,22,24,25,26,27,28,29,30,31,32,33,34,35,36,37,38,41,42,45,46,47,48,49,50,51,52,53,54,55,56,57,58,59,62,63,64,67,68,69,73,74,77,78,81,82,86,87,92,93],
[4,5,6,7,13,14,15,16,17,18,19,20,21,22,24,25,26,27,28,29,30,31,32,33,34,35,36,37,38,41,42,45,46,47,48,49,50,51,52,53,54,55,56,57,58,59,63,64,67,68,74,75,77,78,80,81,84,85,94,95]]
# 飛碟.
CONST_ENEMY_UFO = [[5,6,7,8,9,10,19,20,21,22,23,24,25,26,27,28,34,35,36,37,38,39,40,41,42,43,44,45,49,50,52,53,55,56,58,59,61,62,64,65,66,67,68,69,70,71,72,73,74,75,76,77,78,79,82,83,84,87,88,91,92,93,99,108]]
# 敵人子彈像素.
CONST_ENEMY_BULLET_PIXEL = [
[0,4,8,10,12,16,20],
[2,4,6,10,14,16,18]]
# 敵人爆炸像素.
CONST_ENEMY_BOOM_PIXEL = [
[3,7,12,15,17,20,24,30,36,40,44,45,53,54,58,62,68,74,78,81,83,86,91,95]]

#-------------------------------------------------------------------------
# 變數.
#-------------------------------------------------------------------------
# 視窗大小.
canvas_width = 800
canvas_height = 600

# FPS開關.
enable_fps = True

# 時脈.
# 0:移動敵人時脈.
# 1:敵人發射時間時脈.
# 2~5:敵人爆炸時間時脈.
# 6:玩家死亡重生時間時脈.
# 7:飛碟出現時間時脈.
last_time = []

# 遊戲模式.
# 10 : 遊戲中.
# 20 : GameOver.
# 30 : 下一關.
game_mode = 10
# 敵人-數量.
enemy_quantity = 0
# 敵人-移動列.
enemy_move_begin = 0
enemy_move_end = 0
# 敵人-移動像素.
enemy_move_pixel = 0
# 敵人-移動次數.
enemy_move_number = 0
# 敵人-移動速度.
enemy_speed = 0
# 敵人-發射子彈時脈.
enemy_fire_tick = 0

# 玩家生命.
player_life = COMST_PLAYER_LIFE
# 玩家分數.
player_score = 0
# 玩家最高分數.
player_hi_score = 0
# 加隻分數.
next_add_1up_score =  CONST_ADD_1Up_SCORE

#-------------------------------------------------------------------------
# 函數:初始遊戲.
#-------------------------------------------------------------------------
def initGame():
    global game_mode, enemy_quantity, enemy_move_begin, enemy_move_end, enemy_move_pixel, enemy_move_number, enemy_speed, enemy_fire_tick
    global enemy_sprite

    # 遊戲模式.
    game_mode = 10
    # 敵人-數量.
    enemy_quantity = 55
    # 敵人-移動列.
    enemy_move_begin = 44
    enemy_move_end = 55
    # 敵人-移動像素.
    enemy_move_pixel = 8
    # 敵人-移動次數.
    enemy_move_number = CONST_ENEMY_MOVE_NUMBER
    # 敵人-移動速度.
    enemy_speed = CONST_ENEMY_SPEED
    # 敵人-發射子彈時脈.
    enemy_fire_tick = CONST_ENEMY_FIRE_TICK
    # 初始敵人位置.
    x = 85
    y = 120
    for i in range(0,55):
        # 換行.
        if( i==11 or i==22 or i==33 or i==44):
            x  = 85
            y += 45
        # 設定敵人.
        enemy_sprite[i].x = x
        enemy_sprite[i].y = y
        enemy_sprite[i].setFrame(0)
        enemy_sprite[i].visible = True
        #enemy_sprite[i].debug = True
        x += 50
    # 關閉飛碟.
    enemy_ufo_sprite.visible = False
    # 初始時脈.
    last_time[7] = pygame.time.get_ticks()
    enemy_ufo_sprite.x = -16
    # 關閉敵人子彈
    for i in range(0,32):
        enemy_bullet_sprite[i].visible = False

#-------------------------------------------------------------------------
# 函數:秀字.
#-------------------------------------------------------------------------
def showFont( text, color, x, y):
    global canvas    
    text = font.render(text, 1, color) 
    canvas.blit( text, (x,y))

#-------------------------------------------------------------------------
# 函數:顯示爆炸.
#-------------------------------------------------------------------------
def setBoom( x, y, color):
    for j in range(0,len(enemy_boom_sprite)):
        if (not enemy_boom_sprite[j].visible):
            enemy_boom_sprite[j].x = x 
            enemy_boom_sprite[j].y = y 
            enemy_boom_sprite[j].color = color
            enemy_boom_sprite[j].visible = True
            last_time[j+2] = pygame.time.get_ticks()
            break

#-------------------------------------------------------------------------
# 函數:增加生命.
#-------------------------------------------------------------------------
def add1Up():
    global player_life, player_score , next_add_1up_score
    if( player_score >= next_add_1up_score and  (player_score % CONST_ADD_1Up_SCORE) < 60):
        next_add_1up_score += CONST_ADD_1Up_SCORE
        player_life += 1
        if(player_life > 5):
            player_life = 5

#-------------------------------------------------------------------------
# 初始.
#-------------------------------------------------------------------------
# 初始pygame.
pygame.init()
# 顯示Title.
pygame.display.set_caption(u"太空侵略者")
# 建立畫佈大小.
canvas = pygame.display.set_mode((canvas_width, canvas_height))
# 時脈.
clock = pygame.time.Clock()

# 設定字型.
#font = pygame.font.SysFont(pygame.font.match_font('bitstreamverasans'), 24)
font = pygame.font.SysFont('arial',18)

# 加入時脈.
for i in range( 0, 8):
    last_time.append(pygame.time.get_ticks())

# 玩家飛機.
aircraft_sprite = Sprite(pygame, canvas, 15, 8, [0, 550, 3, 3], CONST_GREEN, CONST_AIRCRAFT_PIXEL) 
# 玩家飛機-飛彈.
aircraft_bullet_sprite = Sprite(pygame, canvas, 1, 4, [0, 0, 2, 2], CONST_WHITE, CONST_AIRCRAFT_BULLET_PIXEL)
aircraft_bullet_sprite.visible = False
# 玩家生命.
aircraft_life_sprite = []
x = 8
y = 8
for i in range(0, 5):
    aircraft_life_sprite.append([])
    aircraft_life_sprite[i] = Sprite(pygame, canvas, 15, 8, [x, y, 2, 2], CONST_GREEN, CONST_AIRCRAFT_PIXEL) 
    x += 35
# 飛碟.
enemy_ufo_sprite = Sprite(pygame, canvas, 16, 7, [-16, 60, 3, 3], CONST_RED, CONST_ENEMY_UFO, [60])
enemy_ufo_sprite.visible = False

# 敵人.
enemy_sprite = []
for i in range(0,55):
    # 敵人1-1.
    if (i < 11):
        enemy_sprite.append([])
        enemy_sprite[i] = Sprite(pygame, canvas, 8, 8, [0, 0, 3, 3], CONST_WHITE, CONST_ENEMY_PIXEL_1, [30])
    # 敵人2-2,3.
    elif (i < 33):
        enemy_sprite.append([])
        enemy_sprite[i] = Sprite(pygame, canvas, 11, 8, [0, 0, 3, 3], CONST_WHITE, CONST_ENEMY_PIXEL_2, [20])
    # 敵人3-4,5.
    elif (i < 55):
        enemy_sprite.append([])
        enemy_sprite[i] = Sprite(pygame, canvas, 12, 8, [0, 0, 3, 3], CONST_WHITE, CONST_ENEMY_PIXEL_3, [10])
# 敵人子彈
enemy_bullet_sprite = []
for i in range(0,32):
    enemy_bullet_sprite.append([])
    enemy_bullet_sprite[i] = Sprite(pygame, canvas, 3, 7, [0, 0, 3, 3], CONST_WHITE, CONST_ENEMY_BULLET_PIXEL)
    enemy_bullet_sprite[i].speed = 50
    enemy_bullet_sprite[i].visible = False

# 敵人爆炸像素.
enemy_boom_sprite = []
for i in range(0,4):
    enemy_boom_sprite.append([])
    enemy_boom_sprite[i] = Sprite(pygame, canvas, 11, 9, [0, 0, 3, 3], CONST_WHITE, CONST_ENEMY_BOOM_PIXEL)
    enemy_boom_sprite[i].visible = False
 
# 初始遊戲.
initGame()

#-------------------------------------------------------------------------    
# 主迴圈.
#-------------------------------------------------------------------------
running = True
while running:
    # 清除畫面.
    canvas.fill(CONST_BLOCK)    
    #---------------------------------------------------------------------
    # 判斷輸入.
    #---------------------------------------------------------------------
    for event in pygame.event.get():
        # 離開遊戲.
        if event.type == pygame.QUIT:
            running = False
        # 判斷按下按鈕.
        if event.type == pygame.KEYDOWN:
            # 判斷按下ESC按鈕.
            if event.key == pygame.K_ESCAPE:
                running = False
            # 開關FPS.
            elif event.key == pygame.K_f:
                enable_fps = not enable_fps
                
        # 判斷Mouse.
        if event.type == pygame.MOUSEBUTTONDOWN:
            # 10 : 遊戲中.
            if(game_mode == 10):
                # 發射飛彈.
                if aircraft_sprite.visible and not aircraft_bullet_sprite.visible:
                    aircraft_bullet_sprite.visible = True
                    aircraft_bullet_sprite.x = aircraft_sprite.x + (aircraft_sprite.getWidth() >> 1)
                    aircraft_bullet_sprite.y = aircraft_sprite.y
            # 20 : GameOver.
            elif (game_mode == 20):
                # 玩家生命.
                player_life = COMST_PLAYER_LIFE
                # 玩家分數.
                player_score = 0
                # 開啟玩家飛機.
                aircraft_sprite.visible = True
                # 初始加隻分數.
                next_add_1up_score =  CONST_ADD_1Up_SCORE
                # 初始遊戲.
                initGame()

    # 10 : 遊戲中.
    if(game_mode == 10):
        #---------------------------------------------------------------------    
        # Gameplay.
        #---------------------------------------------------------------------    
        # 設定玩家飛機跟隨滑鼠.
        aircraftX = pygame.mouse.get_pos()[0] - (aircraft_sprite.getWidth() >> 1)
        # 左邊界.
        if(aircraftX < (aircraft_sprite.getWidth() >> 1)):
            aircraftX = pygame.mouse.get_pos()[0]
        # 右邊界.
        elif (aircraftX > (canvas_width - aircraft_sprite.getWidth()) ):
            aircraftX = canvas_width - aircraft_sprite.getWidth()        
        # 移動玩家飛機.
        aircraft_sprite.x = aircraftX

        # 發射玩家飛彈.
        if aircraft_bullet_sprite.visible:
            # 移動飛彈.
            aircraft_bullet_sprite.y -= 12
            # 超出邊界.
            if aircraft_bullet_sprite.y < 0:
                aircraft_bullet_sprite.visible = False
        # 移動敵人.
        if((pygame.time.get_ticks() - last_time[0]) >= enemy_speed):
            # 移動列.
            for i in range(enemy_move_begin, enemy_move_end):
                enemy_sprite[i].x += enemy_move_pixel
                last_time[0] = pygame.time.get_ticks()
            # 移動單列.
            enemy_move_begin -= 11
            enemy_move_end -= 11
            if(enemy_move_begin < 0):
                enemy_move_begin = 44
                enemy_move_end = 55
            # 左右變換方向移動.
            enemy_move_number -= 1
            if(enemy_move_number <= 0):
                # 左右反轉.
                enemy_move_pixel = -enemy_move_pixel
                enemy_move_number = CONST_ENEMY_MOVE_NUMBER
                # 每下降一次速度就變快一點.
                enemy_speed -= 40
                if(enemy_speed < 0):
                    enemy_speed = 1
                # 每下降一次敵人子彈發射時間縮短. 
                enemy_fire_tick -= 200
                if(enemy_fire_tick < 200):
                    enemy_fire_tick = 200
                # 改變所有敵人.
                for i in range(0,len(enemy_sprite)):
                    # 敵人下降.
                    enemy_sprite[i].y += 20
                    # 判斷敵人是否碰到主角飛機(GameOver).
                    if enemy_sprite[i].visible and aircraft_sprite.colliderect(enemy_sprite[i].getCollisionRect()):                        
                        game_mode = 20
                    # 敵人超出下邊界.             
                    elif enemy_sprite[i].visible and (enemy_sprite[i].y >= (canvas_height - enemy_sprite[i].getHeight())):
                        game_mode = 20

        # 出現飛碟.
        if((pygame.time.get_ticks() - last_time[7]) >= CONST_UFO_TIME):
            enemy_ufo_sprite.visible = True

        #---------------------------------------------------------------------    
        # 更新畫面.
        #---------------------------------------------------------------------    
        # 更新主角飛機.
        aircraft_sprite.update()
        # 更新主角飛機子彈.
        aircraft_bullet_sprite.update()

        # 飛碟.
        if(enemy_ufo_sprite.visible):
            enemy_ufo_sprite.x += 2
            if(enemy_ufo_sprite.x > canvas_width):
                enemy_ufo_sprite.visible = False
                last_time[7] = pygame.time.get_ticks()
                enemy_ufo_sprite.x = -16
            # 更新.
            enemy_ufo_sprite.update()

        # 活著的敵人編號.
        enemy_alive_id = []
        # 更新敵人.
        for i in range(0,len(enemy_sprite)):
            # 判斷子彈是否打中敵人.
            if (enemy_sprite[i].visible and aircraft_bullet_sprite.visible and aircraft_bullet_sprite.colliderect(enemy_sprite[i].getCollisionRect()) ):
                # 關閉敵人.
                enemy_sprite[i].visible = False
                # 關閉子彈.
                aircraft_bullet_sprite.visible = False                
                # 敵人爆炸像素.
                setBoom( enemy_sprite[i].x, enemy_sprite[i].y, CONST_WHITE)
                # 分數.
                player_score += int(enemy_sprite[i].data[0])
                # 敵人數量減1.
                enemy_quantity -= 1
                # 判斷增加生命.
                add1Up()                
                # 30 : 下一關.
                if(enemy_quantity <= 0):
                    game_mode = 30

            # 存入活著的敵人編號.
            if (enemy_sprite[i].visible):
                enemy_alive_id.append(i)
            # 更新.
            enemy_sprite[i].update()
        
        # 敵人發射子彈.        
        if( (len(enemy_alive_id) > 0) and (pygame.time.get_ticks() - last_time[1]) >= enemy_fire_tick):
            last_time[1] = pygame.time.get_ticks()
            id = random.randint(0,len(enemy_alive_id)) - 1
            if (enemy_sprite[enemy_alive_id[id]].visible):
                # 找出未使用的敵人子彈.
                for i in range(0,len(enemy_bullet_sprite)):
                    if(not enemy_bullet_sprite[i].visible):
                        # 依照敵人位置設定發射子彈位置.
                        enemy_bullet_sprite[i].x = enemy_sprite[enemy_alive_id[id]].x + (enemy_sprite[enemy_alive_id[id]].getWidth() >> 1)
                        enemy_bullet_sprite[i].y = enemy_sprite[enemy_alive_id[id]].y + enemy_sprite[enemy_alive_id[id]].getHeight()
                        enemy_bullet_sprite[i].visible = True
                        break
        # 清除活著的敵人編號陣列.
        enemy_alive_id.clear()
        # 敵人子彈
        for i in range(0,len(enemy_bullet_sprite)):
            # 判斷開啟的子彈才處理.
            if(enemy_bullet_sprite[i].visible):
                # 更新子彈.
                enemy_bullet_sprite[i].update()
                # 移動子彈.
                enemy_bullet_sprite[i].y += 4
                if(enemy_bullet_sprite[i].y > canvas_height):
                    enemy_bullet_sprite[i].visible = False
                # 判斷子彈是否碰到玩家飛機
                if(aircraft_sprite.visible and enemy_bullet_sprite[i].colliderect(aircraft_sprite.getCollisionRect()) ):
                    # 紀錄時脈.
                    last_time[6] = pygame.time.get_ticks()                    
                    # 關閉玩家飛機.
                    aircraft_sprite.visible = False
                    # 顯示爆炸.
                    setBoom( aircraft_sprite.x, aircraft_sprite.y, CONST_GREEN)

        # 敵人爆炸像素.
        for i in range(0,len(enemy_boom_sprite)):
            # 判斷爆炸是否開啟
            if(enemy_boom_sprite[i].visible):
                # 判斷停留時間是否以到
                if((pygame.time.get_ticks() - last_time[i+2]) >= CONST_BOOM_TIME):
                    enemy_boom_sprite[i].visible = False
                enemy_boom_sprite[i].update()

        # 處理玩家飛機重生.
        if(not aircraft_sprite.visible):
            if((pygame.time.get_ticks() - last_time[6]) >= COMST_PLAYER_REBIRTH_TIME):
                # 扣生命.
                player_life -= 1
                if(player_life < 0):
                    player_life = 0
                    # GameOver
                    game_mode = 20
                else:    
                    # 開啟玩家飛機.
                    aircraft_sprite.visible = True

        # 判斷子彈是否打中飛碟.
        if (enemy_ufo_sprite.visible and aircraft_bullet_sprite.colliderect(enemy_ufo_sprite.getCollisionRect()) ):
            # 關閉子彈.
            aircraft_bullet_sprite.visible = False                
            # 關閉飛碟.
            enemy_ufo_sprite.visible = False
            # 飛碟爆炸像素.
            setBoom( enemy_ufo_sprite.x, enemy_ufo_sprite.y, CONST_RED)
            # 分數.
            player_score += int(enemy_ufo_sprite.data[0])
            # 判斷增加生命.
            add1Up()                
            # 初始時脈.
            last_time[7] = pygame.time.get_ticks()
            enemy_ufo_sprite.x = -16
    # 20 : GameOver.
    elif (game_mode == 20):
        # 紀錄玩家最高分數.
        if(player_score > player_hi_score):
            player_hi_score = player_score
        # 顯示訊息
        showFont( u"Game Over", CONST_WHITE, 350 , 250)
    # 30 : 下一關.
    elif (game_mode == 30):
        # 初始遊戲.
        initGame()

    #---------------------------------------------------------------------    
    # 更新UI.
    #---------------------------------------------------------------------    
    # 玩家生命.
    for i in range(0,player_life):
        aircraft_life_sprite[i].update()
    # 分數.
    showFont( u"SCORE", CONST_WHITE, 200, 8)
    showFont( str(player_score), CONST_WHITE, 200, 24)
    # 剩餘數量.
    showFont( u"QUANTITY", CONST_WHITE, 370, 8)
    showFont( str(enemy_quantity), CONST_WHITE, 370, 24)
    # 最高分數.
    showFont( u"HI-SCORE", CONST_WHITE, 540, 8)
    showFont( str(player_hi_score), CONST_WHITE, 540, 24)
    # 顯示FPS.
    if(enable_fps):
        showFont( u"FPS:" + str(int(clock.get_fps())), CONST_RED, 8, 8)            
        
    # 更新畫面.
    pygame.display.update()
    clock.tick(CONST_FPS)

# 離開遊戲.
pygame.quit()


