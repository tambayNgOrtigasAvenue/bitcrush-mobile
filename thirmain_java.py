import pygame
import random
import sys

# Initialize Pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Coding Mode")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# Fonts
FONT = pygame.font.Font(None, 36)
INFO_FONT = pygame.font.Font(None, 24)  # Smaller font size for info text

# Load the Minecraft font
MINECRAFT_FONT = pygame.font.Font("images/Minecraft.ttf", 36)  # Adjust size as needed
MINECRAFT_FONT_LARGE = pygame.font.Font("images/Minecraft.ttf", 74)  # Larger font for titles

# Game variables
player_health = 100
enemy_health = 100
current_word = ""
expected_output = ""
typed_word = ""
words = []

# Progress tracking variables
correct_answers = 0
incorrect_answers = 0

# Clock for controlling frame rate
clock = pygame.time.Clock()

# Add a paused variable
paused = False

# Add a timer variable
time_limit = 10  # Time limit in seconds
time_remaining = time_limit
last_time = pygame.time.get_ticks()  # Track the last time a word was reset

# Add a round variable
round_number = 1
max_rounds = 10

# Track used prompts for the current round
used_prompts = []

# Damage values
player_to_opponent_damage = 10  # Default damage dealt by the player to the opponent
opponent_to_player_damage = 5   # Default damage dealt by the opponent to the player

# Define prompts for each difficulty level
basic_prompts = [
    {'syntax': 'System.out.println("Hello, World!");', 'output': 'Hello, World!'},
    {'syntax': 'System.out.println(5 + 3);', 'output': '8'},
    {'syntax': 'System.out.println(10 - 4);', 'output': '6'},
    {'syntax': 'System.out.println(2 * 3);', 'output': '6'},
    {'syntax': 'System.out.println(10 / 2);', 'output': '5'},
    {'syntax': 'int x = 5;\nSystem.out.println(x);', 'output': '5'},
    {'syntax': 'System.out.println("Java".length());', 'output': '4'},
    {'syntax': 'System.out.println("A" + "B");', 'output': 'AB'},
    {'syntax': 'int y = 10;\nSystem.out.println(y);', 'output': '10'},
    {'syntax': 'System.out.println(15 % 4);', 'output': '3'},
    {'syntax': 'System.out.println\n((int)Math.pow(3, 2));', 'output': '9'},
    {'syntax': 'String z = "Code"; \nSystem.out.println(z);', 'output': 'Code'},
    {'syntax': 'System.out.println\n("Easy".toLowerCase());', 'output': 'easy'},
    {'syntax': 'System.out.println\n("Basic".toUpperCase());', 'output': 'BASIC'},
    {'syntax': 'System.out.println(100 / 4);', 'output': '25'},
    {'syntax': 'System.out.println(7 + 8);', 'output': '15'},
    {'syntax': 'System.out.println\n("Java".charAt(0));', 'output': 'J'},
    {'syntax': 'System.out.println\n("Hello".substring(0, 3));', 'output': 'Hel'},
    {'syntax': 'System.out.println(20 - 5);', 'output': '15'},
    {'syntax': 'System.out.println(3 * 7);', 'output': '21'},
]

