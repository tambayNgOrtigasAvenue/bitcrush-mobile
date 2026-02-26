import pygame
import sys
import random

# Initialize pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 800, 600
WHITE = (255, 255, 255)
BLUE = (50, 50, 150)
GRAY = (100, 100, 100)
YELLOW = (255, 255, 0)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)  # Bright green for correct answers
RED = (255, 0, 0)    # Bright red for incorrect answers

# Set up the screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("CodeQuest: Debugging Adventures")

# Load background
background = pygame.image.load('images/testbg2.png').convert()

# Load sprite sheet
sprite_sheet = pygame.image.load('images/character_sprites.png').convert_alpha()

# Define sprite sizes
SPRITE_WIDTH, SPRITE_HEIGHT = 32, 32

# Extract animations
idle_sprites = [sprite_sheet.subsurface((0, 0, SPRITE_WIDTH, SPRITE_HEIGHT))]
walking_sprites = [sprite_sheet.subsurface((i * SPRITE_WIDTH, 0, SPRITE_WIDTH, SPRITE_HEIGHT)) for i in range(1, 4)]
jumping_sprite = sprite_sheet.subsurface((4 * SPRITE_WIDTH, 0, SPRITE_WIDTH, SPRITE_HEIGHT))

# Player properties
player_x, player_y = 100, 500
velocity_x, velocity_y = 0, 0
gravity = 1
is_jumping = False
can_double_jump = False  # Track if the player can double jump
animation_index = 0
clock = pygame.time.Clock()

# Platforms (list of tuples: x, y, width, height)
platforms = [
    (200, 450, 150, 10),  # Existing platform
    (400, 350, 200, 10),  # Existing platform
    (650, 250, 150, 10),  # Existing platform
    (100, 300, 150, 10),  # New platform
    (500, 200, 150, 10),  # New platform
    (300, 150, 200, 10),  # New platform
]

# Portal properties
portal_x, portal_y = 700, 100  # Initial portal position
portal_color = (138, 43, 226)  # Violet color
portal_glow_radius = 20  # Initial portal radius
portal_glow_direction = 1  # Direction of glow animation (1 = increasing, -1 = decreasing)

# Levels
levels = [
    {"prompt": ["_", "x < 10:", "    print('Hello')"], "choices": ["if", "else", "while", "for"], "correct": ["if"]},
    {"prompt": ["for i in ___(5):", "    print(i)"], "choices": ["range", "list", "tuple", "dict"], "correct": ["range"]},
    {"prompt": ["while _:", "    print('Looping')"], "choices": ["True", "False", "None", "0"], "correct": ["True"]},
    {"prompt": ["_ x == 5:", "    print('Equal')"], "choices": ["if", "elif", "else", "while"], "correct": ["if"]},
    {"prompt": ["def func():", "    _ 'Hello'"], "choices": ["return", "print", "yield", "break"], "correct": ["return"]},
]

current_level = 0  # Start at level 0

# Function to generate non-colliding random platforms
def generate_random_platforms():
    platforms = []
    max_attempts = 100  # Limit the number of attempts to avoid infinite loops
    while len(platforms) < 6 and max_attempts > 0:
        plat_x = random.randint(50, WIDTH - 200)  # Ensure the platform fits within the screen
        plat_y = random.randint(150, HEIGHT - 100)
        plat_w = random.randint(100, 200)
        plat_h = 10

        # Check for collisions with existing platforms
        collision = False
        for existing_x, existing_y, existing_w, existing_h in platforms:
            if (
                plat_x < existing_x + existing_w + 20 and  # Add horizontal spacing
                plat_x + plat_w + 20 > existing_x and
                plat_y < existing_y + existing_h + 50 and  # Add vertical spacing
                plat_y + plat_h + 50 > existing_y
            ):
                collision = True
                break

        if not collision:
            platforms.append((plat_x, plat_y, plat_w, plat_h))
        max_attempts -= 1

    return platforms

# Function to load a level
def load_level(level_index):
    global code_prompt, correct_answers, choices, platforms, portal_x, portal_y, current_blank_index, collected_choices, portal_visible
    level = levels[level_index]
    code_prompt = level["prompt"][:]  # Copy the prompt for the current level
    correct_answers = level["correct"][:]  # Copy the correct answers for the current level
    platforms = generate_random_platforms()  # Generate non-colliding platforms
    choices = place_choices_on_platforms(level["choices"], platforms)  # Place choices on platforms
    portal_x, portal_y = random.randint(50, 700), random.randint(50, 200)  # Randomize portal position
    current_blank_index = 0  # Reset the blank index for the new level
    collected_choices = []  # Clear collected choices for the new level
    portal_visible = False  # Reset portal visibility for the new level

    # Debugging output
    print(f"Level {level_index} loaded")
    print(f"Code Prompt: {code_prompt}")
    print(f"Correct Answers: {correct_answers}")
    print(f"Choices: {choices}")

