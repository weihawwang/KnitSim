import os
import pygame
import io
import base64
from PIL import Image
from stitch import Stitch  # Import the Stitch class

# Disable sound and display system for non-GUI environments
os.environ["SDL_AUDIODRIVER"] = "dummy"
os.environ["SDL_VIDEODRIVER"] = "dummy"

# Initialize Pygame
pygame.init()

# Canvas size
WIDTH, HEIGHT = 500, 500

def create_stitch_grid(rows=30, columns=30, stitch_size=5, color="black"):
    """Creates a 2D grid of Stitch objects."""
    grid = []
    row_spacing = HEIGHT // rows
    col_spacing = WIDTH // columns

    for r in range(rows):
        row_stitches = []
        for c in range(columns):
            row_stitches.append(Stitch(address=[r, c], size=stitch_size, color=color))
        grid.append(row_stitches)
    
    return grid, row_spacing, col_spacing  # Return grid and spacing values

def draw_knitting_pattern(rows=30, columns=30):
    """Draws a knitting pattern based on user-selected rows & columns and returns a base64-encoded image."""
    screen = pygame.Surface((WIDTH, HEIGHT))  # Off-screen rendering
    screen.fill((255, 255, 255))  # White background

    # Create grid of Stitch objects
    grid, row_spacing, col_spacing = create_stitch_grid(rows, columns)

    # Draw the knitting grid using Stitch objects
    for r, row in enumerate(grid):
        for c, stitch in enumerate(row):
            x = c * col_spacing + col_spacing // 2
            y = r * row_spacing + row_spacing // 2
            pygame.draw.circle(screen, (0, 0, 0), (x, y), stitch.size)  # Use stitch size

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
