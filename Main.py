import pygame
import os

pygame.init()

WIDTH, HEIGHT= 1000,500
FPS= 60

pygame.display.set_caption("Project Z")
win= pygame.display.set_mode((WIDTH,HEIGHT))

clock= pygame.time.Clock()

bg_img= pygame.image.load('Assets\Background\BG1.png')
bg= pygame.transform.scale(bg_img, (WIDTH, HEIGHT))
i = 0



idlle =  [pygame.image.load(os.path.join("Assets\Characters\Hero\Black\Idlle", "Black_Idle1.png")),
         pygame.image.load(os.path.join("Assets\Characters\Hero\Black\Idlle", "Black_Idle2.png")),
         pygame.image.load(os.path.join("Assets\Characters\Hero\Black\Idlle", "Black_Idle3.png")),
         pygame.image.load(os.path.join("Assets\Characters\Hero\Black\Idlle", "Black_Idle4.png")),
         pygame.image.load(os.path.join("Assets\Characters\Hero\Black\Idlle", "Black_Idle5.png")),]
       

left = [None]*7
for picIndex in range(1,7):
    left[picIndex-1] = pygame.image.load(os.path.join("Assets\Characters\Hero\Black\Running", "Black_Run_L" + str(picIndex) + ".png"))
    picIndex+=1

right = [None]*7
for picIndex in range(1,7):
    right[picIndex-1] = pygame.image.load(os.path.join("Assets\Characters\Hero\Black\Running", "Black_Run_R" + str(picIndex) + ".png"))
    picIndex+=1

bullet_img = pygame.transform.scale(pygame.image.load(os.path.join("Assets\Objects", "Bullet.png")), (20, 20))


class Hero:
    def __init__(self, x, y):
        #walk
        self.x = x
        self.y = y
        self.velx = 3
        self.vely = 15
        self.face_right = True
        self.face_left = False
        self.idlle = True
        self.stepIndex = 0
        self.idlleIndex = 0
        #jump
        self.jump = False
        #bullet
        self.bullets = []
        self.cool_down_count = 0

    def move_hero(self, userInput):
        if userInput [pygame.K_RIGHT] and self.x < 925:
            self.x += self.velx
            self.face_right = True
            self.face_left = False
            self.idlle = False
        elif userInput [pygame.K_LEFT] and self.x > 10:
            self.x -= self.velx
            self.face_right = False
            self.face_left = True
            self.idlle = False
        else :
            self.stepIndex = 0
            self.face_left = False
            self.face_right = False
            self.idlle = True
            
    def draw(self, win):
        if self.stepIndex >= 24:
         self.stepIndex = 0

        if self.idlleIndex >= 25:
            self.idlleIndex = 0

        if self.face_left:
            win.blit(left[self.stepIndex//4], (self.x, self.y))
            self.stepIndex += 1
        elif self.face_right:
            win.blit(right[self.stepIndex//4], (self.x, self.y))
            self.stepIndex += 1
        else :
            win.blit(idlle[self.idlleIndex//5], (self.x, self.y))  
            self.idlleIndex += 1     

    def jump_motion(self, userInput):
     if userInput[pygame.K_UP] and self.jump is False:
            self.jump = True
     if self.jump:
            self.y -= self.vely
            self.vely -= 1
     if self.vely < -15:
            self.jump = False
            self.vely = 15

    def direction(self):
        if self.face_right or self.idlle :
            return 1
        if self.face_left :
            return -1

    def cooldown(self):
        if self.cool_down_count >= 20:
            self.cool_down_count = 0
        elif self.cool_down_count > 0:
            self.cool_down_count += 1
        
    def shoot(self):
        self.cooldown()

        if (userInput[pygame.K_SPACE] and self.cool_down_count == 0):
            bullet = Bullet(self.x, self.y, self.direction())
            self.bullets.append(bullet)
            self.cool_down_count = 1
        for bullet in self.bullets:
            bullet.move()
            if bullet.off_screen():
                self.bullets.remove(bullet)
    

class Bullet:
    def __init__(self, x, y, direction) :
        self.x = x + 63
        self.y = y + 33
        self.direction = direction

    def draw_bullet(self):
        win.blit(bullet_img, (self.x, self.y))
    
    def move(self):
        if self.direction == 1:
            self.x += 15
        if self.direction == -1:
            self.x -= 15
    
    def off_screen(self):
        return not(self.x >= 0 and self.x <= WIDTH)





def draw_game():
    win.fill((0, 0, 0))

    win.blit(bg, (i,0))
    win.blit(bg, (WIDTH+i, 0))
    

    for bullet in player.bullets:
        bullet.draw_bullet()

    player.draw(win)
    clock.tick(FPS)
    pygame.display.update()

player = Hero(0 , 380)

run= True
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    

    userInput = pygame.key.get_pressed()
    
    if i == -1000:
        win.blit(bg, (WIDTH+i, 0))
        i = 0
    i -= 1

    #shoot
    player.shoot()

    # Movement
    player.move_hero(userInput)
    player.jump_motion(userInput)



    draw_game()