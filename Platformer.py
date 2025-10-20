import pygame

WHITE = (255,255,255)
GRAY = (99,99,99)

HEIGHT = 800
WIDTH = 1200
FPS = 60

ACCEL = 1
MAX_SPEED = 5
JUMPGRAV = .314
FALLGRAV = .5
JUMP_POWER = -8
WALL_JUMP = 15
DASH_POWER = 25
DASH_DURATION = 100
DASH_COOLDOWN = 1000

PLATFORM_HEIGHT =int(HEIGHT * 0.05)
PLATFORM_WIDTH = int(WIDTH * 0.05)
PLAYER_HEIGHT = 40
PLAYER_WIDTH = 40

class Player:
    def __init__(self):
        self.vx = 0
        self.vy = 0
        self.jumping = False
        self.onWall = False
        self.wallDir = 0
        self.canJump = True
        self.gravityApply = True
        self.dashDir = 0
        self.dashStarted = False
        self.endTick = 0
        self.dashCooldown = 0
        self.shiftPressed = False
        self.player = pygame.Rect(PLATFORM_WIDTH + 40, PLATFORM_HEIGHT + PLAYER_HEIGHT, PLAYER_WIDTH, PLAYER_HEIGHT)

    def handleInput(self):
        keys = pygame.key.get_pressed()
        
        if not self.dashStarted:
            if keys[pygame.K_d]:
                self.vx = min(ACCEL+self.vx,MAX_SPEED)
            elif keys[pygame.K_a]:
                self.vx = max(self.vx-ACCEL,-MAX_SPEED)
            else:
                self.vx *= .8

        if keys[pygame.K_SPACE]:
            if self.onGround() and self.canJump:
                self.vy = JUMP_POWER
                self.jumping = True
                self.canJump = False
            elif self.onWall:
                self.vy = JUMP_POWER
                self.vx = WALL_JUMP * self.wallDir
                self.onWall = False
                self.jumping = True
                self.canJump = False

        if not keys[pygame.K_SPACE]:
            self.jumping = False
            if self.onGround():
                self.canJump = True
        
        if keys[pygame.K_LSHIFT] and not self.dashStarted and self.canDash:
            current_time = pygame.time.get_ticks()
            if current_time >= self.dashCooldown:
                if keys[pygame.K_d]:
                    self.dashDir = 1
                    self.dashing()
                elif keys[pygame.K_a]:
                    self.dashDir = -1 
                    self.dashing()
        
        if not keys[pygame.K_LSHIFT]:
            self.canDash = True
                
        if keys[pygame.K_q]:
            #will do attack at some point
            pass
    def onGround(self):
        return (self.player.bottom >= HEIGHT - PLATFORM_HEIGHT)
    
    def dashing(self):
        if not self.dashStarted:
            self.endTick = pygame.time.get_ticks() + DASH_DURATION
            self.dashCooldown = pygame.time.get_ticks() + DASH_COOLDOWN
            self.dashStarted = True
            self.canDash = False
        
        if pygame.time.get_ticks() >= self.endTick:
            self.gravityApply = True
            self.dashStarted = False
        else:
            self.gravityApply = False
            self.vx = DASH_POWER * self.dashDir
            self.vy = 0

    def applyGravity(self):
        if self.gravityApply:
            if not self.onGround():
                if self.jumping and self.vy < 0:
                    self.vy += JUMPGRAV * .5
                else:
                    self.vy += FALLGRAV
            elif (self.vy > 0):
                self.vy = 0
                self.player.bottom = HEIGHT - PLATFORM_HEIGHT
    
    def checkCollisions(self, platforms):
        self.onWall = False
        self.wallDir = 0
        for platform in platforms:
            if self.player.colliderect(platform):
                if self.vx > 0:
                    self.player.right = platform.left
                    self.wallDir = -1
                    self.vy *= .25
                    self.vx = 0
                    self.onWall = True
                elif self.vx < 0:
                    self.player.left = platform.right
                    self.wallDir = 1
                    self.onWall = True
                    self.vx = 0
            
    def update(self, platforms):
        self.handleInput()
        if self.dashStarted:
            self.dashing()  
        self.applyGravity()
        self.player.x += self.vx
        self.player.y += self.vy
        self.checkCollisions(platforms)
        self.debugPrint()

    def debugPrint(self):
        if (self.player.x >= WIDTH or self.player.x <= -WIDTH) or (self.player.y >= HEIGHT or self.player.y <= -HEIGHT):
            print(f"Player out of bounds at x{self.player.x} y{self.player.y}")

    def draw(self, screen):
        pygame.draw.rect(screen,WHITE,self.player)

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.clock = pygame.time.Clock()
        self.running = True
        self.player = Player()
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