intermediate_prompts = [
    {'syntax': 'String name = "Java"; System.out.println(name);', 'output': 'Java'},
    {'syntax': 'System.out.println("Java".toUpperCase());', 'output': 'JAVA'},
    {'syntax': 'System.out.println("Hello".length());', 'output': '5'},
    {'syntax': 'System.out.println("Java".toLowerCase());', 'output': 'java'},
    {'syntax': 'System.out.println("Hello".substring(0, 2));', 'output': 'He'},
    {'syntax': 'int[] arr = {1, 2, 3}; System.out.println(arr[1]);', 'output': '2'},
    {'syntax': 'System.out.println("Java".replace("a", "o"));', 'output': 'Jovo'},
    {'syntax': 'System.out.println(Math.max(10, 20));', 'output': '20'},
    {'syntax': 'int[] nums = {10, 20, 30}; System.out.println(nums.length);', 'output': '3'},
    {'syntax': 'System.out.println("Intermediate".indexOf("e"));', 'output': '2'},
    {'syntax': 'System.out.println("Code".repeat(2));', 'output': 'CodeCode'},
    {'syntax': 'int a = 5; int b = 10; System.out.println(a + b);', 'output': '15'},
    {'syntax': 'System.out.println("Java".substring(0, 4));', 'output': 'Java'},
    {'syntax': 'System.out.println("Hello".replace("l", "p"));', 'output': 'Heppo'},
    {'syntax': 'System.out.println(Math.min(5, 10));', 'output': '5'},
    {'syntax': 'System.out.println("Java".contains("va"));', 'output': 'true'},
    {'syntax': 'System.out.println("Hello".endsWith("o"));', 'output': 'true'},
    {'syntax': 'System.out.println("Java".startsWith("J"));', 'output': 'true'},
    {'syntax': 'System.out.println("Intermediate".lastIndexOf("e"));', 'output': '10'},
]

advanced_prompts = [
    {'syntax': 'for (int i = 0; i < 3; i++) { System.out.println(i); }', 'output': '0\n1\n2'},
    {'syntax': 'for (int i = 0; i < 3; i++) { for (int j = 0; j < 2; j++) { System.out.println(i + j); } }', 'output': '0\n1\n1\n2\n2\n3'},
    {'syntax': 'System.out.println(Math.pow(2, Math.sqrt(4)));', 'output': '4.0'},
    {'syntax': 'System.out.println("Java".replace("a", "o"));', 'output': 'Jovo'},
    {'syntax': 'System.out.println("Java".indexOf("a"));', 'output': '1'},
    {'syntax': 'System.out.println("Java".lastIndexOf("a"));', 'output': '3'},
    {'syntax': 'int[][] matrix = {{1, 2}, {3, 4}}; System.out.println(matrix[1][0]);', 'output': '3'},
    {'syntax': 'System.out.println("Java".startsWith("J"));', 'output': 'true'},
    {'syntax': 'Map<String, Integer> obj = Map.of("a", 1, "b", 2); System.out.println(obj.get("a"));', 'output': '1'},
    {'syntax': 'List<Integer> nums = List.of(1, 2, 3); nums.add(4); System.out.println(nums);', 'output': '[1, 2, 3, 4]'},
    {'syntax': 'System.out.println(Arrays.stream(new int[]{1, 2, 3}).map(x -> x * 2).toArray());', 'output': '[2, 4, 6]'},
    {'syntax': 'String str = "Advanced"; System.out.println(new StringBuilder(str).reverse().toString());', 'output': 'decnavdA'},
    {'syntax': 'System.out.println(Math.round(4.7));', 'output': '5'},
    {'syntax': 'System.out.println("Advanced".substring(2, 5));', 'output': 'van'},
    {'syntax': 'System.out.println("Advanced".replaceAll("a", "o"));', 'output': 'ovonced'},
    {'syntax': 'System.out.println("Advanced".matches(".*ced"));', 'output': 'true'},
    {'syntax': 'System.out.println("Advanced".charAt(3));', 'output': 'a'},
    {'syntax': 'System.out.println("Advanced".toUpperCase());', 'output': 'ADVANCED'},
    {'syntax': 'System.out.println("Advanced".toLowerCase());', 'output': 'advanced'},
]

# Load images
man_image = pygame.image.load("images/man2.png")  # Load the left-side image (updated to man2.jpg)a
frog_image = pygame.image.load("images/greenfrog.png")  # Load the right-side image

# Scale images to fit under the health bars (optional)
man_image = pygame.transform.scale(man_image, (100, 100))  # Resize to 100x100
frog_image = pygame.transform.scale(frog_image, (100, 100))  # Resize to 100x100

