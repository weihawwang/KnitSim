import os
import pygame
import pygame_gui
import multiprocessing
from stitch import Stitch
from thin_line_grid import run_thin_line_grid  # Import Thin Line Grid

# Initialize Pygame
pygame.init()

# Canvas size for the Stitches Grid + Control Panel window
WINDOW_WIDTH, WINDOW_HEIGHT = 1600, 800  
FONT = pygame.font.SysFont(None, 24)

def create_stitch_grid(rows, cols, stitch_size=5, spacing=20):
    """Creates a 2D grid of Stitch objects with fixed spacing, starting from the top-left at [1,1]."""
    grid = []
    start_x = spacing // 2  # Left-aligned start
    start_y = spacing // 2  # Top-aligned start

    for r in range(rows):  # Loop through rows (top to bottom)
        row_stitches = []
        for c in range(cols):  # Loop through columns (left to right)
            x = start_x + c * spacing  # Left to right columns
            y = start_y + r * spacing  # Top to bottom rows
            row_stitches.append(Stitch(address=[r + 1, c + 1], size=stitch_size, color="black"))
        grid.append(row_stitches)

    return grid, spacing, spacing  # Keep fixed spacing


def run_stitches_grid_and_control(shared_rows, shared_cols, shared_spacing):
    """Creates a unified window containing the Stitches Grid and Control Panel."""
    pygame.display.init()
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("Knitting Simulation - Stitches Grid & Control Panel")
    clock = pygame.time.Clock()
    
    manager = pygame_gui.UIManager((WINDOW_WIDTH, WINDOW_HEIGHT))

    # Create Sliders
    row_slider = pygame_gui.elements.UIHorizontalSlider(
        relative_rect=pygame.Rect((1200, 300), (300, 30)),
        start_value=shared_rows.value,
        value_range=(10, 50),
        manager=manager
    )

    col_slider = pygame_gui.elements.UIHorizontalSlider(
        relative_rect=pygame.Rect((1200, 400), (300, 30)),
        start_value=shared_cols.value,
        value_range=(15, 60),
        manager=manager
    )

    spacing_slider = pygame_gui.elements.UIHorizontalSlider(
        relative_rect=pygame.Rect((1200, 500), (300, 30)),
        start_value=shared_spacing.value,
        value_range=(10, 30),
        manager=manager
    )

    running = True
    hovered_stitch = None

    while running:
        time_delta = clock.tick(60) / 1000.0
        screen.fill((255, 255, 255))  # White background

        # Draw Stitches Grid (left 1200px)
        rows, cols, spacing = shared_rows.value, shared_cols.value, shared_spacing.value
        grid, _, _ = create_stitch_grid(rows, cols, spacing=spacing)

        mouse_x, mouse_y = pygame.mouse.get_pos()
        hovered_stitch = None  # Reset hovered stitch

        for r, row in enumerate(grid):
            for c, stitch in enumerate(row):
                x = c * spacing + spacing // 2  # Stitches Grid at left side
                y = r * spacing + spacing // 2
                pygame.draw.circle(screen, (0, 0, 0), (x, y), stitch.size)

                # 🔥 Check if the mouse is hovering over this stitch 🔥
                if abs(mouse_x - x) < (spacing // 2) and abs(mouse_y - y) < (spacing // 2):
                    hovered_stitch = stitch  # Store hovered stitch

        # 🔥 Display address if hovering over a stitch 🔥
        if hovered_stitch:
            address_text = FONT.render(f"Stitch: {hovered_stitch.address}", True, (0, 0, 0))
            screen.blit(address_text, (mouse_x + 10, mouse_y + 10))

        # Draw Control Panel UI (right 400px)
        manager.update(time_delta)
        manager.draw_ui(screen)

        pygame.display.flip()

        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            manager.process_events(event)

        # Update shared values from sliders
        shared_rows.value = int(row_slider.get_current_value())
        shared_cols.value = int(col_slider.get_current_value())
        shared_spacing.value = int(spacing_slider.get_current_value())

    pygame.quit()

if __name__ == "__main__":
    with multiprocessing.Manager() as manager:
        shared_rows = manager.Value("i", 30)
        shared_cols = manager.Value("i", 30)
        shared_spacing = manager.Value("i", 20)  # Default spacing

        # Start Thin Line Grid in a separate window
        thin_line_process = multiprocessing.Process(target=run_thin_line_grid)
        thin_line_process.start()

        # Run the Stitches Grid & Control Panel in the main process
        run_stitches_grid_and_control(shared_rows, shared_cols, shared_spacing)

        # Wait for Thin Line Grid process to finish
        thin_line_process.join()
