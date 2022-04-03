import pygame
from copy import deepcopy
import random
import math
import time

WHITE = (255,255,255)
BLACK = (0,0,0)
RED = (255,0,0)
GREY = (150,150,150)
LIGHTGREY = (200,200,200)
BLUE = (0,0,255)
LIGHTBLUE =(171, 252, 255)
GREEN = (0,255,0)
YELLOW = (255,255,0)

initial_size_x = 400
initial_size_y = 600
pygame.init()
clock = pygame.time.Clock()
screen = pygame.display.set_mode((initial_size_x,initial_size_y))
pygame.display.set_caption("Sudoku")

blank_board = [[0, 0, 0, 0, 0, 0, 0, 0, 0],
               [0, 0, 0, 0, 0, 0, 0, 0, 0],
               [0, 0, 0, 0, 0, 0, 0, 0, 0],
               [0, 0, 0, 0, 0, 0, 0, 0, 0],
               [0, 0, 0, 0, 0, 0, 0, 0, 0],
               [0, 0, 0, 0, 0, 0, 0, 0, 0],
               [0, 0, 0, 0, 0, 0, 0, 0, 0],
               [0, 0, 0, 0, 0, 0, 0, 0, 0],
               [0, 0, 0, 0, 0, 0, 0, 0, 0]]
