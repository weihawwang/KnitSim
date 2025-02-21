import os
os.environ["SDL_AUDIODRIVER"] = "dummy"  # Disable sound system
os.environ["SDL_VIDEODRIVER"] = "dummy"  # Disable display system

import pygame
import io
import base64
from PIL import Image

# Initialize Pygame
import os
os.environ["SDL_AUDIODRIVER"] = "dummy"  # Disable sound
os.environ["SDL_VIDEODRIVER"] = "dummy"  # Disable display errors in cloud servers
pygame.init()

# Canvas size
WIDTH, HEIGHT = 500, 500

def draw_knitting_pattern(rows=30, columns=30):
    """Draws a knitting pattern based on user-selected rows & columns and returns a base64-encoded image."""
    screen = pygame.Surface((WIDTH, HEIGHT))  # Off-screen rendering
    screen.fill((255, 255, 255))  # White background

    # Calculate spacing based on rows and columns
    row_spacing = HEIGHT // rows
    col_spacing = WIDTH // columns

    # Draw the knitting grid
    for x in range(0, WIDTH, col_spacing):
        for y in range(0, HEIGHT, row_spacing):
            pygame.draw.circle(screen, (0, 0, 0), (x + col_spacing // 2, y + row_spacing // 2), 5)  # Knit points

    # Convert Pygame surface to an image
    img_str = pygame.image.tostring(screen, "RGB")
    img = Image.frombytes("RGB", (WIDTH, HEIGHT), img_str)

    # Convert to base64 for web display
    buffered = io.BytesIO()
    img.save(buffered, format="PNG")
    return base64.b64encode(buffered.getvalue()).decode()

# Test function
if __name__ == "__main__":
    img_data = draw_knitting_pattern(30, 30)  # Default values
    print("Knitting pattern saved with base64 output (truncated):", img_data[:100], "...")