# Load the lives image
lives_image = pygame.image.load("images/lives.webp")  # Load the lives image
lives_image = pygame.transform.scale(lives_image, (40, 40))  # Resize to 40x40

# Load background images
backgrounds = [
    pygame.image.load("images/autumnbg.png"),
    pygame.image.load("images/desertbg.png"),
    pygame.image.load("images/springbg.jpg"),
    pygame.image.load("images/winterbg.png")
]
background_index = 0  # Start with the first background
current_background = pygame.transform.scale(backgrounds[background_index], (WIDTH, HEIGHT))  # Scale to screen size

# Get the background file name from the command-line argument
background_file = sys.argv[1] if len(sys.argv) > 1 else "autumnbg.png"

# Load the background image
try:
    background = pygame.image.load(f"images/{background_file}")
    current_background = pygame.transform.scale(background, (800, 600))  # Adjust dimensions as needed
except pygame.error as e:
    print(f"Error loading background image: {e}")
    sys.exit(1)

# Get the selected asset from the command-line argument or use the default
selected_asset = sys.argv[2] if len(sys.argv) > 2 else "images/man1cleared.png"

# Load the selected player asset
man_image = pygame.image.load(selected_asset)
man_image = pygame.transform.scale(man_image, (100, 100))  # Resize to 100x100

# Load the opponent image (randomly selected)
opponent_images = [
    "images/greenfrog3cleared.png",
    "images/purplefrog2cleared.png",
    "images/redfrog2cleared.png"
]
selected_opponent_image = random.choice(opponent_images)
frog_image = pygame.image.load(selected_opponent_image)
frog_image = pygame.transform.scale(frog_image, (100, 100))  # Resize to 100x100

# Load the blue background image
pause_background = pygame.image.load("images/bluebg.jpg")
pause_background = pygame.transform.scale(pause_background, (WIDTH, HEIGHT))

# Function to change the opponent image
def change_opponent():

    """Change the opponent image."""
    global frog_image
    selected_opponent_image = random.choice(opponent_images)
    frog_image = pygame.image.load(selected_opponent_image)
    frog_image = pygame.transform.scale(frog_image, (100, 100))  # Resize to 100x100

def draw_health_bars():
    """Draw health bars for player and enemy."""
    pygame.draw.rect(screen, RED, (50, 300, 200, 20))  # Player health bar background (lowered further)
    pygame.draw.rect(screen, GREEN, (50, 300, 2 * player_health, 20))  # Player health bar foreground (lowered further)
    pygame.draw.rect(screen, RED, (500, 300, 200, 20))  # Enemy health bar background (lowered further)
    pygame.draw.rect(screen, GREEN, (500, 300, 2 * enemy_health, 20))  # Enemy health bar foreground (lowered further)

def draw_text(text, x, y, color=BLACK, font=FONT):
    """Draw text on the screen."""
    rendered_text = font.render(text, True, color)
    screen.blit(rendered_text, (x, y))

def reset_word():
    """Reset the current word, timer, and generate a new one."""
    global current_word, expected_output, typed_word, time_remaining, last_time, used_prompts

    # Filter unused prompts
    unused_prompts = [word for word in words if word not in used_prompts]

    # If all prompts are used, reset the used_prompts list
    if not unused_prompts:
        used_prompts = []  # Reset the used prompts
        unused_prompts = words  # Repopulate unused prompts with all available prompts

    # Check if there are still prompts available
    if not unused_prompts:
        print("Error: No unused prompts available!")  # Debugging output
        current_word = ""
        expected_output = ""
        return  # Exit the function to avoid errors

    # Select a random word from the unused prompts
    word_data = random.choice(unused_prompts)
    used_prompts.append(word_data)  # Mark the prompt as used

    current_word = word_data['syntax']  # Java syntax
    expected_output = word_data['output']  # Expected output
    typed_word = ""
    time_remaining = time_limit  # Reset the timer
    last_time = pygame.time.get_ticks()  # Update the last reset time

    print(f"New word selected: {current_word}")  # Debugging output

