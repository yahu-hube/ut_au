import pygame, asyncio
import os
import time

pygame.font.init()
pygame.mixer.init()

WIDTH, HEIGHT = 1800, 1000
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("first au v.0.1")

WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
SKY_BLUE = (150, 150, 255)
GREEN = (0, 255, 0)

map_border = WIDTH//2 - 5, 0, 10, HEIGHT
BORDER = map_border 


#MUSIC
#ENEMY_APPROACHING = 


TEXT_FONT = pygame.font.SysFont('dmsans', 100)

FPS = 250
VEL = 1.2
VEL_FACTOR = 2
CUR_VEL = VEL
FRISK_WIDTH, FRISK_HEIGHT = 80, 120
FRISK_LR_WIDTH, FRISK_LR_HEIGHT = 73, 120

ENCOUTER_MONSTER = pygame.USEREVENT +1

FRISK = pygame.image.load(os.path.join('resources', 'frisk.png'))
FRISK_LEFT = pygame.image.load(os.path.join('resources', 'frisk_left.png'))
FRISK_RIGHT = pygame.image.load(os.path.join('resources', 'frisk_right.png'))
FRISK_BACK = pygame.image.load(os.path.join('resources', 'frisk_back.png'))

FRISK = pygame.transform.rotate(pygame.transform.scale(FRISK,(FRISK_WIDTH, FRISK_HEIGHT)), 0)
FRISK_LEFT = pygame.transform.rotate(pygame.transform.scale(FRISK_LEFT,(FRISK_LR_WIDTH, FRISK_LR_HEIGHT)), 0)
FRISK_RIGHT = pygame.transform.rotate(pygame.transform.scale(FRISK_RIGHT,(FRISK_LR_WIDTH, FRISK_LR_HEIGHT)), 0)
FRISK_BACK = pygame.transform.rotate(pygame.transform.scale(FRISK_BACK,(FRISK_WIDTH, FRISK_HEIGHT)), 0)

SPAWN_ROOM_BACKGROUND = pygame.image.load(os.path.join('resources', 'spawn_room_background.png'))

temp_rate = HEIGHT / SPAWN_ROOM_BACKGROUND.get_width()
SPAWN_ROOM_BACKGROUND = pygame.transform.rotate(pygame.transform.scale(SPAWN_ROOM_BACKGROUND, (WIDTH, HEIGHT * temp_rate)), 0)

