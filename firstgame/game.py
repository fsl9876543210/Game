import pygame
from pygame.locals import *
import sys
# cycle迭代工具，即无限循环
from itertools import cycle
import random

# 窗口宽度
SCREENWIDTH = 822
# 窗口高度
SCREENHEIGHT = 199
# 更新画面的时间
FPS = 30

# 游戏结束的方法
def game_over():
    # 加载撞击音效
    bump_audio = pygame.mixer.Sound('audio/bump.wav')
    # 播放撞击音效
    bump_audio.play()
    # 获取窗体宽、高
    screen_w = pygame.display.Info().current_w
    screen_h = pygame.display.Info().current_h
    # 加载游戏结束的图片
    over_img = pygame.image.load('image/gameover.png').convert_alpha()
    # 将游戏结束的图片绘制在窗体的中间位置
    SCREEN.blit(over_img, ((screen_w - over_img.get_width()) / 2, (screen_h - over_img.get_height()) / 2))
def mainGame():
    # 得分
    score = 0
    # 游戏结束标记，False没有结束
    over = False
    global SCREEN, FPSCLOCK
    # 初始化
    pygame.init()
    # 使用Python时钟控制每个循环多长时间运行一次，在使用时钟前必须先创建Clock对象的一个实例
    FPSCLOCK = pygame.time.Clock()
    # 创建一个窗体
    SCREEN = pygame.display.set_mode((SCREENWIDTH, SCREENHEIGHT))
    # 设置窗体标题
    pygame.display.set_caption("玛丽冒险")
    # 创建背景对象
    bg1 = MyMap(0, 0)
    bg2 = MyMap(800, 0)
    # 创建玛丽对象
    marie = Marie()
    # 添加障碍物的时间
    addObstacleTimer = 0
    # 障碍物对象列表
    obstacle_list = []
    # 创建背景音乐按钮对象
    music_button = Music_Button()
    # 设置背景音乐按钮的默认图片
    btn_img = music_button.open_img
    # 循环播放背景音乐
    music_button.bg_music.play(-1)
    while True:
        # 获取单击事件
        for event in pygame.event.get():
            # 判断鼠标事件
            if event.type == pygame.MOUSEBUTTONUP:
                # 判断鼠标是否在音乐按钮范围
                if music_button.is_select():
                    # 判断背景音乐状态
                    if music_button.is_open:
                        # 单击后显示关闭状态的图片
                        btn_img = music_button.close_img
                        # 关闭背景音乐状态
                        music_button.is_open = False
                        # 停止背景音乐的播放
                        music_button.bg_music.stop()
                    else:
                        btn_img = music_button.open_img
                        music_button.is_open = True
                        music_button.bg_music.play(-1)
            # 如果单击了关闭窗体就将窗体关闭
            if event.type == QUIT:
                # 退出窗口
                pygame.quit()
                # 关闭窗口
                sys.exit()
            # 按下键盘空格键，开启跳的状态
            if event.type == KEYDOWN and event.key == K_SPACE:
                # 如果玛丽在地面上（或地下）
                if marie.rect.y >= marie.lowest_y:
                    # 播放玛丽跳的音效
                    marie.jump_audio.play()
                    # 开启跳的状态
                    marie.jump()
                # 判断游戏结束的开关是否开启
                if over:
                    # 如果开启将调用mainGame方法重新启动游戏
                    mainGame()
        # 实现无限滚动的背景图
        if not over:
            # 绘制背景图，起到更新背景图的作用
            bg1.map_update()
            # 背景图移动
            bg1.map_rolling()
            bg2.map_update()
            bg2.map_rolling()
            # 玛丽移动
            marie.move()
            # 绘制玛丽
            marie.draw_marie()
            # 计算障碍物间隔时间
            if addObstacleTimer >= 1300:
                r = random.randint(0, 100)
                if r > 40:
                    # 创建障碍物对象
                    obstacle = Obstacle()
                    # 将障碍物对象添加到列表中
                    obstacle_list.append(obstacle)
                # 重置添加障碍物时间
                addObstacleTimer = 0
            # 循环遍历障碍物
            for i in range(len(obstacle_list)):
                # 障碍物移动
                obstacle_list[i].obstacle_move()
                # 绘制障碍物
                obstacle_list[i].draw_obstacle()
                # 判断小玛丽与障碍物是否碰撞
                if pygame.sprite.collide_rect(marie, obstacle_list[i]):
                    # 碰撞后开启结束开关
                    over = True
                    # 调用游戏结束的方法
                    game_over()
                    music_button.bg_music.stop()
                else:
                    # 判断小玛丽是否跃过了障碍物
                    if (obstacle_list[i].rect.x + obstacle_list[i].rect.width) <= marie.rect.x:
                        # 加分
                        score += obstacle_list[i].getScore()
                    # 显示分数
                    obstacle_list[i].showScore(score)
        # 增加障碍物时间
        addObstacleTimer += 20
        # 绘制背景音乐按钮
        SCREEN.blit(btn_img, (20, 20))
        # 更新整个窗体
        pygame.display.update()
        # 循环应该多长时间运行一次
        FPSCLOCK.tick(FPS)