def reset_round():
    """Reset the game for the next opponent."""
    global player_health, enemy_health, words, used_prompts

    print("Resetting for the next opponent...")  # Debugging output

    player_health = 100  # Reset player health
    enemy_health = 100  # Reset enemy health

    # Change the opponent image
    change_opponent()

    # Ensure the words list is populated
    if not round_words:
        print("Error: round_words is empty!")  # Debugging output
        return

    # Flatten all prompts into the words list
    words = [prompt for prompt in round_words]  # Ensure `words` contains dictionaries

    # Check if words are available
    if not words:
        print("Error: No words available after resetting round!")  # Debugging output
        return

    used_prompts = []  # Reset used prompts for the new opponent

    reset_word()  # Reset the current word

def reset_progress():
    """Reset progress tracking variables."""
    global correct_answers, incorrect_answers, round_number
    correct_answers = 0
    incorrect_answers = 0
    round_number = 1  # Reset the round number

# Add global variables for rounds
current_round = 1  # Start with the first round
total_rounds = 3  # Default total rounds (will change based on difficulty)

def draw_round_info():
    """Display the current round and difficulty on the screen."""
    round_text = f"Round {current_round}/{total_rounds} - Difficulty: {difficulty}"
    draw_text(round_text, WIDTH // 2 - 150, 10, BLACK, INFO_FONT)  # Display at the top center

def next_round():
    """Progress to the next round or difficulty."""
    global current_round, player_health, enemy_health

    if current_round < total_rounds:
        # Move to the next round
        current_round += 1
        print(f"Starting Round {current_round}/{total_rounds} in {difficulty} difficulty!")  # Debugging output
        player_health = 100
        enemy_health = 100
        reset_round()  # Reset the round
    else:
        # All rounds in the current difficulty are completed
        show_progress_tracker(f"Completed {difficulty} Difficulty!")  # Show completion message
        pygame.quit()
        sys.exit()

def set_difficulty():
    """Set the difficulty level for the game using a Pygame menu."""
    global time_limit, round_words, difficulty, words, used_prompts, total_rounds
    global player_to_opponent_damage, opponent_to_player_damage  # Include damage variables
    global player_health, enemy_health  # Include health variables

    reset_progress()  # Reset progress when changing difficulty

    # Load the blue background image
    difficulty_background = pygame.image.load("images/bluebg.jpg")
    difficulty_background = pygame.transform.scale(difficulty_background, (WIDTH, HEIGHT))

    menu_running = True
    while menu_running:
        # Draw the blue background
        screen.blit(difficulty_background, (0, 0))

        # Use the Minecraft font for the difficulty menu
        minecraft_font = pygame.font.Font("images/Minecraft.ttf", 36)

        # Draw the difficulty options in white
        draw_text("Select Difficulty:", WIDTH // 2 - 150, HEIGHT // 2 - 150, WHITE, minecraft_font)
        draw_text("1. Easy", WIDTH // 2 - 150, HEIGHT // 2 - 100, WHITE, minecraft_font)
        draw_text("2. Intermediate", WIDTH // 2 - 150, HEIGHT // 2 - 50, WHITE, minecraft_font)
        draw_text("3. Advanced", WIDTH // 2 - 150, HEIGHT // 2, WHITE, minecraft_font)
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    time_limit = 15  # Easy: 15 seconds per word
                    round_words = basic_prompts  # Use basic prompts
                    difficulty = "Easy"
                    total_rounds = 3  # Easy has 3 rounds
                    player_to_opponent_damage = 20  # High damage to opponent
                    opponent_to_player_damage = 2   # Low damage to player
                    print(f"Difficulty set to Easy. Prompts: {len(round_words)}")  # Debugging output
                    menu_running = False
                elif event.key == pygame.K_2:
                    time_limit = 10  # Intermediate: 10 seconds per word
                    round_words = intermediate_prompts  # Use intermediate prompts
                    difficulty = "Intermediate"
                    total_rounds = 5  # Intermediate has 5 rounds
                    player_to_opponent_damage = 10  # Balanced damage
                    opponent_to_player_damage = 5   # Balanced damage
                    print(f"Difficulty set to Intermediate. Prompts: {len(round_words)}")  # Debugging output
                    menu_running = False
                elif event.key == pygame.K_3:
                    time_limit = 5  # Advanced: 5 seconds per word
                    round_words = advanced_prompts  # Use advanced prompts
                    difficulty = "Advanced"
                    total_rounds = 8  # Advanced has 8 rounds
                    player_to_opponent_damage = 5   # Low damage to opponent
                    opponent_to_player_damage = 10  # High damage to player
                    print(f"Difficulty set to Advanced. Prompts: {len(round_words)}")  # Debugging output
                    menu_running = False

    # Reset words and used prompts after selecting difficulty
    words = [prompt for prompt in round_words]  # Ensure `words` contains dictionaries
    if not words:
        print("Error: No words available after selecting difficulty!")  # Debugging output
    used_prompts = []  # Clear used prompts

    # Reset health values
    player_health = 100  # Reset player health
    enemy_health = 100  # Reset enemy health
    print("Health values reset after changing difficulty.")  # Debugging output

def show_progress_tracker(win_message):
    """Display the progress tracker after the game ends."""
    global correct_answers, incorrect_answers, running

    print(f"Game Over: {win_message}")  # Debugging output
    print(f"Correct Answers: {correct_answers}, Incorrect Answers: {incorrect_answers}")  # Debugging output

    # Load the current high score
    high_score = load_high_score()

    # Calculate the player's score (only count correct answers)
    player_score = correct_answers

    # Update the high score if the player's score is higher
    if player_score > high_score:
        high_score = player_score
        save_high_score(high_score)

    # Display the game over screen
    screen.blit(pause_background, (0, 0))  # Use the blue background

    # Use a smaller font for the game over/completion message
    smaller_font = pygame.font.Font("images/Minecraft.ttf", 50)  # Adjust size as needed
    game_over_text = smaller_font.render(win_message, True, WHITE)
    game_over_rect = game_over_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 150))
    screen.blit(game_over_text, game_over_rect)

    score_text = MINECRAFT_FONT.render(f"Your Score: {player_score}", True, WHITE)
    score_rect = score_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 50))
    screen.blit(score_text, score_rect)

    high_score_text = MINECRAFT_FONT.render(f"High Score: {high_score}", True, WHITE)
    high_score_rect = high_score_text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
    screen.blit(high_score_text, high_score_rect)

    quit_text = MINECRAFT_FONT.render("Press ENTER to Quit", True, WHITE)
    quit_rect = quit_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 100))
    screen.blit(quit_text, quit_rect)

    pygame.display.flip()

    # Wait for the player to press ENTER to quit
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:  # Quit the game
                    waiting = False
                    running = False  # Exit the main game loop

