import pygame, sys
from button import Button
from os.path import join
import subprocess  # For launching subprocesses
import random  # For typing battle game
import os  # Add this import at the top of the file
import time  # Add this import for delays
import json  # Import JSON for saving and loading data

# Initialize pygame mixer and load background music
pygame.mixer.init()
pygame.mixer.music.load(join('images', '8bit_test.mp3'))
pygame.mixer.music.set_volume(0.5)  # Set default volume to 50%
pygame.mixer.music.play(-1)  # Loop the music indefinitely

# Global volume variable
volume = 0.5

# Define assets
assets = [
    join('images', 'rocket1.png'),
    join('images', 'rocket2.png'),
    join('images', 'rocket3.png')
]
selected_asset = None  # Initialize selected asset

# Add new assets for "Coding" and "Binary"
binary_assets = [
    join('images', 'rocket1.png'),
    join('images', 'rocket2.png'),
    join('images', 'rocket3.png'),
    join('images', 'rocket4bgcleared.png')  # New rocket added
]
coding_assets = [
    join('images', 'man1cleared.png'),
    join('images', 'man2.png'),
    join('images', 'man3cleared.png'),
    join('images', 'man4cleared.png'),
    join('images', 'man5cleared.png')  # Added new assets
]

# Add assets for "Fill in the Blanks"
fill_in_the_blanks_assets = [
    'images/customcharacleared.png',
    'images/customchara2cleared.png',
    'images/customchara3.png'
]

# Background options for Fill in the Blanks
fill_in_the_blanks_backgrounds = [
    "greenfieldbg.png",
    "stonefieldbg.png",
    "snowfieldbg.png"
]
selected_background = None  # Track the selected background

# Track the current category
current_category = "Binary"

# Global variables for stage tracking
language_stages = {
    "Java": [
        {"name": "Stage 1", "background": "autumnbg.png", "unlocked": True},
        {"name": "Stage 2", "background": "desertbg.png", "unlocked": False},
        {"name": "Stage 3", "background": "springbg.jpg", "unlocked": False},
        {"name": "Stage 4", "background": "winterbg.png", "unlocked": False},
    ],
    "Python": [
        {"name": "Stage 1", "background": "autumnbg.png", "unlocked": True},
        {"name": "Stage 2", "background": "desertbg.png", "unlocked": False},
        {"name": "Stage 3", "background": "springbg.jpg", "unlocked": False},
        {"name": "Stage 4", "background": "winterbg.png", "unlocked": False},
    ],
    "JavaScript": [
        {"name": "Stage 1", "background": "autumnbg.png", "unlocked": True},
        {"name": "Stage 2", "background": "desertbg.png", "unlocked": False},
        {"name": "Stage 3", "background": "springbg.jpg", "unlocked": False},
        {"name": "Stage 4", "background": "winterbg.png", "unlocked": False},
    ],
}

# Global variables for Fill in the Blanks stages
fill_in_the_blanks_stages = [
    {"name": "Stage 1", "background": "grassfieldbg.png", "unlocked": True},
    {"name": "Stage 2", "background": "stoneyardbg.png", "unlocked": True},
    {"name": "Stage 3", "background": "snowfieldbg.png", "unlocked": True},
]
selected_fill_stage = None  # Track the selected stage for Fill in the Blanks

# Initialize the stages for the selected language
stages = language_stages["Java"]  # Default to Java
selected_stage = None  # Track the selected stage

# Initialize screen
window_width, window_height = 980, 520
SCREEN = pygame.display.set_mode((window_width, window_height))
pygame.display.set_caption("BITCRUSH")  # Updated window name

# Load font
pygame.font.init()
FONT = pygame.font.Font(join('images', 'Minecraft.ttf'), 50)
FONT_SMALL = pygame.font.Font(join('images', 'Minecraft.ttf'), 30)  # Smaller font for buttons

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Add buttons for toggling categories (move this after FONT is defined)
binary_button = Button("Binary", FONT_SMALL, BLACK, WHITE, 150, 100, 150, 40)
coding_button = Button("Coding", FONT_SMALL, BLACK, WHITE, 350, 100, 150, 40)

# Load the background image from the 'images' folder
background_image = pygame.image.load(join('images', 'bitcrushuibghd.png'))
background_image = pygame.transform.scale(background_image, (window_width, window_height))

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

# Buttons with consistent 10px gaps
play_button = Button("PLAY", FONT_SMALL, WHITE, WHITE, 200, 150, 150, 50)
options_button = Button("OPTIONS", FONT_SMALL, WHITE, WHITE, 200, 210, 150, 50)
customize_button = Button("CUSTOMIZE", FONT_SMALL, WHITE, WHITE, 200, 270, 180, 50)
help_button = Button("HELP", FONT_SMALL, WHITE, WHITE, 200, 330, 150, 50)
learning_button = Button("LEARNING", FONT_SMALL, WHITE, WHITE, 200, 390, 180, 50)  # Positioned below Help
leaderboard_button = Button("LEADERBOARD", FONT_SMALL, WHITE, WHITE, 200, 450, 200, 50)  # Adjusted below Learning
exit_button = Button("EXIT", FONT_SMALL, WHITE, WHITE, 200, 510, 150, 50)
back_button = Button("<", FONT_SMALL, WHITE, WHITE, 50, 50, 100, 40)

# Game mode buttons
typing_button = Button("BINARY", FONT_SMALL, WHITE, WHITE, 200, 200, 180, 50)
coding_button = Button("DEBUG", FONT_SMALL, WHITE, WHITE, 200, 260, 180, 50)  # Adjusted position
fill_in_the_blanks_button = Button("FILL IN THE BLANKS", FONT_SMALL, WHITE, WHITE, 200, 320, 250, 50)  # Adjusted positions

# Difficulty buttons
easy_button = Button("EASY", FONT_SMALL, WHITE, WHITE, 200, 200, 150, 50)
normal_button = Button("NORMAL", FONT_SMALL, WHITE, WHITE, 200, 260, 150, 50)  # 10px gap
hard_button = Button("HARD", FONT_SMALL, WHITE, WHITE, 200, 320, 150, 50)  # 10px gap

