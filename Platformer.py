import pygame

WHITE = (255,255,255)
GRAY = (99,99,99)

HEIGHT = 800
WIDTH = 1200
FPS = 60

speed = 200 
GRAVITY = .5
JUMP_POWER = -40

PLATFORM_HEIGHT =int(HEIGHT * 0.05)
PLATFORM_WIDTH = int(WIDTH * 0.05)
PLAYER_HEIGHT = 30
PLAYER_WIDTH = 10

class Player:
    def __init__(self):
        self.vx = 0
        self.vy = 0
        self.player = pygame.Rect(PLATFORM_WIDTH + 40, PLATFORM_HEIGHT + PLAYER_HEIGHT, PLATFORM_WIDTH, PLATFORM_HEIGHT)

    def handleInput(self):
        keys = pygame.key.get_pressed()
        
        if keys[pygame.K_d]:
            self.vx = 2
        if keys[pygame.K_a]:
            self.vx = -2

        if keys[pygame.K_SPACE] and self.onGround():
            self.vy = JUMP_POWER

    def onGround(self):
        return (self.player.bottom >= HEIGHT - PLATFORM_HEIGHT)

    def applyGravity(self, dt):
        if not self.onGround:
            self.vy += GRAVITY
            self.player.y += self.vy
        else:
            self.player.bottom = HEIGHT-PLATFORM_HEIGHT
            self.vy = 0
    

    def update(self, dt):
        #handles inputs, gravity and movement
        self.handleInput()
        self.applyGravity(dt)

        self.player.x += self.vx
        self.player.y += self.vy

    def draw(self, screen):
        pygame.draw.rect(screen,WHITE,self.player)




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

    def update(self, dt):
        self.player.update(dt)

    def draw(self):
        self.screen.fill(GRAY)
        [pygame.draw.rect(self.screen, WHITE, plat) for plat in self.platforms]
        self.player.draw(self.screen)
        pygame.display.flip()

game = Game()
game.run()
pygame.quit()