# 定义一个移动地图类
class MyMap():
    def __init__(self, x, y):
        # 加载背景图片，定义X与Y的坐标
        self.bg = pygame.image.load("image/bg.png").convert_alpha()
        self.x = x
        self.y = y
    # 根据X坐标判断背景图片是否移出窗体
    def map_rolling(self):
        # 小于-790说明背景图已经完全移动完毕
        if self.x < -790:
            # 给背景图一个新的坐标点
            self.x = 800
        else:
            # 背景图每次向左移动五个像素
            self.x -= 5
    # 实现背景图无限滚动效果
    def map_update(self):
        SCREEN.blit(self.bg, (self.x, self.y))

# 玛丽类
class Marie():
    def __init__(self):
        # 初始化玛丽矩形
        self.rect = pygame.Rect(0, 0, 0, 0)
        # 跳跃的状态
        self.jumpState = False
        # 跳跃的高度
        self.jumpHeight = 130
        # 地面坐标，即跳跃后落地坐标
        self.lowest_y = 140
        # 跳跃增变量，既跳跃时向上或向下移动的速度，初始化为0
        self.jumpValue = 0
        # 玛丽动图索引
        self.marieIndex = 0
        self.marieIndexGen = cycle([0, 1, 2])
        # 加载玛丽图片
        self.adventure_img = (
            pygame.image.load("image/adventure1.png").convert_alpha(),
            pygame.image.load("image/adventure2.png").convert_alpha(),
            pygame.image.load("image/adventure3.png").convert_alpha()
        )
        # 跳跃音效
        self.jump_audio = pygame.mixer.Sound("audio/jump.wav")
        # 设置玛丽矩形的大小
        self.rect.size = self.adventure_img[0].get_size()
        # 确定玛丽矩形的x坐标
        self.x = 50
        # 确定玛丽矩形的y坐标
        self.y = self.lowest_y
        # 确定玛丽矩形在左上角显示的位置
        self.rect.topleft = (self.x, self.y)
    # 跳状态
    def jump(self):
        self.jumpState = True
    # 玛丽矩形移动
    def move(self):
        if self.jumpState:
            # 如果玛丽矩形站在地上，就向上移动（-5）像素
            if self.rect.y == self.lowest_y:
                self.jumpValue = -5
            # 如果玛丽矩形到达顶部，就向下移动（5）像素
            if self.rect.y == self.lowest_y - self.jumpHeight:
                self.jumpValue = 5
            # 改变玛丽矩形的y坐标
            self.rect.y += self.jumpValue
            # 判断玛丽矩形是否回到原位置（地面或地下）
            if self.rect.y == self.lowest_y:
                # 关闭跳跃状态
                self.jumpState = False
    # 绘制玛丽
    def draw_marie(self):
        # 匹配玛丽矩形动图
        self.marieIndex = next(self.marieIndexGen)
        # 绘制玛丽
        SCREEN.blit(self.adventure_img[self.marieIndex], (self.x, self.rect.y))

