import pygame
import random
import time

pygame.font.init()
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (3, 82, 252)
GREEN = (0, 128, 0)
RED = (255, 0, 0)
FPS = 0.05
SIZE = 40
FONT = pygame.font.SysFont('Verdana', 20)
WIDTH = 840
HEIGHT = 450
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Sorting Visualizer')
clock = pygame.time.Clock()

moves = [pygame.K_b, pygame.K_s, pygame.K_i, pygame.K_m]


def merge(a, b):
    c = []
    indexA, indexB = 0, 0
    while indexA < len(a) and indexB < len(b):
        if a[indexA] < b[indexB]:
            c.append(a[indexA])
            indexA += 1
        else:
            c.append(b[indexB])
            indexB += 1
    if indexA == len(a):
        c.extend(b[indexB:])
    else:
        c.extend(a[indexA:])
    return c


def merge_sort(a):
    if len(a) <= 1:
        return a
    left, right = merge_sort(a[:len(a)//2]), merge_sort(a[len(a)//2:])
    return merge(left, right)


class Board:
    def __init__(self):
        self.vals = [0] * SIZE
        self.coords = [[0, 0] for _ in range(SIZE)]
        self.color = [WHITE] * SIZE

        x = 20
        for i in range(SIZE):
            self.vals[i] = random.randint(1, 41)
            y = 420 - 10*self.vals[i]
            self.coords[i][0], self.coords[i][1] = x, y
            x += 20

        self.display()
        text = FONT.render('B: Bubble Sort, S: Selection Sort, I: Insertion Sort', True, WHITE)
        WIN.blit(text, (20, 420))
        pygame.display.update()

    def display(self):
        WIN.fill(BLACK)
        for i in range(SIZE):
            self.coords[i][1] = 420 - 10 * self.vals[i]
            pygame.draw.rect(WIN, self.color[i],
                             pygame.Rect(self.coords[i][0], self.coords[i][1], 19, 10 * self.vals[i]))

        pygame.display.update()

    def bubble_sort(self):
        # start = time.process_time()
        swapped = True
        iters = 0
        while swapped:
            swapped = False
            for i in range(1, len(self.vals)):
                iters += 1
                self.color[i], self.color[i - 1] = GREEN, WHITE
                if self.vals[i - 1] > self.vals[i]:
                    self.vals[i], self.vals[i - 1] = self.vals[i - 1], self.vals[i]
                    self.display()
                    time.sleep(FPS)
                    swapped = True
            self.color[len(self.color) - 1] = WHITE
        # time_to_complete = time.process_time() - start
        self.sort_complete('Bubble Sort', iters)

    def selection_sort(self):
        # start = time.process_time()
        iters = 0
        for i in range(len(self.vals) - 1):
            self.color[i] = GREEN
            index = i + 1  # index of current smalles
            for j in range(i + 1, len(self.vals)):  # j = index of block being checked
                self.color[index], self.color[j] = RED, RED
                self.display()
                time.sleep(FPS)
                if self.vals[j] < self.vals[index]:  # when a new smallest is found
                    self.color[index] = WHITE
                    index = j
                iters += 1
                self.color[j] = WHITE
            if self.vals[i] > self.vals[index]:
                self.vals[i], self.vals[index] = self.vals[index], self.vals[i]
                self.color[index] = WHITE
            self.color[i] = WHITE
            self.display()
        # time_to_complete = time.process_time() - start
        self.sort_complete('Selection Sort', iters)

    def insertion_sort(self):
        iters = 0
        index = 0
        switch = False
        for i in range(1, len(self.vals)):
            self.color[i] = GREEN
            self.color[i-1] = RED
            for j in range(i-1, -1, -1):
                iters += 1
                if self.vals[i] < self.vals[j]:
                    index = j
                    switch = True
            if switch is True:
                tmp_curr = self.vals[i]
                for k in range(i-1, index-1, -1):
                    iters += 1
                    self.vals[k+1] = self.vals[k]
                self.vals[index] = tmp_curr
                switch = False
                self.display()
                time.sleep(FPS*2)
        self.sort_complete('Insertion Sort', iters)

    def sort_complete(self, name, iters):
        for i in range(0, len(self.color)):
            self.color[i] = BLUE
            self.display()
            time.sleep(0.02)

        text = FONT.render(f'{name} completed {iters} iterations. Press R to restart.', True, WHITE)
        WIN.blit(text, (20, 420))
        pygame.display.update()


def main():
    run = True
    board = Board()
    mode = None
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    board = Board()
                    mode = None
                if mode is None and event.key in moves:
                    if event.key == pygame.K_b:
                        board.bubble_sort()
                    elif event.key == pygame.K_s:
                        board.selection_sort()
                    elif event.key == pygame.K_i:
                        board.insertion_sort()
                    elif event.key == pygame.K_m:
                        board.vals = merge_sort(board.vals)
                        board.display()

                    mode = True


if __name__ == '__main__':
    main()
