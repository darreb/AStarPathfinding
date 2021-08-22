import heapq
import math

# PriorityQueue implemented with heapq functions
class PriorityQueue:
    def __init__(self):
        self.q = []

    def push(self, item):
        heapq.heappush(self.q, item)

    def pop(self):
        heapq.heapify(self.q)
        return heapq.heappop(self.q)

    def empty(self):
        return len(self.q) == 0

    def top(self):
        if self.size() > 0:
            return heapq.nsmallest(1, self.q)[0]
        else:
            return -1

    def size(self):
        return len(self.q)


class Coord:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __lt__(self, other):
        return True

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __str__(self):
        return "({}, {})".format(self.x, self.y)

    def __repr__(self):
        return "({}, {})".format(self.x, self.y)


class Graph:
    def __init__(self, rows, cols):
        self.rows = rows
        self.cols = cols
        self.nodes_arr = []
        # Add nodes from cells to nodes_arr
        for i in range(self.rows):
            node_row = []
            for j in range(self.cols):
                node_row.append(Node(Coord(i, j)))
            self.nodes_arr.append(node_row)
        self.next = PriorityQueue()
        self.start = Coord(0, 0)
        self.end = Coord(0, 0)
        self.path = []
        self.visited_nodes = []
        self.blocks = []

    def set_start(self, x, y):
        if x < 0 or x >= self.rows:
            print("Invalid coordinate: Not within bounds")
            return

        if y < 0 or y >= self.cols:
            print("Invalid coordinate: Not within bounds")
            return
        self.start = Coord(x, y)

    def set_end(self, x, y):
        if x < 0 or x >= self.rows:
            print("Invalid coordinate: Not within bounds")
            return

        if y < 0 or y >= self.cols:
            print("Invalid coordinate: Not within bounds")
            return
        self.end = Coord(x, y)

    def set_block(self, x, y):
        coord = Coord(x, y)
        self.nodes_arr[coord.x][coord.y].block = True
        self.blocks.append(coord)

    def print_graph(self):
        for i in range(self.rows):
            for j in range(self.cols):

                if(i, j) == (self.start.x, self.start.y):
                    st = '{:<17}'.format('{}'.format("S"))
                    print(st, end='')
                elif(i, j) == (self.end.x, self.end.y):
                    st = '{:<17}'.format('{}'.format("X"))
                    print(st, end='')
                else:
                    print(self.nodes_arr[i][j], end='')
            print("\n")

    def calculate_cost(self, coord, dist_from_start):
        node = Node(coord)
        g_cost = dist_from_start
        h_cost = math.sqrt(((self.end.x - coord.x) * 10) ** 2 + ((self.end.y - coord.y) * 10) ** 2)
        node.set_hcost(h_cost)
        node.set_gcost(g_cost)
        node.set_fcost(h_cost + g_cost)
        return node

    def update_cost(self, coord, dist_from_start):
        node = self.nodes_arr[coord.x][coord.y]
        g_cost = dist_from_start
        h_cost = math.sqrt(((self.end.x - coord.x)*10) ** 2 + ((self.end.y - coord.y)*10) ** 2)
        node.set_hcost(h_cost)
        node.set_gcost(g_cost)
        node.set_fcost(h_cost + g_cost)

    def update_node(self, cur_node, new_node):
        if cur_node > new_node:
            cur_node.set_fcost(new_node.get_fcost())
            cur_node.set_gcost(new_node.get_gcost())
            cur_node.set_hcost(new_node.get_hcost())
            cur_node.last = new_node.last
            return True
        return False

    def next_neighbor(self):
        next_node = self.next.pop()
        return next_node

    def add_neighbors(self, coord):
        center_node = self.nodes_arr[coord.x][coord.y]

        # Top Col Neighbors
        if coord.y - 1 >= 0:
            for i in (range(-1, 2)):
                if 0 <= coord.x + i < self.rows:
                    if i != 0:
                        diag = math.sqrt(10 ** 2 + 10 ** 2)
                        cur_coord = Coord(coord.x + i, coord.y - 1)
                        cur_node = self.nodes_arr[cur_coord.x][cur_coord.y]
                        if not cur_node.visited and not cur_node.is_block():
                            new_node = self.calculate_cost(cur_coord, center_node.get_gcost() + diag)
                            new_node.last = center_node
                            if self.update_node(cur_node, new_node):
                                self.next.push(cur_node)
                    else:
                        cur_coord = Coord(coord.x + i, coord.y - 1)
                        cur_node = self.nodes_arr[cur_coord.x][cur_coord.y]
                        if not cur_node.visited and not cur_node.is_block():
                            new_node = self.calculate_cost(cur_coord, center_node.get_gcost() + 10)
                            new_node.last = center_node
                            if self.update_node(cur_node, new_node):
                                self.next.push(cur_node)

        # Middle Col neighbors
        for i in (range(-1, 2)):
            if 0 <= coord.x + i < self.rows:
                if i != 0:
                    cur_coord = Coord(coord.x + i, coord.y)
                    cur_node = self.nodes_arr[cur_coord.x][cur_coord.y]
                    if not cur_node.visited and not cur_node.is_block():
                        new_node = self.calculate_cost(cur_coord, center_node.get_gcost() + 10)
                        new_node.last = center_node
                        if self.update_node(cur_node, new_node):
                            self.next.push(cur_node)

        # Bottom Col neighbors
        if coord.y + 1 < self.cols:
            for i in (range(-1, 2)):
                if 0 <= coord.x + i < self.rows:
                    if i != 0:
                        diag = math.sqrt(10 ** 2 + 10 ** 2)
                        cur_coord = Coord(coord.x + i, coord.y + 1)
                        cur_node = self.nodes_arr[cur_coord.x][cur_coord.y]
                        if not cur_node.visited and not cur_node.is_block():
                            new_node = self.calculate_cost(cur_coord, center_node.get_gcost() + diag)
                            new_node.last = center_node
                            if self.update_node(cur_node, new_node):
                                self.next.push(cur_node)
                    else:
                        cur_coord = Coord(coord.x + i, coord.y + 1)
                        cur_node = self.nodes_arr[cur_coord.x][cur_coord.y]
                        if not cur_node.visited and not cur_node.is_block():
                            new_node = self.calculate_cost(cur_coord, center_node.get_gcost() + 10)
                            new_node.last = center_node
                            if self.update_node(cur_node, new_node):
                                self.next.push(cur_node)

    def visit_next(self):
        if self.next.size() == 0:
            return None
        next_node = self.next_neighbor()
        while next_node.visited:  # Come back here if ur code runs for too long o.o

            next_node = self.next_neighbor()
            # for i in self.next.q:
            #     i.print_node()
        if next_node.coord == self.end:
            print("Done")
            return None

        self.visited_nodes.append(next_node)

        self.add_neighbors(next_node.coord)
        next_node.visited = True
        return next_node

    def start_path_finding(self):
        self.reset()
        start_node = self.nodes_arr[self.start.x][self.start.y]
        self.next.push(start_node)
        self.update_cost(self.start, 0)

    def build_path(self):
        start_node = self.nodes_arr[self.start.x][self.start.y]
        prev_node = self.nodes_arr[self.end.x][self.end.y]
        if prev_node.last != prev_node:
            while prev_node != start_node:
                self.path.insert(0, prev_node.coord)
                prev_node = prev_node.last
            self.path.insert(0, start_node.coord)

    def find_path(self):
        self.start_path_finding()
        while self.visit_next():
            pass

        self.build_path()

    def print_path(self):
        if len(self.path) > 0:
            print(self.path)
        else:
            print("No path found")

    def reset(self):
        self.path = []
        self.visited_nodes = []
        self.next = PriorityQueue()
        self.nodes_arr = []
        for i in range(self.rows):
            node_row = []
            for j in range(self.cols):
                node_row.append(Node(Coord(i, j)))
            self.nodes_arr.append(node_row)

        for coord in self.blocks:
            self.nodes_arr[coord.x][coord.y].block = True


