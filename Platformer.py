import pygame

WHITE = (255,255,255)
GRAY = (99,99,99)

HEIGHT = 800
WIDTH = 1200
FPS = 60

ACCEL = 1
MAX_SPEED = 5
GRAVITY = .5
JUMP_POWER = -10

PLATFORM_HEIGHT =int(HEIGHT * 0.05)
PLATFORM_WIDTH = int(WIDTH * 0.05)
PLAYER_HEIGHT = 40
PLAYER_WIDTH = 40

class Player:
    def __init__(self):
        self.vx = 0
        self.vy = 0
        self.jumping = False
        self.canJump = True
        self.player = pygame.Rect(PLATFORM_WIDTH + 40, PLATFORM_HEIGHT + PLAYER_HEIGHT, PLAYER_WIDTH, PLAYER_HEIGHT)

    def handleInput(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_d]:
            self.vx = min(ACCEL+self.vx,MAX_SPEED)
        elif keys[pygame.K_a]:
            self.vx = max(self.vx-ACCEL,-MAX_SPEED)
        else:
            self.vx *= .8

        if keys[pygame.K_SPACE] and self.onGround() and self.canJump:
            self.vy = JUMP_POWER
            self.jumping = True
            self.canJump = False

        if not keys[pygame.K_SPACE]:
            if self.vy < 0:
                self.vy += GRAVITY * 4
            self.jumping = False
            self.canJump = True

    def onGround(self):
        return (self.player.bottom >= HEIGHT - PLATFORM_HEIGHT)

    def applyGravity(self):
        if not self.onGround():
            if self.jumping and self.vy < 0:
                self.vy += GRAVITY * .3
            else:
                self.vy += GRAVITY
        elif (self.vy > 0):
            self.player.bottom = HEIGHT-PLATFORM_HEIGHT
            self.vy = 0
    
    def checkCollisions(self, platforms):
        for platform in platforms:
            if self.player.colliderect(platform):
                if self.vx > 0:
                    self.player.right = platform.left
                elif self.vx < 0:
                    self.player.left = platform.right
        
    def update(self, platforms):
        #handles inputs, gravity and movement
        self.handleInput()
        self.applyGravity()
        self.player.x += self.vx
        self.player.y += self.vy
        self.checkCollisions(platforms)

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
            self.update()
            self.draw()

    def handleEvents(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

    def update(self):
        self.player.update(self.platforms[1::])

    def draw(self):
        self.screen.fill(GRAY)
        [pygame.draw.rect(self.screen, WHITE, plat) for plat in self.platforms]
        self.player.draw(self.screen)
        pygame.display.flip()

game = Game()
game.run()
pygame.quit()
