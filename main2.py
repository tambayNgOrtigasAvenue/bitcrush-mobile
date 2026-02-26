import pygame
import random
import sys
import json

# Get the selected asset from the command-line argument
selected_asset = sys.argv[1] if len(sys.argv) > 1 else "images/rocket1.png"

# Initialize pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Binary Mode")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
LIGHT_BLUE = (173, 216, 230)  # Light blue color

# Fonts
FONT = pygame.font.Font(None, 36)

# Load the Minecraft font
try:
    MINECRAFT_FONT = pygame.font.Font('images/minecraft.ttf', 36)  # Set font size to 36
    MINECRAFT_FONT_LARGE = pygame.font.Font('images/minecraft.ttf', 74)  # Larger font for titles
except FileNotFoundError:
    print("Error: 'minecraft.ttf' not found in the 'images' folder.")
    sys.exit()

# Load the blue background image
try:
    PAUSE_BACKGROUND = pygame.image.load("images/bluebg.jpg")
    PAUSE_BACKGROUND = pygame.transform.scale(PAUSE_BACKGROUND, (WIDTH, HEIGHT))
except pygame.error as e:
    print(f"Error loading background image: {e}")
    sys.exit()

# Clock
clock = pygame.time.Clock()

# Load images from the 'images' folder
try:
    ROCKET_IMAGE = pygame.image.load(selected_asset)
    METEOR_IMAGE = pygame.image.load('images/asteroid.png')
    BACKGROUND_IMAGE = pygame.image.load('images/star.png')
    LASER_IMAGE = pygame.image.load('images/laser1.png')  # Load the laser image
except pygame.error as e:
    print(f"Error loading image: {e}")
    sys.exit()

# Scale images while maintaining the aspect ratio
def scale_image(image, target_width, target_height):
    original_width, original_height = image.get_size()
    aspect_ratio = original_width / original_height

    # Calculate new dimensions while maintaining the aspect ratio
    if target_width / target_height > aspect_ratio:
        new_height = target_height
        new_width = int(new_height * aspect_ratio)
    else:
        new_width = target_width
        new_height = int(new_width / aspect_ratio)

    return pygame.transform.scale(image, (new_width, new_height))

# Scale the rocket image to make it slightly bigger
ROCKET_IMAGE = scale_image(ROCKET_IMAGE, 60, 120)  # Increased size while maintaining aspect ratio

# Scale other images as needed
METEOR_IMAGE = pygame.transform.scale(METEOR_IMAGE, (50, 50))
BACKGROUND_IMAGE = pygame.transform.scale(BACKGROUND_IMAGE, (WIDTH, HEIGHT))
LASER_IMAGE = pygame.transform.scale(LASER_IMAGE, (10, 30))  # Adjust size as needed
STAR_IMAGE = pygame.transform.scale(BACKGROUND_IMAGE, (20, 20))  # Adjust size as needed

# Pre-generate star positions
STAR_POSITIONS = [(random.randint(0, WIDTH), random.randint(0, HEIGHT)) for _ in range(100)]

# Function to draw stars at fixed positions
def draw_stars():
    for x, y in STAR_POSITIONS:
        screen.blit(STAR_IMAGE, (x, y))