player_rect = pygame.Rect(WIDTH//2, HEIGHT//2, FRISK_WIDTH, FRISK_HEIGHT)
player_direction_image = FRISK

joystick_rect = pygame.Rect(1450, 650, 280, 280)
joystick_inner_rect = pygame.Rect(1550, 750, 80, 80)
joystick_outofbox_x = False
joystick_outofbox_y = False
mouse_dragging_joystick = False

screen_rect = pygame.Rect(0, 0, WIDTH, HEIGHT)

mouse_buttons = pygame.mouse.get_pressed()

WIN.fill(SKY_BLUE)
pygame.display.update()

def player_handle_movement(keys_pressed, player_rect, CUR_VEL):
    if keys_pressed[pygame.K_LEFT] or keys_pressed[pygame.K_a]: # LEFT
        if keys_pressed[pygame.K_x]:
            CUR_VEL = VEL_FACTOR * VEL
        else:
            CUR_VEL = VEL
        player_rect.x -= CUR_VEL
        return "left"
    if keys_pressed[pygame.K_RIGHT] or keys_pressed[pygame.K_d]: # RIGHT
        if keys_pressed[pygame.K_x]:
            CUR_VEL = VEL_FACTOR * VEL
        else:
            CUR_VEL = VEL
        player_rect.x += CUR_VEL
        return "right"
    if keys_pressed[pygame.K_UP] or keys_pressed[pygame.K_w]: # UP
        if keys_pressed[pygame.K_x]:
            CUR_VEL = VEL_FACTOR * VEL
        else:
            CUR_VEL = VEL
        player_rect.y -= CUR_VEL
        return "up"
    if keys_pressed[pygame.K_DOWN] or keys_pressed[pygame.K_s]: # DOWN
        if keys_pressed[pygame.K_x]:
            CUR_VEL = VEL_FACTOR * VEL
        else:
            CUR_VEL = VEL
        player_rect.y += CUR_VEL
        return "back"

def joystick_handle_movement(joystick_rect, joystick_inner_rect, joystick_outofbox_x, joystick_outofbox_y):   
    global  mouse_dragging_joystick
    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = event.pos
            '''
            if mouse_x > joystick_rect.x and mouse_x < joystick_rect.x + 280:
                mouse_dragging_joystick = True
            else:
                joystick_inner_rect.x = 1550
                joystick_inner_rect.y = 750
                
            if mouse_dragging_joystick == True:
                mouse_x = joystick_inner_rect.x + 40
                mouse_y = joystick_inner_rect.y + 40
                if mouse_x < joystick_rect.x:
                    joystick_outofbox_x = True
                if mouse_x > joystick_rect.x + 280:
                        joystick_outofbox_x = True
                if mouse_y < joystick_rect.y or mouse_y > joystick_rect.y + 280:
                    joystick_outofbox_y = True
                '''
            joystick_inner_rect.x, joystick_inner_rect.y = 1550, 850
            #if joystick_outofbox_x == True:
            #    joystick_inner_rect.x = 
                
        elif event.type == pygame.MOUSEBUTTONUP:
            joystick_inner_rect.x = 1550
            joystick_inner_rect.y = 750
        
        elif event.type == pygame.FINGERDOWN:
            mouse_x, mouse_y = event.pos
            
            if mouse_x > joystick_rect.x and mouse_x < joystick_rect.x + 280:
                mouse_dragging_joystick = True
            else:
                joystick_inner_rect.x = 1550
                joystick_inner_rect.y = 750
                
            if mouse_dragging_joystick == True:
                mouse_x = joystick_inner_rect.x + 40
                mouse_y = joystick_inner_rect.y + 40
                if mouse_x < joystick_rect.x or mouse_x > joystick_rect.x + 280:
                    joystick_outofbox_x = True
                if mouse_y < joystick_rect.y or mouse_y > joystick_rect.y + 280:
                    joystick_outofbox_y = True
                #if joystick_outofbox_x == True:
                #    joystick_inner_rect.x = mouse_x, mouse_y = event.pos
                
        elif event.type == pygame.FINGERUP:
            joystick_inner_rect.x = 1550
            joystick_inner_rect.y = 750
        
    
def draw_window(player_rect, image, joystick_rect, screen_rect, joystick_inner_rect):
    WIN.fill(SKY_BLUE)
    
    #WIN.blit(SPAWN_ROOM_BACKGROUND, (0, 0)) 
    
    dirty_rect = pygame.Rect(player_rect.x - 7, player_rect.y - 7, FRISK_WIDTH + 14, FRISK_HEIGHT + 14)
    
    WIN.fill(SKY_BLUE, dirty_rect)
    WIN.blit(image, player_rect)
    
    WIN.fill(BLACK, joystick_rect) 
    WIN.fill(WHITE, joystick_inner_rect)
    
    pygame.display.update(screen_rect)

async def web_main():
    
    if player_direction_image == FRISK or player_direction_image == FRISK_BACK:
        player_rect = pygame.Rect(WIDTH//2, HEIGHT//2, FRISK_WIDTH, FRISK_HEIGHT)
    else:
        player_rect = pygame.Rect(WIDTH//2, HEIGHT//2, FRISK_LR_WIDTH, FRISK_LR_HEIGHT)

    clock = pygame.time.Clock()
    run = True
    image = FRISK
    pygame.mouse.set_visible(True)
    while run:
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                run = False
                pygame.quit()
                return
        
        BORDER = pygame.Rect(map_border)
        
        keys_pressed = pygame.key.get_pressed()
        d = player_handle_movement(keys_pressed, player_rect, CUR_VEL)

        if (d == "left"):
            image = FRISK_LEFT
        if (d == "right"):
            image = FRISK_RIGHT
        if (d == "up"):
            image = FRISK_BACK
        if (d == "back"):
            image = FRISK
        
        draw_window (player_rect, image, joystick_rect, screen_rect, joystick_inner_rect)
        joystick_handle_movement(joystick_rect, joystick_inner_rect, joystick_outofbox_x, joystick_outofbox_y)
        clock.tick(FPS)
    print("run = ", run)    
    pygame.quit()

if __name__ == "__main__":
    web_main()

asyncio.sleep(0)
asyncio.run(web_main())