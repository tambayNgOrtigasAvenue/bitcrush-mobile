import pygame
import random
import sys
import time
from os.path import join

# Initialize Pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 800, 600
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Fill in the Blanks")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)
BLUE = (0, 0, 255)
PURPLE = (128, 0, 128)

# Clock for controlling frame rate
clock = pygame.time.Clock()
FPS = 60

# Player settings
PLAYER_SIZE = 50  # Increased from 30 to 50
PLAYER_COLOR = GREEN
PLAYER_SPEED = 5
PLAYER_MAX_HP = 5  # Initial maximum HP
PLAYER_HP_BAR_WIDTH = 30
PLAYER_HP_BAR_HEIGHT = 5

# Buffs
BUFF_RESET_HEALTH = "reset_health"
BUFF_GAIN_HP = "gain_hp"

# Enemy settings
ENEMY_SIZE = 40  # Increased from 20 to 40
ENEMY_COLOR = RED
ENEMY_SPEED = 2
ENEMY_SPAWN_RATE = 30  # Frames between enemy spawns
ENEMY_SPAWN_INCREMENT = 5  # Decrease spawn interval by this amount after each level-up

# Boss settings
BOSS_SIZE = 60  # Increased from 40 to 60
BOSS_COLOR = PURPLE
BOSS_SPEED = 1
BOSS_HITS = 2  # Number of hits required to destroy the boss

# Purple Boss settings
PURPLE_BOSS_SIZE = 80  # Increased from 50 to 80
PURPLE_BOSS_COLOR = PURPLE
PURPLE_BOSS_SPEED = 1.5
PURPLE_BOSS_HITS = 5  # Number of hits required to destroy the purple boss

# Bullet settings
BULLET_SIZE = 10
BULLET_COLOR = YELLOW
BULLET_SPEED = 10

# Game state
paused = False
lives = 5
level_progress = 0
level_goal = 100  # Points needed to fill the level gauge
question_active = False
question_timer = 10  # Time to answer the question
question_start_time = 0
current_question = None
current_answer = None
player_input = ""
start_time = time.time()  # Track the start time of the game
final_time_survived = None  # Store the final time survived
correct_answers = 0
wrong_answers = 0
paused_time = 0  # Total time the game has been paused
pause_start_time = None  # When the pause started
bosses_defeated = 0  # Track the number of bosses defeated
levels_survived = 0  # Track the number of levels survived

# Fill-in-the-blank Python code questions (Basic)
questions = [
    {
        "question": "Fill in the blank to print 'Hello, World!':\n\n___('Hello, World!')",
        "answer": "print"  # Correct answer
    },
    {
        "question": "What is the keyword to create a loop that iterates over a range of numbers?\n\nfor i ___ range(5):",
        "answer": "in"  # Correct answer
    },
    {
        "question": "Fill in the blank to add 5 and 3:\n\nprint(5 ___ 3)",
        "answer": "+"  # Correct answer
    },
    {
        "question": "Fill in the blank to check if 10 is greater than 5:\n\nif 10 ___ 5:\n\n    print('Yes')",
        "answer": ">"  # Correct answer
    },
    {
        "question": "Fill in the blank to create a list with numbers 1, 2, and 3:\n\nmy_list = [1, 2, ___]",
        "answer": "3"  # Correct answer
    },
    {
        "question": "Fill in the blank to get the length of the string 'Python':\n\nprint(len(___))",
        "answer": "'Python'"  # Correct answer
    },
    {
        "question": "Fill in the blank to define a function:\n\n\ndef my_function():\n\n    ___('Hello')",
        "answer": "print"  # Correct answer
    },
    {
        "question": "Fill in the blank to iterate over a list:\n\nfor item ___ my_list:\n\n    print(item)",
        "answer": "in"  # Correct answer
    },
    {
        "question": "What is the keyword to check a condition in Python?\n\n___ x > 5:",
        "answer": "if"   # Correct answer
    },
    {
        "question": "What is the keyword to return a value from a function?\n\n___ x + y",
        "answer": "return"  # Correct answer
    },
    {
        "question": "What is the method to convert a string to lowercase in Python?\n\n'Hello'.___()",
        "answer": "lower"  # Correct answer
    },
        {
        "question": "What is the method to add an element to a list in Python?\n\nmy_list.___(5)",
        "answer": "append"  # Correct answer
    },
        {
        "question": "What is the keyword to handle exceptions in Python?\n\ntry:\n    x = 1 / 0\n\n___ ZeroDivisionError as e:",
        "answer": "except"  # Correct answer
    },
        {
        "question": "What is the keyword to define a class in Python?\n\n___ MyClass:",
        "answer": "class"  # Correct answer
    },
    {
        "question": "What is the operator to multiply two numbers in Python?\n\nprint(2 ___ 3)",
        "answer": "*"  # Correct answer
    },
        {
        "question": "What is the keyword to create an infinite loop in Python?\n\n___ True:\n    print('Looping')",
        "answer": "while"  # Correct answer
    },
        {
        "question": "What is the keyword to stop a loop in Python?\n\nfor i in range(5):\n    if i == 3:\n        ___",
        "answer": "break"  # Correct answer
    },
    {
        "question": "What is the keyword to skip the current iteration of a loop in Python?\n\nfor i in range(5):\n    if i == 3:\n        ___",
        "answer": "continue"  # Correct answer
    }
]
  
