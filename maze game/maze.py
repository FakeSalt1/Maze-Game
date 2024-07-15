from pygame import*
import random
window_width = 1024
window_height = 768
window = display.set_mode((window_width,window_height))
hp =100

font.init()
style = font.SysFont(None,50)

bg = transform.scale(image.load("background.jpg"),(window_width,window_height))

class Character():
    def __init__(self,filename,size_x,size_y,pos_x,pos_y, speed):
        self.filename = filename
        self.size_x = size_x
        self.size_y = size_y
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.speed = speed
        self.image = transform.scale(image.load(self.filename),(self.size_x, self.size_y))
        self.rect = self.image.get_rect()
        self.rect.x = pos_x
        self.rect.y = pos_y
    def show(self):
        window.blit(self.image, (self.rect.x,self.rect.y))
class Wall(Character):
    def __init__(self,size_x,size_y,pos_x,pos_y):
        
        self.size_x = size_x
        self.size_y = size_y
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.image = Surface((size_x, size_y))
        self.image.fill((89, 63, 13))
        self.rect = self.image.get_rect()
        self.rect.x = pos_x
        self.rect.y = pos_y
player1 = Character("hero.png",100,100,50,670,5)
player2 = Character("cyborg.png",100,100,300,300,5)
treasure = Character("treasure.png",100,100,900,670,0)
rocks = Character("rocks.png",200,120,400, 500, 0)


clock = time.Clock()
fps = 60
game = True
finish = False

#w1 = Wall(50,900,200,100)
#w2 = Wall(50,900,500,-300)
#w3 = Wall(50,900,900,100)
wall_list= []
wall_list.append(Wall(50,900,200,100))
wall_list.append(Wall(50,900,400,-300))
wall_list.append(Wall(250,50,550,100))
wall_list.append(Wall(250,50,450,250))
wall_list.append(Wall(50,900,800,100))




route_list = []
for i in range(6):
    x = random.randint(0,window_width-100)
    y = random.randint(0,window_height-100)
    route_list.append((x,y))
print(route_list)

route = 0
ok_x = False
ok_y =  False

while game:
    window.blit(bg,(0,0))
    for e in event.get():
        if e.type == QUIT:
            game = False
    if finish == False:
        safety_x = player1.rect.x
        safety_y = player1.rect.y
        keys_pressed = key.get_pressed()
        if keys_pressed[K_w] and player1.rect.y > 0:
            player1.rect.y -= player1.speed
        elif keys_pressed[K_d] and player1.rect.x < window_width-player1.size_x:
            player1.rect.x  += player1.speed
        elif keys_pressed[K_a] and player1.rect.x >  0:
            player1.rect.x  -= player1.speed
        elif keys_pressed[K_s] and player1.rect.y <window_height-player1.size_y:
            player1.rect.y  += player1.speed
        for wall in wall_list:
            isCollide = sprite.collide_rect(player1,wall)
            if isCollide:
                player1.rect.x = safety_x
                player1.rect.y = safety_y
        

        goto_x, goto_y= route_list [route]
        if (ok_x == False):
            d = abs(player2.rect.x - goto_x)
            if (player2.rect.x - goto_x):
                player2.rect.x += min(player2.speed, d)
            elif (player2.rect.x > goto_x): 
                player2.rect.x -= min(player2.speed, d)
                ok_x = True
        if (ok_y == False):
            d = abs(player2.rect.y - goto_y)
            if (player2.rect.y < goto_y):
                player2.rect.y += min(player2.speed, d)
            elif (player2.rect.y > goto_y): 
                player2.rect.y -= min(player2.speed, d)
            else:
                ok_y = True   
        if (ok_x== True and ok_y == True):
            route += 1
            ok_x = False
            ok_y = False
            if (route == len(route_list)): 
                route = 1
        


        
        iscollide = sprite.collide_rect(player1,player2)
        if iscollide:
            print("YOU WERE HURT BY CYBROG")
            hp -= 40 
            player1.rect.x = 50
            player1.rect.y = 670
        iscollide = sprite.collide_rect(player1,rocks)
        if iscollide:
            hp -= 10            
            print("YOU WERE HURT BY ROCKS")
            player1.rect.y = 670
                            
        iscollide = sprite.collide_rect(player1,treasure)
        if iscollide:
            finish = True
    else:
        if hp <= 0:
            text_END = style.render("YOU LOSE", True, (225,225,225))
        else:
            text_END = style.render("YOU WIN", True, (225,225,225))
        window.blit(text_END,(200,200))

    text_hp = style.render("HP:"+str(hp), True, (225,225,225))
    window.blit(text_hp,(10,10))
    player1.show()
    player2.show()
    treasure.show()
    rocks.show()



    for wall in wall_list:
        wall.show()
    display.update()
    clock.tick(fps)