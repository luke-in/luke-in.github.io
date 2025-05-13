import pygame
import random
import os

# --- Setup ---
pygame.init()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
pygame.font.init()
font = pygame.font.SysFont(None, 60)

# --- Functions ---
def play_game():
    player_pos = pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2)
    circle_pos = pygame.Vector2(screen.get_width() / 4, screen.get_height() / 4)
    score = 0
    dt = 0
    speed = 1000  # Default speed, controlled by slider
    start_ticks = pygame.time.get_ticks()
    running = True

    def spot():
        circle_pos.x = random.randint(100, 1180)
        circle_pos.y = random.randint(100, 620)

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            player_pos.y = max(player_pos.y - speed * dt, 0)
        if keys[pygame.K_s]:
            player_pos.y = min(player_pos.y + speed * dt, 720)
        if keys[pygame.K_a]:
            player_pos.x = max(player_pos.x - speed * dt, 0)
        if keys[pygame.K_d]:
            player_pos.x = min(player_pos.x + speed * dt, 1280)

        # Slider control with LEFT/RIGHT arrows
        if keys[pygame.K_LEFT]:
            speed = max(100, speed - 300 * dt)
        if keys[pygame.K_RIGHT]:
            speed = min(2000, speed + 300 * dt)

        # Check collision
        if abs(circle_pos.x - player_pos.x) < 100 and abs(circle_pos.y - player_pos.y) < 100:
            score += 1
            spot()

        # Drawing
        screen.fill("purple")
        pygame.draw.circle(screen, "blue", player_pos, 80)
        pygame.draw.circle(screen, "orange", circle_pos, 40)

        score_text = font.render(f"Score: {score}", True, (255, 255, 255))
        screen.blit(score_text, (20, 20))

        speed_text = font.render(f"Speed: {int(speed)}", True, (255, 255, 255))
        screen.blit(speed_text, (20, 80))

        seconds_passed = (pygame.time.get_ticks() - start_ticks) / 1000
        time_left = max(0, 20 - int(seconds_passed))
        timer_text = font.render(f"Time Left: {time_left}", True, (255, 255, 255))
        screen.blit(timer_text, (1000, 20))

        if time_left <= 0:
            running = False

        pygame.display.flip()
        dt = clock.tick(60) / 1000

    return score

score=play_game()

# Save high score
high_score = 0
if os.path.exists("gamelog.txt"):
    with open("gamelog.txt", "r") as file:
        content = file.read().strip()
        if content.isdigit():
            high_score = int(content)
if score > high_score:
    with open("gamelog.txt", "w") as file:
        file.write(str(score))



def game_over_screen(score):
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    return  # Restart the game

        screen.fill("black")
        final_text = font.render(f"Final Score: {score}", True, (255, 255, 255))
        score_text = font.render(f"High Score: {max(score,high_score)}", True, (255, 255, 255))
        restart_text = font.render("Press SPACE to play again", True, (255, 255, 255))

        screen.blit(final_text, (screen.get_width() / 2 - final_text.get_width() / 2, 300))
        screen.blit(score_text, (screen.get_width() / 2 - final_text.get_width() / 2, 500))

        screen.blit(restart_text, (screen.get_width() / 2 - restart_text.get_width() / 2, 400))
        pygame.display.flip()

# --- Main Game Loop ---
while True:
    final_score = play_game()
    game_over_screen(final_score)
