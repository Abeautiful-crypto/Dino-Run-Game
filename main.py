#导入的模块
import pygame #游戏引擎
import os #读写文件
import random #随机数

pygame.init() #初始化游戏引擎

# 把资源路径锚定到本文件所在目录，避免运行时因工作目录不同找不到图片
# 注意：main.py 本身就在 Assects 文件夹里，图片相对它就是 Dino/、Cactus/ 等，不需要再拼一层 Assects
ASSETS = os.path.dirname(os.path.abspath(__file__))

#全局
SCREEN_HEIGHT =600 #游戏界面的高
SCREEN_WIDTH =1100 #游戏界面的宽
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT)) #SCREEN 是 pygame 的“画布”，后面所有的 blit()（贴图）都画在它上面。

#加载游戏中使用的图像资源
def load_images():
    #奔跑
    running = [pygame.image.load(os.path.join(ASSETS,"Dino","pao","Chrome_T-Rex_Left_Run.png")),
               pygame.image.load(os.path.join(ASSETS,"Dino","pao","Chrome_T-Rex_Right_Run.png"))] #存了恐龙奔跑的两帧，实现了奔跑的效果
    #跳跃
    jumping =  [pygame.image.load(os.path.join(ASSETS,"Dino","pao","Chrome_T-Rex_Left_Run.png"))]
    #下蹲
    ducking =  [pygame.image.load(os.path.join(ASSETS,"Dino","dun","Chrome_T-Rex_Left_Duck.png")),
               pygame.image.load(os.path.join(ASSETS,"Dino","dun","Chrome_T-Rex_Right_Duck.png"))]
    #小仙人掌
    small_cactus =  [pygame.image.load(os.path.join(ASSETS,"Cactus","1_Cactus_Chrome_Dino.png"))]
    #大仙人掌
    large_cactus = [pygame.image.load(os.path.join(ASSETS,"Cactus","3_Cactus_Chrome_Dino.png"))]
    #翼龙
    bird = [pygame.image.load(os.path.join(ASSETS,"Cactus","Chrome_Pterodactyl.png"))]
    #白云
    cloud = [pygame.image.load(os.path.join(ASSETS,"Other","Chromium_T-Rex-cloud.png"))]
    #背景
    bg = [pygame.image.load(os.path.join(ASSETS,"Other","Chromium_T-Rex-horizon.png"))]

    return running, jumping, ducking, small_cactus, large_cactus, bird, cloud, bg

RUNNING, JUMPING, DUCKING ,SMALL_CACTUS,LARGE_CACTUS,BIRD,CLOUD,BG = load_images()
#将上面的图片设置为全局常量

#定义小恐龙
class Dinosaur:
    X_POS = 80 #恐龙的X坐标
    Y_POS = 310#恐龙的Y坐标
    Y_POS_DUCK = 340 #恐龙下蹲的Y坐标
    JUMP_VEL = 8.5 #恐龙初始跳跃速度

    def __init__(self):
        #将下蹲，奔跑，跳跃这三个属性加到恐龙自身上，因为DUCKING是全局常量，游戏操作的是小恐龙本身
        self.duck_img = DUCKING
        self.run_img = RUNNING
        self.jump_img = JUMPING