# Language selection buttons
java_button = Button("JAVA", FONT_SMALL, WHITE, WHITE, 200, 200, 150, 50)
python_button = Button("PYTHON", FONT_SMALL, WHITE, WHITE, 200, 260, 180, 50)  # 10px gap
javascript_button = Button("JAVASCRIPT", FONT_SMALL, WHITE, WHITE, 200, 320, 200, 50)  # 10px gap

# Learning buttons
java_learn_button = Button("JAVA", FONT_SMALL, WHITE, WHITE, 200, 200, 150, 50)
javascript_learn_button = Button("JAVASCRIPT", FONT_SMALL, WHITE, WHITE, 200, 260, 200, 50)
python_learn_button = Button("PYTHON", FONT_SMALL, WHITE, WHITE, 200, 320, 180, 50)

# Sub-tab buttons for the leaderboard
binary_tab_button = Button("Binary", FONT_SMALL, WHITE, WHITE, 150, 100, 150, 40)
debug_tab_button = Button("Debug", FONT_SMALL, WHITE, WHITE, 350, 100, 150, 40)
fill_tab_button = Button("Fill in the Blanks", FONT_SMALL, WHITE, WHITE, 550, 100, 200, 40)

# Track the current leaderboard sub-tab
current_leaderboard_tab = "Binary"  # Default to Binary tab

# Global variables
current_tab = "title"
subprocess_instance = None  # To track the subprocess instance
selected_language = None  # To track the selected language
current_help_mode = None  # Track the current help mode
current_help_mode = None  # None means the main help menu is displayed

# Scroll offset for the Debug tab
debug_scroll_offset = 0  # Initial scroll position
debug_scroll_speed = 20  # Speed of scrolling

LEADERBOARD_FILE = "leaderboard_data.json"  # File to store leaderboard data

def save_leaderboard():
    """Save the leaderboard data to a JSON file."""
    try:
        print("Saving leaderboard to:", "leaderboard_data.json")  # Debugging output
        with open("leaderboard_data.json", "w") as file:
            json.dump(leaderboard_data, file, indent=4)
        print("Leaderboard data saved successfully.")
    except Exception as e:
        print(f"Error saving leaderboard data: {e}")

def load_leaderboard():
    """Load the leaderboard data from a JSON file."""
    global leaderboard_data
    try:
        print("Loading leaderboard from:", "leaderboard_data.json")  # Debugging output
        with open("leaderboard_data.json", "r") as file:
            leaderboard_data = json.load(file)
        print("Leaderboard data loaded successfully.")
    except FileNotFoundError:
        print("Leaderboard file not found. Initializing with default values.")
        leaderboard_data = {
            "Binary": {"meteors_shot": 0, "wave_count": 0, "high_score": 0},
            "Debug": {
                "Java": {"Easy": {"high_score": 0, "correct": 0, "wrong": 0},
                         "Intermediate": {"high_score": 0, "correct": 0, "wrong": 0},
                         "Hard": {"high_score": 0, "correct": 0, "wrong": 0}},
                "Python": {"Easy": {"high_score": 0, "correct": 0, "wrong": 0},
                           "Intermediate": {"high_score": 0, "correct": 0, "wrong": 0},
                           "Hard": {"high_score": 0, "correct": 0, "wrong": 0}},
                "JavaScript": {"Easy": {"high_score": 0, "correct": 0, "wrong": 0},
                               "Intermediate": {"high_score": 0, "correct": 0, "wrong": 0},
                               "Hard": {"high_score": 0, "correct": 0, "wrong": 0}}
            },
            "Fill in the Blanks": {
                "normal_mobs_shot": 0,
                "bosses_shot": 0,
                "wave_count": 0,
                "correct_prompts": 0,
                "wrong_prompts": 0,
                "time_record": 0
            }
        }
    except Exception as e:
        print(f"Error loading leaderboard data: {e}")

def draw_text(text, x, y, color=BLACK):
    """Draw text on the screen."""
    rendered_text = FONT.render(text, True, color)
    SCREEN.blit(rendered_text, (x, y))


def draw_bootup_screen():
    """Display the bootup screen with text appearing letter by letter."""
    text = "Booting Up..."
    x, y = window_width // 2, window_height // 2
    rendered_text = ""

    for char in text:
        rendered_text += char
        SCREEN.blit(background_image, (0, 0))  # Use the main menu wallpaper
        bootup_text = FONT.render(rendered_text, True, WHITE)  # Use white text for visibility
        bootup_rect = bootup_text.get_rect(center=(x, y))
        SCREEN.blit(bootup_text, bootup_rect)
        pygame.display.flip()
        pygame.time.wait(100)  # Wait 100ms for each letter


def draw_title_screen():
    """Display the title screen with BIT in white and CRUSH in light blue."""
    SCREEN.blit(background_image, (0, 0))  # Use the background image

    # Render BIT in white
    bit_text = FONT.render("BIT", True, WHITE)
    bit_x = 150  # Move BIT to the left to align with the buttons
    bit_y = 100
    SCREEN.blit(bit_text, (bit_x, bit_y))

    # Render CRUSH in light blue
    light_blue = (173, 216, 230)  # Light blue color
    crush_text = FONT.render("CRUSH", True, light_blue)
    crush_x = bit_x + bit_text.get_width() - 3  # Position CRUSH with a gap of -3
    crush_y = 100
    SCREEN.blit(crush_text, (crush_x, crush_y))

    # Draw the buttons
    play_button.draw(SCREEN)
    options_button.draw(SCREEN)
    customize_button.draw(SCREEN)
    help_button.draw(SCREEN)
    learning_button.draw(SCREEN)  # Draw the Learning button
    leaderboard_button.draw(SCREEN)  # Draw the Leaderboard button
    exit_button.draw(SCREEN)


