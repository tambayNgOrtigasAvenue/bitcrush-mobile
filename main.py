# import pygame module
import pygame
import sys
from os.path import join
from random import randint
import random  # For generating binary strings

# Difficulty and player HP
player_hp = 100  # Default HP for the player

# Add this near the top of the file
wave = 1  # Start at wave 1
wave_timer = 0  # Timer to track wave progression
wave_duration = 30  # Duration of each wave in seconds

def generate_binary(length=4):
    """Generate a random binary string of a given length."""
    return ''.join(random.choice('01') for _ in range(length))

def load_high_score():
    """Load the high score from a file."""
    try:
        with open("highscore.txt", "r") as file:
            return int(file.read().strip())
    except (FileNotFoundError, ValueError):
        return 0  # Default to 0 if the file doesn't exist or is invalid


def save_high_score(new_high_score):
    """Save the high score to a file."""
    with open("highscore.txt", "w") as file:
        file.write(str(new_high_score))

class Player(pygame.sprite.Sprite):
    def __init__(self, groups):
        super().__init__(groups)
        self.image = pygame.image.load(join('images', 'rocket.png')).convert_alpha()
        self.image = pygame.transform.scale(self.image, (60, 60))  # Image size
        self.rect = self.image.get_rect(center=(window_width / 2, window_height - 50))
        self.direction = pygame.math.Vector2()
        self.speed = 300

    def update(self, dt):
        keys = pygame.key.get_pressed()
        self.direction.x = int(keys[pygame.K_d]) - int(keys[pygame.K_a])
        self.direction = self.direction.normalize() if self.direction else self.direction
        self.rect.center += self.direction * self.speed * dt

class Star(pygame.sprite.Sprite): 
  def __init__(self, groups, surf):
    super().__init__(groups)
    self.image = surf
    self.image = pygame.transform.scale(self.image, (30, 30))
    self.rect = self.image.get_rect(center = (randint(0, window_width), randint(0, window_height)))

class Laser(pygame.sprite.Sprite):
    def __init__(self, surf, pos, target_pos, groups):
        super().__init__(groups)
        self.image = surf
        self.rect = self.image.get_rect(midbottom=pos)

        # Calculate the direction vector toward the target (meteor)
        target_vector = pygame.math.Vector2(target_pos) - pygame.math.Vector2(self.rect.center)
        self.direction = target_vector.normalize()  # Normalize to get a unit vector
        self.speed = 400  # Speed of the laser

    def update(self, dt):
        # Move the laser toward the target
        self.rect.center += self.direction * self.speed * dt

        # Remove the laser if it moves off-screen
        if (
            self.rect.bottom < 0
            or self.rect.top > window_height
            or self.rect.left > window_width
            or self.rect.right < 0
        ):
            self.kill()

class Meteor(pygame.sprite.Sprite):
    def __init__(self, surf, pos, groups):
        super().__init__(groups)
        self.image = surf
        self.rect = self.image.get_rect(center=pos)
        self.speed = randint(*current_meteor_speed)  # Use the current speed range
        self.binary_prompt = generate_binary()  # Add a binary prompt for each meteor
        self.font = pygame.font.Font(None, 30)  # Font for displaying the binary prompt

    def draw_prompt(self, surface):
        """Draw the binary prompt above the meteor."""
        text_surf = self.font.render(self.binary_prompt, True, (255, 255, 255))
        text_rect = text_surf.get_rect(center=(self.rect.centerx, self.rect.top - 10))
        surface.blit(text_surf, text_rect)

    def update(self, dt):
        """Move the meteor straight downward."""
        self.rect.y += self.speed * dt
        print(f"Meteor position: {self.rect.y}, Speed: {self.speed}, dt: {dt}")  # Debugging output

        if self.rect.top > window_height:
            print("Meteor removed (off-screen)")  # Debugging output
            self.kill()

def collisions():
    """Handle collisions between the player and meteors."""
    global score, player_hp

    # Check for collisions between the player and meteors
    collision_sprites = pygame.sprite.spritecollide(player, meteor_sprites, False)
    if collision_sprites:
        for meteor in collision_sprites:
            player_hp -= 10  # Reduce player HP by 10 for each collision
            meteor.kill()  # Remove the meteor after collision
            print(f"Player HP: {player_hp}")  # Debugging output

    # End the game if the player's HP reaches 0
    if player_hp <= 0:
        game_over()

def display_score():
    # Display the current score
    score_text = font.render(f"Score: {score}", True, (200, 50, 100))
    score_rect = score_text.get_rect(topleft=(10, 10))  # Display the score at the top-left corner
    display_surface.blit(score_text, score_rect)

