# encoding: utf-8

#-------------------------------------------------------------------------
# 點陣動畫系統.
#-------------------------------------------------------------------------
class Sprite(object):
    #-------------------------------------------------------------------------
    # 建構式.
    #   pygame      : pygame.
    #   canvas      : 畫佈.
    #   column      : 列.
    #   row         : 行.
    #   rect        : 位置、磚塊大小.
    #   color       : 磚塊顏色.
    #   aniArray    : 動畫敘述陣列.
    #   data        : 資料.
    #-------------------------------------------------------------------------
    def __init__(self, pygame,  canvas, column, row, rect, color, aniArray, data=[]):
        # 初始變數.
        self.__pygame = pygame
        self.__canvas = canvas
        self.__column = column
        self.__row = row
        self.__rect = rect
        self.__aniArray = aniArray

        # 顯示動畫frame.
        self.__frame = 0        
        # 紀錄時間.
        self.__last_time = self.__pygame.time.get_ticks()
        # 碰撞區域.
        self.__collision_rect = self.__pygame.Rect(self.__rect[0], self.__rect[1], self.__rect[2] * column, self.__rect[3] * row)        

        # 資料.
        self.data = data
        # 播放速度(1/1000)
        self.speed = 1000
        # 顏色.
        self.color = color
        # 是否顯示.
        self.visible = True
        # 設定除錯模式.
        self.debug = False
        # 顯示座標.
        self.x = self.__rect[0]
        self.y = self.__rect[1]

    #-------------------------------------------------------------------------
    # 設定播放的frame.
    #-------------------------------------------------------------------------
    def setFrame(self, frame):
        self.__frame = frame

    #-------------------------------------------------------------------------
    # 取得碰撞區域.
    #-------------------------------------------------------------------------
    def getCollisionRect(self):
        return self.__collision_rect

    #-------------------------------------------------------------------------
    # 取得寬.
    #-------------------------------------------------------------------------
    def getWidth(self):
        return self.__collision_rect.width

    #-------------------------------------------------------------------------
    # 取得高.
    #-------------------------------------------------------------------------
    def getHeight(self):
        return self.__collision_rect.height

    #-------------------------------------------------------------------------
    # 測試碰撞(兩個矩形是否重疊).
    #-------------------------------------------------------------------------
    def colliderect(self, collideRect):
        return self.__collision_rect.colliderect(collideRect)

    #-------------------------------------------------------------------------
    # 更新.
    #-------------------------------------------------------------------------
    def update(self):
        # 是否顯示.
        if(self.visible):
            # 判斷時脈播放下一個frame.
            if ((self.__pygame.time.get_ticks() - self.__last_time) >= self.speed):
                # 播放下一個framel.
                self.__frame += 1
                # 巡迴播放.
                if(self.__frame >= len(self.__aniArray)):
                    self.__frame = 0
                # 紀錄時脈.
                self.__last_time = self.__pygame.time.get_ticks()

            # 設定座標.
            self.__rect[0] = self.__collision_rect.x = self.x
            self.__rect[1] = self.__collision_rect.y = self.y

            # 畫方塊.
            for i in range(0,len(self.__aniArray[self.__frame])):
                # 轉換要畫得方塊位置.
                y = int(self.__aniArray[self.__frame][i] / self.__column)
                x = int(self.__aniArray[self.__frame][i] % self.__column)
                rect = [(x*self.__rect[2]) + self.__rect[0], (y*self.__rect[3]) + self.__rect[1], self.__rect[2], self.__rect[3]]
                self.__pygame.draw.rect( self.__canvas, self.color, rect)

            # 除錯模式.
            if(self.debug):
                # 畫出碰撞區.
                self.__pygame.draw.lines( self.__canvas, (255, 0, 0), True, 
                    [
                    [self.__collision_rect.x, self.__collision_rect.y],
                    [self.__collision_rect.x+self.__collision_rect.width, self.__collision_rect.y], 
                    [self.__collision_rect.x+self.__collision_rect.width, self.__collision_rect.y+self.__collision_rect.height], 
                    [self.__collision_rect.x, self.__collision_rect.y+self.__collision_rect.height]
                    ], 1)