def pause_game():
    """Pause the game and display a pause menu with the current score and progress."""
    global running, paused

    # Pause text
    pause_text = MINECRAFT_FONT_LARGE.render("Game Paused", True, (255, 255, 255))
    pause_rect = pause_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 200))

    # High score text
    high_score = load_high_score()
    high_score_text = MINECRAFT_FONT.render(f"High Score: {high_score}", True, WHITE)
    high_score_rect = high_score_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 150))

    # Difficulty text
    difficulty_text = MINECRAFT_FONT.render(f"Difficulty: {difficulty}", True, WHITE)
    difficulty_rect = difficulty_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 100))

    # Opponents defeated text
    opponents_defeated = correct_answers  # Assuming each correct answer defeats one opponent
    opponents_text = MINECRAFT_FONT.render(f"Opponents Defeated: {opponents_defeated}", True, WHITE)
    opponents_rect = opponents_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 50))

    # Correct and incorrect prompts text
    correct_text = MINECRAFT_FONT.render(f"Correct Prompts: {correct_answers}", True, GREEN)
    correct_rect = correct_text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
    incorrect_text = MINECRAFT_FONT.render(f"Incorrect Prompts: {incorrect_answers}", True, RED)
    incorrect_rect = incorrect_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 50))

    # Instructions
    resume_text = MINECRAFT_FONT.render("Press ESC to Resume", True, (255, 255, 255))
    resume_rect = resume_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 100))

    quit_text = MINECRAFT_FONT.render("Press F9 to Exit", True, (255, 255, 255))
    quit_rect = quit_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 150))

    difficulty_change_text = MINECRAFT_FONT.render("Press D to Change Difficulty", True, (255, 255, 255))
    difficulty_change_rect = difficulty_change_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 200))

    while paused:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:  # Unpause the game
                    paused = False
                elif event.key == pygame.K_F9:  # Quit the game
                    if show_modal_confirmation("Do you want to exit?"):  # Show exit confirmation
                        pygame.quit()
                        sys.exit()
                elif event.key == pygame.K_d:  # Change difficulty
                    if show_modal_confirmation("Do you want to change difficulty?"):  # Show modal and check response
                        set_difficulty()  # Open the difficulty selection menu
                        paused = False  # Resume the game after changing difficulty

        # Draw the pause menu
        screen.blit(pause_background, (0, 0))  # Use the blue background
        screen.blit(pause_text, pause_rect)
        screen.blit(high_score_text, high_score_rect)
        screen.blit(difficulty_text, difficulty_rect)
        screen.blit(opponents_text, opponents_rect)
        screen.blit(correct_text, correct_rect)
        screen.blit(incorrect_text, incorrect_rect)
        screen.blit(resume_text, resume_rect)
        screen.blit(quit_text, quit_rect)
        screen.blit(difficulty_change_text, difficulty_change_rect)

        pygame.display.flip()
        clock.tick(30)  # Limit the frame rate during pause