# Load assets
background_file = sys.argv[1] if len(sys.argv) > 1 else "defaultbg.png"  # Background file
player_asset = sys.argv[2] if len(sys.argv) > 2 else "images/customchara.png"  # Player asset

# Construct the full path for the background
background_path = join("images", background_file)

# Load the background image
try:
    background = pygame.image.load(background_path)
    background = pygame.transform.scale(background, (WIDTH, HEIGHT))
except FileNotFoundError:
    print(f"Error: Background file '{background_path}' not found. Using white background.")
    background = None

# Load the player asset
try:
    player_image = pygame.image.load(player_asset)  # Use the player_asset path as-is
    player_image = pygame.transform.scale(player_image, (50, 50))  # Scale the player image
except FileNotFoundError:
    print(f"Error: Player asset '{player_asset}' not found. Using default placeholder.")
    player_image = pygame.Surface((50, 50))  # Placeholder player image
    player_image.fill((0, 255, 0))  # Green placeholder
redfrog_image = pygame.image.load("images/redsmolfrog.png")  # Small enemy 1
orangefrog_image = pygame.image.load("images/orangesmolfrog.png")  # Small enemy 2
greenfrog_image = pygame.image.load("images/greensmolfrog.png")  # Small enemy 3
bluefrog_image = pygame.image.load("images/bluesmolfrog.png")  # Small enemy 4
purpleboss_image = pygame.image.load("images/purplebossfrog.png")  # Boss enemy
lives_image = pygame.image.load("images/lives.webp")

# Scale images
player_image = pygame.transform.scale(player_image, (PLAYER_SIZE, PLAYER_SIZE))
redfrog_image = pygame.transform.scale(redfrog_image, (ENEMY_SIZE, ENEMY_SIZE))
orangefrog_image = pygame.transform.scale(orangefrog_image, (ENEMY_SIZE, ENEMY_SIZE))
greenfrog_image = pygame.transform.scale(greenfrog_image, (ENEMY_SIZE, ENEMY_SIZE))
bluefrog_image = pygame.transform.scale(bluefrog_image, (ENEMY_SIZE, ENEMY_SIZE))
purpleboss_image = pygame.transform.scale(purpleboss_image, (PURPLE_BOSS_SIZE, PURPLE_BOSS_SIZE))
lives_image = pygame.transform.scale(lives_image, (30, 30))

# Load the Minecraft font
try:
    MINECRAFT_FONT = pygame.font.Font('images/Minecraft.ttf', 36)  # Set font size to 36
    MINECRAFT_FONT_LARGE = pygame.font.Font('images/Minecraft.ttf', 74)  # Larger font for titles
except FileNotFoundError:
    print("Error: 'Minecraft.ttf' not found in the 'images' folder.")
    sys.exit()

# Load the blue background image
try:
    PAUSE_BACKGROUND = pygame.image.load("images/bluebg.jpg")
    PAUSE_BACKGROUND = pygame.transform.scale(PAUSE_BACKGROUND, (WIDTH, HEIGHT))
except pygame.error as e:
    print(f"Error loading background image: {e}")
    sys.exit()

