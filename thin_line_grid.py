import pygame
import os
import re

INPUT_FILE = "input.txt"

class PolylineSet:
    """Represents a collection of polylines with a name and display color."""
    
    def __init__(self, name, display_colour=(0, 0, 255)):  # Default color: Blue
        self.name = name
        self.display_colour = display_colour
        self.polylines = []  # Stores multiple polylines as lists of (x, y) points

    def add_polylines(self, polylines):
        """Adds multiple polylines to the set."""
        self.polylines.extend(polylines)  # Ensure all polylines are stored

    def __repr__(self):
        return f"PolylineSet(name={self.name}, colour={self.display_colour}, polylines={len(self.polylines)} polylines)"

def parse_input_file():
    """Reads and parses the input file for multiple polyline sets with multiple polylines."""
    polyline_sets = []

    if not os.path.exists(INPUT_FILE):
        print("❌ input.txt not found!")
        return polyline_sets

    with open(INPUT_FILE, "r", encoding="utf-8") as file:
        content = file.read().strip()

    content = re.sub(r'\s+', ' ', content).strip()

    matches = re.findall(r'polyline_set\["(.*?)",\s*\((\d+),(\d+),(\d+)\)\]\s*=\s*(\[\s*\[.*?\]\s*\])', content, re.DOTALL)

    if not matches:
        print("❌ No matching polyline sets found!")
        return polyline_sets

    for match in matches:
        name = match[0]
        color = (int(match[1]), int(match[2]), int(match[3]))
        polylines_str = match[4]

        try:
            raw_polyline_groups = re.findall(r'\[\s*\((.*?)\)\s*\]', polylines_str)
            polylines = []
            for group in raw_polyline_groups:
                points = []
                point_pairs = group.split("), (")
                for pair in point_pairs:
                    clean_pair = pair.replace("(", "").replace(")", "").strip()
                    coords = clean_pair.split(",")
                    if len(coords) == 2:
                        x, y = map(int, coords)
                        points.append((x, y))
                if points:
                    polylines.append(points)

            polyline_set = PolylineSet(name, display_colour=color)
            polyline_set.add_polylines(polylines)
            polyline_sets.append(polyline_set)
        except Exception as e:
            print(f"❌ Error parsing polyline set: {e}")
    
    return polyline_sets

def run_thin_line_grid():
    print("✅ run_thin_line_grid() function is running!")
    pygame.init()
    pygame.font.init()
    screen = pygame.display.set_mode((800, 800))
    pygame.display.set_caption("Thin Line Grid - Multiple Polylines per Set")
    clock = pygame.time.Clock()
    font = pygame.font.SysFont(None, 24)

    print("✅ Calling parse_input_file() to load polylines...")
    polyline_sets = parse_input_file()
    print(f"✅ Loaded {len(polyline_sets)} polyline sets")

    last_modified_time = os.path.getmtime(INPUT_FILE) if os.path.exists(INPUT_FILE) else 0
    last_printed_time = None

    running = True
    while running:
        screen.fill((255, 255, 255))
        
        for x in range(0, 800, 20):
            pygame.draw.line(screen, (200, 200, 200), (x, 0), (x, 800), 1)
        for y in range(0, 800, 20):
            pygame.draw.line(screen, (200, 200, 200), (0, y), (800, y), 1)

        if os.path.exists(INPUT_FILE):
            modified_time = os.path.getmtime(INPUT_FILE)
            if modified_time != last_modified_time:
                last_modified_time = modified_time
                polyline_sets = parse_input_file()
                last_printed_time = None

        if last_printed_time != last_modified_time:
            last_printed_time = last_modified_time

        for polyline_set in polyline_sets:
            for polyline in polyline_set.polylines:
                if len(polyline) > 1:
                    scaled_points = [(x * 20, y * 20) for x, y in polyline]
                    pygame.draw.lines(screen, polyline_set.display_colour, False, scaled_points, 2)

        mouse_x, mouse_y = pygame.mouse.get_pos()
        grid_x = round(mouse_x / 20, 2)
        grid_y = round(mouse_y / 20, 2)
        coord_text = font.render(f"X: {grid_x}, Y: {grid_y}", True, (0, 0, 0))
        screen.blit(coord_text, (10, 780))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    print("🔥 thin_line_grid.py script is running!")
    print("🔥 Starting Thin Line Grid Window...")
    run_thin_line_grid()