# Dynamically place choices on platforms
def place_choices_on_platforms(choices, platforms):
    placed_choices = []
    available_platforms = platforms.copy()  # Copy the platforms list to avoid reusing the same platform
    for choice_text in choices:
        if available_platforms:  # Ensure there are platforms left to place the choice
            # Randomly select a platform and remove it from the available list
            plat_x, plat_y, plat_w, plat_h = available_platforms.pop(random.randint(0, len(available_platforms) - 1))
            # Randomly place the ball within the platform's width
            choice_x = random.randint(plat_x + 15, plat_x + plat_w - 15)
            choice_y = plat_y - 15  # Place the ball slightly above the platform
            placed_choices.append((choice_text, choice_x, choice_y))
            print(f"Placed choice '{choice_text}' at ({choice_x}, {choice_y})")  # Debugging output
    return placed_choices

# Code Fragments (choices as blue balls)
choices_text = ["if", "else", "while", "for"]
choices = place_choices_on_platforms(choices_text, platforms)

collected_choices = []

# Code Prompt
code_prompt = ["_", "x < 10:", "    print('Hello')"]
correct_answers = ["if"]  # Correct answers for the blanks
current_blank_index = 0  # Track which blank is being filled

# Add a paused variable
paused = False

# Initialize portal visibility outside the game loop
portal_visible = False  # Initially, the portal is not visible
answer_glow_color = None  # Color for the player's answer glow
answer_glow_timer = 0  # Timer for how long the glow effect lasts

