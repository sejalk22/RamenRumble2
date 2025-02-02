import pygame
import os

def run_ending_scene():
    pygame.init()

    # Screen settings
    WIDTH, HEIGHT = 800, 600
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("RamenRumble - Ending Scene")

    # Colors
    CREAM = (255, 243, 224)  # Background
    TEXTBOX_COLOR = (50, 50, 50)  # Darker textbox background
    TEXT_COLOR = (255, 255, 255)  # White text
    BUTTON_COLOR = (80, 80, 80)  # Button background
    BUTTON_BORDER = (255, 255, 255)  # White border
    ARROW_COLOR = (255, 255, 255)  # White arrow

    # Image size
    SQUARE_SIZE = 350

    # Function to load and crop images
    def load_and_crop_image(path, size):
        """Loads an image and crops it to a square."""
        img = pygame.image.load(path)
        width, height = img.get_size()
        min_dim = min(width, height)  # Find the smallest dimension
        crop_rect = pygame.Rect((width - min_dim) // 2, (height - min_dim) // 2, min_dim, min_dim)
        img = img.subsurface(crop_rect)  # Crop to square
        return pygame.transform.scale(img, (size, size))  # Resize

    # Load images from endingScene folder
    BASE_PATH = os.path.dirname(os.path.abspath(__file__))
    images = [
        load_and_crop_image(os.path.join(BASE_PATH, "End1.jpeg"), SQUARE_SIZE),
        load_and_crop_image(os.path.join(BASE_PATH, "End2.jpeg"), SQUARE_SIZE),
        load_and_crop_image(os.path.join(BASE_PATH, "End3.jpeg"), SQUARE_SIZE),
        load_and_crop_image(os.path.join(BASE_PATH, "End4.jpeg"), SQUARE_SIZE)
    ]

    # Built-in font for captions
    font = pygame.font.Font(None, 28)

    # Scene captions
    captions = [
        "Soup has now become RAMEN!!",
        "The world celebrates the return of ramen",
        "The chef tries to win the ramen back, but fails",
        "The story of Soup has ended... for now."
    ]

    current_slide = 0
    running = True

    def draw_arrow_button(screen, x, y, size=50):
        """Draws a button around the right-facing arrow."""
        button_rect = pygame.Rect(x - size // 2, y - size // 2, size, size)
        pygame.draw.rect(screen, BUTTON_COLOR, button_rect, border_radius=10)  # Button background
        pygame.draw.rect(screen, BUTTON_BORDER, button_rect, 3, border_radius=10)  # Button border

        # Draw arrow inside the button
        arrow_points = [
            (x - 10, y - 15),
            (x + 10, y),
            (x - 10, y + 15)
        ]
        pygame.draw.polygon(screen, ARROW_COLOR, arrow_points)

        return button_rect  # Return rect for collision detection

    while running:
        screen.fill(CREAM)  # Set background color

        # Display current image centered
        image_x = (WIDTH - SQUARE_SIZE) // 2
        image_y = 100
        screen.blit(images[current_slide], (image_x, image_y))

        # Draw caption textbox if there is text
        if captions[current_slide]:
            textbox_width = WIDTH - 150
            textbox_height = 60
            textbox_x = (WIDTH - textbox_width) // 2
            textbox_y = HEIGHT - 100

            textbox_rect = pygame.Rect(textbox_x, textbox_y, textbox_width, textbox_height)
            pygame.draw.rect(screen, TEXTBOX_COLOR, textbox_rect, border_radius=15)

            # Render centered text
            text_surface = font.render(captions[current_slide], True, TEXT_COLOR)
            text_rect = text_surface.get_rect(center=textbox_rect.center)
            screen.blit(text_surface, text_rect)

        # Draw the button-styled arrow inside the textbox on the right
        arrow_x = textbox_x + textbox_width - 40
        arrow_y = textbox_y + textbox_height // 2
        arrow_button_rect = draw_arrow_button(screen, arrow_x, arrow_y, 40)

        pygame.display.flip()

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key in (pygame.K_RIGHT, pygame.K_SPACE):
                    if current_slide < len(images) - 1:
                        current_slide += 1  # Go to next scene
                    else:
                        running = False  # Exit when the last slide is reached
                elif event.key == pygame.K_LEFT:
                    if current_slide > 0:
                        current_slide -= 1  # Go back
            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                if arrow_button_rect.collidepoint(x, y):
                    if current_slide < len(images) - 1:
                        current_slide += 1  # Click right arrow to go forward
                    else:
                        running = False  # Exit when the last slide is reached

    pygame.quit()

if __name__ == "__main__":
    run_ending_scene()
