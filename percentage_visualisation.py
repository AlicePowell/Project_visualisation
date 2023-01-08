
import pygame as py
import random
import math
from pygame.locals import (K_ESCAPE, KEYDOWN)


def percentage_visualisation(percentage):
    py.init()  # initialize pygame  
        
    # introduce time
    clock = py.time.Clock()  
    py.time.set_timer(py.USEREVENT, 10)
    FPS = 20  
    delay = True

    # create screen
    WIDTH, HEIGHT = 1000, 800
    MID_HEIGHT = (HEIGHT//2)
    screen = py.display.set_mode((WIDTH , HEIGHT)) 
    py.display.set_caption("press Escape to close screen") 
    
    # Use Exception Handling in case the background image doesn't load
    BLACK, CORAL, DUSK, PALE = (0, 0, 0), ('#ffd6d1'), ('#5f7285'), ('#FCFFFA')
    try: 
        background_image = py.image.load("bleached_sunset3.jpg").convert()
        background_image = py.transform.scale(background_image, (WIDTH, HEIGHT))
        key = 'hasimage'
    except FileNotFoundError:
        key = 'noimage'


    # basic block template
    block_size = 34
    image_orig = py.Surface((block_size, block_size)).convert()
    image_orig.set_colorkey(BLACK) 
    image_orig.fill(DUSK)  
    image_orig.fill(BLACK, image_orig.get_rect().inflate(-2, -2.5))


    class Block(py.sprite.Sprite):
        def __init__(self, x, y, angle, speed):
            super().__init__()
            self.image = image_orig.copy()
            self.colour = ""
            self.image.set_colorkey(BLACK)  
            self.rect = self.image.get_rect()
            self.center = (WIDTH - 800 + x, MID_HEIGHT - 268 + y) 
            self.bottomleft = (WIDTH - 800 - (block_size/2) + x) , (MID_HEIGHT - 268 + (block_size/2) + y)
            self.rot = 0
            self.rot_speed = speed # speed - a random integer between 1 and 4
            self.angle = angle # angle - potential rotation range
            self.rot_amount = random.randrange(0, angle + 3) # Generates a random final rotation within the given range

        def update(self):
            if self.angle == 270 or self.angle == 0:
                self.rot_amount = 0 
            self.rot = (self.rot + self.rot_speed) % 360
            
            # ensure the dysfunctional rotating blocks stop at the right point
            if self.rot > (self.rot_amount + 270):
                self.rot = self.rot_amount
                self.rot_speed = 0
    

    ######
    ### Create 2 grids of blocks to rotate ###
    a, b = 8, 16  # a = number of grid columns, b = number of grid rows
    target_percentage = 51  

    # Two sprite Groups - one for target percentage & one for actual percentage     
    block_list_target = py.sprite.Group() 
    block_list = py.sprite.Group()

    # call function for a list of x coordinate, y coordinate, range of rotation
    position_list = create_blockgrid(percentage, target_percentage, a, b, block_size)

    # populate the 2 Sprite groups with blocks  
    # Info required:  [x coordinate, y coordinate, range of rotation, rotation speed]
    target_blocks = [Block(position_list[i][0], position_list[i][1], 270, 2) for i in range(a*b)]
    for entry in target_blocks:
        block_list_target.add(entry)
    blocks = [Block(position_list[i][0] + 360, position_list[i][1], position_list[i][2], random.uniform(1,4)) for i in range(a*b)]
    for entry in blocks:
        block_list.add(entry)

    ######


    # labels - if font not available on the users system it will use the default Pygame font
    myfont = py.font.SysFont("arial", 15)
    creditfont = py.font.SysFont("arial", 12)
    titlelabela = myfont.render(f"We want {target_percentage}% of the Tech Industry to be made up of strong, brilliant, creative, innovative WOMEN", True, (DUSK))
    titlelabelb = myfont.render(f"How perfect that would feel!", True, (DUSK))
    label1 = myfont.render(f"Imagine {target_percentage}% of the UK Tech workforce were women...", True, (DUSK))
    label2 = myfont.render(f" but sadly today only {percentage}% are women", True, (DUSK))
    creditlabel = creditfont.render("Designed and coded by Alice Powell, November 2022.  Inspired by Georg Nees, 'Schotter', 1968", True, (PALE))
   

    
    ### Animate the visualisation ###
    running = True  
    while running:  
        py.display.init()
        clock.tick(FPS)  
        
        if key == 'hasimage':
            screen.blit(background_image, [0, 0])
        else:
            screen.fill(CORAL)

        screen.blit(titlelabela, (WIDTH - 819, 25))
        screen.blit(titlelabelb, (WIDTH - 819, 45))
        screen.blit(label1, (WIDTH - 820, (MID_HEIGHT) + 320))
        screen.blit(label2, (WIDTH - 423, (MID_HEIGHT) + 320))
        screen.blit(creditlabel, (20, HEIGHT - 21))

        # check for the exit  
        for event in py.event.get():  
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    running = False
            elif event.type == py.QUIT:  
                running = False  
        
        # blocks
        block_list.update()
        for i in blocks:       
            if i.angle == 0:           
                old_center = i.center
                new_image = py.transform.rotate(image_orig, i.rot)    
                i.rect = new_image.get_rect()
                i.rect.center = old_center
            else:
                old_bottomleft = i.bottomleft
                new_image = py.transform.rotate(image_orig, i.rot) 
                i.rect = new_image.get_rect()  
                i.rect.bottomleft = old_bottomleft
            screen.blit(new_image, i.rect) 

        block_list_target.update()
        for i in target_blocks:
            old_center = i.center
            new_image = py.transform.rotate(image_orig, i.rot)    
            i.rect = new_image.get_rect()
            i.rect.center = old_center
            screen.blit(new_image, i.rect) 
            
        py.display.update()

        if delay:
            py.time.delay(400)
            delay = False
        
    py.display.quit
    return percentage



### Function create_blockgrid ###
# produces an embedded list
# containing for each block in an a*b grid:
# the position coordinates and the rotation range 

# No. of rows rotated reflects the difference between the actual percentage and the target percentage 
# the range of rotation for upper rows also reflects the size of the percentage difference
# Therefore the lower the actual percentage the more dysfunctional the final grid will appear

def create_blockgrid(percentage, target_percentage, a, b, block_size):
 
    position_list = [[(x * block_size) + x, (y * block_size) + y] for y in range(b) for x in range(a)]
    percentage = min(percentage, 51)

    # calculate k - the number of rows to rotate - 
    k = min(math.ceil((target_percentage - percentage) / (target_percentage / b)* 1.08), b)   # (*1.08) is an aesthetic calculation 
    
    # create a list of all potential degrees of rotation ranges for 'b' rows of blocks.              
    poss_rotation_list = [(int((90/b)*i)) for i in range(0,b+1)]  
    
    # add the row rotation ranges to each entry in the position_list
    count = 0
    for i in range(b):
        for j in range(a):
            position_list[count].append(poss_rotation_list[k])
            count +=1
        if k > 0:
            k -= 1
    
    return (position_list)


# Add unit test to check if works for 51% and 1% and 60% - tick
# Backgroud image loading
# No font

# Call function
percentage_visualisation(13)

