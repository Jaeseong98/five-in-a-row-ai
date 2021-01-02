import pygame

pygame.init()

size = [800, 600]
screen = pygame.display.set_mode(size)

title_name = "Five In A Row"
pygame.display.set_caption(title_name)

done = False
clock = pygame.time.Clock()

while not done:
    clock.tick(10)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True

    screen.fill((255, 255, 255))

    pygame.display.flip()