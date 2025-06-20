import pygame
import random
from random import randint
import time

# Initialize game
pygame.init()

# Game display
SCREEN_WIDTH = 1366
SCREEN_HEIGHT = 768
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Dynamic Snakes and Ladders")

# Constant
TILE_SIZE = 60  

#----Colors-----
BLACK = (10, 10, 10)  # Font
WHITE = (250, 250, 250)  # Text backgrounds and boxes
RED = (200, 0, 0)  # Snakes
BROWN = (139, 69, 19)  # Ladders
YELLOW = (150, 150, 0)  # Winner

# Clock
clock = pygame.time.Clock()

#------Background-----
start_background = pygame.image.load("images/background.png")
start_background = pygame.transform.scale(start_background, (SCREEN_WIDTH, SCREEN_HEIGHT))
main_background = pygame.image.load("images/mainbg.png")
main_background = pygame.transform.scale(main_background, (SCREEN_WIDTH, SCREEN_HEIGHT))

#----Game Buttons ---
start_button = pygame.image.load("images/startgame.png")
start_button = pygame.transform.scale(start_button, (400, 200))
start_rect = start_button.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 + 50))

quitmain_button = pygame.image.load("images/quitgame.png")
quitmain_button = pygame.transform.scale(quitmain_button, (400, 200))
quit_rect = quitmain_button.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 + 150))

restart_button = pygame.image.load("images/restartgame.png")
restart_button = pygame.transform.scale(restart_button, (200, 80))
restart_rect = pygame.Rect(SCREEN_WIDTH - 350, 50, 200, 80)

quitgame_button = pygame.image.load("images/quitgame.png")
quitgame_button = pygame.transform.scale(quitgame_button, (200, 80))
quitgame_rect = pygame.Rect(SCREEN_WIDTH - 350, 150, 200, 80)

rolldice_button = pygame.image.load("images/rolldice.png")
rolldice_button = pygame.transform.scale(rolldice_button, (200, 80))
rolldice_rect = pygame.Rect(50, SCREEN_HEIGHT - 150, 200, 80)

#----Players----
human_player = pygame.image.load("images/player.png")
human_player = pygame.transform.scale(human_player, (40, 40))
ai_player = pygame.image.load("images/ai.png")
ai_player = pygame.transform.scale(ai_player, (40, 40))

#----Dice------
dice_images = [pygame.image.load(f"images/dice_image{i}.png") for i in range(1, 7)]
dice_images = [pygame.transform.scale(img, (100, 100)) for img in dice_images]

# Tile colors
tile_palette = [
    (255, 102, 102), (255, 255, 255), (255, 255, 153),
    (153, 204, 255), (153, 255, 153)
]
tile_colors = []
for row in range(10):
    tile_colors.append([])
    for col in range(10):
        left_color = tile_colors[row][col - 1] if col > 0 else None
        top_color = tile_colors[row - 1][col] if row > 0 else None
        available_colors = [c for c in tile_palette if c != left_color and c != top_color]
        tile_colors[row].append(random.choice(available_colors))

# To Display Text Message
def display_message(text, x, y, color):
    font = pygame.font.SysFont("comicsansms", 24)
    screen_text = font.render(text, True, color)
    background_rect = pygame.Rect(x - 10, y - 10, screen_text.get_width() + 20, screen_text.get_height() + 20)

    pygame.draw.rect(screen, WHITE, background_rect)
    screen.blit(screen_text, (x, y))

#Draw Controll Buttons on the Game Screen
def draw_control_buttons():
    screen.blit(restart_button, restart_rect)
    screen.blit(quitgame_button, quitgame_rect)
    screen.blit(rolldice_button, rolldice_rect)

#To Calculate Center Position of a Tile
def center_tile_position(position):
    base_x = (SCREEN_WIDTH - TILE_SIZE * 10) // 2 - 30
    base_y = (SCREEN_HEIGHT - TILE_SIZE * 10) // 2 + 9 * TILE_SIZE - 30

    if position == 0:  
        return base_x, base_y 

    row = (position - 1) // 10
    col = (position - 1) % 10

    if row % 2 == 0:
        x = base_x + col * TILE_SIZE
    else:
        x = base_x + (9 - col) * TILE_SIZE

    y = base_y - row * TILE_SIZE
    return x + 10, y + 10