# Game loop
running = True
while running:
    screen.blit(background, (0, 0))

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:  # Pause/Resume the game
                paused = not paused
            elif event.key == pygame.K_F9:  # Exit the game
                running = False
            elif event.key == pygame.K_d:  # Move right
                velocity_x = 5
            elif event.key == pygame.K_a:  # Move left
                velocity_x = -5
            elif event.key == pygame.K_SPACE:
                if not is_jumping:  # Single jump
                    velocity_y = -15
                    is_jumping = True
                    can_double_jump = True  # Allow double jump after the first jump
                elif can_double_jump:  # Double jump
                    velocity_y = -15
                    can_double_jump = False  # Disable further jumps
        elif event.type == pygame.KEYUP:
            if event.key in [pygame.K_d, pygame.K_a]:  # Stop horizontal movement
                velocity_x = 0

    if paused:
        # Fill the screen with a black background
        screen.fill((0, 0, 0))  # Black background

        # Display "Paused" message
        font_large = pygame.font.Font(None, 74)  # Use a larger font for the pause text
        pause_text = font_large.render("Paused", True, (255, 255, 255))
        pause_text_rect = pause_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 50))
        screen.blit(pause_text, pause_text_rect)

        # Display "ESC to resume" message
        font_small = pygame.font.Font(None, 50)  # Use a smaller font for instructions
        resume_text = font_small.render("ESC to resume", True, (255, 255, 255))
        resume_text_rect = resume_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 10))
        screen.blit(resume_text, resume_text_rect)

        # Display "F9 to exit" message
        exit_text = font_small.render("F9 to exit", True, (255, 255, 255))
        exit_text_rect = exit_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 60))
        screen.blit(exit_text, exit_text_rect)

        pygame.display.update()
        continue  # Skip the rest of the loop while paused

    # Apply gravity
    velocity_y += gravity
    player_y += velocity_y
    player_x += velocity_x

    # Collision with ground
    if player_y >= 500:
        player_y = 500
        is_jumping = False
        can_double_jump = False  # Reset double jump when on the ground

    # Platform collision
    for plat_x, plat_y, plat_w, plat_h in platforms:
        if player_x + SPRITE_WIDTH > plat_x and player_x < plat_x + plat_w:
            if player_y + SPRITE_HEIGHT >= plat_y and player_y + velocity_y < plat_y:
                player_y = plat_y - SPRITE_HEIGHT
                velocity_y = 0
                is_jumping = False
                can_double_jump = False  # Reset double jump when on a platform

    # Select sprite
    if is_jumping:
        current_sprite = jumping_sprite
    elif velocity_x != 0:
        animation_index = (animation_index + 1) % len(walking_sprites)
        current_sprite = walking_sprites[animation_index]
    else:
        current_sprite = idle_sprites[0]

    # Draw platforms
    for plat_x, plat_y, plat_w, plat_h in platforms:
        pygame.draw.rect(screen, GRAY, (plat_x, plat_y, plat_w, plat_h))

    # Draw Code Prompt
    font = pygame.font.Font(None, 36)
    prompt_text = " ".join(code_prompt)
    prompt_surface = font.render(prompt_text, True, YELLOW)
    screen.blit(prompt_surface, (50, 50))

    # Draw Choices (Blue Balls)
    for choice_text, choice_x, choice_y in choices:
        pygame.draw.circle(screen, BLUE, (choice_x, choice_y), 15)
        choice_surface = font.render(choice_text, True, WHITE)
        screen.blit(choice_surface, (choice_x - 10, choice_y - 30))

    # Check for collisions with choices
    for choice_text, choice_x, choice_y in choices:  # Do not modify the choices list
        if abs(player_x - choice_x) < 20 and abs(player_y - choice_y) < 20:
            print(f"Player collided with choice: {choice_text}")  # Debugging output
            if current_blank_index < len(code_prompt) and code_prompt[current_blank_index] == "_":
                code_prompt[current_blank_index] = choice_text  # Fill the blank
                current_blank_index += 1
                if choice_text in correct_answers:
                    print(f"Correct answer: {choice_text}")  # Debugging output
                    collected_choices.append((choice_text, choice_x, choice_y, "green"))  # Mark as correct (green)
                    answer_glow_color = GREEN  # Set glow color to green
                else:
                    print(f"Wrong answer: {choice_text}")  # Debugging output
                    collected_choices.append((choice_text, choice_x, choice_y, "red"))  # Mark as incorrect (red)
                    answer_glow_color = RED  # Set glow color to red
                answer_glow_timer = 30  # Set the glow effect duration (e.g., 30 frames)
                # Check if all blanks are filled
                portal_visible = "_" not in code_prompt
            break  # Exit the loop since an answer was picked

    # Draw Choices (Balls)
    for choice_text, choice_x, choice_y in choices:
        # Default color is blue
        ball_color = BLUE
        for collected_choice_text, collected_choice_x, collected_choice_y, color in collected_choices:
            if choice_text == collected_choice_text and choice_x == collected_choice_x and choice_y == collected_choice_y:
                ball_color = GREEN if color == "green" else RED  # Change color to green or red if collected
        pygame.draw.circle(screen, ball_color, (choice_x, choice_y), 15)
        choice_surface = font.render(choice_text, True, WHITE)
        screen.blit(choice_surface, (choice_x - 10, choice_y - 30))

    # Draw the player's answer glow
    if answer_glow_timer > 0:
        answer_glow_timer -= 1  # Decrease the timer
        if answer_glow_color:
            pygame.draw.circle(screen, answer_glow_color, (player_x + SPRITE_WIDTH // 2, player_y), 30, 5)  # Draw glow

    # Draw portal only if the question is answered
    if portal_visible:  # Check if the portal should be visible
        # Animate the portal's glow
        portal_glow_radius += portal_glow_direction
        if portal_glow_radius >= 30 or portal_glow_radius <= 20:  # Glow range
            portal_glow_direction *= -1  # Reverse the glow direction

        # Draw the glowing portal
        pygame.draw.circle(screen, portal_color, (portal_x, portal_y), portal_glow_radius)

        # Check for portal collision
        if abs(player_x - portal_x) < 20 and abs(player_y - portal_y) < 20:
            if current_level < len(levels) - 1:
                current_level += 1
                print(f"Loading level {current_level}")  # Debugging output
                load_level(current_level)  # Load the next level
            else:
                font = pygame.font.Font(None, 40)
                text = font.render("Congratulations! You completed all levels!", True, (255, 255, 0))
                screen.blit(text, (200, 250))
                pygame.display.flip()
                pygame.time.wait(3000)
                running = False

    # Draw character
    screen.blit(current_sprite, (player_x, player_y))

    # Debugging output
    print(f"Collected Choices: {collected_choices}")
    print(f"Portal Visible: {portal_visible}")
    print(f"Code Prompt: {code_prompt}")
    print(f"Correct Answers: {correct_answers}")
    print(f"Choices: {choices}")

    pygame.display.flip()
    clock.tick(30)

pygame.quit()
sys.exit()