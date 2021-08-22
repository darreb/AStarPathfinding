import time
from grid import *
from style import *
from ui import *


class Simulator:
    def __init__(self, screen):
        self.grid = Grid(NUM_ROWS, NUM_COLS, UNIT_WIDTH, UNIT_HEIGHT)
        self.ui = UI()
        self.style = Style(screen)
        self.screen = screen

        self.cell_state = 0
        # Cell_states: 0 = Start
        #              1 = End

    def set_cell_state(self, cell_state):
        self.cell_state = cell_state
        if self.cell_state == 0:
            self.ui.press_start()
            self.ui.unpress_end()
        elif self.cell_state == 1:
            self.ui.press_end()
            self.ui.unpress_start()

    def set_cell(self, coord):
        if self.cell_state == 0:
            self.grid.set_start_cell(coord)
        elif self.cell_state == 1:
            self.grid.set_end_cell(coord)

    def clear_grid(self):
        self.grid.clear()

    def run(self):
        # Keep Running
        running = True
        while running:
            self.screen.fill(GRAY)  # Default color of screen

            # Draw a rectangle for each cell in cell_arr
            # This gives each cell a display on the screen.
            self.grid.draw(self.screen)

            # Draw buttons in UI
            self.ui.draw(self.screen)

            # Draw the styling
            self.style.draw()

            for event in pygame.event.get():
                if event.type == QUIT:
                    running = False

                # === DON'T FORGET ABOUT CLICK AND DROP ===

                # Left Click
                if pygame.mouse.get_pressed()[0]:
                    pos = pygame.mouse.get_pos()  # Current Mouse position

                    # Check for left click on start button in UI
                    if self.ui.start_but.collidepoint(pos):
                        self.set_cell_state(0)

                    # Check for left click on end button in UI
                    if self.ui.end_but.collidepoint(pos):
                        self.set_cell_state(1)

                    # Check for left click on clear button in UI and clear
                    if self.ui.clear_but.collidepoint(pos):
                        self.clear_grid()
                        # Draw a rectangle for each cell in cell_arr
                        # This gives each cell a display on the screen.
                        for row in self.grid.cell_arr:
                            for cell in row:
                                cell.draw()

                        # Draw buttons in UI
                        self.ui.draw(self.screen)

                    if self.ui.run_but.collidepoint(pos):
                        self.grid.graph.start_path_finding()
                        self.grid.update_cells()
                        self.grid.draw(self.screen)
                        self.grid.update()
                        next_node = self.grid.graph.visit_next()
                        while next_node:
                            coord = next_node.coord
                            cell = self.grid.cell_arr[coord.x][coord.y]
                            time.sleep(0.01)
                            self.grid.update_cells()
                            cell.draw(self.screen)
                            cell.update()
                            next_node = self.grid.graph.visit_next()

                        self.grid.graph.build_path()
                        self.grid.update_cells()

                    # Setting cells in the grid
                    # There can be only one start/end_cell
                    for i in range(NUM_ROWS):
                        for j in range(NUM_COLS):
                            cell = self.grid.cell_arr[i][j]
                            if cell.rect.collidepoint(pos):
                                self.set_cell(Coord(i, j))

                # Right Click
                if pygame.mouse.get_pressed()[2]:
                    pos = pygame.mouse.get_pos()

                    # Check every rect to see if it's being moused over
                    #   And change it to black
                    for i in range(NUM_ROWS):
                        for j in range(NUM_COLS):
                            cell = self.grid.cell_arr[i][j]
                            if cell.rect.collidepoint(pos):
                                self.grid.set_cell_block(Coord(i, j))

            # Update every rect on the display
            self.grid.update()

            # Update each ui element on the display
            self.ui.update()