def draw_player_lives():
    """Display the player's HP as a text indicator near the player sprite."""
    hp_text = font.render(f"HP: {player_hp}", True, (255, 0, 0))  # Red text for HP
    # Position the HP text to the right of the player sprite
    hp_rect = hp_text.get_rect(midleft=(player.rect.right + 10, player.rect.centery))
    display_surface.blit(hp_text, hp_rect)

def pause_game():
    """Pause the game and display a pause menu with the current score."""
    global difficulty  # Ensure difficulty can be updated
    paused = True
    font_large = pygame.font.Font(None, 74)
    font_small = pygame.font.Font(None, 50)

    # Pause text
    pause_text = font_large.render("Game Paused", True, (255, 255, 255))
    pause_rect = pause_text.get_rect(center=(window_width // 2, window_height // 2 - 150))

    # Score text
    score_text = font_small.render(f"Score: {score}", True, (255, 255, 255))
    score_rect = score_text.get_rect(center=(window_width // 2, window_height // 2 - 50))

    # Instruction to quit
    quit_text = font_small.render("Press F9 to Exit to Main Menu", True, (255, 255, 255))
    quit_rect = quit_text.get_rect(center=(window_width // 2, window_height // 2 + 50))

    # Instruction to retry
    retry_text = font_small.render("Press R to Retry", True, (255, 255, 255))
    retry_rect = retry_text.get_rect(center=(window_width // 2, window_height // 2 + 100))

    while paused:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:  # Unpause when ESC is pressed
                    paused = False
                elif event.key == pygame.K_F9:  # Quit the game when F9 is pressed
                    pygame.quit()
                    sys.exit()
                elif event.key == pygame.K_r:  # Restart the game when R is pressed
                    reset_game()
                    paused = False

        # Draw the pause screen
        display_surface.fill((0, 0, 0))  # Black background
        display_surface.blit(pause_text, pause_rect)
        display_surface.blit(score_text, score_rect)
        display_surface.blit(quit_text, quit_rect)
        display_surface.blit(retry_text, retry_rect)

        pygame.display.flip()
        clock.tick(30)  # Limit the frame rate during pause

def game_over():
    """Display the Game Over screen with the player's score and high score."""
    global score

    # Load the current high score
    high_score = load_high_score()

    # Update the high score if the player's score is higher
    if score > high_score:
        high_score = score
        save_high_score(high_score)

    font_large = pygame.font.Font(None, 74)
    font_small = pygame.font.Font(None, 50)

    # Game Over text
    game_over_text = font_large.render("Game Over", True, (255, 0, 0))
    game_over_rect = game_over_text.get_rect(center=(window_width // 2, window_height // 2 - 150))

    # Score text
    score_text = font_small.render(f"Your Score: {score}", True, (255, 255, 255))
    score_rect = score_text.get_rect(center=(window_width // 2, window_height // 2 - 50))

    # High Score text
    high_score_text = font_small.render(f"High Score: {high_score}", True, (255, 255, 255))
    high_score_rect = high_score_text.get_rect(center=(window_width // 2, window_height // 2))

    # Instruction to quit
    quit_text = font_small.render("Press ENTER to Quit", True, (255, 255, 255))
    quit_rect = quit_text.get_rect(center=(window_width // 2, window_height // 2 + 100))

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:  # Quit when ENTER is pressed
                    pygame.quit()
                    sys.exit()

        # Draw the Game Over screen
        display_surface.fill((0, 0, 0))  # Black background
        display_surface.blit(game_over_text, game_over_rect)
        display_surface.blit(score_text, score_rect)
        display_surface.blit(high_score_text, high_score_rect)
        display_surface.blit(quit_text, quit_rect)

        pygame.display.update()
        clock.tick(30)  # Limit the frame rate

def reset_game():
    """Reset the game state to start over."""
    global score, player_input, all_sprites, meteor_sprites, laser_sprites

    # Reset score and player input
    score = 0
    player_input = ""

    # Clear all sprite groups
    all_sprites.empty()
    meteor_sprites.empty()
    laser_sprites.empty()

    # Reinitialize the player and stars
    for i in range(20):
        Star(all_sprites, star_surf)
    global player
    player = Player(all_sprites)

# Function to gradually increase meteor speed
def increase_meteor_speed():
    global current_meteor_speed
    min_speed, max_speed = current_meteor_speed
    if max_speed < 300:  # Cap the maximum speed to prevent meteors from becoming too fast
        current_meteor_speed = (min_speed + 1, max_speed + 1)  # Gradually increase speed

# General setup
pygame.init()
window_width, window_height = 980, 520  # Ensure these are defined before creating the player
display_surface = pygame.display.set_mode((window_width, window_height))
pygame.display.set_caption('BITCRUSH')

running = True
paused = False
clock = pygame.time.Clock()

# Initialize the score
score = 0

player_input = ""  # Track the player's current input

#import
star_surf = pygame.image.load(join('images','star.png')).convert_alpha()
bug_surf = pygame.image.load(join('images', 'asteroid.png')).convert_alpha()
new_width2 = 75
new_height2 = 75
bug_surf = pygame.transform.scale(bug_surf, (new_width2, new_height2))
laser_surf = pygame.image.load(join('images','laser.png')).convert_alpha()
new_width3 = 25
new_width3 = 25
laser_surf = pygame.transform.scale(laser_surf, (new_width3, new_width3))
font = pygame.font.Font(join('images', 'Idealy.ttf'), 20)
text_surf = font.render('text', True, (200, 50, 100))

#sprite groups
all_sprites = pygame.sprite.Group()
meteor_sprites = pygame.sprite.Group()
laser_sprites = pygame.sprite.Group()
for i in range(20):
  Star(all_sprites, star_surf)
player = Player(all_sprites)

#custom events: meteor event
meteor_event = pygame.event.custom_type()

# Replace the current meteor speed and spawn rate initialization with this:
current_meteor_speed = (150, 200)  # Increase the speed range
meteor_spawn_rate = 2000  # Initial spawn rate (milliseconds)

# Update meteor speed and spawn rate as the wave increases
def update_wave():
    global wave, current_meteor_speed, meteor_spawn_rate
    wave += 1  # Increment the wave
    min_speed, max_speed = current_meteor_speed
    current_meteor_speed = (min_speed + 10, max_speed + 10)  # Increase meteor speed
    meteor_spawn_rate = max(500, meteor_spawn_rate - 100)  # Decrease spawn rate (cap at 500ms)
    pygame.time.set_timer(meteor_event, meteor_spawn_rate)  # Update the spawn timer

# Set the meteor spawn timer
pygame.time.set_timer(meteor_event, meteor_spawn_rate)

def display_wave():
    """Display the current wave on the screen."""
    wave_text = font.render(f"Wave: {wave}", True, (0, 0, 255))  # Blue text for wave
    wave_rect = wave_text.get_rect(topright=(window_width - 10, 10))  # Top-right corner
    display_surface.blit(wave_text, wave_rect)

#game loop

while running:
    dt = clock.tick(60) / 1000  # Cap frame rate to 60 FPS

    # Event loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                if pause_game():
                    running = False
            elif event.unicode in '01':  # Check for binary input (only '0' or '1')
                typed_char = event.unicode
                for meteor in list(meteor_sprites):  # Iterate through all meteors
                    if meteor.binary_prompt.startswith(typed_char):  # Check if the input matches the start of the prompt
                        meteor.binary_prompt = meteor.binary_prompt[1:]  # Remove the first character from the prompt
                        if not meteor.binary_prompt:  # If the prompt is empty, destroy the meteor
                            meteor.kill()
                            score += 1  # Increase the score
                        break  # Stop checking after the first match
        elif event.type == meteor_event:
            if len(meteor_sprites) < wave + 2:  # Increase max meteors with wave
                x = randint(50, window_width - 50)
                y = randint(-50, 0)  # Spawn slightly above the screen
                new_meteor = Meteor(bug_surf, (x, y), (all_sprites, meteor_sprites))
                
                # Check for overlap with existing meteors
                if pygame.sprite.spritecollide(new_meteor, meteor_sprites, False):
                    new_meteor.kill()  # Remove the meteor if it overlaps
                else:
                    meteor_sprites.add(new_meteor)

    # Update wave timer
    wave_timer += dt
    if wave_timer >= wave_duration:
        wave_timer = 0
        update_wave()

    # Gradually increase meteor speed over time
    if pygame.time.get_ticks() % 5000 == 0:
        increase_meteor_speed()

    # Update game
    all_sprites.update(dt)
    meteor_sprites.update(dt)

    # Handle collisions
    collisions()

    # Draw game
    display_surface.fill('light blue')
    all_sprites.draw(display_surface)

    # Draw binary prompts for meteors
    for meteor in meteor_sprites:
        meteor.draw_prompt(display_surface)

    display_score()
    draw_player_lives()
    display_wave()  # Display the current wave

    pygame.display.update()

# Only show the Game Over screen if the game ends due to a loss or win
if not running:
    game_over()

pygame.quit()