#To Generate random snakes and ladders
def generate_snakes_ladders():
    snakes = {}
    ladders = {}
    # Generate 5 snakes
    while len(snakes) < 5:
        head = random.randint(11, 99)
        tail = random.randint(1, head - 10)
        if head not in snakes and head not in ladders:
            snakes[head] = tail
            
    # Generate 5 ladders
    while len(ladders) < 5:
        bottom = random.randint(1, 89)
        top = random.randint(bottom + 10, 99)
        if bottom not in ladders and bottom not in snakes:
            ladders[bottom] = top
            
    return snakes, ladders

#To draw a 10x10 game board 
def draw_board():
    BOARD_SIZE = 10
    origin_x = (SCREEN_WIDTH - BOARD_SIZE * TILE_SIZE) // 2 - 30
    origin_y = (SCREEN_HEIGHT - BOARD_SIZE * TILE_SIZE) // 2 - 30
    
    for row in range(BOARD_SIZE):
        for col in range(BOARD_SIZE):
            actual_col = col if row % 2 == 0 else 9 - col
            tile_num = row * 10 + actual_col + 1

            x1 = origin_x + col * TILE_SIZE
            y1 = origin_y + (9 - row) * TILE_SIZE

            color = tile_colors[row][actual_col]
            pygame.draw.rect(screen, color, (x1, y1, TILE_SIZE, TILE_SIZE))
            pygame.draw.rect(screen, BLACK, (x1, y1, TILE_SIZE, TILE_SIZE), 1)

            num_text = pygame.font.SysFont("arial", 14).render(str(tile_num), True, BLACK)
            screen.blit(num_text, (x1 + 5, y1 + 5))

#To Draw the snakes and ladders           
def draw_snakes_ladders(snakes, ladders):
    # Draw Snakes 
    for head, tail in snakes.items():
        start_pos = center_tile_position(head)
        end_pos = center_tile_position(tail)
        # Snake Tail 
        pygame.draw.line(screen, RED, start_pos, end_pos, 5)
        # Snake Head 
        pygame.draw.circle(screen, RED, start_pos, 8)
    
    #Draw Ladders
    for bottom, top in ladders.items():
        start_pos = center_tile_position(bottom)
        end_pos = center_tile_position(top)
        offset = 6 # Space Between two ladder lines
        pygame.draw.line(screen, BROWN, (start_pos[0]-offset, start_pos[1]), (end_pos[0]-offset, end_pos[1]), 3)
        pygame.draw.line(screen, BROWN, (start_pos[0]+offset, start_pos[1]), (end_pos[0]+offset, end_pos[1]), 3)

#To display current dice roll 
def display_dice(value):
    screen.blit(dice_images[value - 1], (250, 600))
    pygame.display.update()

#Players turns w/ dice roll
def turn(score, ladders, snakes, dice_roll):
    ladder = False
    snake = False
    new_score = score + dice_roll
    
    # Automatic win for each roll that exceeds 100
    if new_score >= 100:
        return 100, ladder, snake 
    
    score = new_score
    if score in ladders:
        score = ladders[score]
        ladder = True
    elif score in snakes:
        score = snakes[score]
        snake = True
    
    return score, ladder, snake

def expectiminimax(position, depth, is_maximizing, snakes, ladders):
    if depth == 0 or position >= 100:
        return position

    if is_maximizing:
        return max(expectiminimax(position + i, depth - 1, False, snakes, ladders) for i in range(1, 7))
    else:
        values = []
        for i in range(1, 7):
            new_pos = position + i
            if new_pos in snakes:
                new_pos = snakes[new_pos]
            elif new_pos in ladders:
                new_pos = ladders[new_pos]
            values.append(expectiminimax(new_pos, depth - 1, True, snakes, ladders))
        return sum(values) / len(values)

def expectiminimax_decision(position, snakes, ladders):
    best_value = -float('inf')
    best_move = 1
    # Evaluate all possible dice rolls 
    for dice in range(1, 7):
        next_pos = position + dice
        
        if next_pos in snakes:
            next_pos = snakes[next_pos]
        elif next_pos in ladders:
            next_pos = ladders[next_pos]
        value = expectiminimax(next_pos, 1, False, snakes, ladders)
        # Choose Best Move
        if value > best_value:
            best_value = value
            best_move = dice
    return best_move

# Quit Game
def quit_game():
    pygame.quit()
    quit()

