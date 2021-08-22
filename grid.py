from pathfinding import *
from constants import *
import pygame
from pygame.locals import *


class Cell:
    def __init__(self, _rect, _color):
        self.rect = _rect
        self.color = _color

    def to_black(self):
        self.color = BLACK

    def to_white(self):
        self.color = WHITE

    def to_purple(self):
        self.color = PURPLE

    def to_green(self):
        self.color = GREEN

    def to_blue(self):
        self.color = BLUE

    def to_yellow(self):
        self.color = YELLOW

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)

    def update(self):
        pygame.display.update(self.rect)


class Grid:
    def __init__(self, rows, cols, unit_width, unit_height):
        self.rows = rows
        self.cols = cols
        self.unit_width = unit_width
        self.unit_height = unit_height

        # Default values for cells
        self.start_cell = Cell(Rect(0, 0, 0, 0), WHITE)
        self.end_cell = Cell(Rect(0, 0, 0, 0), WHITE)

        self.cell_arr = []
        # init cells
        for i in range(self.rows):
            cell_row = []
            for j in range(self.cols):
                rect = Rect(i * unit_width, j * unit_height + 100, unit_width, unit_height)
                cell_row.append(Cell(rect, WHITE))
            self.cell_arr.append(cell_row)

        # Send nodes_arr to graph obj
        self.graph = Graph(rows, cols)

    def set_cell_block(self, coord):
        cur_cell = self.cell_arr[coord.x][coord.y]
        if self.start_cell is not cur_cell and self.end_cell is not cur_cell:
            self.cell_arr[coord.x][coord.y].to_black()
            self.graph.set_block(coord.x, coord.y)

    def set_start_cell(self, coord):
        self.start_cell.to_white()
        self.start_cell = self.cell_arr[coord.x][coord.y]
        self.graph.set_start(coord.x, coord.y)
        self.start_cell.to_purple()

    def set_end_cell(self, coord):
        self.end_cell.to_white()
        self.end_cell = self.cell_arr[coord.x][coord.y]
        self.graph.set_end(coord.x, coord.y)
        self.end_cell.to_green()

    def update_cells(self):
        for r in self.cell_arr:
            for c in r:
                c.to_white()
        for node in self.graph.visited_nodes:
            c = self.cell_arr[node.coord.x][node.coord.y]
            c.to_blue()

        for coord in self.graph.path:
            c = self.cell_arr[coord.x][coord.y]
            c.to_yellow()

        for coord in self.graph.blocks:
            c = self.cell_arr[coord.x][coord.y]
            c.to_black()

        self.start_cell.to_purple()
        self.end_cell.to_green()

    def find_path(self):
        self.graph.start_path_finding()
        while self.graph.visit_next():
            self.update_cells()

        self.graph.build_path()
        self.update_cells()

    def draw(self, screen):
        for r in self.cell_arr:
            for c in r:
                c.draw(screen)

    def update(self):
        for r in self.cell_arr:
            for c in r:
                c.update()

    def clear_path(self):
        for cell_row in self.cell_arr:
            for cell_col in cell_row:
                if cell_col.color == BLUE or cell_col.color == YELLOW:
                    cell_col.to_white()

    def clear(self):
        for cell_row in self.cell_arr:
            for cell_col in cell_row:
                cell_col.to_white()

        self.start_cell = Cell(Rect(0, 0, 0, 0), WHITE)
        self.end_cell = Cell(Rect(0, 0, 0, 0), WHITE)
        self.graph = Graph(self.rows, self.cols)
