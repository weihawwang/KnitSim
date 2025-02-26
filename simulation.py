import os
import pygame
import multiprocessing
from stitch import Stitch
from control_panel import ControlPanel  # Import the control panel

# Initialize Pygame
pygame.init()

# Canvas sizes
GRID_WIDTH, GRID_HEIGHT = 800, 800
FONT = pygame.font.SysFont(None, 24)

def create_stitch_grid(rows, cols, stitch_size=5, spacing=20):
    """Creates a 2D grid of Stitch objects with fixed spacing, starting from the top-left at [1,1]."""
    grid = []

    # 🔥 Set the top-left starting position
    start_x = spacing // 2  # Left-aligned start
    start_y = spacing // 2  # Top-aligned start

    for r in range(rows):  # Loop through rows (top to bottom)
        row_stitches = []
        for c in range(cols):  # Loop through columns (left to right)
            x = start_x + c * spacing  # Left to right columns
            y = start_y + r * spacing  # Top to bottom rows

            # 🔥 Assign correct stitch address (starting from [1,1])
            row_stitches.append(Stitch(address=[r + 1, c + 1], size=stitch_size, color="black"))

        grid.append(row_stitches)

    return grid, spacing, spacing  # Keep fixed spacing




def draw_knitting_pattern(shared_rows, shared_cols, shared_spacing):
    """Runs the knitting grid display window and updates when shared values change."""
    pygame.display.init()
    screen = pygame.display.set_mode((GRID_WIDTH, GRID_HEIGHT))
    pygame.display.set_caption("Knitting Grid")
    clock = pygame.time.Clock()

    running = True
    hovered_stitch = None
    rows, cols = shared_rows.value, shared_cols.value
    spacing = shared_spacing.value  # 🔥 Get initial spacing value
    grid, row_spacing, col_spacing = create_stitch_grid(rows, cols, spacing=spacing)

    while running:
        time_delta = clock.tick(60) / 1000.0
        screen.fill((255, 255, 255))  # White background

        # Check if rows, cols, or spacing have changed
        if (rows != shared_rows.value or cols != shared_cols.value or spacing != shared_spacing.value):
            rows, cols = shared_rows.value, shared_cols.value
            spacing = shared_spacing.value  # 🔥 Update spacing dynamically
            grid, row_spacing, col_spacing = create_stitch_grid(rows, cols, spacing=spacing)

        # Get mouse position
        mouse_x, mouse_y = pygame.mouse.get_pos()
        hovered_stitch = None  # Reset hovered stitch

        # Draw the knitting grid using Stitch objects
        for r, row in enumerate(grid):
            for c, stitch in enumerate(row):
                x = c * col_spacing + col_spacing // 2
                y = r * row_spacing + row_spacing // 2
                pygame.draw.circle(screen, (0, 0, 0), (x, y), stitch.size)  # Draw stitch

                # Check if the mouse is hovering over this stitch
                if abs(mouse_x - x) < (col_spacing // 2) and abs(mouse_y - y) < (row_spacing // 2):
                    hovered_stitch = stitch  # Store hovered stitch

        # Display address if hovering over a stitch
        if hovered_stitch:
            address_text = FONT.render(f"Stitch: {hovered_stitch.address}", True, (0, 0, 0))
            screen.blit(address_text, (mouse_x + 10, mouse_y + 10))

        pygame.display.flip()

        # Handle Pygame events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False  # Exit loop if window is closed

    pygame.quit()

if __name__ == "__main__":
    with multiprocessing.Manager() as manager:
        # Shared values between processes
        shared_rows = manager.Value("i", 30)
        shared_cols = manager.Value("i", 30)
        shared_spacing = manager.Value("i", 20)  # 🔥 Default spacing set to 20 pixels

        # Start the knitting grid display process
        grid_process = multiprocessing.Process(target=draw_knitting_pattern, args=(shared_rows, shared_cols, shared_spacing))
        grid_process.start()

        # Run the control panel in the main process
        control_panel = ControlPanel(shared_rows, shared_cols, shared_spacing)
        control_panel.run()

        # Wait for grid display process to finish
        grid_process.join()