# Display Menu Screen
def main_menu():
    while True:
        screen.blit(start_background, (0, 0))
        screen.blit(start_button, start_rect)
        screen.blit(quitmain_button, quit_rect)
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit_game()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                quit_game()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if start_rect.collidepoint(mouse_pos):
                    playing() # Start Game
                elif quit_rect.collidepoint(mouse_pos):
                    quit_game() # Quit Game 

def playing():
    human_score = 0
    ai_score = 0
    snakes, ladders = generate_snakes_ladders()
    turn_count = 0
    game_over = False 

    while True:
        # Game Screen
        screen.blit(main_background, (0, 0))
        draw_board()
        draw_snakes_ladders(snakes, ladders)
        draw_control_buttons()
        
        # Player Tokens
        x_human, y_human = center_tile_position(human_score)
        x_ai, y_ai = center_tile_position(ai_score)
        screen.blit(human_player, (x_human, y_human))
        screen.blit(ai_player, (x_ai, y_ai))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit_game()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                quit_game()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if restart_rect.collidepoint(mouse_pos):
                    playing() # Restart Game
                    return
                elif quitgame_rect.collidepoint(mouse_pos):
                    quit_game() # Quit Game
                elif rolldice_rect.collidepoint(mouse_pos) and not game_over:
                    # Human Player Turn
                    dice_value = randint(1, 6)
                    display_dice(dice_value)
                    pygame.time.wait(500)
                    
                    human_score, ladder, snake = turn(human_score, ladders, snakes, dice_value)
                    
                    # Redraw final position
                    screen.blit(main_background, (0, 0))
                    draw_board()
                    draw_snakes_ladders(snakes, ladders)
                    draw_control_buttons()
                    screen.blit(human_player, center_tile_position(human_score))
                    screen.blit(ai_player, center_tile_position(ai_score))
                    
                    # Display messages
                    if ladder:
                        display_message("You Climbed a Ladder!", 560, 680, BLACK)
                    elif snake:
                        display_message("You Got Bitten by a Snake!", 560, 680, BLACK)
                    
                    pygame.display.update()
                    pygame.time.wait(1500)

                    # Check for human win
                    if human_score == 100:
                        display_message("You Win!!", 560, 680, YELLOW)
                        pygame.display.update()
                        game_over = True
                        pygame.time.wait(3000)
                        break

                    # AI Player Turn
                    screen.blit(main_background, (0, 0))
                    draw_board()
                    draw_snakes_ladders(snakes, ladders)
                    draw_control_buttons()
                    screen.blit(human_player, center_tile_position(human_score))
                    screen.blit(ai_player, center_tile_position(ai_score))
                    display_message("AI Turn to Roll Dice...", 560, 680, BLACK)
                    pygame.display.update()
                    pygame.time.wait(2500)

                    # AI decision
                    dice_value = expectiminimax_decision(ai_score, snakes, ladders)
                    display_dice(dice_value)
                    pygame.time.wait(1000)
                    
                    ai_score, ladder, snake = turn(ai_score, ladders, snakes, dice_value)
                    
                    # Redraw final position
                    screen.blit(main_background, (0, 0))
                    draw_board()
                    draw_snakes_ladders(snakes, ladders)
                    draw_control_buttons()
                    screen.blit(human_player, center_tile_position(human_score))
                    screen.blit(ai_player, center_tile_position(ai_score))
                    
                    # Display messages
                    if ladder:
                        display_message("AI Climbed a Ladder!", 560, 680, BLACK)
                    elif snake:
                        display_message("AI Got Bitten by a Snake!", 560, 680, BLACK)

                    pygame.display.update()
                    pygame.time.wait(1500)

                    # Check for AI win
                    if ai_score == 100:
                        display_message("AI Wins!", 560, 680, YELLOW)
                        pygame.display.update()
                        game_over = True
                        pygame.time.wait(3000)
                        break

                    # Board Shuffling every 2 turns 
                    turn_count += 1
                    if turn_count >= 2: 
                        display_message("Board is Shuffling!!", 560, 680, BLACK)
                        snakes, ladders = generate_snakes_ladders()
                        turn_count = 0
                        pygame.display.update()
                        pygame.time.wait(1500)

        # Restart game if Game over
        if game_over:
            display_message("Click Restart to play again", 560, 680, BLACK)
            pygame.display.update()

        pygame.display.update()
        clock.tick(10)

if __name__ == "__main__":
    main_menu()