# Rocket class
class Rocket:
    def __init__(self):
        self.image = ROCKET_IMAGE
        self.original_image = ROCKET_IMAGE  # Keep the original image for rotation
        self.rect = self.image.get_rect(center=(WIDTH // 2, HEIGHT - 60))
        self.speed = 5
        self.hp = 100  # Player HP
        self.angle = 0  # Rotation angle

    def rotate(self, angle):
        """Rotate the rocket by a given angle."""
        self.angle = angle
        self.image = pygame.transform.rotate(self.original_image, self.angle)
        self.rect = self.image.get_rect(center=self.rect.center)

    def draw(self):
        screen.blit(self.image, self.rect)

# Laser class
class Laser:
    def __init__(self, x, y, target_x, target_y, target_id, angle=0):
        self.image = LASER_IMAGE
        self.original_image = LASER_IMAGE  # Keep the original image for rotation
        self.rect = self.image.get_rect(center=(x, y))
        self.speed = 10  # Laser speed
        self.target_id = target_id  # ID of the target meteor
        self.angle = angle  # Rotation angle of the laser
        # Calculate the direction vector toward the target
        dx = target_x - x
        dy = target_y - y
        distance = (dx**2 + dy**2)**0.5
        self.velocity_x = (dx / distance) * self.speed
        self.velocity_y = (dy / distance) * self.speed

    def move(self):
        """Move the laser in the direction of its velocity."""
        self.rect.x += self.velocity_x
        self.rect.y += self.velocity_y

    def rotate(self, angle):
        """Rotate the laser by a given angle."""
        self.angle = angle
        self.image = pygame.transform.rotate(self.original_image, self.angle)
        self.rect = self.image.get_rect(center=self.rect.center)

    def draw(self):
        screen.blit(self.image, self.rect)

# Meteor class
class Meteor:
    def __init__(self, target_x, speed):
        self.image = METEOR_IMAGE
        self.rect = self.image.get_rect(center=(random.randint(50, WIDTH - 50), -50))
        self.speed = speed
        self.prompt = bin(random.randint(1, 15))[2:]  # Binary prompt
        self.target_x = target_x  # Target player's x position
        self.typed_length = 0  # Tracks how much of the prompt has been typed
        self.horizontal_speed = 2  # Horizontal movement speed
        self.fully_typed = False  # Flag to indicate if the prompt is fully typed

    def move(self):
        """Move the meteor straight down."""
        self.rect.y += self.speed  # Move downward

    def draw(self):
        screen.blit(self.image, self.rect)
        if self.prompt:  # Only draw the prompt if it hasn't been fully typed
            # Split the prompt into typed and untyped parts
            typed_part = self.prompt[:self.typed_length]
            untyped_part = self.prompt[self.typed_length:]

            # Render the typed part in green
            typed_surface = FONT.render(typed_part, True, GREEN)
            screen.blit(typed_surface, (self.rect.x + 5, self.rect.y - 40))  # Adjusted position for visibility

            # Render the untyped part in white
            untyped_surface = FONT.render(untyped_part, True, WHITE)
            screen.blit(untyped_surface, (self.rect.x + 5 + typed_surface.get_width(), self.rect.y - 40))  # Adjusted position

def avoid_collisions(meteors, safe_distance=80):
    """Ensure meteors maintain a safe distance from each other."""
    for i, meteor1 in enumerate(meteors):
        for j, meteor2 in enumerate(meteors):
            if i != j:
                # Check if the meteors are too close horizontally and vertically
                dx = meteor1.rect.x - meteor2.rect.x
                dy = meteor1.rect.y - meteor2.rect.y
                distance = (dx**2 + dy**2)**0.5  # Calculate Euclidean distance

                if distance < safe_distance:
                    # Calculate adjustment to maintain safe distance
                    overlap = safe_distance - distance
                    adjust_x = (dx / distance) * (overlap / 2) if distance != 0 else safe_distance / 2
                    adjust_y = (dy / distance) * (overlap / 2) if distance != 0 else safe_distance / 2

                    # Apply adjustments to meteor1 and meteor2
                    meteor1.rect.x += int(adjust_x)
                    meteor1.rect.y += int(adjust_y)
                    meteor2.rect.x -= int(adjust_x)
                    meteor2.rect.y -= int(adjust_y)

                    # Ensure meteors stay within screen bounds
                    meteor1.rect.x = max(0, min(WIDTH - meteor1.rect.width, meteor1.rect.x))
                    meteor1.rect.y = max(0, min(HEIGHT - meteor1.rect.height, meteor1.rect.y))
                    meteor2.rect.x = max(0, min(WIDTH - meteor2.rect.width, meteor2.rect.x))
                    meteor2.rect.y = max(0, min(HEIGHT - meteor2.rect.height, meteor2.rect.y))

def pause_menu(score, waves_survived, opponents_shot):
    """Display the pause menu."""
    paused = True
    show_modal = False  # Flag to show the retry confirmation window
    exit_modal = False  # Flag to show the exit confirmation window

    while paused:
        screen.blit(PAUSE_BACKGROUND, (0, 0))  # Use the blue background

        # Display pause menu text
        pause_text = MINECRAFT_FONT_LARGE.render("PAUSED", True, WHITE)
        screen.blit(pause_text, (WIDTH // 2 - pause_text.get_width() // 2, HEIGHT // 2 - 150))

        waves_text = MINECRAFT_FONT.render(f"Waves Survived: {waves_survived}", True, WHITE)
        screen.blit(waves_text, (WIDTH // 2 - waves_text.get_width() // 2, HEIGHT // 2 - 50))

        opponents_text = MINECRAFT_FONT.render(f"Opponents Shot: {opponents_shot}", True, WHITE)
        screen.blit(opponents_text, (WIDTH // 2 - opponents_text.get_width() // 2, HEIGHT // 2))

        resume_text = MINECRAFT_FONT.render("Press ESC to Resume", True, WHITE)
        screen.blit(resume_text, (WIDTH // 2 - resume_text.get_width() // 2, HEIGHT // 2 + 50))

        retry_text = MINECRAFT_FONT.render("Press D to Retry", True, WHITE)
        screen.blit(retry_text, (WIDTH // 2 - retry_text.get_width() // 2, HEIGHT // 2 + 100))

        quit_text = MINECRAFT_FONT.render("Press F9 to Quit to Main Menu", True, WHITE)
        screen.blit(quit_text, (WIDTH // 2 - quit_text.get_width() // 2, HEIGHT // 2 + 150))

        # If the retry confirmation is active, display it
        if show_modal:
            # Use the blue background image for the modal
            modal_background = pygame.transform.scale(PAUSE_BACKGROUND, (700, 400))  # Scale the background to modal size
            screen.blit(modal_background, (WIDTH // 2 - 350, HEIGHT // 2 - 200))  # Adjusted position

            # Display confirmation text
            modal_text = MINECRAFT_FONT.render("Do you want to reset?", True, WHITE)
            screen.blit(modal_text, (WIDTH // 2 - modal_text.get_width() // 2, HEIGHT // 2 - 75))

            back_text = MINECRAFT_FONT.render("Press B to Back", True, WHITE)
            screen.blit(back_text, (WIDTH // 2 - back_text.get_width() // 2, HEIGHT // 2 - 25))

            confirm_text = MINECRAFT_FONT.render("Press C to Confirm", True, WHITE)
            screen.blit(confirm_text, (WIDTH // 2 - confirm_text.get_width() // 2, HEIGHT // 2 + 25))

        # If the exit confirmation is active, display it
        if exit_modal:
            # Draw a larger opaque background for the confirmation
            modal_background = pygame.Surface((700, 400))  # Increased size
            modal_background = pygame.transform.scale(PAUSE_BACKGROUND, (700, 400))  # Scale the background to modal size
            screen.blit(modal_background, (WIDTH // 2 - 350, HEIGHT // 2 - 200))  # Adjusted position

            # Display confirmation text
            modal_text = MINECRAFT_FONT.render("Do you want to exit?", True, WHITE)
            screen.blit(modal_text, (WIDTH // 2 - modal_text.get_width() // 2, HEIGHT // 2 - 75))

            no_text = MINECRAFT_FONT.render("Press N for No", True, WHITE)
            screen.blit(no_text, (WIDTH // 2 - no_text.get_width() // 2, HEIGHT // 2 - 25))

            yes_text = MINECRAFT_FONT.render("Press Y to Yes", True, WHITE)
            screen.blit(yes_text, (WIDTH // 2 - yes_text.get_width() // 2, HEIGHT // 2 + 25))

        pygame.display.flip()

        # Handle pause menu events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if show_modal:
                    # Handle retry confirmation-specific events
                    if event.key == pygame.K_b:  # Back
                        show_modal = False  # Close the confirmation
                    elif event.key == pygame.K_c:  # Confirm
                        main()  # Restart the game
                elif exit_modal:
                    # Handle exit confirmation-specific events
                    if event.key == pygame.K_n:  # No
                        exit_modal = False  # Close the confirmation
                    elif event.key == pygame.K_y:  # Yes
                        pygame.quit()
                        sys.exit()
                else:
                    # Handle regular pause menu events
                    if event.key == pygame.K_ESCAPE:  # Resume game
                        paused = False
                    elif event.key == pygame.K_d:  # Show the retry confirmation
                        show_modal = True
                    elif event.key == pygame.K_F9:  # Show the exit confirmation
                        exit_modal = True

# File to store Binary mode statistics
BINARY_STATS_FILE = "binary_stats.json"

def save_binary_stats(stats):
    """Save Binary mode statistics to a JSON file."""
    try:
        with open(BINARY_STATS_FILE, "w") as file:
            json.dump(stats, file, indent=4)
        print("Binary stats saved successfully:", stats)
    except Exception as e:
        print(f"Error saving Binary stats: {e}")

# Main game function
def main():
    rocket = Rocket()
    meteors = []  # Start with no meteors on screen
    lasers = []  # Track lasers
    current_input = ""
    score = 0
    meteor_speed = 1  # Initial speed of meteors
    spawn_delay = 1000  # Initial spawn delay in milliseconds
    last_spawn_time = pygame.time.get_ticks()
    wave_meteor_count = 5  # Start with 5 meteors in the first wave
    meteors_spawned = 0  # Track how many meteors have been spawned in the current wave
    meteors_destroyed = 0  # Track how many meteors have been destroyed
    waves_survived = 1  # Start with wave 1
    opponents_shot = 0  # Track opponents shot

    # Main game loop (adjusted part)
    running = True
    wave_start_time = pygame.time.get_ticks()  # Track when the current wave started
    wave_duration = 15000  # Duration of each wave in milliseconds (15 seconds)

    while running:
        # Draw the light blue background
        screen.fill(LIGHT_BLUE)
        # Draw scattered stars
        draw_stars()

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:  # Pause the game
                    pause_menu(score, waves_survived, opponents_shot)
                elif event.key == pygame.K_BACKSPACE:
                    current_input = current_input[:-1]
                elif event.key == pygame.K_RETURN:
                    pass  # No action needed for RETURN key
                else:
                    if meteors:  # Focus on the first meteor
                        meteor = meteors[0]
                        # Check if the typed character matches the next character in the prompt
                        if meteor.prompt.startswith(current_input + event.unicode):
                            current_input += event.unicode
                            meteor.typed_length += 1  # Update the typed length
                            # Shoot the laser immediately when a correct character is typed
                            lasers.append(Laser(rocket.rect.centerx, rocket.rect.top, meteor.rect.centerx, meteor.rect.centery, id(meteor)))
                            if meteor.typed_length == len(meteor.prompt):  # If fully typed
                                meteor.fully_typed = True  # Mark the meteor as fully typed
                                current_input = ""  # Reset the input
                        else:
                            # Only reset if the input is completely invalid
                            current_input = ""  # Reset input if it doesn't match
                            meteor.typed_length = 0  # Reset typed length

            if event.type == pygame.KEYUP:
                # Reset the rocket's rotation when the key is released
                rocket.rotate(0)

        # Meteor movement
        for meteor in meteors[:]:
            meteor.move()  # Move the meteor straight down
            # Check if meteor collides with the player
            if meteor.rect.colliderect(rocket.rect):
                meteors.remove(meteor)
                rocket.hp -= 10  # Decrease HP by 10
            elif meteor.rect.top > HEIGHT:  # If the meteor passes through the bottom of the screen
                meteors.remove(meteor)
                rocket.hp -= 10  # Decrease HP by 10

        # Laser movement
        for laser in lasers[:]:
            laser.move()
            # Remove the laser if it moves off the screen
            if laser.rect.bottom < 0 or laser.rect.top > HEIGHT or laser.rect.left > WIDTH or laser.rect.right < 0:
                lasers.remove(laser)
            # Check if the laser hits its target meteor
            for meteor in meteors[:]:
                if id(meteor) == laser.target_id and laser.rect.colliderect(meteor.rect):
                    lasers.remove(laser)  # Stop the laser at the meteor
                    if meteor.fully_typed:  # Only remove the meteor if it was fully typed
                        meteors.remove(meteor)  # Remove the meteor
                        score += 1
                        opponents_shot += 1
                        meteors_destroyed += 1  # Increment destroyed meteors

        # Avoid collisions between meteors
        avoid_collisions(meteors)

        # Spawn meteors for the current wave
        current_time = pygame.time.get_ticks()
        if current_time - last_spawn_time > spawn_delay and meteors_spawned < wave_meteor_count:
            new_meteor = Meteor(random.randint(50, WIDTH - 50), speed=meteor_speed)
            meteors.append(new_meteor)
            meteors_spawned += 1  # Increment spawned meteors
            last_spawn_time = current_time
            print(f"Spawned meteor {meteors_spawned}/{wave_meteor_count}")

        # Check if the wave duration has elapsed
        if current_time - wave_start_time > wave_duration:
            waves_survived += 1  # Increment waves survived
            wave_meteor_count += 5  # Increase meteors in the next wave
            meteors_spawned = 0  # Reset spawned meteors for the new wave
            meteors_destroyed = 0  # Reset destroyed meteors for the new wave
            meteor_speed += 0.1  # Gradually increase meteor speed
            wave_start_time = current_time  # Reset the wave start time
            print(f"Wave {waves_survived} started! Meteors in this wave: {wave_meteor_count}")

        # Drawing
        rocket.draw()
        for meteor in meteors:
            meteor.draw()
        for laser in lasers:
            laser.draw()

        # Display wave number
        wave_surface = FONT.render(f"Wave: {waves_survived}", True, BLACK)
        screen.blit(wave_surface, (WIDTH // 2 - 50, 10))

        # Display score
        score_surface = FONT.render(f"Score: {score}", True, BLACK)
        screen.blit(score_surface, (10, 10))

        # Display player HP
        hp_surface = FONT.render(f"HP: {rocket.hp}", True, BLACK)
        screen.blit(hp_surface, (WIDTH - 100, 10))

        # Check for game over
        if rocket.hp <= 0:
            screen.blit(PAUSE_BACKGROUND, (0, 0))  # Use the blue background

            # Display "GAME OVER" in white
            game_over_surface = MINECRAFT_FONT_LARGE.render("GAME OVER", True, WHITE)
            screen.blit(game_over_surface, (WIDTH // 2 - game_over_surface.get_width() // 2, HEIGHT // 2 - 150))

            # Display score
            score_surface = MINECRAFT_FONT.render(f"Score: {score}", True, WHITE)
            screen.blit(score_surface, (WIDTH // 2 - score_surface.get_width() // 2, HEIGHT // 2 - 50))

            # Display waves cleared
            waves_surface = MINECRAFT_FONT.render(f"Waves Cleared: {waves_survived}", True, WHITE)
            screen.blit(waves_surface, (WIDTH // 2 - waves_surface.get_width() // 2, HEIGHT // 2))

            # Display meteors shot
            meteors_surface = MINECRAFT_FONT.render(f"Meteors Shot: {opponents_shot}", True, WHITE)
            screen.blit(meteors_surface, (WIDTH // 2 - meteors_surface.get_width() // 2, HEIGHT // 2 + 50))

            # Display high score
            high_score = max(score, opponents_shot)  # Example logic for high score
            high_score_surface = MINECRAFT_FONT.render(f"High Score: {high_score}", True, WHITE)
            screen.blit(high_score_surface, (WIDTH // 2 - high_score_surface.get_width() // 2, HEIGHT // 2 + 100))

            # Display quit instructions
            quit_surface = MINECRAFT_FONT.render("Press ENTER to Quit", True, WHITE)
            screen.blit(quit_surface, (WIDTH // 2 - quit_surface.get_width() // 2, HEIGHT // 2 + 150))

            pygame.display.flip()
            waiting = True
            while waiting:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                    elif event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_RETURN:  # Quit the game
                            waiting = False
                            running = False

        # Update display
        pygame.display.flip()
        # Cap the frame rate
        clock.tick(60)

    # Save Binary mode statistics when the game ends
    binary_stats = {
        "meteors_shot": opponents_shot,
        "wave_count": waves_survived,
        "high_score": max(score, opponents_shot)  # Save the high score
    }
    save_binary_stats(binary_stats)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
