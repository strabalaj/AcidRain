import pygame
import time
import random
pygame.font.init()

#create the window
WIDTH, HEIGHT = 1000, 800
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Acid Rain")


BG = pygame.transform.scale(pygame.image.load("rainforest.jpg"), (WIDTH, HEIGHT))
#BG = pygame.image.load("rainforest.jpg")


def draw(player, elapsed_time, rains):
    #blit is used to draw something onto a surface (screen)
    #0,0 is the starting point @ top left
    WIN.blit(BG, (0,0))

    #time counter for game
    time_text = FONT.render(f"Time: {round(elapsed_time)}s", 1 , "white")
    WIN.blit(time_text, (10,10))

    #player rectagle
    pygame.draw.rect(WIN, "red", player)

    for rain in rains:
            pygame.draw.rect(WIN, "orange", rain)

    pygame.display.update()

PLAYER_WIDTH = 40
PLAYER_HEIGHT = 60
PLAYER_VELOCITY = 5

acid_rain_WIDTH = 10
acid_rain_HEIGHT = 20
acid_ran_VELOCITY = 3

FONT = pygame.font.SysFont("comicsans", 30)

#main game loop
def main():
    run = True
    #RECT(x,y,width, height)
    player = pygame.Rect(200, HEIGHT - PLAYER_HEIGHT, PLAYER_WIDTH, PLAYER_HEIGHT)

    #will control how fast while loop controling game 
    clock = pygame.time.Clock()

    #for counting seconds in game
    start_time = time.time()
    elapsed_time = 0

    acid_rain_add_increment = 2000
    acid_rain_count = 0

    rains = []
    hit = False

    while run:
        acid_rain_count += clock.tick(60)
        elapsed_time = time.time() - start_time

        #generate acid rain
        if acid_rain_count > acid_rain_add_increment:
            for _ in range(2):
                acid_rain_x = random.randint(0, WIDTH - acid_rain_WIDTH)
                rain = pygame.Rect(acid_rain_x, -acid_rain_HEIGHT, acid_rain_WIDTH, acid_rain_HEIGHT)
                rains.append(rain)

            acid_rain_add_increment = max(200, acid_rain_add_increment - 50)
            acid_rain_count = 0

        #generate event 
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break

        #generate player movement 
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and player.x - PLAYER_VELOCITY >= 0:
            player.x -= PLAYER_VELOCITY
        if keys[pygame.K_RIGHT]and player.x + PLAYER_VELOCITY + player.width <= WIDTH:
            player.x += PLAYER_VELOCITY
        
        #Move all stars 
        #make copy of list and work from copy while updating OG 
        for rain in rains[:]:
            rain.y += acid_ran_VELOCITY
            if rain.y > HEIGHT:
                rains.remove(rain)
            elif rain.y + acid_rain_HEIGHT >= player.y and rain.colliderect(player):
                rains.remove(rain)
                hit = True
                break

        if hit:
            lost_text = FONT.render("YOU LOST", 1, "red")
            WIN.blit(lost_text, (WIDTH/2 - lost_text.get_width()/2, HEIGHT/2 - lost_text.get_height()/2))
            pygame.display.update()
            pygame.time.delay(4000)
            break

                

        draw(player, elapsed_time, rains)
    
    pygame.quit()

if __name__ == "__main__":
    main()