def load_high_score():
    """Load the high score from a file."""
    try:
        with open("highscore_java.txt", "r") as file:
            return int(file.read().strip())
    except (FileNotFoundError, ValueError):
        return 0  # Default to 0 if the file doesn't exist or is invalid


def save_high_score(new_high_score):
    """Save the high score to a file."""
    with open("highscore_java.txt", "w") as file:
        file.write(str(new_high_score))

def draw_bubble_text(text, x, y, font, text_color, bubble_color, padding=10, max_width=300):
    """Draw text inside a bubble with dynamic wrapping and ensure it stays within the screen."""
    # Wrap the text into multiple lines
    lines = wrap_text(text, font, max_width)

    # Calculate the bubble dimensions based on the wrapped text
    line_height = font.size("Tg")[1]  # Height of a single line of text
    bubble_width = max(font.size(line)[0] for line in lines) + 2 * padding
    bubble_height = len(lines) * line_height + 2 * padding

    # Ensure the bubble stays within the screen boundaries
    if x + bubble_width > WIDTH:
        x = WIDTH - bubble_width - 10  # Adjust x to fit within the screen
    if y + bubble_height > HEIGHT:
        y = HEIGHT - bubble_height - 10  # Adjust y to fit within the screen

    # Draw the bubble (rounded rectangle)
    bubble_rect = pygame.Rect(x, y, bubble_width, bubble_height)
    pygame.draw.rect(screen, bubble_color, bubble_rect, border_radius=8)

    # Draw each line of text inside the bubble
    for i, line in enumerate(lines):
        text_surface = font.render(line, True, text_color)
        screen.blit(text_surface, (bubble_rect.x + padding, bubble_rect.y + padding + i * line_height))

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
        screen.blit(pause_background, (0, 0))  # Use the main blue background
        screen.blit(modal_background_image, modal_rect)  # Use the blue background for the modal
        screen.blit(question_text, question_rect)
        screen.blit(yes_text, yes_rect)
        screen.blit(no_text, no_rect)

        pygame.display.flip()
        clock.tick(30)

