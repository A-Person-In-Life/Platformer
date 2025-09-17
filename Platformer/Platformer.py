import pygame

WHITE = (255,255,255)
GRAY = (99,99,99)

HEIGHT = 800
WIDTH = 1200
FPS = 60

speed = 200 
GRAVITY = 1500

PLATFORM_HEIGHT =int(HEIGHT * 0.05)
PLATFORM_WIDTH = int(WIDTH * 0.05)
PLAYER_HEIGHT = 30
PLAYER_WIDTH = 10

class Player:
    def __init__(self):
        self.vx
        self.vy
        self.gravity = GRAVITY
        self.player = pygame.Rect(PLATFORM_WIDTH + 40, PLATFORM_HEIGHT + PLAYER_HEIGHT, PLATFORM_WIDTH, PLATFORM_HEIGHT)

    def handleInput(self, keys):
        keys = pygame.key.get_pressed
        
        if keys[pygame.K_d]:
            self.vx = 2
        if keys[pygame.K_a]:
            self.vx = -2

    def applyGravity(self, dt):

        if not self.player.bottom <= PLATFORM_HEIGHT:
            self.player.bottom = self.player.bottom

    def jump(self):
        #check if onground then jump by applying jump power to vel Y
        pass

    def update(self, dt, platforms, keys):
        #handles inputs, gravity and movement
        pass
    def draw(self, screen):
        pygame.Rect.draw(self.player)



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