import pygame
import random

# Initialize pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Coding Prompt Game")

# Colors
WHITE = (255, 255, 255)
GRAY = (169, 169, 169)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)

# Clock for controlling frame rate
clock = pygame.time.Clock()

# Fonts
font = pygame.font.Font(None, 36)

# Player setup
player_size = 40
player_x, player_y = WIDTH // 2, HEIGHT - player_size - 10
player_speed = 5
is_jumping = False
jump_count = 10

# Ball setup
ball_radius = 20
balls = [
    {"x": 200, "y": 300, "text": "def", "correct": False},
    {"x": 400, "y": 300, "text": "class", "correct": True},
    {"x": 600, "y": 300, "text": "if", "correct": False},
    {"x": 300, "y": 400, "text": "else", "correct": False},
]
ball_colors = [BLUE] * len(balls)

# Floating surfaces setup (lowered and randomized)
floating_surfaces = [
    {"x": 150, "y": 350, "width": 100, "height": 10},  # Lowered surface
    {"x": 350, "y": 300, "width": 100, "height": 10},  # Lowered surface
    {"x": 550, "y": 250, "width": 100, "height": 10},  # Lowered surface
]

# Add random surfaces
for _ in range(3):  # Add 3 random surfaces
    floating_surfaces.append({
        "x": random.randint(50, WIDTH - 150),
        "y": random.randint(200, HEIGHT - 200),
        "width": 100,
        "height": 10,
    })

# Assign choices to floating surfaces
floating_balls = [
    {"x": surface["x"] + surface["width"] // 2, "y": surface["y"] - ball_radius, "text": choice["text"], "correct": choice["correct"]}
    for surface, choice in zip(floating_surfaces, balls)
]
ball_colors = [BLUE] * len(floating_balls)

# Portal setup
portal_active = False
portal_x, portal_y = WIDTH // 2, 100
portal_size = 50

# Ground setup
ground_height = 50

# Game loop variables
running = True
answered = False

# Main game loop
while running:
    screen.fill(WHITE)

    # Draw ground
    pygame.draw.rect(screen, GRAY, (0, HEIGHT - ground_height, WIDTH, ground_height))

    # Draw floating surfaces
    for surface in floating_surfaces:
        pygame.draw.rect(screen, BLACK, (surface["x"], surface["y"], surface["width"], surface["height"]))

    # Draw player
    pygame.draw.rect(screen, BLUE, (player_x, player_y, player_size, player_size))

    # Draw balls
    for i, ball in enumerate(floating_balls):
        pygame.draw.circle(screen, ball_colors[i], (ball["x"], ball["y"]), ball_radius)
        text = font.render(ball["text"], True, WHITE)
        screen.blit(text, (ball["x"] - text.get_width() // 2, ball["y"] - text.get_height() // 2))

    # Draw portal if active
    if portal_active:
        pygame.draw.rect(screen, GREEN, (portal_x, portal_y, portal_size, portal_size))

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Player movement
    keys = pygame.key.get_pressed()
    if keys[pygame.K_a]:  # Move left
        player_x -= player_speed
    if keys[pygame.K_d]:  # Move right
        player_x += player_speed
    if not is_jumping:
        if keys[pygame.K_SPACE]:  # Start jump
            is_jumping = True
    else:
        if jump_count >= -10:
            neg = 1 if jump_count > 0 else -1
            player_y -= (jump_count ** 2) * 0.5 * neg
            jump_count -= 1
        else:
            is_jumping = False
            jump_count = 10

    # Check collision with balls
    for i, ball in enumerate(floating_balls):
        ball_rect = pygame.Rect(ball["x"] - ball_radius, ball["y"] - ball_radius, ball_radius * 2, ball_radius * 2)
        player_rect = pygame.Rect(player_x, player_y, player_size, player_size)
        if player_rect.colliderect(ball_rect) and not answered:
            answered = True
            if ball["correct"]:
                ball_colors[i] = GREEN
                portal_active = True
            else:
                ball_colors[i] = RED

    # Check collision with portal
    if portal_active:
        portal_rect = pygame.Rect(portal_x, portal_y, portal_size, portal_size)
        player_rect = pygame.Rect(player_x, player_y, player_size, player_size)
        if player_rect.colliderect(portal_rect):
            print("Level Complete!")
            running = False

    # Keep player within screen bounds
    player_x = max(0, min(WIDTH - player_size, player_x))
    player_y = max(0, min(HEIGHT - player_size - ground_height, player_y))

    # Update display
    pygame.display.flip()
    clock.tick(30)

pygame.quit()