starting_table = None
class Board():
    def __init__(self):
        self.size_of_single_square = (initial_size_x - 20) // 9

    def draw_board(self):
        start_point_x = 10
        start_point_y = 10
        pygame.draw.rect(screen, BLACK, [start_point_x, start_point_y, self.size_of_single_square * 9, self.size_of_single_square * 9], 4)
        pygame.draw.rect(screen, BLACK, [start_point_x, 3 * self.size_of_single_square + start_point_y, self.size_of_single_square * 9, self.size_of_single_square * 3], 4)
        pygame.draw.rect(screen, BLACK, [start_point_x + self.size_of_single_square * 3, start_point_y, 3 * self.size_of_single_square, 9 * self.size_of_single_square], 4)

        pygame.draw.rect(screen, BLACK, [start_point_x, start_point_y + self.size_of_single_square * 1, self.size_of_single_square * 9, self.size_of_single_square * 1], 2)
        pygame.draw.rect(screen, BLACK, [start_point_x, start_point_y + self.size_of_single_square * 4, self.size_of_single_square * 9, self.size_of_single_square * 1], 2)
        pygame.draw.rect(screen, BLACK, [start_point_x, start_point_y + self.size_of_single_square * 7, self.size_of_single_square * 9, self.size_of_single_square * 1], 2)

        pygame.draw.rect(screen, BLACK, [start_point_x + self.size_of_single_square * 1, start_point_y, self.size_of_single_square, 9 * self.size_of_single_square], 2)
        pygame.draw.rect(screen, BLACK, [start_point_x + self.size_of_single_square * 4, start_point_y, self.size_of_single_square, 9 * self.size_of_single_square], 2)
        pygame.draw.rect(screen, BLACK, [start_point_x + self.size_of_single_square * 7, start_point_y, self.size_of_single_square, 9 * self.size_of_single_square], 2)

    def draw_number(self,pos_x,pos_y,number,color):
        font = pygame.font.Font('freesansbold.ttf', 30)
        render_text = font.render(str(number), 1, color)
        size_for_single_digit_x, size_for_single_digit_y = font.size(str(number))
        screen.blit(render_text, (
        10 + (self.size_of_single_square - size_for_single_digit_x) // 2 + self.size_of_single_square * (pos_x-1),
        13 + (self.size_of_single_square - size_for_single_digit_y) // 2 + self.size_of_single_square * (pos_y-1)))

    def draw_lines(self,pos_x,pos_y):
        if pos_x > -1 and pos_y > -1:
            pygame.draw.rect(screen, LIGHTGREY, [10 ,10  + self.size_of_single_square * (pos_y), self.size_of_single_square * 9,self.size_of_single_square ])
            pygame.draw.rect(screen, LIGHTGREY, [10 + self.size_of_single_square * (pos_x), 10 , self.size_of_single_square , self.size_of_single_square * 9])

    def draw_allert(self,text):
        font = pygame.font.Font('freesansbold.ttf', 20)
        render_text = font.render(text, 1, RED)
        size_x, size_y = font.size(text)
        pygame.draw.rect(screen, LIGHTGREY, [200 - size_x // 2 - 10, 540, size_x + 20, size_y + 10])
        screen.blit(render_text, (200 - size_x // 2 ,550))

    def draw_mistake_counter(self,number_of_mistakes):
        text = "Mistakes: " + str(number_of_mistakes)
        font = pygame.font.Font('freesansbold.ttf', 18)
        render_text = font.render("MISTAKES", 1, RED)
        size_x, size_y = font.size(text)
        screen.blit(render_text, (330 - size_x//2, 465))

        font = pygame.font.Font('freesansbold.ttf', 23)
        render_text = font.render(str(number_of_mistakes), 1, RED)
        size_x, size_y = font.size(str(number_of_mistakes))
        screen.blit(render_text, (330 - size_x//2, 485))

    def draw_selection(self,pos_x,pos_y,color):
        pygame.draw.rect(screen, color, [10 + self.size_of_single_square * pos_x, 10 + self.size_of_single_square * pos_y, self.size_of_single_square,self.size_of_single_square])




class Buttons():
    def __init__(self):
        self.button_width = (initial_size_x - 20) // 9
        self.button_height = 50
        self.start_point_x = 10
        self.start_point_y = 400
        self.selected_number = Game().selected_number
        self.difficulty = Game().difficulty_selected
    def draw_number_buttons(self):
        font = pygame.font.Font('freesansbold.ttf', 30)
        for i in range(1, 10):
            if self.selected_number == i:
                pygame.draw.rect(screen, LIGHTBLUE, [self.start_point_x + (i - 1) * self.button_width, self.start_point_y,
                                                self.button_width, self.button_height])
                pygame.draw.rect(screen, BLACK, [self.start_point_x + (i - 1) * self.button_width, self.start_point_y,
                                                 self.button_width, self.button_height], 2)
                render_text = font.render(str(i), 1, BLACK)
                size_for_single_digit_x, size_for_single_digit_y = font.size(str(i))
                screen.blit(render_text, (
                10 + (self.button_width - size_for_single_digit_x) // 2 + self.button_width * (i - 1), 13 + 400))
            else:
                pygame.draw.rect(screen, BLACK, [self.start_point_x + (i - 1) * self.button_width, self.start_point_y,
                                                 self.button_width, self.button_height], 2)
                render_text = font.render(str(i), 1, BLACK)
                size_for_single_digit_x, size_for_single_digit_y = font.size(str(i))
                screen.blit(render_text, (
                10 + (self.button_width - size_for_single_digit_x) // 2 + self.button_width * (i - 1), 13 + 400))

    def draw_interface_buttons(self):
        font = pygame.font.Font('freesansbold.ttf', 24)
        pygame.draw.rect(screen, GREY, [self.start_point_x , 460,
                                        150, 50])
        pygame.draw.rect(screen, BLACK, [self.start_point_x , 460,
                                        150, 50], 2)
        render_text = font.render("NEW GAME", 1, BLACK)
        size_x, size_y = font.size("NEW GAME")
        screen.blit(render_text, (
            10 + (150 - size_x) // 2 , 13 + 460))

    def draw_difficulty_selector(self):
        font = pygame.font.Font('freesansbold.ttf', 18)
        #pygame.font.Font.get_bold(font)
        render_text = font.render("DIFFICULTY", 1, BLACK)
        size_x, size_y = font.size("DIFICULTY")
        screen.blit(render_text, (215 - size_x // 2, 465))

        pygame.draw.circle(screen, BLACK, [190, 495], 10, 2)
        pygame.draw.circle(screen, BLACK, [215, 495], 10, 2)
        pygame.draw.circle(screen, BLACK, [240, 495], 10, 2)

        if self.difficulty == 1:
            pygame.draw.circle(screen, GREEN, [190, 495], 6)
        elif self.difficulty == 2:
            pygame.draw.circle(screen, YELLOW, [215, 495], 6)
        else:
            pygame.draw.circle(screen, RED, [240, 495], 6)



    def draw_interface(self):
        self.draw_number_buttons()
        self.draw_interface_buttons()
        self.draw_difficulty_selector()

class Game():
    def __init__(self):
        self.starting_table = [[5, 0, 0, 8, 4, 0, 9, 0, 0],
                               [0, 9, 2, 0, 0, 0, 5, 0, 0],
                               [8, 6, 3, 0, 0, 0, 0, 4, 0],
                               [0, 0, 0, 7, 6, 1, 0, 0, 5],
                               [3, 0, 5, 0, 0, 4, 0, 7, 6],
                               [6, 0, 1, 3, 0, 0, 0, 0, 4],
                               [0, 3, 0, 0, 2, 9, 4, 0, 7],
                               [0, 0, 0, 6, 0, 0, 2, 0, 0],
                               [0, 0, 8, 4, 0, 0, 6, 1, 9]]
        self.solved_table = None
        self.user_input = deepcopy(self.starting_table)
        self.selected_number = 0
        self.selected_pos_x = -1
        self.selected_pos_y = -1
        self.check_solution = False
        self.mistake_counter = 0
        self.previous_state = None
        self.previous_table = None
        self.new_game = True
        self.difficulty_selected = 1

        self.autosolve = False

    def print_board_numbers(self):
        for y in range(len(self.user_input)):
            for x in range(len(self.user_input[0])):
                if self.user_input[y][x] == self.starting_table[y][x] and self.user_input[y][x] != 0:
                    board.draw_number(x+1,y+1,self.user_input[y][x],BLACK)
                elif self.user_input[y][x] != 0 and self.starting_table[y][x] == 0 and self.user_input[y][x] == self.solved_table[y][x]:
                    board.draw_number(x + 1, y + 1, self.user_input[y][x], BLUE)
                elif self.user_input[y][x] != 0 and self.starting_table[y][x] == 0 and self.user_input[y][x] != self.solved_table[y][x]:
                    board.draw_number(x + 1, y + 1, self.user_input[y][x], RED)
                    if self.previous_state != self.user_input[y][x] and self.user_input[y][x] != self.previous_table[y][x]:
                        self.mistake_counter += 1
                    self.previous_state = self.user_input[y][x]
        self.previous_table = deepcopy(self.user_input)

    def refresh(self):
        screen.fill(WHITE)
        if self.new_game == True:
            generator.empty_board = deepcopy(blank_board)
            generator.generate_new_game()
            self.starting_table = deepcopy(generator.empty_board)
            #print(self.starting_table)
            global starting_table
            starting_table = deepcopy(self.starting_table)
            self.user_input = deepcopy(self.starting_table)
            self.solved_table = deepcopy(solver.solve(deepcopy(self.starting_table)))
            self.new_game = False

        if self.starting_table[self.selected_pos_y][self.selected_pos_x] == 0 and self.autosolve == False:
            self.user_input[self.selected_pos_y][self.selected_pos_x] = deepcopy(self.selected_number)
        elif self.starting_table[self.selected_pos_y][self.selected_pos_x] != 0 and self.selected_pos_x > -1 and self.selected_pos_y >-1:
            board.draw_allert("THIS NUMBER CAN NOT BE CHANGED")
        board.draw_lines(self.selected_pos_x, self.selected_pos_y)
        board.draw_board()
        self.print_board_numbers()
        buttons.selected_number = deepcopy(self.selected_number)
        buttons.draw_interface()
        board.draw_mistake_counter(deepcopy(self.mistake_counter))

class Solver():
    def __init__(self):
        self.solving_table = [[0, 0, 0, 0, 0, 0, 0, 0, 0],
                              [0, 0, 0, 0, 0, 0, 0, 0, 0],
                              [0, 0, 0, 0, 0, 0, 0, 0, 0],
                              [0, 0, 0, 0, 0, 0, 0, 0, 0],
                              [0, 0, 0, 0, 0, 0, 0, 0, 0],
                              [0, 0, 0, 0, 0, 0, 0, 0, 0],
                              [0, 0, 0, 0, 0, 0, 0, 0, 0],
                              [0, 0, 0, 0, 0, 0, 0, 0, 0],
                              [0, 0, 0, 0, 0, 0, 0, 0, 0]]
        self.solver_input = None

    def print_board_numbers(self):
        for y in range(len(self.solver_input)):
            for x in range(len(self.solver_input[0])):
                if self.solver_input[y][x] != 0:
                    board.draw_number(x+1,y+1,self.solver_input[y][x],BLACK)

    def possible(self,table, y, x, n):
        for i in range(0, 9):
            if table[y][i] == n:
                return False
        for i in range(0, 9):
            if table[i][x] == n:
                return False
        x0 = (x // 3) * 3
        y0 = (y // 3) * 3
        for i in range(0, 3):
            for j in range(0, 3):
                if table[y0 + i][x0 + j] == n:
                    return False

        return True

    def solve(self,table):
        if game.autosolve:
            self.solver_input = deepcopy(starting_table)
            for y in range(9):
                for x in range(9):
                    if table[y][x] == 0:
                        for n in range(1, 10):
                            screen.fill(WHITE)
                            self.solving_table[y][x] = 1
                            for y1 in range(9):
                                for x1 in range(9):
                                    if self.solving_table[y1][x1] == 1:
                                        board.draw_selection(x1,y1,RED)
                                    elif self.solving_table[y1][x1] == 2:
                                        board.draw_selection(x1, y1, GREEN)
                            self.solver_input[y][x] = n
                            self.solver_refresh()
                            pygame.display.update()
                            #time.sleep(1)
                            if self.possible(table, y, x, n):
                                table[y][x] = n
                                self.solver_input[y][x] = n
                                #print(Game().user_input)
                                self.solver_refresh()
                                pygame.display.update()
                                clock.tick(30)
                                self.solving_table[y][x] = 2
                                if self.solve(table):
                                    return table
                                else:
                                    table[y][x] = 0
                                    self.solving_table[y][x] = 0
                                    self.solver_input[y][x] = 0
                                    for y1 in range(y,9):
                                        for x1 in range(x,9):
                                            self.solving_table[y1][x1] = 0
                                            if self.solver_input[y1][x1] != starting_table[y1][x1]:
                                                self.solver_input[y1][x1] = 0
                        return
            screen.fill(WHITE)
            for y1 in range(9):
                for x1 in range(9):
                    if self.solving_table[y1][x1] == 1:
                        board.draw_selection(x1, y1, RED)
                    elif self.solving_table[y1][x1] == 2:
                        board.draw_selection(x1, y1, GREEN)
            self.solver_refresh()
            pygame.display.update()
            return table
        else:
            for y in range(9):
                for x in range(9):
                    if table[y][x] == 0:
                        for n in range(1, 10):
                            if self.possible(table, y, x, n):
                                table[y][x] = n
                                if self.solve(table):
                                    #print(self.solving_table)
                                    return table
                                else:
                                    table[y][x] = 0

                        return
            return table

    def solver_refresh(self):
        #screen.fill(WHITE)
        #board.draw_lines(self.selected_pos_x, self.selected_pos_y)
        board.draw_board()
        self.print_board_numbers()
        buttons.draw_interface()

counter = 0
class Generator():
    def __init__(self):
        self.empty_board = [[0, 0, 0, 0, 0, 0, 0, 0, 0],
                            [0, 0, 0, 0, 0, 0, 0, 0, 0],
                            [0, 0, 0, 0, 0, 0, 0, 0, 0],
                            [0, 0, 0, 0, 0, 0, 0, 0, 0],
                            [0, 0, 0, 0, 0, 0, 0, 0, 0],
                            [0, 0, 0, 0, 0, 0, 0, 0, 0],
                            [0, 0, 0, 0, 0, 0, 0, 0, 0],
                            [0, 0, 0, 0, 0, 0, 0, 0, 0],
                            [0, 0, 0, 0, 0, 0, 0, 0, 0]]
        self.number_list = [1,2,3,4,5,6,7,8,9]
        self.dificulty = Game().difficulty_selected

    def possible(self,table, y, x, n):
        for i in range(0, 9):
            if table[y][i] == n:
                return False
        for i in range(0, 9):
            if table[i][x] == n:
                return False
        x0 = (x // 3) * 3
        y0 = (y // 3) * 3
        for i in range(0, 3):
            for j in range(0, 3):
                if table[y0 + i][x0 + j] == n:
                    return False

        return True

    def check_for_empty_places(self,table):
        for y in range(9):
            for x in range(9):
                if table[y][x] == 0:
                    return False
        return True

    def generate_grid(self,grid):
        for i in range(0, 81):
            row = i // 9
            col = i % 9
            if grid[row][col] == 0:
                random.shuffle(self.number_list)
                for n in self.number_list:
                    if self.possible(grid, row, col, n):
                        grid[row][col] = n
                        if self.check_for_empty_places(grid):
                            return True
                        else:
                            if self.generate_grid(grid):
                                return True
                break
        grid[row][col] = 0

    def solver(self,table):
        global counter
        for y in range(9):
            for x in range(9):
                if table[y][x] == 0:
                    for n in range(1, 10):
                        if self.possible(table, y, x, n):
                            table[y][x] = n
                            self.solver(table)
                            table[y][x] = 0
                    return
        counter += 1
        if counter > 1:
            return

    def remove_numbers(self,table, number_of_attempts):
        global counter
        while number_of_attempts > 0:
            y = random.randint(0, 8)
            x = random.randint(0, 8)
            while table[y][x] == 0:
                y = random.randint(0, 8)
                x = random.randint(0, 8)

            old_number = table[y][x]
            table[y][x] = 0

            counter = 0
            self.solver(table)
            if counter > 1:
                table[y][x] = old_number
                number_of_attempts -= 1
        return

    def generate_new_game(self):
        self.generate_grid(self.empty_board)
        self.remove_numbers(self.empty_board,self.dificulty)




screen.fill(WHITE)
board = Board()
buttons = Buttons()
solver = Solver()
game = Game()
generator = Generator()

board.draw_board()
buttons.draw_interface()

#game.solved_table = deepcopy(solver.solve(deepcopy(game.starting_table)))



running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                x, y =  pygame.mouse.get_pos()
                if x > 10 and x < (10 + board.size_of_single_square * 9) and y > 10 and y < (10 + board.size_of_single_square * 9):
                    if game.user_input[(y - 10) // board.size_of_single_square][(x - 10) // board.size_of_single_square] == 0:
                        game.selected_number = 0
                    else:
                        game.selected_number = game.user_input[(y - 10) // board.size_of_single_square][(x - 10) // board.size_of_single_square]
                    if game.selected_pos_x == (x - 10) // board.size_of_single_square and game.selected_pos_y == (y - 10) // board.size_of_single_square:
                        game.selected_pos_x = -1
                        game.selected_pos_y = -1
                        game.selected_number = 0
                    else:
                        game.selected_pos_x = (x - 10) // board.size_of_single_square
                        game.selected_pos_y = (y - 10) // board.size_of_single_square
                elif x > 10 and x < (10 + buttons.button_width * 9) and y > 400 and y <(400 + buttons.button_height):
                    game.selected_number = (x - 10) // buttons.button_width + 1
                elif x > 10 and x < 160 and y > 460 and y < 510:
                    game.new_game = True
                else:
                    if math.sqrt((x - 190)**2 + (y - 495)**2) < 10:
                        game.difficulty_selected = 1
                        buttons.difficulty = 1
                        generator.dificulty = 1
                    if math.sqrt((x - 215)**2 + (y - 495)**2) < 10:
                        game.difficulty_selected = 2
                        buttons.difficulty = 2
                        generator.dificulty = 2
                    if math.sqrt((x - 240)**2 + (y - 495)**2) < 10:
                        game.difficulty_selected = 3
                        buttons.difficulty = 3
                        generator.dificulty = 3

                    game.selected_pos_x = -1
                    game.selected_pos_y = -1
                    game.selected_number = 0

        if event.type == pygame.KEYDOWN:
            if game.selected_pos_x > -1 and game.selected_pos_y > -1:
                if event.key == pygame.K_0 or event.key == pygame.K_KP0:
                    game.selected_number = 0
                if event.key == pygame.K_1 or event.key == pygame.K_KP1:
                    game.selected_number = 1
                if event.key == pygame.K_2 or event.key == pygame.K_KP2:
                    game.selected_number = 2
                if event.key == pygame.K_3 or event.key == pygame.K_KP3:
                    game.selected_number = 3
                if event.key == pygame.K_4 or event.key == pygame.K_KP4:
                    game.selected_number = 4
                if event.key == pygame.K_5 or event.key == pygame.K_KP5:
                    game.selected_number = 5
                if event.key == pygame.K_6 or event.key == pygame.K_KP6:
                    game.selected_number = 6
                if event.key == pygame.K_7 or event.key == pygame.K_KP7:
                    game.selected_number = 7
                if event.key == pygame.K_8 or event.key == pygame.K_KP8:
                    game.selected_number = 8
                if event.key == pygame.K_9 or event.key == pygame.K_KP9:
                    game.selected_number = 9
            if event.key == pygame.K_SPACE:
                game.autosolve = not game.autosolve
                if game.autosolve:
                    solver.solve(starting_table)

    if not game.autosolve:
        game.refresh()
        pygame.display.update()
    clock.tick(24)