# Player class
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = player_image  # Use the player image
        self.rect = self.image.get_rect(center=(WIDTH // 2, HEIGHT // 2))
        self.max_hp = PLAYER_MAX_HP
        self.current_hp = self.max_hp

    def update(self, keys):
        if keys[pygame.K_w] or keys[pygame.K_UP]:
            self.rect.y -= PLAYER_SPEED
        if keys[pygame.K_s] or keys[pygame.K_DOWN]:
            self.rect.y += PLAYER_SPEED
        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            self.rect.x -= PLAYER_SPEED
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            self.rect.x += PLAYER_SPEED

        # Keep player within screen bounds
        self.rect.x = max(0, min(WIDTH - PLAYER_SIZE, self.rect.x))
        self.rect.y = max(0, min(HEIGHT - PLAYER_SIZE, self.rect.y))

    def apply_buff(self, buff):
        if buff == BUFF_RESET_HEALTH:
            self.current_hp = self.max_hp  # Fully restore health
        elif buff == BUFF_GAIN_HP:
            self.max_hp += 1  # Increase max HP
            self.current_hp = self.max_hp  # Fully restore health

# Enemy class
class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        # Randomly select one of the small enemy images
        self.image = random.choice([redfrog_image, orangefrog_image, greenfrog_image, bluefrog_image])
        self.rect = self.image.get_rect(
            center=(random.randint(0, WIDTH), random.randint(0, HEIGHT))
        )

    def update(self, player_pos):
        # Move towards the player
        dx, dy = player_pos[0] - self.rect.x, player_pos[1] - self.rect.y
        dist = max(1, (dx**2 + dy**2) ** 0.5)  # Avoid division by zero
        self.rect.x += int(ENEMY_SPEED * dx / dist)
        self.rect.y += int(ENEMY_SPEED * dy / dist)

# Boss class
class Boss(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((BOSS_SIZE, BOSS_SIZE))
        self.image.fill(BOSS_COLOR)
        self.rect = self.image.get_rect(
            center=(random.randint(0, WIDTH), random.randint(0, HEIGHT))
        )
        self.hits = BOSS_HITS

    def update(self, player_pos):
        # Move towards the player
        dx, dy = player_pos[0] - self.rect.x, player_pos[1] - self.rect.y
        dist = max(1, (dx**2 + dy**2) ** 0.5)  # Avoid division by zero
        self.rect.x += int(BOSS_SPEED * dx / dist)
        self.rect.y += int(BOSS_SPEED * dy / dist)

# Purple Boss class
class PurpleBoss(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = purpleboss_image  # Use the purple boss frog image
        self.rect = self.image.get_rect(
            center=(random.randint(0, WIDTH), random.randint(0, HEIGHT))
        )
        self.hits = PURPLE_BOSS_HITS  # Number of hits required to destroy the purple boss

    def update(self, player_pos):
        # Move towards the player
        dx, dy = player_pos[0] - self.rect.x, player_pos[1] - self.rect.y
        dist = max(1, (dx**2 + dy**2) ** 0.5)  # Avoid division by zero
        self.rect.x += int(PURPLE_BOSS_SPEED * dx / dist)
        self.rect.y += int(PURPLE_BOSS_SPEED * dy / dist)

# Bullet class
class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, dx, dy):
        super().__init__()
        self.image = pygame.Surface((BULLET_SIZE, BULLET_SIZE))
        self.image.fill(BULLET_COLOR)
        self.rect = self.image.get_rect(center=(x, y))
        self.dx = dx
        self.dy = dy

    def update(self):
        self.rect.x += self.dx * BULLET_SPEED
        self.rect.y += self.dy * BULLET_SPEED

        # Remove bullet if it goes off-screen
        if (
            self.rect.right < 0
            or self.rect.left > WIDTH
            or self.rect.bottom < 0
            or self.rect.top > HEIGHT
        ):
            self.kill()

# Initialize player, enemy, boss, and bullet groups
player = Player()
player_group = pygame.sprite.Group(player)
enemies = pygame.sprite.Group()
bosses = pygame.sprite.Group()
purple_bosses = pygame.sprite.Group()
bullets = pygame.sprite.Group()

current_enemy_spawn_rate = ENEMY_SPAWN_RATE  # Start with the initial spawn rate

# Function to find the nearest enemy
def find_nearest_enemy(player, enemies):
    nearest_enemy = None
    min_distance = float("inf")
    for enemy in enemies:
        dx = enemy.rect.centerx - player.rect.centerx
        dy = enemy.rect.centery - player.rect.centery
        distance = (dx**2 + dy**2) ** 0.5
        if distance < min_distance:
            min_distance = distance
            nearest_enemy = enemy
    return nearest_enemy

# Function to display the level gauge
def draw_level_gauge():
    """Draw the level gauge as a small line at the bottom of the screen."""
    gauge_width = WIDTH - 20  # Full width with padding
    gauge_height = 5  # Small height for the line
    gauge_x = 10  # Left padding
    gauge_y = HEIGHT - 20  # Position near the bottom

    # Draw the outline
    pygame.draw.rect(SCREEN, WHITE, (gauge_x, gauge_y, gauge_width, gauge_height), 2)

    # Draw the fill based on level progress
    fill_width = gauge_width * (level_progress / level_goal)
    pygame.draw.rect(SCREEN, BLUE, (gauge_x, gauge_y, fill_width, gauge_height))

# Function to display lives
def draw_lives():
    """Draw the player's lives using the lives.webp image."""
    for i in range(lives):
        SCREEN.blit(lives_image, (10 + i * 35, 10))

# Function to handle the programming question
def handle_question():
    """Handle the programming question popup with fill-in-the-blank answers."""
    global question_active, question_start_time, current_question, current_answer, player_input, level_progress, pause_start_time, paused_time, correct_answers, wrong_answers

    if not question_active:
        return

    if question_active and pause_start_time is None:
        pause_start_time = time.time()  # Record when the pause started

    # Pause the game
    font = pygame.font.SysFont(None, 30)
    popup_width, popup_height = 500, 300
    popup_x = (WIDTH - popup_width) // 2
    popup_y = (HEIGHT - popup_height) // 2

    # Draw the popup background
    pygame.draw.rect(SCREEN, WHITE, (popup_x, popup_y, popup_width, popup_height))
    pygame.draw.rect(SCREEN, BLACK, (popup_x, popup_y, popup_width, popup_height), 2)  # Border

    # Render the question with line wrapping
    question_lines = wrap_text(current_question, font, popup_width - 40)  # Leave padding
    for i, line in enumerate(question_lines):
        line_surface = font.render(line, True, BLACK)
        SCREEN.blit(line_surface, (popup_x + 20, popup_y + 20 + i * 30))  # Adjust line spacing

    # Display the player's input
    input_surface = font.render(f"Your Answer: {player_input}", True, BLACK)
    SCREEN.blit(input_surface, (popup_x + 20, popup_y + popup_height - 80))

    # Display the timer
    time_elapsed = time.time() - question_start_time  # Calculate elapsed time
    time_left = max(0, question_timer - time_elapsed)  # Ensure time_left is not negative
    timer_surface = font.render(f"Time: {int(time_left)}s", True, BLACK)
    SCREEN.blit(timer_surface, (popup_x + 20, popup_y + popup_height - 40))

    # Check if time is up
    if time_left <= 0:
        question_active = False
        level_progress = 0  # Reset the level gauge
        print("Time's up! A Purple Boss has been summoned!")
        purple_bosses.add(PurpleBoss())  # Summon a purple boss

    # Check for player input submission
    if pygame.key.get_pressed()[pygame.K_RETURN]:  # Press Enter to submit
        normalized_input = player_input.strip()
        if normalized_input == current_answer:
            print("Correct answer! Resetting level progress.")
            question_active = False
            level_progress = 0  # Reset level progress
            correct_answers += 1
        else:
            print("Wrong answer! A Purple Boss has been summoned.")
            question_active = False
            purple_bosses.add(PurpleBoss())  # Summon a purple boss
            wrong_answers += 1

        # Resume the timer
        if pause_start_time is not None:
            paused_time += time.time() - pause_start_time
            pause_start_time = None

        player_input = ""  # Reset the player's input

# Update collisions to decrease HP instead of instant game over
def check_collisions():
    """Check for collisions and reduce the player's HP and lives."""
    global lives, game_over, final_time_survived

    # Check for collisions with normal enemies
    hit_enemies = pygame.sprite.spritecollide(player, enemies, True)  # Remove enemies on collision
    if hit_enemies:
        lives -= len(hit_enemies)  # Decrease lives by the number of enemies that hit the player
        lives = max(lives, 0)  # Ensure lives do not go below 0
        print(f"Player hit by {len(hit_enemies)} enemy/enemies! Lives remaining: {lives}")

    # Check for collisions with bosses
    hit_bosses = pygame.sprite.spritecollide(player, bosses, False)  # Do not remove bosses
    if hit_bosses:
        lives -= 2  # Decrease lives by 2 for each boss collision
        lives = max(lives, 0)  # Ensure lives do not go below 0
        print(f"Player hit by {len(hit_bosses)} boss/bosses! Lives remaining: {lives}")

    # Check for collisions with purple bosses
    hit_purple_bosses = pygame.sprite.spritecollide(player, purple_bosses, False)  # Do not remove purple bosses
    if hit_purple_bosses:
        lives -= 2  # Decrease lives by 2 for each purple boss collision
        lives = max(lives, 0)  # Ensure lives do not go below 0
        print(f"Player hit by {len(hit_purple_bosses)} purple boss/bosses! Lives remaining: {lives}")

    # Trigger game over if lives reach 0
    if lives <= 0 and not game_over:
        game_over = True  # Trigger the Game Over state
        final_time_survived = int(time.time() - start_time - paused_time)  # Store the final time survived

def draw_pause_menu():
    """Draw the pause menu."""
    SCREEN.blit(PAUSE_BACKGROUND, (0, 0))  # Use the blue background

    # Display pause menu text
    pause_text = MINECRAFT_FONT_LARGE.render("Game Paused", True, WHITE)
    SCREEN.blit(pause_text, (WIDTH // 2 - pause_text.get_width() // 2, HEIGHT // 2 - 150))

    resume_text = MINECRAFT_FONT.render("Press ESC to Resume", True, WHITE)
    SCREEN.blit(resume_text, (WIDTH // 2 - resume_text.get_width() // 2, HEIGHT // 2 - 50))

    restart_text = MINECRAFT_FONT.render("Press R to Restart", True, WHITE)
    SCREEN.blit(restart_text, (WIDTH // 2 - restart_text.get_width() // 2, HEIGHT // 2))

    exit_text = MINECRAFT_FONT.render("Press F9 to Exit", True, WHITE)
    SCREEN.blit(exit_text, (WIDTH // 2 - exit_text.get_width() // 2, HEIGHT // 2 + 50))

    bosses_text = MINECRAFT_FONT.render(f"Bosses Defeated: {bosses_defeated}", True, WHITE)
    SCREEN.blit(bosses_text, (WIDTH // 2 - bosses_text.get_width() // 2, HEIGHT // 2 + 100))

    levels_text = MINECRAFT_FONT.render(f"Levels Survived: {levels_survived}", True, WHITE)
    SCREEN.blit(levels_text, (WIDTH // 2 - levels_text.get_width() // 2, HEIGHT // 2 + 150))

def draw_game_over_screen():
    """Draw the game over screen."""
    SCREEN.blit(PAUSE_BACKGROUND, (0, 0))  # Use the blue background

    # Display game over text higher on the screen and in white
    game_over_text = MINECRAFT_FONT_LARGE.render("Game Over!", True, WHITE)
    SCREEN.blit(game_over_text, (WIDTH // 2 - game_over_text.get_width() // 2, HEIGHT // 2 - 220))  # Adjusted position

    # Add a small gap between "Game Over" and "Time Survived"
    time_survived_text = MINECRAFT_FONT.render(f"Time Survived: {final_time_survived} seconds", True, WHITE)
    SCREEN.blit(time_survived_text, (WIDTH // 2 - time_survived_text.get_width() // 2, HEIGHT // 2 - 145))  # Adjusted position

    correct_text = MINECRAFT_FONT.render(f"Correct Answers: {correct_answers}", True, GREEN)
    SCREEN.blit(correct_text, (WIDTH // 2 - correct_text.get_width() // 2, HEIGHT // 2 - 100))

    wrong_text = MINECRAFT_FONT.render(f"Wrong Answers: {wrong_answers}", True, RED)
    SCREEN.blit(wrong_text, (WIDTH // 2 - wrong_text.get_width() // 2, HEIGHT // 2 - 50))

    bosses_text = MINECRAFT_FONT.render(f"Bosses Defeated: {bosses_defeated}", True, WHITE)
    SCREEN.blit(bosses_text, (WIDTH // 2 - bosses_text.get_width() // 2, HEIGHT // 2))

    levels_text = MINECRAFT_FONT.render(f"Levels Survived: {levels_survived}", True, WHITE)
    SCREEN.blit(levels_text, (WIDTH // 2 - levels_text.get_width() // 2, HEIGHT // 2 + 50))

    restart_text = MINECRAFT_FONT.render("Press R to Restart", True, WHITE)
    SCREEN.blit(restart_text, (WIDTH // 2 - restart_text.get_width() // 2, HEIGHT // 2 + 100))

    exit_text = MINECRAFT_FONT.render("Press F9 to Exit", True, WHITE)
    SCREEN.blit(exit_text, (WIDTH // 2 - exit_text.get_width() // 2, HEIGHT // 2 + 150))

def draw_elapsed_time():
    """Draw the elapsed time at the top center of the screen."""
    font = pygame.font.SysFont(None, 30)
    if pause_start_time is not None:
        # If the game is paused, calculate paused time
        current_paused_time = time.time() - pause_start_time
    else:
        current_paused_time = 0

    # Calculate elapsed time
    elapsed_time = int(time.time() - start_time - paused_time - current_paused_time)
    elapsed_time = max(0, elapsed_time)  # Ensure elapsed time is not negative
    time_text = font.render(f"Time: {elapsed_time} seconds", True, BLACK)
    SCREEN.blit(time_text, (WIDTH // 2 - time_text.get_width() // 2, 10))

def wrap_text(text, font, max_width):
    """Split text into multiple lines to fit within the specified width."""
    words = text.split(' ')
    lines = []
    current_line = ""

    for word in words:
        test_line = f"{current_line} {word}".strip()
        if font.size(test_line)[0] <= max_width:
            current_line = test_line
        else:
            lines.append(current_line)
            current_line = word

    if current_line:
        lines.append(current_line)

    return lines

def show_modal_confirmation(message):
    """Display a modal confirmation window with a custom message."""
    modal_running = True

    # Load the blue background image for the modal
    modal_background_image = pygame.image.load("images/bluebg.jpg")
    modal_background_image = pygame.transform.scale(modal_background_image, (400, 200))
    modal_rect = modal_background_image.get_rect(center=(WIDTH // 2, HEIGHT // 2))

    # Modal text
    modal_font = pygame.font.Font("images/Minecraft.ttf", 36)
    question_text = modal_font.render(message, True, WHITE)  # Change text color to WHITE
    question_rect = question_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 50))

    yes_text = modal_font.render("Y: Yes", True, WHITE)  # Change text color to WHITE
    yes_rect = yes_text.get_rect(center=(WIDTH // 2 - 100, HEIGHT // 2 + 50))

    no_text = modal_font.render("N: No", True, WHITE)  # Change text color to WHITE
    no_rect = no_text.get_rect(center=(WIDTH // 2 + 100, HEIGHT // 2 + 50))

    while modal_running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_y:  # Confirm action
                    modal_running = False
                    return True  # User confirmed
                elif event.key == pygame.K_n:  # Cancel action
                    modal_running = False
                    return False  # User canceled

        # Draw the modal
        SCREEN.blit(PAUSE_BACKGROUND, (0, 0))  # Use the main blue background
        SCREEN.blit(modal_background_image, modal_rect)  # Use the blue background for the modal
        SCREEN.blit(question_text, question_rect)
        SCREEN.blit(yes_text, yes_rect)
        SCREEN.blit(no_text, no_rect)

        pygame.display.flip()
        clock.tick(30)

# Main game loop
frame_count = 0
running = True
game_over = False

def main():
    global running, frame_count, game_over, paused, question_active, question_start_time
    global current_question, current_choices, current_answer, lives, level_progress
    global pause_start_time, paused_time, correct_answers, wrong_answers
    global bosses_defeated, levels_survived, start_time, final_time_survived, player_input
    global current_enemy_spawn_rate  # Declare this as global to avoid UnboundLocalError

    # Get the background and player asset from the command-line arguments
    background_file = sys.argv[1] if len(sys.argv) > 1 else "defaultbg.png"
    player_asset = sys.argv[2] if len(sys.argv) > 2 else "images/customchara.png"

    # Construct the full paths for the background and player asset
    background_path = join("images", background_file)
    player_asset_path = join("images", player_asset)

    # Load the background image
    try:
        background = pygame.image.load(background_path)
        background = pygame.transform.scale(background, (WIDTH, HEIGHT))
    except FileNotFoundError:
        print(f"Error: Background file '{background_path}' not found. Using white background.")
        background = None

    # Load the player asset
    try:
        player_image = pygame.image.load(player_asset_path)
        player_image = pygame.transform.scale(player_image, (50, 50))  # Scale the player image
    except FileNotFoundError:
        print(f"Error: Player asset '{player_asset_path}' not found. Using default placeholder.")
        player_image = pygame.Surface((50, 50))  # Placeholder player image
        player_image.fill((0, 255, 0))  # Green placeholder

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    paused = not paused  # Toggle pause state
                elif event.key == pygame.K_r and not question_active:
                    # Show restart confirmation
                    if show_modal_confirmation("Do you want to restart?"):
                        # Restart the game
                        start_time = time.time()
                        correct_answers = 0
                        wrong_answers = 0
                        lives = 5
                        level_progress = 0
                        player.current_hp = player.max_hp
                        enemies.empty()
                        bosses.empty()
                        purple_bosses.empty()
                        bullets.empty()
                        game_over = False
                        paused = False
                elif event.key == pygame.K_F9:
                    # Show exit confirmation
                    if show_modal_confirmation("Do you want to exit?"):
                        running = False
                elif event.key == pygame.K_SPACE and not paused and not game_over and not question_active:
                    # Shoot a bullet toward the nearest enemy
                    nearest_enemy = find_nearest_enemy(player, enemies)
                    if nearest_enemy:
                        dx = nearest_enemy.rect.centerx - player.rect.centerx
                        dy = nearest_enemy.rect.centery - player.rect.centery
                        dist = max(1, (dx**2 + dy**2) ** 0.5)  # Normalize the direction
                        dx /= dist
                        dy /= dist
                        bullet = Bullet(player.rect.centerx, player.rect.centery, dx, dy)
                        bullets.add(bullet)
                elif event.key == pygame.K_RETURN and question_active:
                    # Normalize input and answer for comparison
                    normalized_input = player_input.strip().lower()
                    normalized_answer = current_answer.strip().lower()

                    if normalized_input == normalized_answer:
                        print("Correct answer! Applying buff.")
                        question_active = False
                        level_progress = 0  # Reset level progress

                        # Apply a random buff
                        buff = random.choice([BUFF_RESET_HEALTH, BUFF_GAIN_HP])
                        player.apply_buff(buff)

                        correct_answers += 1
                    else:
                        print("Wrong answer! Spawning Purple Boss.")
                        question_active = False
                        lives -= 1
                        level_progress = 0  # Reset level progress
                        purple_bosses.add(PurpleBoss())
                        wrong_answers += 1

                    # Resume the timer
                    if pause_start_time is not None:
                        paused_time += time.time() - pause_start_time
                        pause_start_time = None

                    player_input = ""  # Reset the player's input
                elif event.key == pygame.K_BACKSPACE and question_active:
                    # Remove the last character from the player's input
                    player_input = player_input[:-1]
                elif question_active:
                    # Add the typed character to the player's input
                    player_input += event.unicode
                elif event.key == pygame.K_r and game_over:
                    # Restart the game
                    start_time = time.time()
                    correct_answers = 0
                    wrong_answers = 0
                    lives = 5
                    level_progress = 0
                    player.current_hp = player.max_hp
                    enemies.empty()
                    bosses.empty()
                    purple_bosses.empty()
                    bullets.empty()
                    game_over = False
                    paused = False
                elif event.key == pygame.K_F9 and game_over:
                    # Exit the game
                    running = False
                elif event.key in [pygame.K_1, pygame.K_2, pygame.K_3, pygame.K_4] and question_active:
                    # Map key presses to choices
                    selected_choice = str(event.key - pygame.K_1 + 1)  # Convert key press to "1", "2", "3", or "4"

                    if selected_choice == current_answer:
                        print("Correct answer!")
                        question_active = False
                        level_progress = 0  # Reset level progress
                        correct_answers += 1
                    else:
                        print("Wrong answer! Spawning Purple Boss.")
                        question_active = False
                        lives -= 1
                        level_progress = 0  # Reset level progress
                        purple_bosses.add(PurpleBoss())  # Spawn a purple boss
                        wrong_answers += 1

                    # Resume the timer
                    if pause_start_time is not None:
                        paused_time += time.time() - pause_start_time
                        pause_start_time = None
                elif event.key in [pygame.K_a, pygame.K_b, pygame.K_c, pygame.K_d] and question_active:
                    # Map key presses to choices
                    selected_choice = chr(event.key).upper()  # Convert key press to "A", "B", "C", or "D"

                    # Map "A", "B", "C", "D" to "1", "2", "3", "4" for comparison
                    choice_mapping = {"A": "1", "B": "2", "C": "3", "D": "4"}
                    selected_choice_number = choice_mapping.get(selected_choice)

                    if selected_choice_number == current_answer:
                        print("Correct answer! Resetting lives.")
                        question_active = False
                        lives = 5  # Reset lives to the maximum
                        level_progress = 0  # Reset level progress
                        correct_answers += 1
                    else:
                        print("Wrong answer! Spawning Purple Boss.")
                        question_active = False
                        purple_bosses.add(PurpleBoss())  # Spawn a purple boss
                        wrong_answers += 1

                    # Resume the timer
                    if pause_start_time is not None:
                        paused_time += time.time() - pause_start_time
                        pause_start_time = None

        # Pause game logic if a question is active
        if question_active:
            SCREEN.fill(WHITE)
            handle_question()
            pygame.display.flip()
            clock.tick(FPS)
            continue

        if game_over:
            SCREEN.fill(WHITE)
            draw_game_over_screen()  # Display the Game Over screen
            pygame.display.flip()
            clock.tick(FPS)
            continue

        if paused:
            SCREEN.fill(WHITE)
            draw_pause_menu()
            pygame.display.flip()
            clock.tick(FPS)
            continue

        # Update game logic
        keys = pygame.key.get_pressed()
        player_group.update(keys)

        # Spawn enemies
        frame_count += 1
        if frame_count % current_enemy_spawn_rate == 0:
            enemies.add(Enemy())

        # Gradually decrease the spawn rate as the game progresses
        if frame_count % (FPS * 30) == 0:  # Every 30 seconds
            current_enemy_spawn_rate = max(10, current_enemy_spawn_rate - 1)  # Decrease spawn rate, but not below 10
            print(f"Enemy spawn rate increased! Current spawn rate: {current_enemy_spawn_rate}")

        # Spawn bosses periodically
        if frame_count % (FPS * 60) == 0:  # Every 60 seconds
            bosses.add(Boss())
            print("A new boss has spawned!")

        # Update enemies, bosses, purple bosses, and bullets
        enemies.update(player.rect.center)
        bosses.update(player.rect.center)
        purple_bosses.update(player.rect.center)
        bullets.update()

        # Check for collisions and decrease HP
        check_collisions()

        # Check for bullet-enemy collisions
        for bullet in bullets:
            # Check for collisions with normal enemies
            hit_enemies = pygame.sprite.spritecollide(bullet, enemies, True)
            if hit_enemies:
                bullet.kill()
                level_progress += 10  # Increase level progress
                if level_progress >= level_goal:
                    question_active = True
                    question_start_time = time.time()
                    question = random.choice(questions)
                    current_question = question["question"]
                    current_answer = question["answer"]
                    
                    # Only assign choices if they exist in the question
                    current_choices = question.get("choices", None)  # Use None if "choices" is not present

                    player_input = ""  # Reset the player's input
                    level_progress = 0  # Reset level progress when a question appears
                    levels_survived += 1  # Increment levels survived

            # Check for collisions with bosses
            hit_bosses = pygame.sprite.spritecollide(bullet, bosses, False)
            for boss in hit_bosses:
                boss.hits -= 1
                bullet.kill()
                if boss.hits <= 0:
                    boss.kill()
                    bosses_defeated += 1  # Increment bosses defeated
                    level_progress += 20  # Boss gives more progress
                    if level_progress >= level_goal:
                        question_active = True
                        question_start_time = time.time()
                        question = random.choice(questions)
                        current_question = question["question"]
                        current_answer = question["answer"]
                        
                        # Only assign choices if they exist in the question
                        current_choices = question.get("choices", None)  # Use None if "choices" is not present

                        player_input = ""  # Reset the player's input
                        level_progress = 0  # Reset level progress when a question appears
                        levels_survived += 1  # Increment levels survived

            # Check for collisions with purple bosses
            hit_purple_bosses = pygame.sprite.spritecollide(bullet, purple_bosses, False)
            for purple_boss in hit_purple_bosses:
                purple_boss.hits -= 1
                bullet.kill()
                if purple_boss.hits <= 0:
                    purple_boss.kill()
                    bosses_defeated += 1  # Increment bosses defeated
                    level_progress += 30  # Purple boss gives more progress
                    if level_progress >= level_goal:
                        question_active = True
                        question_start_time = time.time()
                        question = random.choice(questions)
                        current_question = question["question"]
                        current_answer = question["answer"]
                        
                        # Only assign choices if they exist in the question
                        current_choices = question.get("choices", None)  # Use None if "choices" is not present

                        player_input = ""  # Reset the player's input
                        level_progress = 0  # Reset level progress when a question appears
                        levels_survived += 1  # Increment levels survived

        # Draw everything
        if background:
            SCREEN.blit(background, (0, 0))
        else:
            SCREEN.fill(WHITE)  # Fallback to white background
        player_group.draw(SCREEN)
        enemies.draw(SCREEN)
        bosses.draw(SCREEN)
        purple_bosses.draw(SCREEN)
        bullets.draw(SCREEN)
        draw_level_gauge()  # Draw the updated level gauge at the bottom
        draw_lives()
        draw_elapsed_time()  # Draw the elapsed time
        handle_question()

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()