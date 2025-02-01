import pygame

def runGame(width, height):
    window:pygame.Surface = pygame.display.set_mode((width, height));
    run:bool = True
    
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                
            window.fill("pink")
            pygame.display.flip()