# 障碍物类
class Obstacle():
    # 通过一个障碍物所获得的分数
    score = 1
    # 障碍物移动距离
    move = 5
    # 障碍物的y坐标
    obstacle_y = 150
    def __init__(self):
        # 初始化障碍物矩形
        self.rect = pygame.Rect(0, 0, 0, 0)
        # 加载障碍物图片
        self.missile = pygame.image.load("image/missile.png").convert_alpha()
        self.pipe = pygame.image.load("image/pipe.png").convert_alpha()
        # 加载分数图片
        self.numbers = (
            pygame.image.load("image/0.png").convert_alpha(),
            pygame.image.load("image/1.png").convert_alpha(),
            pygame.image.load("image/2.png").convert_alpha(),
            pygame.image.load("image/3.png").convert_alpha(),
            pygame.image.load("image/4.png").convert_alpha(),
            pygame.image.load("image/5.png").convert_alpha(),
            pygame.image.load("image/6.png").convert_alpha(),
            pygame.image.load("image/7.png").convert_alpha(),
            pygame.image.load("image/8.png").convert_alpha(),
            pygame.image.load("image/9.png").convert_alpha()
        )
        # 加载加分音效
        self.score_audio = pygame.mixer.Sound("audio/score.wav")
        # 产生0和1的随机数，如果为0则产生导弹障碍物，否则产生管道障碍物
        r = random.randint(0, 1)
        if r == 0:
            # 显示导弹障碍
            self.image = self.missile
            # 导弹移动速度加快
            self.move = 15
            # 导弹y坐标在天上
            self.obstacle_y = 100
        else:
            # 显示管道障碍
            self.image = self.pipe
        # 根据障碍物图的宽、高来设置障碍物矩形
        self.rect.size = self.image.get_size()
        # 获取障碍物的宽、高
        self.width, self.height = self.rect.size
        # 确定障碍物在背景图上出现的坐标，center（中心点坐标）
        self.x = 800
        self.y = self.obstacle_y
        self.rect.center = (self.x, self.y)
    # 障碍物移动
    def obstacle_move(self):
        self.rect.x -= self.move
    # 绘制障碍物
    def draw_obstacle(self):
        SCREEN.blit(self.image, (self.rect.x, self.rect.y))
    # 获取分数
    def getScore(self):
        tmp = self.score
        if tmp == 1:
            # 播放加分音效
            self.score_audio.play()
        self.score = 0
        return tmp
    # 显示分数
    def showScore(self, score):
        # 获取得分数字
        self.scoreDigits = [int(x) for x in list(str(score))]
        # 要显示的所有数字的总宽度
        totalWidth = 0
        for digit in self.scoreDigits:
            # 获取积分图片的宽度
            totalWidth += self.numbers[digit].get_width()
        # 分数横向位置
        Xoffset = (SCREENWIDTH - (totalWidth + 30))
        for digit in self.scoreDigits:
            # 绘制分数
            SCREEN.blit(self.numbers[digit], (Xoffset, SCREENHEIGHT * 0.1))
            # 随着数字增加改变位置
            Xoffset += self.numbers[digit].get_width()

# 背景音乐按钮
class Music_Button():
    # 背景音乐的状态，True播放，False暂停
    is_open = True
    def __init__(self):
        # 背景音乐开启图片
        self.open_img = pygame.image.load("image/btn_open.png").convert_alpha()
        # 背景音乐关闭图片
        self.close_img = pygame.image.load("image/btn_close.png").convert_alpha()
        # 加载bgm
        self.bg_music = pygame.mixer.Sound("audio/bg_music.wav")
    # 判断鼠标是否在按钮范围内
    def is_select(self):
        # 获取鼠标的坐标
        point_x, point_y = pygame.mouse.get_pos()
        # 获取按钮图片的大小
        w, h = self.open_img.get_size()
        # 判断鼠标是否在按钮范围内
        return 20 < point_x < 20 + w and 20 < point_y < 20 + h

if __name__ == '__main__':
    mainGame()