# Load the high score at the start of the game
high_score = load_high_score()

# Initialize the game
set_difficulty()  # Select difficulty
reset_round()  # Start the first round

# Main game loop
running = True
while running:
    screen.blit(current_background, (0, 0))  # Draw the current background

    # Draw the round and difficulty info
    draw_round_info()

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:  # Pause/Resume the game
                paused = not paused
                if paused:
                    pause_game()  # Call the pause menu
            elif event.key == pygame.K_F9:  # Exit the game
                if show_modal_confirmation("Do you want to exit?"):  # Show exit confirmation
                    running = False
            elif not paused:  # Only handle other keys if the game is not paused
                if event.key == pygame.K_BACKSPACE:
                    typed_word = typed_word[:-1]  # Remove the last character
                elif event.key == pygame.K_RETURN:  # Check the word when Enter is pressed
                    if typed_word == expected_output:  # Compare typed word with the expected output
                        enemy_health -= player_to_opponent_damage  # Reduce enemy health
                        correct_answers += 1  # Increment correct answers
                        if enemy_health <= 0:  # Enemy defeated
                            next_round()  # Progress to the next round
                    else:
                        player_health -= opponent_to_player_damage  # Reduce player health
                        incorrect_answers += 1  # Increment incorrect answers
                    reset_word()  # Generate a new word
                else:
                    typed_word += event.unicode  # Add the typed character to the word

    # Handle pause state
    if paused:
        continue  # Skip the rest of the loop while paused

    # Update the timer for running out of time
    current_time = pygame.time.get_ticks()
    time_elapsed = (current_time - last_time) / 1000  # Time elapsed in seconds
    time_remaining = max(0, time_limit - time_elapsed)

    # Check if time runs out
    if time_remaining <= 0:
        player_health -= 5  # Penalize player for running out of time
        reset_word()  # Generate a new word

    # End game conditions
    if player_health <= 0:
        show_progress_tracker("Game Over! You Lose!")  # Show progress tracker
        running = False  # Exit the game loop

    # Draw correct and incorrect records on the left
    draw_text(f"Correct: {correct_answers}", 50, 20, GREEN, INFO_FONT)  # Correct answers
    draw_text(f"Incorrect: {incorrect_answers}", 50, 50, RED, INFO_FONT)  # Incorrect answers

    # Draw the timer on the right side
    draw_text(f"Time: {time_remaining:.1f}s", WIDTH - 200, 20, BLACK, INFO_FONT)  # Timer on the right

    # Display the opponent's prompt in a bubble under the health bar
    bubble_x = 500  # X-coordinate for the bubble
    bubble_y = 330  # Y-coordinate for the bubble (under the health bar)
    draw_bubble_text(current_word, bubble_x, bubble_y, INFO_FONT, BLACK, WHITE, padding=5)

    # Display the syntax (current_word) like a dialogue under the opponent's health bar
    bubble_x = 500  # X-coordinate for the bubble
    bubble_y = 330  # Y-coordinate for the bubble (adjusted to be under the health bar)
    draw_bubble_text(
        current_word, bubble_x, bubble_y, INFO_FONT, BLACK, WHITE, padding=10, max_width=300
    )

    # Display the typed word above the player's health bar
    draw_text(typed_word, 50, 350, BLACK, INFO_FONT)

    # Draw health bars below the game information
    draw_health_bars()

    # Draw images under the health bars
    screen.blit(man_image, (50, 400))  # Display the man image on the left
    screen.blit(frog_image, (500, 400))  # Display the frog image on the right

    # Update the display
    pygame.display.flip()

    # Cap the frame rate
    clock.tick(30)

# Quit Pygame
pygame.quit()
sys.exit()