def draw_play_tab():
    """Display the game mode selection screen."""

    # Lower the title text
    play_text = FONT.render("Game Mode", True, WHITE)
    SCREEN.blit(play_text, (window_width // 2 - play_text.get_width() // 2, 100))  # Lowered to match BITCRUSH height

    # Lower the buttons slightly
    typing_button.rect.x = window_width // 2 - 100
    typing_button.rect.y = window_height // 2 - 80  # Adjusted to center
    typing_button.draw(SCREEN)

    coding_button.rect.x = window_width // 2 - 100
    coding_button.rect.y = window_height // 2 - 10  # Adjusted to center
    coding_button.draw(SCREEN)

    fill_in_the_blanks_button.rect.x = window_width // 2 - 125
    fill_in_the_blanks_button.rect.y = window_height // 2 + 60  # Adjusted to center
    fill_in_the_blanks_button.draw(SCREEN)

    # Draw the back button
    back_button.rect.x = 20  # Position back button on the top-left
    back_button.rect.y = 20
    back_button.draw(SCREEN)


def draw_options_tab():
    """Display the options tab with a volume adjuster and toggle."""
    global volume

    SCREEN.blit(background_image, (0, 0))  # Use the background image
    options_text = FONT.render("Options Tab", True, WHITE)  # Already WHITE
    SCREEN.blit(options_text, (300, 100))

    # Draw the volume slider
    volume_text = FONT.render(f"Volume: {int(volume * 100)}%", True, WHITE)  # Already WHITE
    SCREEN.blit(volume_text, (300, 200))

    # Slider bar
    slider_x = 300
    slider_y = 250
    slider_width = 300
    slider_height = 10
    pygame.draw.rect(SCREEN, GRAY, (slider_x, slider_y, slider_width, slider_height))

    # Slider handle
    handle_x = slider_x + int(volume * slider_width) - 5
    handle_y = slider_y - 5
    handle_width = 10
    handle_height = 20
    pygame.draw.rect(SCREEN, WHITE, (handle_x, handle_y, handle_width, handle_height))

    # Draw the Volume On/Off toggle button
    toggle_text = "Mute" if volume > 0 else "Unmute"
    toggle_button = Button(toggle_text, FONT, WHITE, WHITE, 300, 300, 150, 40)
    toggle_button.draw(SCREEN)

    back_button.draw(SCREEN)

    return toggle_button  # Return the toggle button for click handling


def handle_options_tab_click(mouse_pos, toggle_button):
    """Handle clicks in the options tab."""
    global volume

    slider_x = 300
    slider_y = 250
    slider_width = 300
    slider_height = 10

    # Check if the click is on the slider
    if slider_x <= mouse_pos[0] <= slider_x + slider_width and slider_y <= mouse_pos[1] <= slider_y + slider_height:
        # Update the volume based on the click position
        volume = (mouse_pos[0] - slider_x) / slider_width
        pygame.mixer.music.set_volume(volume)
        print(f"Volume set to: {int(volume * 100)}%")

    # Check if the click is on the toggle button
    if toggle_button.is_clicked(mouse_pos):
        if volume > 0:
            volume = 0  # Mute
        else:
            volume = 0.5  # Restore to default volume (50%)
        pygame.mixer.music.set_volume(volume)
        print("Volume toggled:", "Muted" if volume == 0 else "Unmuted")


def draw_customize_tab():
    """Display the customize tab with category buttons and assets."""
    global selected_asset, current_category

    # Clear the screen and set the background
    SCREEN.blit(background_image, (0, 0))  # Use the background image

    # Draw the title text
    customize_text = FONT.render("Customize Your Player", True, WHITE)
    SCREEN.blit(customize_text, (window_width // 2 - customize_text.get_width() // 2, 50))

    # Draw the larger back button on the top-left corner
    back_button.rect.x = 20  # Position back button on the top-left
    back_button.rect.y = 20
    back_button.rect.width = 80  # Make the button larger
    back_button.rect.height = 50
    back_button.text = "<"  # Ensure the text is "<"
    back_button.draw(SCREEN)

    # Ensure consistent placement of category buttons
    binary_button.text = "BINARY"  # Make Binary button text all caps
    binary_button.text_color = WHITE  # Change Binary button text color to white
    binary_button.rect.x = 120  # Align Binary button slightly to the left
    binary_button.rect.y = 150
    binary_button.draw(SCREEN)

    coding_button.rect.x = 120  # Align Coding button slightly to the left
    coding_button.rect.y = 220
    coding_button.draw(SCREEN)

    fill_in_the_blanks_button.rect.x = 120  # Align Fill in the Blanks button slightly to the left
    fill_in_the_blanks_button.rect.y = 290
    fill_in_the_blanks_button.draw(SCREEN)

    # Display assets on the right side if a category is selected
    if current_category:
        if current_category == "Binary":
            assets_to_display = binary_assets
        elif current_category == "Coding":
            assets_to_display = coding_assets
        elif current_category == "Fill in the Blanks":
            assets_to_display = fill_in_the_blanks_assets

        # Draw asset selection grid on the right side
        x_start, y_start = 400, 150  # Starting position for the grid on the right
        asset_size = 100  # Size of each asset box
        padding = 20  # Padding between asset boxes

        for i, asset_path in enumerate(assets_to_display):
            x = x_start + (i % 3) * (asset_size + padding)  # 3 assets per row
            y = y_start + (i // 3) * (asset_size + padding)

            # Check if the file exists
            if not os.path.exists(asset_path):
                print(f"Warning: File not found - {asset_path}")
                continue  # Skip this asset if the file is missing

            # Load and draw the asset image
            asset_image = pygame.image.load(asset_path)
            asset_image = pygame.transform.scale(asset_image, (asset_size, asset_size))
            SCREEN.blit(asset_image, (x, y))

            # Highlight the selected asset
            if selected_asset == asset_path:
                pygame.draw.rect(SCREEN, WHITE, (x - 5, y - 5, asset_size + 10, asset_size + 10), 3)

            # Draw a border around each asset
            pygame.draw.rect(SCREEN, GRAY, (x, y, asset_size, asset_size), 2)


def handle_customize_tab_click(mouse_pos):
    """Handle clicks in the customize tab."""
    global selected_asset, current_category, current_tab

    # Check if the back button is clicked
    if back_button.is_clicked(mouse_pos):
        current_category = None  # Reset to category selection
        print("Returning to the main menu.")
        current_tab = "title"  # Go back to the main menu
        return

    # Check if the category buttons are clicked
    if binary_button.is_clicked(mouse_pos):
        current_category = "Binary"
        print("Switched to Binary category.")
        return
    elif coding_button.is_clicked(mouse_pos):
        current_category = "Coding"
        print("Switched to Coding category.")
        return
    elif fill_in_the_blanks_button.is_clicked(mouse_pos):
        current_category = "Fill in the Blanks"
        print("Switched to Fill in the Blanks category.")
        return

    # Display assets only if a category is selected
    if current_category:
        if current_category == "Binary":
            assets_to_check = binary_assets
        elif current_category == "Coding":
            assets_to_check = coding_assets
        elif current_category == "Fill in the Blanks":
            assets_to_check = fill_in_the_blanks_assets

        x_start, y_start = 400, 150  # Starting position for the grid on the right
        asset_size = 100  # Size of each asset box
        padding = 20  # Padding between asset boxes

        for i, asset_path in enumerate(assets_to_check):
            x = x_start + (i % 3) * (asset_size + padding)
            y = y_start + (i // 3) * (asset_size + padding)

            # Check if the click is within the asset box
            if x <= mouse_pos[0] <= x + asset_size and y <= mouse_pos[1] <= y + asset_size:
                selected_asset = asset_path  # Set the selected asset
                print(f"Selected asset: {selected_asset}")
                return


def draw_help_tab():
    """Display the help screen with game mechanics for each mode."""
    global current_help_mode

    SCREEN.blit(background_image, (0, 0))  # Use the background image

    # Draw the back button
    back_button.rect.x = 20  # Position the back button on the top-left
    back_button.rect.y = 20
    back_button.rect.width = 80  # Make the button larger
    back_button.rect.height = 50
    back_button.text = "<"  # Ensure the text is "<"
    back_button.draw(SCREEN)

    if current_help_mode is None:
        # Draw the title
        help_title = FONT.render("Help Menu", True, WHITE)
        SCREEN.blit(help_title, (window_width // 2 - help_title.get_width() // 2, 150))  # Lowered title

        # Adjust the y-positions of the buttons to center them vertically
        typing_button.rect.x = window_width // 2 - 100
        typing_button.rect.y = window_height // 2 - 50  # Adjusted to center
        typing_button.draw(SCREEN)

        coding_button.rect.x = window_width // 2 - 100
        coding_button.rect.y = window_height // 2 + 20  # Adjusted to center
        coding_button.draw(SCREEN)

        fill_in_the_blanks_button.rect.x = window_width // 2 - 125
        fill_in_the_blanks_button.rect.y = window_height // 2 + 90  # Adjusted to center
        fill_in_the_blanks_button.draw(SCREEN)
    else:
        # Display the title for the selected mode
        mode_title = FONT.render(current_help_mode, True, WHITE)
        SCREEN.blit(mode_title, (window_width // 2 - mode_title.get_width() // 2, 100))  # Title above instructions

        # Display instructions for the selected mode
        instructions = {
            "Binary": "Type the prompt and it'll automatically write.",
            "Debug": "Type the output and defeat the mobs to proceed.",
            "Fill in the Blanks": [
                "Click on the correct answer, SPACE to shoot,",
                "and W/A/S/D to move."
            ]
        }

        # Draw the instructions
        if isinstance(instructions[current_help_mode], list):
            # Render each line separately
            for i, line in enumerate(instructions[current_help_mode]):
                instruction_text = FONT_SMALL.render(line, True, WHITE)
                SCREEN.blit(instruction_text, (window_width // 2 - instruction_text.get_width() // 2, 200 + i * 40))
        else:
            # Render single-line instructions
            instruction_text = FONT_SMALL.render(instructions[current_help_mode], True, WHITE)
            SCREEN.blit(instruction_text, (window_width // 2 - instruction_text.get_width() // 2, 200))


def handle_help_tab_click(mouse_pos):
    """Handle clicks in the help tab."""
    global current_help_mode, current_tab

    if current_help_mode is None:
        # Check if a game mode button is clicked
        if typing_button.is_clicked(mouse_pos):
            current_help_mode = "Binary"
        elif coding_button.is_clicked(mouse_pos):
            current_help_mode = "Debug"
        elif fill_in_the_blanks_button.is_clicked(mouse_pos):
            current_help_mode = "Fill in the Blanks"
    else:
        # Check if the back button is clicked
        if back_button.is_clicked(mouse_pos):
            current_help_mode = None  # Reset to the main help menu
            print("Returning to the main help menu.")


def draw_exit_tab():
    """Display the exit screen with text appearing letter by letter."""
    text = "Exiting..."
    x, y = window_width // 2, window_height // 2
    rendered_text = ""

    for char in text:
        rendered_text += char
        SCREEN.blit(background_image, (0, 0))  # Use the main menu wallpaper
        exit_text = FONT.render(rendered_text, True, WHITE)  # Use white text for visibility
        exit_rect = exit_text.get_rect(center=(x, y))
        SCREEN.blit(exit_text, exit_rect)
        pygame.display.flip()
        pygame.time.wait(100)  # Wait 100ms for each letter


def draw_difficulty_tab():
    """Display the difficulty selection screen."""
    SCREEN.blit(background_image, (0, 0))  # Use the background image
    difficulty_text = FONT.render("Difficulty", True, WHITE)
    difficulty_rect = difficulty_text.get_rect(center=(window_width // 2, 100))
    SCREEN.blit(difficulty_text, difficulty_rect)

    # Draw difficulty buttons
    easy_button.draw(SCREEN)
    normal_button.draw(SCREEN)
    hard_button.draw(SCREEN)

    # Draw the back button
    back_button.draw(SCREEN)


def draw_language_select_tab():
    """Display the language selection screen."""
    SCREEN.blit(background_image, (0, 0))  # Use the background image
    language_text = FONT.render("Select Language", True, WHITE)
    language_rect = language_text.get_rect(center=(window_width // 2, 100))
    SCREEN.blit(language_text, language_rect)

    # Draw language buttons
    java_button.draw(SCREEN)
    python_button.draw(SCREEN)
    javascript_button.draw(SCREEN)

    # Draw the back button
    back_button.draw(SCREEN)


def handle_language_select_click(mouse_pos):
    """Handle clicks in the language selection screen."""
    global selected_language, current_tab, stages

    if java_button.is_clicked(mouse_pos):
        selected_language = "Java"
        stages = language_stages["Java"]  # Switch to Java stages
        print("Java selected. Moving to stage selection.")
        current_tab = "stage_select"  # Go to the stage selection menu
    elif python_button.is_clicked(mouse_pos):
        selected_language = "Python"
        stages = language_stages["Python"]  # Switch to Python stages
        print("Python selected. Moving to stage selection.")
        current_tab = "stage_select"  # Go to the stage selection menu
    elif javascript_button.is_clicked(mouse_pos):
        selected_language = "JavaScript"
        stages = language_stages["JavaScript"]  # Switch to JavaScript stages
        print("JavaScript selected. Moving to stage selection.")
        current_tab = "stage_select"  # Go to the stage selection menu
    elif back_button.is_clicked(mouse_pos):
        current_tab = "play"  # Go back to the play tab


def draw_stage_select_tab():
    """Display the stage selection screen."""
    SCREEN.blit(background_image, (0, 0))  # Use the background image
    stage_text = FONT.render(f"Select Stage ({selected_language})", True, WHITE)
    stage_rect = stage_text.get_rect(center=(window_width // 2, 50))
    SCREEN.blit(stage_text, stage_rect)

    # Draw stage boxes
    x_start, y_start = 150, 150  # Starting position for the grid
    box_size = 150  # Size of each stage box
    padding = 20  # Padding between boxes

    for i, stage in enumerate(stages):
        x = x_start + (i % 3) * (box_size + padding)  # 3 stages per row
        y = y_start + (i // 3) * (box_size + padding)

        print(f"Drawing stage {stage['name']} at ({x}, {y})")  # Debugging

        # Load and draw the background image for the stage
        stage_background = pygame.image.load(join("images", stage["background"]))
        stage_background = pygame.transform.scale(stage_background, (box_size, box_size))
        SCREEN.blit(stage_background, (x, y))

        # If the stage is locked, overlay the lock image
        if not stage["unlocked"]:
            lock_image = pygame.image.load(join("images", "lock.png"))
            lock_image = pygame.transform.scale(lock_image, (50, 50))  # Scale the lock image
            lock_rect = lock_image.get_rect(center=(x + box_size // 2, y + box_size // 2))
            SCREEN.blit(lock_image, lock_rect)

    # Draw the back button
    back_button.draw(SCREEN)


def handle_stage_select_click(mouse_pos):
    """Handle clicks in the stage selection screen."""
    global selected_stage, subprocess_instance, current_tab

    x_start, y_start = 150, 150  # Starting position for the grid
    box_size = 150  # Size of each stage box
    padding = 20  # Padding between boxes

    print(f"Mouse clicked at: {mouse_pos}")  # Debugging

    # Map the script to the selected language
    script_map = {
        "Java": "thirmain_java.py",
        "Python": "thirmain_python.py",
        "JavaScript": "thirmain_js.py"
    }
    script_to_launch = script_map.get(selected_language)
    print(f"Selected language: {selected_language}, Script to launch: {script_to_launch}")  # Debugging

    for i, stage in enumerate(stages):
        x = x_start + (i % 3) * (box_size + padding)
        y = y_start + (i // 3) * (box_size + padding)

        print(f"Checking stage {stage['name']} at box ({x}, {y}, {x + box_size}, {y + box_size})")  # Debugging

        # Check if the mouse click is within the stage box
        if x <= mouse_pos[0] <= x + box_size and y <= mouse_pos[1] <= y + box_size:
            if stage["unlocked"]:
                selected_stage = stage
                print(f"Selected stage: {stage['name']} with background {stage['background']}")

                # Ensure only Coding assets are used for Coding Mode
                if current_category != "Coding" or selected_asset not in coding_assets:
                    selected_asset_to_use = "images/man1cleared.png"  # Default man asset for Coding Mode
                    print(f"No valid Coding asset selected! Using default asset: {selected_asset_to_use}")
                else:
                    selected_asset_to_use = selected_asset

                # Launch the corresponding thirmain file
                try:
                    subprocess_instance = subprocess.Popen(
                        ["python", script_to_launch, stage["background"], selected_asset_to_use],
                        stdout=subprocess.PIPE,
                        stderr=subprocess.PIPE
                    )
                    print(f"Launching {script_to_launch} with background {stage['background']} and asset {selected_asset_to_use}")
                except FileNotFoundError as e:
                    print(f"Error: Script not found - {e}")
                except Exception as e:
                    print(f"Error launching subprocess: {e}")
                return
            else:
                print(f"{stage['name']} is locked!")

    # Check if the back button is clicked
    if back_button.is_clicked(mouse_pos):
        current_tab = "language_select"
        print("Returning to language selection menu.")


def unlock_next_stage():
    """Unlock the next stage after completing the current one."""
    global selected_stage

    for i, stage in enumerate(stages):
        if stage["unlocked"] and i + 1 < len(stages):  # Find the first unlocked stage
            if selected_stage == stage:  # Ensure the current stage was played
                stages[i + 1]["unlocked"] = True  # Unlock the next stage
                print(f"{stages[i + 1]['name']} is now unlocked for {selected_language}!")
                selected_stage = None  # Reset the selected stage
                break


def launch_first_unlocked_stage():
    """Automatically launch the first unlocked stage."""
    global selected_stage, subprocess_instance

    for stage in stages:
        if stage["unlocked"]:
            selected_stage = stage
            print(f"Automatically launching {stage['name']} with background {stage['background']}")
            subprocess_instance = subprocess.Popen(["python", "thirmain_java.py", stage["background"]])  # Pass the background as an argument
            return


def draw_learn_tab():
    """Display the learn tab with language learning options."""
    SCREEN.blit(background_image, (0, 0))  # Use the background image

    # Draw the title
    learn_title = FONT.render("Learn Programming", True, WHITE)
    SCREEN.blit(learn_title, (window_width // 2 - learn_title.get_width() // 2, 50))

    # Draw the language learning buttons
    java_learn_button.draw(SCREEN)
    javascript_learn_button.draw(SCREEN)
    python_learn_button.draw(SCREEN)

    # Draw the back button
    back_button.rect.x = 20  # Position the back button on the top-left
    back_button.rect.y = 20
    back_button.rect.width = 80  # Make the button larger
    back_button.rect.height = 50
    back_button.text = "<"  # Ensure the text is "<"
    back_button.draw(SCREEN)


def handle_learn_tab_click(mouse_pos):
    """Handle clicks in the learn tab."""
    global current_tab

    try:
        if java_learn_button.is_clicked(mouse_pos):
            script_path = join(os.getcwd(), "javalearning.py")
            print(f"Launching: {script_path}")
            subprocess.Popen(["python", script_path])  # Launch Java learning script
        elif javascript_learn_button.is_clicked(mouse_pos):
            script_path = join(os.getcwd(), "jslearning.py")
            print(f"Launching: {script_path}")
            subprocess.Popen(["python", script_path])  # Launch JavaScript learning script
        elif python_learn_button.is_clicked(mouse_pos):
            script_path = join(os.getcwd(), "pylearning.py")
            print(f"Launching: {script_path}")
            subprocess.Popen(["python", script_path])  # Launch Python learning script
        elif back_button.is_clicked(mouse_pos):
            current_tab = "title"  # Return to the main menu
    except FileNotFoundError as e:
        print(f"File not found: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")


def draw_fill_in_the_blanks_stage_select_tab():
    """Display the stage selection screen for Fill in the Blanks."""
    SCREEN.blit(background_image, (0, 0))  # Use the background image
    stage_text = FONT.render("Select Stage (Fill in the Blanks)", True, WHITE)
    stage_rect = stage_text.get_rect(center=(window_width // 2, 50))
    SCREEN.blit(stage_text, stage_rect)

    # Draw stage boxes
    x_start, y_start = 150, 150  # Starting position for the grid
    box_size = 150  # Size of each stage box
    padding = 20  # Padding between boxes

    for i, stage in enumerate(fill_in_the_blanks_stages):
        x = x_start + (i % 3) * (box_size + padding)  # 3 stages per row
        y = y_start + (i // 3) * (box_size + padding)

        # Load and draw the background image for the stage
        stage_background = pygame.image.load(join("images", stage["background"]))
        stage_background = pygame.transform.scale(stage_background, (box_size, box_size))
        SCREEN.blit(stage_background, (x, y))

        # If the stage is locked, overlay the lock image
        if not stage["unlocked"]:
            lock_image = pygame.image.load(join("images", "lock.png"))
            lock_image = pygame.transform.scale(lock_image, (50, 50))  # Scale the lock image
            lock_rect = lock_image.get_rect(center=(x + box_size // 2, y + box_size // 2))
            SCREEN.blit(lock_image, lock_rect)

    # Draw the back button
    back_button.draw(SCREEN)


def handle_fill_in_the_blanks_stage_select_click(mouse_pos):
    """Handle clicks in the Fill in the Blanks stage selection screen."""
    global selected_fill_stage, current_tab

    x_start, y_start = 150, 150  # Starting position for the grid
    box_size = 150  # Size of each stage box
    padding = 20  # Padding between boxes

    for i, stage in enumerate(fill_in_the_blanks_stages):
        x = x_start + (i % 3) * (box_size + padding)
        y = y_start + (i // 3) * (box_size + padding)

        # Check if the mouse click is within the stage box
        if x <= mouse_pos[0] <= x + box_size and y <= mouse_pos[1] <= y + box_size:
            if stage["unlocked"]:
                selected_fill_stage = stage
                print(f"Selected stage: {stage['name']} with background {stage['background']}")

                # Ensure a valid player asset is selected
                if selected_asset not in fill_in_the_blanks_assets:
                    selected_asset_to_use = "images/customchara.png"  # Default player asset
                    print(f"No valid asset selected! Using default asset: {selected_asset_to_use}")
                else:
                    selected_asset_to_use = selected_asset

                # Launch maintry.py with the selected stage background and player asset
                try:
                    script_path = os.path.join(os.getcwd(), "maintry.py")
                    print(f"Launching script: {script_path} with background: {stage['background']} and asset: {selected_asset_to_use}")
                    process = subprocess.Popen(
                        ["python", script_path, stage["background"], selected_asset_to_use],
                        stdout=subprocess.PIPE,
                        stderr=subprocess.PIPE
                    )
                    stdout, stderr = process.communicate()
                    print(f"Subprocess output: {stdout.decode()}")
                    print(f"Subprocess error: {stderr.decode()}")
                except FileNotFoundError as e:
                    print(f"Error: Script not found - {e}")
                except Exception as e:
                    print(f"Error launching subprocess: {e}")
                return
            else:
                print(f"{stage['name']} is locked!")

    # Check if the back button is clicked
    if back_button.is_clicked(mouse_pos):
        current_tab = "play"  # Return to the play tab
        print("Returning to the play tab.")


def draw_leaderboard_tab():
    """Display the leaderboard tab with sub-tabs for each game mode."""
    global current_leaderboard_tab

    SCREEN.blit(background_image, (0, 0))  # Use the background image

    # Title
    leaderboard_title = FONT.render("Leaderboard", True, WHITE)
    SCREEN.blit(leaderboard_title, (window_width // 2 - leaderboard_title.get_width() // 2, 50))

    # Draw sub-tab buttons
    binary_tab_button.draw(SCREEN)
    debug_tab_button.draw(SCREEN)
    fill_tab_button.draw(SCREEN)

    # Display data for the active sub-tab
    if current_leaderboard_tab == "Binary":
        draw_binary_leaderboard()
    elif current_leaderboard_tab == "Debug":
        draw_debug_leaderboard()
    elif current_leaderboard_tab == "Fill in the Blanks":
        draw_fill_leaderboard()

    # Draw the back button
    back_button.draw(SCREEN)


def handle_leaderboard_tab_click(mouse_pos):
    """Handle clicks in the leaderboard tab."""
    global current_tab, current_leaderboard_tab

    # Check if the back button is clicked
    if back_button.is_clicked(mouse_pos):
        current_tab = "title"  # Return to the main menu

    # Check if a sub-tab button is clicked
    elif binary_tab_button.is_clicked(mouse_pos):
        current_leaderboard_tab = "Binary"
    elif debug_tab_button.is_clicked(mouse_pos):
        current_leaderboard_tab = "Debug"
    elif fill_tab_button.is_clicked(mouse_pos):
        current_leaderboard_tab = "Fill in the Blanks"


def update_leaderboard(game_mode, stats):
    """Update the leaderboard with the latest stats."""
    global leaderboard_data

    if game_mode == "Binary":
        print("Updating Binary leaderboard with stats:", stats)  # Debugging output
        leaderboard_data["Binary"]["meteors_shot"] += stats.get("meteors_shot", 0)
        leaderboard_data["Binary"]["wave_count"] = max(
            leaderboard_data["Binary"]["wave_count"], stats.get("wave_count", 0)
        )
        leaderboard_data["Binary"]["high_score"] = max(
            leaderboard_data["Binary"].get("high_score", 0), stats.get("high_score", 0)
        )

    # Save the updated leaderboard data
    save_leaderboard()
    print("Leaderboard updated:", leaderboard_data)  # Debugging output


def draw_binary_leaderboard():
    """Display the Binary leaderboard."""
    binary_stats = leaderboard_data["Binary"]
    print("Rendering Binary leaderboard with stats:", binary_stats)  # Debugging output

    binary_text = [
        f"Meteors Shot: {binary_stats['meteors_shot']}",
        f"Wave Count: {binary_stats['wave_count']}",
    ]
    for i, line in enumerate(binary_text):
        stat_text = FONT_SMALL.render(line, True, WHITE)
        SCREEN.blit(stat_text, (120, 180 + i * 30))


def draw_debug_leaderboard():
    """Display the Debug leaderboard with scrolling."""
    global debug_scroll_offset

    debug_stats = leaderboard_data["Debug"]
    y_offset = 180 + debug_scroll_offset  # Apply scroll offset

    for language, difficulties in debug_stats.items():
        # Render the language title
        language_title = FONT_SMALL.render(language, True, WHITE)
        SCREEN.blit(language_title, (120, y_offset))
        y_offset += 30

        for difficulty, stats in difficulties.items():
            # Render the difficulty stats
            difficulty_text = FONT_SMALL.render(
                f"{difficulty}: High Score: {stats['high_score']}, Correct: {stats['correct']}, Wrong: {stats['wrong']}",
                True,
                WHITE,
            )
            SCREEN.blit(difficulty_text, (140, y_offset))
            y_offset += 30

    # Draw a scroll indicator (optional)
    pygame.draw.rect(SCREEN, GRAY, (window_width - 20, 150, 10, 300))  # Scroll bar background
    scroll_bar_height = 100  # Height of the scroll bar
    scroll_bar_y = 150 + (debug_scroll_offset / -500) * 300  # Adjust based on scroll offset
    pygame.draw.rect(SCREEN, WHITE, (window_width - 20, scroll_bar_y, 10, scroll_bar_height))  # Scroll bar


def draw_fill_leaderboard():
    """Display the Fill in the Blanks leaderboard."""
    fill_stats = leaderboard_data["Fill in the Blanks"]
    fill_text = [
        f"Normal Mobs Shot: {fill_stats['normal_mobs_shot']}",
        f"Bosses Shot: {fill_stats['bosses_shot']}",
        f"Wave Count: {fill_stats['wave_count']}",
        f"Correct Prompts: {fill_stats['correct_prompts']}",
        f"Wrong Prompts: {fill_stats['wrong_prompts']}",
        f"Time Record: {fill_stats['time_record']}s",
    ]
    for i, line in enumerate(fill_text):
        stat_text = FONT_SMALL.render(line, True, WHITE)
        SCREEN.blit(stat_text, (120, 180 + i * 30))


def handle_debug_scroll(event):
    """Handle mouse wheel scrolling in the Debug tab."""
    global debug_scroll_offset

    # Adjust scroll offset based on mouse wheel movement
    if event.type == pygame.MOUSEWHEEL:
        debug_scroll_offset += event.y * debug_scroll_speed  # Scroll up or down
        debug_scroll_offset = max(debug_scroll_offset, -500)  # Prevent scrolling too far up
        debug_scroll_offset = min(debug_scroll_offset, 0)  # Prevent scrolling too far down


def load_binary_stats():
    """Load Binary mode statistics from a JSON file and update the leaderboard."""
    global leaderboard_data
    BINARY_STATS_FILE = "binary_stats.json"

    try:
        with open(BINARY_STATS_FILE, "r") as file:
            binary_stats = json.load(file)

        # Update the leaderboard with the loaded stats
        print("Binary stats loaded:", binary_stats)  # Debugging output
        update_leaderboard("Binary", binary_stats)

        # Remove the stats file after loading
        os.remove(BINARY_STATS_FILE)
        print("Binary stats loaded and leaderboard updated.")
    except FileNotFoundError:
        print("No Binary stats file found.")
    except Exception as e:
        print(f"Error loading Binary stats: {e}")


def main():
    # Show bootup screen
    draw_bootup_screen()

    global current_tab, subprocess_instance, current_help_mode  # Declare global variables
    current_tab = "title"
    toggle_button = None

    # Initialize the clock
    clock = pygame.time.Clock()

    # Load leaderboard data
    load_leaderboard()

    while True:
        # Check if the subprocess has exited
        if subprocess_instance is not None:
            if subprocess_instance.poll() is not None:  # Check if the subprocess has finished
                print(f"Subprocess finished with return code: {subprocess_instance.returncode}")
                subprocess_instance = None  # Reset the subprocess instance

                # Check if Binary stats need to be loaded
                if current_tab == "play" and current_category == "Binary":
                    print("Loading Binary stats...")
                    load_binary_stats()

                unlock_next_stage()  # Unlock the next stage only after the subprocess exits
                selected_stage = None  # Reset the selected stage so it becomes clickable again
                current_tab = "language_select"  # Return to the language selection screen

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                save_leaderboard()  # Save leaderboard data before quitting
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEMOTION:
                # Check hover state for buttons only in the current tab
                if current_tab == "title":
                    play_button.check_hover(event.pos)
                    options_button.check_hover(event.pos)
                    customize_button.check_hover(event.pos)
                    help_button.check_hover(event.pos)
                    learning_button.check_hover(event.pos)
                    exit_button.check_hover(event.pos)
                elif current_tab == "play":
                    typing_button.check_hover(event.pos)
                    coding_button.check_hover(event.pos)
                    fill_in_the_blanks_button.check_hover(event.pos)
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                # Handle clicks only in the current tab
                if current_tab == "title":
                    if play_button.is_clicked(event.pos):
                        current_tab = "play"  # Switch to the play tab
                    elif options_button.is_clicked(event.pos):
                        current_tab = "options"
                    elif customize_button.is_clicked(event.pos):
                        current_tab = "customize"
                    elif help_button.is_clicked(event.pos):
                        current_tab = "help"
                    elif learning_button.is_clicked(event.pos):  # Handle Learning button click
                        current_tab = "learn"  # Switch to the Learn tab
                    elif leaderboard_button.is_clicked(event.pos):  # Handle Leaderboard button click
                        current_tab = "leaderboard"  # Switch to the Leaderboard tab
                    elif exit_button.is_clicked(event.pos):
                        current_tab = "exit"
                elif current_tab == "play":
                    if back_button.is_clicked(event.pos):
                        current_tab = "title"
                    elif typing_button.is_clicked(event.pos):
                        # Ensure only Binary assets are used for Typing Mode
                        if current_category != "Binary" or selected_asset not in binary_assets:
                            selected_asset_to_use = "images/rocket1.png"  # Default rocket asset for Typing Mode
                            print(f"No valid Binary asset selected! Using default asset: {selected_asset_to_use}")
                        else:
                            selected_asset_to_use = selected_asset

                        print(f"Launching main2.py for Typing Mode with asset: {selected_asset_to_use}")
                        subprocess.Popen(["python", "main2.py", selected_asset_to_use])  # Pass the selected asset
                        current_tab = "title"
                    elif coding_button.is_clicked(event.pos):
                        # Ensure only Coding assets are used for Coding Mode
                        if current_category != "Coding" or selected_asset not in coding_assets:
                            selected_asset_to_use = "images/man1cleared.png"  # Default man asset for Coding Mode
                            print(f"No valid Coding asset selected! Using default asset: {selected_asset_to_use}")
                        else:
                            selected_asset_to_use = selected_asset

                        print(f"Launching language selection for Coding Mode with asset: {selected_asset_to_use}")
                        current_tab = "language_select"  # Go to language selection
                    elif fill_in_the_blanks_button.is_clicked(event.pos):  # Handle the Fill in the Blanks button click
                        current_tab = "fill_in_the_blanks_stage_select"  # Switch to the stage selector tab
                elif current_tab == "language_select":
                    handle_language_select_click(event.pos)
                elif current_tab == "customize":
                    if back_button.is_clicked(event.pos):
                        current_tab = "title"
                    else:
                        handle_customize_tab_click(event.pos)
                elif current_tab == "options":
                    if back_button.is_clicked(event.pos):
                        current_tab = "title"
                    else:
                        handle_options_tab_click(event.pos, toggle_button)
                elif current_tab == "help":
                    if back_button.is_clicked(event.pos):
                        if current_help_mode is None:
                            current_tab = "title"  # Go back to the main menu
                        else:
                            current_help_mode = None  # Go back to the main help menu
                    else:
                        handle_help_tab_click(event.pos)
                elif current_tab == "learn":
                    if back_button.is_clicked(event.pos):
                        current_tab = "title"
                    else:
                        handle_learn_tab_click(event.pos)
                elif current_tab == "stage_select":
                    handle_stage_select_click(event.pos)
                elif current_tab == "fill_in_the_blanks_stage_select":
                    handle_fill_in_the_blanks_stage_select_click(event.pos)
                elif current_tab == "leaderboard":
                    if back_button.is_clicked(event.pos):
                        current_tab = "title"
                    else:
                        handle_leaderboard_tab_click(event.pos)
            elif event.type == pygame.MOUSEWHEEL:
                if current_tab == "leaderboard" and current_leaderboard_tab == "Debug":
                    handle_debug_scroll(event)

        # Draw the appropriate screen based on the current tab
        if current_tab == "title":
            SCREEN.blit(background_image, (0, 0))  # Use the main menu background
            draw_title_screen()
        elif current_tab == "play":
            SCREEN.blit(background_image, (0, 0))  # Use the same background as the main menu
            draw_play_tab()
        elif current_tab == "options":
            SCREEN.fill((0, 0, 0))  # Clear the screen with a black background
            toggle_button = draw_options_tab()
        elif current_tab == "customize":
            SCREEN.fill((0, 0, 0))  # Clear the screen with a black background
            draw_customize_tab()
        elif current_tab == "help":
            SCREEN.fill((0, 0, 0))  # Clear the screen with a black background
            draw_help_tab()
        elif current_tab == "language_select":
            SCREEN.fill((0, 0, 0))  # Clear the screen with a black background
            draw_language_select_tab()
        elif current_tab == "stage_select":
            SCREEN.fill((0, 0, 0))  # Clear the screen with a black background
            draw_stage_select_tab()
        elif current_tab == "learn":
            SCREEN.fill((0, 0, 0))  # Clear the screen with a black background
            draw_learn_tab()
        elif current_tab == "exit":
            SCREEN.fill((0, 0, 0))  # Clear the screen with a black background
            draw_exit_tab()
            pygame.display.flip()
            pygame.time.wait(2000)  # Wait for 2 seconds to display "Exiting..."
            pygame.quit()
            sys.exit()
        elif current_tab == "fill_in_the_blanks_stage_select":
            SCREEN.fill((0, 0, 0))  # Clear the screen with a black background
            draw_fill_in_the_blanks_stage_select_tab()
        elif current_tab == "leaderboard":
            SCREEN.fill((0, 0, 0))  # Clear the screen with a black background
            draw_leaderboard_tab()
            
        pygame.display.flip()
        clock.tick(60)  # Limit the frame rate to 60 FPS


if __name__ == "__main__":
    import sys

    # Load leaderboard data from file
    load_leaderboard()

    # Get the background from the command-line argument
    background_file = sys.argv[1] if len(sys.argv) > 1 else "autumnbg.png"

    # Load the background image
    background = pygame.image.load(f"images/{background_file}")

    main()