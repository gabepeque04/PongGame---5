import pygame
import sys
import math

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 600, 400  # Set the width and height of the game window
PADDLE_WIDTH, PADDLE_HEIGHT = 15, 60  # Set the dimensions of the paddles
BALL_SIZE = 15  # Set the diameter of the ball
FPS = 60  # Set the frame rate per second
WHITE = (255, 255, 255)  # Define the color white
BLACK = (0, 0, 0)  # Define the color black
RED = (255, 0, 0)
LIGHT_BLUE = (100, 149, 237)  # Adjusted light blue color with increased intensity
TIMER_DURATION = 60  # Set the duration of the timer in seconds
TARGET_SCORE = 10  # Set the target score for winning

# Spin Factors
MAX_SPIN_FACTOR = 5  # Maximum spin factor
MIN_SPIN_FACTOR = 1  # Minimum spin factor

# Acceleration factor
ACCELERATION_FACTOR = 1.02  # Increase speed by 2% after each hit

# Create the game window
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pong")  # Set the title of the game window

# Create a clock object for controlling the frame rate
clock = pygame.time.Clock()

# Define the initial positions of the paddles
player1_paddle = pygame.Rect(30, HEIGHT // 2 - PADDLE_HEIGHT // 2, PADDLE_WIDTH, PADDLE_HEIGHT)
player2_paddle = pygame.Rect(WIDTH - 30 - PADDLE_WIDTH, HEIGHT // 2 - PADDLE_HEIGHT // 2, PADDLE_WIDTH, PADDLE_HEIGHT)

# Define the initial position and speed of the ball
ball = pygame.Rect(WIDTH // 2 - BALL_SIZE // 2, HEIGHT // 2 - BALL_SIZE // 2, BALL_SIZE, BALL_SIZE)
ball_speed = [5, 5]

# Initialize scores and timer
player1_score = 0
player2_score = 0
timer = TIMER_DURATION * FPS  # Convert seconds to frames

# Initialize a font object for rendering text
font = pygame.font.Font(None, 36)

# Main game loop
running = True
while running:  # Start the main loop
    for event in pygame.event.get():  # Iterate through each event
        if event.type == pygame.QUIT:  # Check if the user wants to quit
            running = False  # Set running to False to exit the loop

    keys = pygame.key.get_pressed()  # Get the state of all keyboard keys
    # Move player 1 paddle up and down based on keyboard input
    if keys[pygame.K_w] and player1_paddle.top > 0:
        player1_paddle.y -= 7
    if keys[pygame.K_s] and player1_paddle.bottom < HEIGHT:
        player1_paddle.y += 7
    # Move player 2 paddle up and down based on keyboard input
    if keys[pygame.K_UP] and player2_paddle.top > 0:
        player2_paddle.y -= 7
    if keys[pygame.K_DOWN] and player2_paddle.bottom < HEIGHT:
        player2_paddle.y += 7

    # Move the ball
    ball.x += ball_speed[0]
    ball.y += ball_speed[1]

    # Check for collisions with the top and bottom walls
    if ball.top <= 0:
        ball_speed[1] = abs(ball_speed[1])  # Reverse the vertical direction of the ball
    elif ball.bottom >= HEIGHT:
        ball_speed[1] = -abs(ball_speed[1])  # Reverse the vertical direction of the ball

    # Check for collisions with the paddles
    if ball.colliderect(player1_paddle):
        ball_speed[0] = abs(ball_speed[0])  # Ensure ball moves to the right after hitting player 1 paddle
       
        player1_paddle_color = WHITE
        player2_paddle_color = RED
        # Determine which paddle the ball collided with
        paddle = player1_paddle
    elif ball.colliderect(player2_paddle):
        ball_speed[0] = -abs(ball_speed[0])  # Ensure ball moves to the left after hitting player 2 paddle
        
        player1_paddle_color = RED
        player2_paddle_color = WHITE
        # Determine which paddle the ball collided with
        paddle = player2_paddle
    else:
        player1_paddle_color = RED
        player2_paddle_color = RED
        paddle = None

    if paddle:
        # Calculate the angle of collision
        relative_intersect_y = (paddle.centery - ball.centery) / (paddle.height // 2)
        bounce_angle = relative_intersect_y * (math.pi / 8)  # Maximum bounce angle is 90 degrees

        # Calculate the spin factor based on the speed of the ball
        ball_speed_mag = math.sqrt(ball_speed[0] ** 2 + ball_speed[1] ** 2)
        spin_factor = MIN_SPIN_FACTOR + (MAX_SPIN_FACTOR - MIN_SPIN_FACTOR) * (ball_speed_mag // 10)
        spin_factor = min(spin_factor, MAX_SPIN_FACTOR)

        # Update ball speed with enhanced spin effect
        speed = ball_speed_mag * spin_factor
        direction = math.atan2(ball_speed[1], ball_speed[0])
        new_angle = direction - bounce_angle
        ball_speed = [math.cos(new_angle) * speed, math.sin(new_angle) * speed]

        # Increase ball speed
        ball_speed[0] *= ACCELERATION_FACTOR
        ball_speed[1] *= ACCELERATION_FACTOR

    # Check if player 1 scores
    if ball.left <= 0:
        player2_score += 1  # Increment player 2 score
        ball_speed = [5, 5]
        # Check if player 2 wins
        if player2_score >= TARGET_SCORE:
            winner_text = font.render("Player 2 Wins!", True, WHITE)  # Render the winning message
            screen.blit(winner_text, (WIDTH // 2 - winner_text.get_width() // 2, HEIGHT // 2))
            pygame.display.flip()  # Update the display
            pygame.time.wait(3000)  # Wait 3 seconds before quitting
            running = False  # Exit the loop
        ball.x = WIDTH // 2 - BALL_SIZE // 2  # Reset the ball position
        ball.y = HEIGHT // 2 - BALL_SIZE // 2

    # Check if player 2 scores
    elif ball.right >= WIDTH:
        player1_score += 1  # Increment player 1 score
        ball_speed = [5, 5]
        # Check if player 1 wins
        if player1_score >= TARGET_SCORE:
            winner_text = font.render("Player 1 Wins!", True, WHITE)  # Render the winning message
            screen.blit(winner_text, (WIDTH // 2 - winner_text.get_width() // 2, HEIGHT // 2))
            pygame.display.flip()  # Update the display
            pygame.time.wait(3000)  # Wait 3 seconds before quitting
            running = False  # Exit the loop
        ball.x = WIDTH // 2 - BALL_SIZE // 2  # Reset the ball position
        ball.y = HEIGHT // 2 - BALL_SIZE // 2

    screen.fill(BLACK)  # Fill the screen with black color
    pygame.draw.rect(screen, player1_paddle_color, player1_paddle)  # Draw player 1 paddle
    pygame.draw.rect(screen, player2_paddle_color, player2_paddle)  # Draw player 2 paddle
    pygame.draw.ellipse(screen, WHITE, ball)  # Draw the ball

    # Render scores
    player1_text = font.render(f"Player 1: {player1_score}", True, WHITE)
    player2_text = font.render(f"Player 2: {player2_score}", True, WHITE)
    screen.blit(player1_text, (20, 20))  # Draw player 1 score
    screen.blit(player2_text, (WIDTH - player2_text.get_width() - 20, 20))  # Draw player 2 score

    # Update display
    pygame.display.flip()

    # Cap the frame rate
    clock.tick(FPS)

pygame.quit()  # Quit Pygame
sys.exit()  # Exit the program

