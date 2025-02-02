import pygame

def run_opening_scene():
    pygame.init()

    # Screen settings
    WIDTH, HEIGHT = 800, 600
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("RamenRumble - Opening Scene")

    # Colors
    CREAM = (255, 243, 224)  # Nice cream background
    TEXTBOX_COLOR = (50, 50, 50)  # Darker textbox background
    TEXT_COLOR = (255, 255, 255)  # White text
    BUTTON_COLOR = (80, 80, 80)  # Button background
    BUTTON_BORDER = (255, 255, 255)  # White border
    ARROW_COLOR = (255, 255, 255)  # White arrow

    # Desired square size for images
    SQUARE_SIZE = 350  # Set all images to 350x350

    def load_and_crop_image(path, size):
        try:
            img = pygame.image.load(path)
            width, height = img.get_size()
            
            # Instead of cropping, just scale the image directly
            img = pygame.transform.scale(img, (size, size))  

            return img
        except Exception as e:
            print(f"ERROR: Failed to load image {path} - {e}")
            return pygame.Surface((size, size))  # Return a blank surface if loading fails

    # Load and crop images from openingScene folder
    images = [
        load_and_crop_image("openingScene/Op1.jpeg", SQUARE_SIZE),
        load_and_crop_image("openingScene/Op2.jpeg", SQUARE_SIZE),
        load_and_crop_image("openingScene/Op3.jpeg", SQUARE_SIZE),
        load_and_crop_image("openingScene/Op4.jpeg", SQUARE_SIZE),
        load_and_crop_image("openingScene/Op5.jpeg", SQUARE_SIZE),
        load_and_crop_image("openingScene/Op6.jpeg", SQUARE_SIZE)
    ]

    # Built-in font (small size for pixel-like look)
    font = pygame.font.Font(None, 28)

    # Scene captions
    captions = [
        "No one is ordering Soup!",  # Scene 1
        "",  # Scene 2 (No caption)
        "",  # Scene 3 (No caption)
        "The Chef starts serving burgers and fries instead",  # Scene 4
        "",  # Scene 5 (No caption)
        "Soup feels betrayed and swears VENGEANCE!"  # Scene 6
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
            (x - 10, y - 15),  # Top-left of arrow
            (x + 10, y),  # Arrow tip
            (x - 10, y + 15)  # Bottom-left of arrow
        ]
        pygame.draw.polygon(screen, ARROW_COLOR, arrow_points)

        return button_rect  # Return rect for collision detection

    while running:
        screen.fill(CREAM)  # Set background color

        # Display current square image centered
        image_x = (WIDTH - SQUARE_SIZE) // 2
        image_y = 100
        screen.blit(images[current_slide], (image_x, image_y))

        # Draw caption textbox only if there is text
        if captions[current_slide]:
            textbox_width = WIDTH - 150
            textbox_height = 60
            textbox_x = (WIDTH - textbox_width) // 2  # Center horizontally
            textbox_y = HEIGHT - 100  # Position at bottom

            textbox_rect = pygame.Rect(textbox_x, textbox_y, textbox_width, textbox_height)
            pygame.draw.rect(screen, TEXTBOX_COLOR, textbox_rect, border_radius=15)

            # Render centered text
            text_surface = font.render(captions[current_slide], True, TEXT_COLOR)
            text_rect = text_surface.get_rect(center=textbox_rect.center)  # Center text inside textbox
            screen.blit(text_surface, text_rect)

        # Draw the button-styled arrow **inside** the textbox on the right
        arrow_x = textbox_x + textbox_width - 40  # Align arrow inside the textbox
        arrow_y = textbox_y + textbox_height // 2  # Center vertically in the textbox
        arrow_button_rect = draw_arrow_button(screen, arrow_x, arrow_y, 40)

        pygame.display.flip()

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key in (pygame.K_RIGHT, pygame.K_SPACE):  # Right arrow or space bar
                    if current_slide < len(images) - 1:
                        current_slide += 1  # Go to next scene
                elif event.key == pygame.K_LEFT:  # Left arrow
                    if current_slide > 0:
                        current_slide -= 1  # Go back
            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                if arrow_button_rect.collidepoint(x, y):
                    if current_slide < len(images) - 1:
                        current_slide += 1  # Go to the next scene
                    else:
                        running = False  # Exit the loop when the last slide is reached

    pygame.quit()

if __name__ == "__main__":
    run_opening_scene()