class Node:
    def __init__(self, coord):
        self.f = -1
        self.g = 0
        self.h = -1
        self.last = self
        self.block = False
        self.visited = False
        self.coord = coord

    def __gt__(self, other):
        if self.f == -1 and other.f >= 0:
            return True
        elif other.f == -1 and self.f >= 0:
            return False
        if self.f == other.f:
            return self.h > other.h
        return self.f > other.f

    def __lt__(self, other):
        if self.f == -1 and other.f >= 0:
            return False
        elif other.f == -1 and self.f >= 0:
            return True
        if self.f == other.f:
            return self.h < other.h
        return self.f < other.f

    def __ge__(self, other):
        if self.f == -1:
            return True
        if self.f == other.f:
            return self.h >= other.h
        return self.f >= other.f

    def __le__(self, other):
        if other.f == -1:
            return True
        if self.f == other.f:
            return self.h <= other.h
        return self.f <= other.h

    def __repr__(self):
        if self.is_block():
            st = '{:<17}'.format("[==]")
            return st
        if self.visited:
            st = '{:<17}'.format("({}, {})".format('{:.0f}'.format(self.f), '{:.0f}'.format(self.h)))
            # st = "{}, {}".format(self.coord.x, self.coord.y)
            return st
        else:
            st = '{:<17}'.format('{:.0f}, {:.0f}'.format(self.f, self.h))
            # = "{}, {}".format(self.coord.x, self.coord.y)
            return st

    def is_block(self):
        return self.block

    def set_fcost(self, f):
        self.f = f

    def set_hcost(self, h):
        self.h = h

    def set_gcost(self, g):
        self.g = g

    def get_fcost(self):
        return self.f

    def get_hcost(self):
        return self.h

    def get_gcost(self):
        return self.g