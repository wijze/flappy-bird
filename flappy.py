import pygame
import random


# window
WIDTH, HEIGHT = 80, 60
SCALE = 10
RIGHT_X = WIDTH
# colors
BACKGROUNDCOLOR = (0, 0, 0)
BIRDCOLOR = "yellow"
PILLARCOLOR = "green"
SCORECOLOR = "white"
# score
SCOREPOSITION = (10, 10)
SCORE_FONT_SIZE = 80

# rules
FPS = 60
DELTATIME = 1 / FPS
GRAVITY = 50

# bird
FLAPSTRENGTH = 20
MAXSPEED = 40
BIRDX = 10
BIRDRADIUS = 3.5

# pillars
MAX_PILLAR_OFFSET = 20
MIN_PILLAR_HEIGHT = int(HEIGHT / 2 - MAX_PILLAR_OFFSET)
MAX_PILLAR_HEIGHT = int(HEIGHT / 2 + MAX_PILLAR_OFFSET)
PILLAR_WIDTH = 7.5
PILLAR_GAP = 15

PILLAR_SPEED = 15

pygame.init()
clock = pygame.time.Clock()
screen = pygame.display.set_mode((WIDTH * SCALE, HEIGHT * SCALE))
pygame.font.init()
FONT = pygame.font.SysFont(None, SCORE_FONT_SIZE)


class Bird:
    def __init__(self) -> None:
        self.vely = 0
        self.y = HEIGHT / 3

    def update(self):
        self.y += self.vely * DELTATIME
        self.vely += GRAVITY * DELTATIME
        if self.y > HEIGHT + BIRDRADIUS:
            reset_game()

    def flap(self):
        if self.vely > 0:
            self.vely = -FLAPSTRENGTH
        else:
            self.vely = max(self.vely - FLAPSTRENGTH, -MAXSPEED)

    def draw(self):
        pygame.draw.circle(
            screen, BIRDCOLOR, (BIRDX * SCALE, bird.y * SCALE), BIRDRADIUS * SCALE
        )


class Pillar:
    def __init__(self) -> None:
        self.x = RIGHT_X + PILLAR_WIDTH
        self.height = random.randrange(MIN_PILLAR_HEIGHT, MAX_PILLAR_HEIGHT)
        self.completed = False

    def update(self):
        self.x -= PILLAR_SPEED * DELTATIME

        self.check_collision()
        if not self.completed and self.x < BIRDX:
            self.completed = True
            global score
            score += 1

    def draw(self):
        top = pygame.rect.Rect(
            SCALE * (self.x - PILLAR_WIDTH / 2),
            SCALE * (self.height + PILLAR_GAP / 2),
            SCALE * PILLAR_WIDTH,
            SCALE * HEIGHT,
        )
        bottom = pygame.rect.Rect(
            SCALE * (self.x - PILLAR_WIDTH / 2),
            SCALE * (self.height - PILLAR_GAP / 2 - HEIGHT),
            SCALE * PILLAR_WIDTH,
            SCALE * HEIGHT,
        )
        pygame.draw.rect(screen, PILLARCOLOR, bottom)
        pygame.draw.rect(screen, PILLARCOLOR, top)

    def check_collision(self):
        x = self.x - PILLAR_WIDTH / 2 if BIRDX < self.x else self.x + PILLAR_WIDTH / 2
        if (
            bird.y < self.height - PILLAR_GAP / 2
            or bird.y > self.height + PILLAR_GAP / 2
        ):
            dist = distance((BIRDX, bird.y), (x, bird.y))
        else:
            dist = min(
                distance((BIRDX, bird.y), (x, self.height - PILLAR_GAP / 2)),
                distance((BIRDX, bird.y), (x, self.height + PILLAR_GAP / 2)),
            )
        if dist < BIRDRADIUS:
            reset_game()


class Repeater:
    def __init__(self, func, time=100, start_immediate=True) -> None:
        self.timer = time / 1000 if start_immediate else 0
        self.time = time
        self.func = func

    def update(self):
        self.timer += DELTATIME
        if self.timer * 1000 >= self.time:
            self.timer = 0
            self.func()

    def do_now(self):
        self.func()
        self.timer = 0

    def max_delay(self):
        self.timer = 0


def draw_score():
    text_surface = FONT.render(str(score), True, SCORECOLOR)
    screen.blit(text_surface, SCOREPOSITION)


def distance(a, b):
    return ((a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2) ** 0.5


def reset_game():
    global bird, pillars, score
    score = 0
    bird = Bird()
    pillars = []
    repeater.do_now()


def update_physics():
    repeater.update()
    bird.update()
    for pillar in pillars:
        pillar.update()
        if pillar.x < -10:
            pillars.remove(pillar)


def update_graphics():
    screen.fill(BACKGROUNDCOLOR)
    for pillar in pillars:
        pillar.draw()
    bird.draw()
    draw_score()

    pygame.display.update()


score = 0
bird = Bird()
pillars = []
running = True
repeater = Repeater(lambda: pillars.append(Pillar()), 1750)

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                bird.flap()

    update_physics()
    update_graphics()

    clock.tick(FPS)