#恐龙的状态，是什么状态，哪个状态就为True
        self.dino_duck = False
        self.dino_run = True
        self.dino_jump = False

        self.step_index=0
        self.jump_vel= self.JUMP_VEL
        self.image=self.run_img[0]
        self.dino_rect = self.image.get_rect()
        self.dino_rect.x = self.X_POS
        self.dino_rect.y = self.Y_POS

        self.collision_rect = pygame.Rect(
            self.dino_rect.x+15,
            self.dino_rect.y+10,
            self.dino_rect.width-30,
            self.dino_rect.height-10
        )

    def update(self,userInput):
            if self.dino_duck:
                self.duck()
            if self.dino_run:
                self.run()
            if self.dino_jump:
                self.jump()

            if self.step_index>=10:
                self.step_index=0

            if userInput[pygame.K_UP] and not self.dino_jump:
                self.dino_duck = False
                self.dino_run = False
                self.dino_jump = True
            elif userInput[pygame.K_DOWN] and not self.dino_jump:
                self.dino_duck = True
                self.dino_run = False
                self.dino_jump = False
            elif not (self.dino_jump or userInput[pygame.K_DOWN]):
                self.dino_duck = False
                self.dino_run = True
                self.dino_jump = False

            self._update_collision_rect()
              #处理碰撞体积
    def _update_collision_rect(self):
            if self.dino_duck:
                self.collision_rect.x = self.dino_rect.x+20
                self.collision_rect.y = self.dino_rect.y+15
                self.collision_rect.width = self.dino_rect.width-40
                self.collision_rect.height = self.dino_rect.height-15
            else:
                self.collision_rect.x = self.dino_rect.x+15
                self.collision_rect.y = self.dino_rect.y+10
                self.collision_rect.width = self.dino_rect.width-30
                self.collision_rect.height = self.dino_rect.height-10
              #处理恐龙下蹲动作
    def duck(self):
            self.image = self.duck_img[self.step_index // 5]
            self.dino_rect = self.image.get_rect()
            self.dino_rect.x = self.X_POS
            self.dino_rect.y = self.Y_POS_DUCK
            self.step_index+=1
            # 处理恐龙奔跑动作
    def run(self):
            self.image = self.run_img[self.step_index // 5] #换帧（恐龙奔跑是有两张图片，来回切换就实现了奔跑效果）
            self.dino_rect = self.image.get_rect()
            self.dino_rect.x = self.X_POS
            self.dino_rect.y = self.Y_POS
            self.step_index+=1
            # 处理恐龙跳跃动作
    def jump(self):
           self.image = self.jump_img[0]  # jump_img 是列表，取第一张图
           if self.dino_jump:
               self.dino_rect.y -= self.jump_vel*4   # 每帧上升
               self.jump_vel -= 0.8                 # 速度递减（模拟重力减速）
               # 落回地面位置 Y_POS 时才结束跳跃，而不是第一帧就取消
               if self.dino_rect.y >= self.Y_POS:
                   self.dino_rect.y = self.Y_POS
                   self.dino_jump = False
                   self.jump_vel = self.JUMP_VEL
         #在屏幕中绘制小恐龙
    def draw(self,SCREEN):
            SCREEN.blit(self.image,(self.dino_rect.x,self.dino_rect.y)) #将这一帧贴到游戏中,self.image是贴的图片，后面是位置


 #定义白云
class Cloud:
    def __init__(self):
        self.x = SCREEN_WIDTH + random.randint(800,1000)
        self.y = random.randint(50,100)
        self.image = CLOUD[0]  # CLOUD 是列表，取第一张图
        self.width = self.image.get_width()
        #更新白云的位置
    def update(self):
        self.x -= game_speed
        if self.x < -self.width:
            self.x = SCREEN_WIDTH + random.randint(2500,3000)
            self.y = random.randint(50,100)
    #绘制屏幕中的云
    def draw(self,SCREEN):
        SCREEN.blit(self.image,(self.x,self.y))

#定义障碍物
class Obstacle:
    def __init__(self,image,type):
        self.image = image
        self.type = type
        self.rect = self.image[self.type].get_rect()
        self.rect.x = SCREEN_WIDTH

        #碰撞体积
        self.collision_rect = pygame.Rect(
            self.rect.x + 10,
            self.rect.y + 5,
            self.rect.width - 20,
            self.rect.height - 10
        )
        #更新障碍物的位置
    def update(self,):
        self.rect.x -= game_speed
        self.collision_rect.x = self.rect.x + 10

        #绘制障碍物
    def draw(self,SCREEN):
        SCREEN.blit(self.image[self.type],self.rect)

#定义小仙人掌
class SmallCactus(Obstacle):
    def __init__(self, image):
        self.type = random.randint(0, len(image)-1)
        super().__init__(image, self.type)
        self.rect.y = 325

        self.collision_rect = pygame.Rect(
            self.rect.x + 8,
            self.rect.y + 5,
            self.rect.width - 16,
            self.rect.height - 5
        )
#定义大仙人掌
class LargeCactus(Obstacle):
    def __init__(self, image):
        self.type = random.randint(0, len(image)-1)
        super().__init__(image, self.type)
        self.rect.y = 300

        self.collision_rect = pygame.Rect(
            self.rect.x + 10,
            self.rect.y + 5,
            self.rect.width - 20,
            self.rect.height - 5
        )

#定义翼龙
class BirdCactus(Obstacle):
    def __init__(self, image,):
        self.type = 0
        super().__init__(image, self.type)
        self.rect.y = 200
        self.index = 0
        self.collision_rect = pygame.Rect(
            self.rect.x + 12,
            self.rect.y + 10,
            self.rect.width - 24,
            self.rect.height - 15
        )

    def draw(self,SCREEN):
        if self.index >= 9:
            self.index = 0
        # 对图片数量取模，有几帧就循环几帧，避免越界
        SCREEN.blit(self.image[self.index // 5 % len(self.image)],self.rect)
        self.collision_rect.x = self.rect.x + 12
        self.index += 1
def main():
    global game_speed,x_pos_bg,y_pos_bg,points,obstacles
    run = True
    clock = pygame.time.Clock()
    player = Dinosaur()
    cloud = Cloud()
    game_speed = 20 #初始速度
    x_pos_bg = 0
    y_pos_bg = 380
    points = 0
    font = pygame.font.Font(pygame.font.get_default_font(), 20)
    obstacles = []
    death_count = 0

    #得分函数
    def score():
        global points, game_speed
        points += 1
        if points %100 ==0:#每得100分，速度加1
            game_speed += 1

        text = font.render("Points: "+ str(points),True,(0,0,0))
        textRect = text.get_rect()
        textRect.center = (1000,40)
        SCREEN.blit(text,textRect)

    #背景滚动函数
    def background():
        global x_pos_bg,y_pos_bg
        image_wight = BG[0].get_width()
        SCREEN.blit(BG[0],(x_pos_bg,y_pos_bg))
        SCREEN.blit(BG[0],(image_wight+x_pos_bg,y_pos_bg))
        if x_pos_bg <= -image_wight:
            x_pos_bg = 0
        x_pos_bg -=game_speed

    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        SCREEN.fill((255,255,255))
        userInput = pygame.key.get_pressed()

        player.draw(SCREEN)
        player.update(userInput)

        if len(obstacles)==0:
            rand = random.randint(0,3)
            #随机生成障碍物
            if rand == 0:
              obstacles.append(SmallCactus(SMALL_CACTUS))#小仙人掌
            elif rand == 1:
               obstacles.append(LargeCactus(LARGE_CACTUS))#大仙人掌
            elif rand == 2:
                obstacles.append(BirdCactus(BIRD))#翼龙

        for obstacle in obstacles:
            obstacle.draw(SCREEN)
            obstacle.update()
            if obstacle.rect.x < -obstacle.rect.width:
                obstacles.remove(obstacle)

            if player.collision_rect.colliderect(obstacle.collision_rect):
                pygame.time.delay(2000)
                death_count += 1
                menu(death_count)

        background()

        cloud.draw(SCREEN)
        cloud.update()

        score()

        clock.tick(30)#帧数30帧
        pygame.display.update()


#菜单函数
def menu(death_count):
    global points,obstacles,text
    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
            elif event.type == pygame.KEYDOWN:
                points = 0
                obstacles = []
                main()

                SCREEN.fill((255,255,255))
                font = pygame.font.Font(pygame.font.get_default_font(), 20)

                if death_count == 0:
                    text = font.render("Press any key to start",True,(0,0,0))
                elif death_count > 0:
                    text = font.render("Press any key to Restart",True,(0,0,0))
                    score = font.render("YOU Score:" + str(points),True,(0,0,0))
                    scoreRect = score.get_rect()
                    scoreRect.center = (SCREEN_WIDTH // 2,SCREEN_HEIGHT // 2 + 50)
                    SCREEN.blit(score,scoreRect)
                    textRect = text.get_rect()
                    textRect.center = (SCREEN_WIDTH // 2,SCREEN_HEIGHT // 2)
                    SCREEN.blit(text,textRect)
                    SCREEN.blit(RUNNING[0],(SCREEN_WIDTH // 2 - 20,SCREEN_HEIGHT // 2 - 140))
                    pygame.display.update()


menu(death_count=0)


