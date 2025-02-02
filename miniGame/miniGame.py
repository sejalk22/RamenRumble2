import pygame
import random
import os
import time

def run_mini_game():

    # Initialize pygame
    pygame.init()

    # Constants
    WIDTH, HEIGHT = 800, 900
    GRID_SIZE = 60
    ROWS, COLS = 13, 13  # Ensuring a path exists
    FPS = 30
    ENEMY_MOVE_DELAY = 10  # Slow down enemy movement

    # Colors
    CREAM = (255, 243, 224)
    DARK_BROWN = (80, 40, 20)
    BORDER_COLOR = (50, 25, 10)
    TAN = (210, 180, 140)
    TEXT_COLOR = (0, 0, 0)

    # Load images
    BASE_PATH = os.path.dirname(os.path.abspath(__file__))  # Get current file's directory
    soup_img = pygame.image.load(os.path.join(BASE_PATH, "soup.png"))
    burger1_img = pygame.image.load(os.path.join(BASE_PATH, "burger1.png"))
    burger2_img = pygame.image.load(os.path.join(BASE_PATH, "burger2.png"))
    noodles_img = pygame.image.load(os.path.join(BASE_PATH, "noodles.png"))


    # Scale images
    IMG_SIZE = (GRID_SIZE, GRID_SIZE)
    soup_img = pygame.transform.scale(soup_img, IMG_SIZE)
    burger1_img = pygame.transform.scale(burger1_img, IMG_SIZE)
    burger2_img = pygame.transform.scale(burger2_img, IMG_SIZE)
    noodles_img = pygame.transform.scale(noodles_img, IMG_SIZE)

    # Setup screen
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Guide Soup to the Noodles!")

    # Maze position
    MAZE_OFFSET_Y = 100
    MAZE_OFFSET_X = (WIDTH - (COLS * GRID_SIZE)) // 2

    # Function to generate a maze with a guaranteed path
    def generate_maze(rows, cols):
        maze = [[1 for _ in range(cols)] for _ in range(rows)]
        stack = [(1, 1)]
        visited = {(1, 1)}

        while stack:
            x, y = stack[-1]
            maze[y][x] = 0
            neighbors = []
            for dx, dy in [(0, -2), (0, 2), (-2, 0), (2, 0)]:
                nx, ny = x + dx, y + dy
                if 1 <= nx < cols - 1 and 1 <= ny < rows - 1 and (nx, ny) not in visited:
                    neighbors.append((nx, ny))
            if neighbors:
                nx, ny = random.choice(neighbors)
                maze[(ny + y) // 2][(nx + x) // 2] = 0
                stack.append((nx, ny))
                visited.add((nx, ny))
            else:
                stack.pop()
        return maze

    maze = generate_maze(ROWS, COLS)

    # Ensure a valid path to the goal
    player_x, player_y = 1, 1
    goal_x, goal_y = COLS - 2, ROWS - 2
    maze[goal_y][goal_x] = 0

    # Enemies at open paths
    enemies = []
    for _ in range(2):
        while True:
            ex, ey = random.randint(1, COLS-2), random.randint(1, ROWS-2)
            if maze[ey][ex] == 0 and (ex, ey) != (player_x, player_y) and (ex, ey) != (goal_x, goal_y):
                enemies.append([ex, ey, random.choice([(1, 0), (-1, 0), (0, 1), (0, -1)])])
                break

    directions = {
        pygame.K_UP: (0, -1),
        pygame.K_DOWN: (0, 1),
        pygame.K_LEFT: (-1, 0),
        pygame.K_RIGHT: (1, 0)
    }

    enemy_move_counter = 0

    # Game loop
    running = True
    clock = pygame.time.Clock()
    while running:
        screen.fill(CREAM)

        # Draw text
        font = pygame.font.Font(None, 50)
        text_surface = font.render("Guide Soup to the Noodles!", True, TEXT_COLOR)
        text_rect = text_surface.get_rect(center=(WIDTH // 2, 50))
        pygame.draw.rect(screen, TAN, text_rect.inflate(40, 20), border_radius=15)
        pygame.draw.rect(screen, TEXT_COLOR, text_rect.inflate(40, 20), 3, border_radius=15)
        screen.blit(text_surface, text_rect)

        # Draw maze
        for y in range(ROWS):
            for x in range(COLS):
                if maze[y][x] == 1:
                    pygame.draw.rect(screen, DARK_BROWN, (x * GRID_SIZE + MAZE_OFFSET_X, y * GRID_SIZE + MAZE_OFFSET_Y, GRID_SIZE, GRID_SIZE))

        # Draw elements
        screen.blit(soup_img, (player_x * GRID_SIZE + MAZE_OFFSET_X, player_y * GRID_SIZE + MAZE_OFFSET_Y))
        screen.blit(noodles_img, (goal_x * GRID_SIZE + MAZE_OFFSET_X, goal_y * GRID_SIZE + MAZE_OFFSET_Y))
        for enemy in enemies:
            screen.blit(burger1_img if enemy == enemies[0] else burger2_img, (enemy[0] * GRID_SIZE + MAZE_OFFSET_X, enemy[1] * GRID_SIZE + MAZE_OFFSET_Y))
        
        pygame.display.flip()
        
        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key in directions:
                    dx, dy = directions[event.key]
                    new_x, new_y = player_x + dx, player_y + dy
                    if maze[new_y][new_x] == 0:
                        player_x, player_y = new_x, new_y

        # Move enemies every few frames
        if enemy_move_counter % ENEMY_MOVE_DELAY == 0:
            for enemy in enemies:
                ex, ey, (dx, dy) = enemy
                new_ex, new_ey = ex + dx, ey + dy
                if 1 <= new_ex < COLS - 1 and 1 <= new_ey < ROWS - 1 and maze[new_ey][new_ex] == 0:
                    enemy[0], enemy[1] = new_ex, new_ey
                else:
                    enemy[2] = random.choice([(1, 0), (-1, 0), (0, 1), (0, -1)])
                
                # Restart if player collides with an enemy
                if (player_x, player_y) == (enemy[0], enemy[1]):
                    print("You were caught by a burger! Restarting...")
                    player_x, player_y = 1, 1

        enemy_move_counter += 1

        # Check if player reaches goal
        if (player_x, player_y) == (goal_x, goal_y):
            print("You reached the noodles! Congratulations!")
            running = False

        clock.tick(FPS)

    pygame.quit()

if __name__ == "__main__":
    run_mini_game()