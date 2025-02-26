import pygame
import pygame_gui
import multiprocessing

class ControlPanel:
    def __init__(self, shared_rows, shared_cols, shared_spacing):
        """Initializes the control panel with shared values."""
        self.shared_rows = shared_rows
        self.shared_cols = shared_cols
        self.shared_spacing = shared_spacing

        # Pygame setup
        pygame.display.init()
        self.screen = pygame.display.set_mode((400, 250))  # Increased height to fit the new slider
        pygame.display.set_caption("Control Panel")
        self.clock = pygame.time.Clock()

        # UI Manager
        self.manager = pygame_gui.UIManager((400, 250))

        # Create sliders for rows, columns, and spacing
        self.row_slider = pygame_gui.elements.UIHorizontalSlider(
            relative_rect=pygame.Rect((20, 50), (300, 30)),
            start_value=shared_rows.value,
            value_range=(10, 50),
            manager=self.manager
        )

        self.col_slider = pygame_gui.elements.UIHorizontalSlider(
            relative_rect=pygame.Rect((20, 100), (300, 30)),
            start_value=shared_cols.value,
            value_range=(15, 60),
            manager=self.manager
        )

        self.spacing_slider = pygame_gui.elements.UIHorizontalSlider(
            relative_rect=pygame.Rect((20, 150), (300, 30)),  # Position the new slider below others
            start_value=shared_spacing.value,
            value_range=(10, 30),  # Range for spacing
            manager=self.manager
        )

    def run(self):
        """Runs the control panel window loop."""
        running = True
        while running:
            time_delta = self.clock.tick(60) / 1000.0
            self.screen.fill((200, 200, 200))  # Gray background

            # Event handling
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False  # Close control panel
                self.manager.process_events(event)

            # Update shared variables
            self.shared_rows.value = int(self.row_slider.get_current_value())
            self.shared_cols.value = int(self.col_slider.get_current_value())
            self.shared_spacing.value = int(self.spacing_slider.get_current_value())  # 🔥 Update spacing dynamically

            # Update UI
            self.manager.update(time_delta)
            self.manager.draw_ui(self.screen)

            pygame.display.flip()

        pygame.quit()
