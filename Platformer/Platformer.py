import pygame

WHITE = (255,255,255)
GRAY = (99,99,99)

HEIGHT = 800
WIDTH = 1200
FPS = 60

speed = 200 
GRAVITY = .5
JUMP_POWER = 4

PLATFORM_HEIGHT =int(HEIGHT * 0.05)
PLATFORM_WIDTH = int(WIDTH * 0.05)
PLAYER_HEIGHT = 30
PLAYER_WIDTH = 10

class Player:
    def __init__(self):
        self.vx
        self.vy
        self.player = pygame.Rect(PLATFORM_WIDTH + 40, PLATFORM_HEIGHT + PLAYER_HEIGHT, PLATFORM_WIDTH, PLATFORM_HEIGHT)

    def handleInput(self, keys):
        keys = pygame.key.get_pressed
        
        if keys[pygame.K_d]:
            self.vx = 2
        if keys[pygame.K_a]:
            self.vx = -2

    def applyGravity(self, dt):

        if self.player.bottom > PLATFORM_HEIGHT:
            self.player.bottom = self.player.bottom[0], self.player.bottom[1] + ((self.vy - GRAVITY) / dt)
        

    def jump(self):
        if self.player.bottom == PLATFORM_HEIGHT:
            self.vy = self.vy + JUMP_POWER


    def update(self, dt, platforms, keys):
        #handles inputs, gravity and movement
        self.handleInput
        self.jump
        self.applyGravity
        



    def draw(self, screen):
        pygame.draw.rect(self.player)



class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.clock = pygame.time.Clock()
        self.running = True
        #Player setup
        self.player = Player()
        #Platform setup
        self.platforms = [pygame.Rect(0, HEIGHT-PLATFORM_HEIGHT,WIDTH,PLATFORM_HEIGHT), 
                          pygame.Rect(WIDTH - PLATFORM_WIDTH, 0, PLATFORM_WIDTH,HEIGHT), 
                          pygame.Rect(0, 0, PLATFORM_WIDTH, HEIGHT)]

    def run(self):
        while self.running:
            dt = self.clock.tick(FPS) / 1000
            self.handleEvents()
            self.update(dt)
            self.draw()

    def handleEvents(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False


        if self.player.bottom > PLATFORM_HEIGHT:
            self.vy = GRAVITY

    def update(self, dt):
        keys = pygame.key.get_pressed()
        self.player.update(dt, self.platforms, keys)

    def draw(self):
        self.screen.fill(GRAY)
        [pygame.draw.rect(self.screen, WHITE, plat) for plat in self.platforms]

        pygame.display.flip()

game = Game()
game.run()
pygame.quit()