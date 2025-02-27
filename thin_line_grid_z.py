import pygame
import ast
import math

# Constants
WINDOW_WIDTH, WINDOW_HEIGHT = 800, 800
GRID_MARGIN = 50  # Blank margin around edges
BASE_DOT_SIZE = 5  # Base dot size
MIN_DOT_SIZE = 2  # Smallest possible dot size
MAX_DOT_SIZE = 10  # Largest possible dot size
PERSPECTIVE_FACTOR = 0.05  # Controls how much z shifts the position
BUTTON_WIDTH, BUTTON_HEIGHT = 60, 30  # Button size
DROPDOWN_WIDTH, DROPDOWN_HEIGHT = 150, 30  # Dropdown size

# Colors
BACKGROUND_COLOR = (255, 255, 255)
GRID_COLOR = (200, 200, 200)
LIGHT_GREY = (200, 200, 200)
DARK_GREY = (100, 100, 100)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Read cable pattern library
def load_cable_patterns(filename):
    with open(filename, 'r') as file:
        data = file.read().strip()
    return ast.literal_eval(data)  # Convert string to dictionary

# Compute dot size based on z-value
def compute_dot_size(z, z_enabled):
    if not z_enabled:
        return BASE_DOT_SIZE  # Fixed size when 3D effect is off
    dot_size = BASE_DOT_SIZE * (1 + z / 5)  # Scale by z
    return max(MIN_DOT_SIZE, min(dot_size, MAX_DOT_SIZE))  # Clamp size

# Compute reversed greyscale color based on z-value
def compute_greyscale_color(z, z_enabled):
    if not z_enabled:
        return DARK_GREY  # Fixed grey when 3D effect is off
    brightness = int(255 * ((z + 5) / 10))  # Map z in [-5,5] to [0, 255]
    return (brightness, brightness, brightness)

# Compute perspective-based position shift
def apply_perspective(x, y, z, center_x, center_y, z_enabled):
    if not z_enabled:
        return x, y  # No perspective shift when 3D effect is off
    shift_x = PERSPECTIVE_FACTOR * z * (x - center_x)
    shift_y = PERSPECTIVE_FACTOR * z * (y - center_y)
    return x + shift_x, y + shift_y

class ToggleButton:
    def __init__(self, x, y, width, height, text):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text
        self.active = False

    def draw(self, screen):
        color = DARK_GREY if self.active else LIGHT_GREY
        pygame.draw.rect(screen, color, (self.x, self.y, self.width, self.height))
        font = pygame.font.Font(None, 24)
        text_surf = font.render(self.text, True, WHITE)
        text_rect = text_surf.get_rect(center=(self.x + self.width // 2, self.y + self.height // 2))
        screen.blit(text_surf, text_rect)
    
    def check_click(self, pos):
        if self.x <= pos[0] <= self.x + self.width and self.y <= pos[1] <= self.y + self.height:
            self.active = not self.active
            return True
        return False

class DropdownMenu:
    def __init__(self, x, y, width, height, options):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.options = options
        self.selected_option = options[0]
        self.expanded = False

    def draw(self, screen):
        pygame.draw.rect(screen, LIGHT_GREY, (self.x, self.y, self.width, self.height))
        font = pygame.font.Font(None, 24)
        text_surf = font.render(self.selected_option, True, BLACK)
        text_rect = text_surf.get_rect(center=(self.x + self.width // 2, self.y + self.height // 2))
        screen.blit(text_surf, text_rect)
        
        if self.expanded:
            for i, option in enumerate(self.options):
                rect = pygame.Rect(self.x, self.y + (i + 1) * self.height, self.width, self.height)
                pygame.draw.rect(screen, WHITE, rect)
                text_surf = font.render(option, True, BLACK)
                text_rect = text_surf.get_rect(center=rect.center)
                screen.blit(text_surf, text_rect)

    def check_click(self, pos):
        if pygame.Rect(self.x, self.y, self.width, self.height).collidepoint(pos):
            self.expanded = not self.expanded
            return None
        if self.expanded:
            for i, option in enumerate(self.options):
                rect = pygame.Rect(self.x, self.y + (i + 1) * self.height, self.width, self.height)
                if rect.collidepoint(pos):
                    self.selected_option = option
                    self.expanded = False
                    return option
        self.expanded = False
        return None

# Initialize pygame
pygame.init()
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Thin Line Grid with Depth Effect")

# Load cable patterns
cable_patterns = load_cable_patterns("cable_pattern_lib.txt")
pattern_keys = list(cable_patterns.keys())

# Create UI elements
button_3D = ToggleButton(WINDOW_WIDTH - BUTTON_WIDTH - 10, 10, BUTTON_WIDTH, BUTTON_HEIGHT, "3D")
dropdown_menu = DropdownMenu(10, 10, DROPDOWN_WIDTH, DROPDOWN_HEIGHT, pattern_keys)

# Default pattern selection
selected_pattern_key = pattern_keys[0]
selected_pattern = cable_patterns[selected_pattern_key]

# Compute grid center
center_x = WINDOW_WIDTH // 2
center_y = WINDOW_HEIGHT // 2

running = True
while running:
    screen.fill(BACKGROUND_COLOR)

    # Draw grid with margin
    for x in range(GRID_MARGIN, WINDOW_WIDTH - GRID_MARGIN, 20):
        pygame.draw.line(screen, GRID_COLOR, (x, GRID_MARGIN), (x, WINDOW_HEIGHT - GRID_MARGIN))
    for y in range(GRID_MARGIN, WINDOW_HEIGHT - GRID_MARGIN, 20):
        pygame.draw.line(screen, GRID_COLOR, (GRID_MARGIN, y), (WINDOW_WIDTH - GRID_MARGIN, y))
    
    # Draw UI elements
    button_3D.draw(screen)
    dropdown_menu.draw(screen)
    
    z_enabled = button_3D.active  # Toggle z-value effects
    
    # Extract pattern details
    selected_pattern = cable_patterns[selected_pattern_key]
    color = selected_pattern["color"]
    polylines = selected_pattern["polylines"]
    
    # Draw polylines with lines and dots
    for polyline in polylines:
        point_positions = []  # Store transformed (x, y) points for drawing lines
        
        for x, y, z in polyline:
            screen_x = GRID_MARGIN + x * 20
            screen_y = GRID_MARGIN + y * 20
            screen_x, screen_y = apply_perspective(screen_x, screen_y, z, center_x, center_y, z_enabled)
            dot_size = compute_dot_size(z, z_enabled)
            dot_color = compute_greyscale_color(z, z_enabled)
            point_positions.append((screen_x, screen_y))
            pygame.draw.circle(screen, dot_color, (int(screen_x), int(screen_y)), int(dot_size))
        if len(point_positions) > 1:
            pygame.draw.lines(screen, color, False, point_positions, 1)
    pygame.display.flip()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if button_3D.check_click(event.pos):
                z_enabled = button_3D.active
            selected = dropdown_menu.check_click(event.pos)
            if selected:
                selected_pattern_key = selected
pygame.quit()
