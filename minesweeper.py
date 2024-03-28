import pygame
from time import time
import random

class Game:
    def __init__(self):
        self.unvisited_image = pygame.image.load('img/notvisited.png')
        self.visited_image = pygame.image.load('img/visited.png')
        self.mine_image = pygame.image.load('img/mine.png')
        self.flag_image = pygame.image.load('img/flag.png')
        self.one = pygame.image.load('img/1.png')
        self.two = pygame.image.load('img/2.png')
        self.three = pygame.image.load('img/3.png')
        self.four = pygame.image.load('img/4.png')
        self.five = pygame.image.load('img/5.png')
        self.six = pygame.image.load('img/6.png')
        self.seven = pygame.image.load('img/7.png')
        self.eight = pygame.image.load('img/8.png')
        self.menu= pygame.image.load('img/menu.png')
        self.won= pygame.image.load('img/won.png')
        self.lost= pygame.image.load('img/lost.png')
        self.again= pygame.image.load('img/again.png')
        self.numbers = [
            self.visited_image, self.one, self.two, self.three,
            self.four, self.five, self.six, self.seven, self.eight, self.visited_image
        ]
        self.menu= pygame.transform.scale(self.menu,(1000,700))
        
    def initialize(self):
        self.window = pygame.display.set_mode((self.window_width, self.window_height))
        self.cell_size = self.window.get_width() // self.cols
        for i in range(len(self.numbers)):
            self.numbers[i] = pygame.transform.scale(self.numbers[i], (self.cell_size, self.cell_size))
        self.unvisited_image = pygame.transform.scale(self.unvisited_image, (self.cell_size, self.cell_size))
        self.visited_image = pygame.transform.scale(self.visited_image, (self.cell_size, self.cell_size))
        self.mine_image = pygame.transform.scale(self.mine_image, (self.cell_size, self.cell_size))
        self.flag_image = pygame.transform.scale(self.flag_image, (self.cell_size, self.cell_size))
        self.won= pygame.transform.scale(self.won,(self.window_width//2,100))
        self.lost= pygame.transform.scale(self.lost,(self.window_width//2,100))
        self.again= pygame.transform.scale(self.again,(self.window_width//2,100))
        self.grid = [[0] * self.cols for _ in range(self.rows)]
        self.visited = [[0] * self.cols for _ in range(self.rows)]
        self.neighboors=[-1,0,1]
    
    def valid(self,i,j):
        return i>=0 and i<self.rows and j>=0 and j<self.cols #and self.visited[i][j]<=0

    def prepare_grid(self,x,y): #places mines and numbers
        mines = 0
        while mines < self.num_mines:
            row = random.randint(0, self.rows - 1)
            col = random.randint(0, self.cols - 1)
            if self.grid[row][col] == 0 and not (abs(row-x)<=1 and abs(col-y)<=1):
                self.grid[row][col] = 10
                mines += 1
        
        for i in range(self.rows):
            for j in range(self.cols):
                if self.grid[i][j]==10: continue
                num=0
                for dx in self.neighboors:
                    for dy in self.neighboors:
                        if dx == 0 and dy == 0:continue
                        if self.valid(i + dx, j + dy) and self.grid[i + dx][j + dy] == 10:
                            num += 1
                self.grid[i][j] = num



    def flags_around(self,i,j): #counts how many flags are around
        num=0
        for dx in self.neighboors:
            for dy in self.neighboors:
                if dx == 0 and dy == 0:continue
                if self.valid(i + dx, j + dy) and self.visited[i + dx][j + dy] == -1:
                    num += 1
        return num


    def visit_zeros(self,i,j): #dfs
        if self.visited[i][j] or self.grid[i][j]: return
        self.visited[i][j]=1
        self.visit_around(i,j)

    def visit_around(self,i,j,temporary=False): # 1 for visit, 2 for temporary visit
        if self.visited[i][j]==0:
            if self.grid[i][j]==0: 
                self.visit_zeros(i,j)
            else:
                self.visited[i][j]=1
            return
        for dx in self.neighboors:
            for dy in self.neighboors:
                if self.valid(i + dx, j + dy) and not self.visited[i + dx][j + dy]:
                    if not temporary and self.grid[i+dx][j+dy]==0 and self.visited[i+dx][j+dy]!=-1:
                        self.visit_zeros(i+dx,j+dy)
                    else:    
                        self.visited[i + dx][j + dy]= 2 if temporary else 1
        
    def unvisit_around(self,i,j): #fix
        for dx in self.neighboors:
            for dy in self.neighboors:
                if self.valid(i + dx, j + dy) and self.visited[i + dx][j + dy]==2: #temporary visited
                    self.visited[i + dx][j + dy]=0

    def draw_grid(self):
        for i in range(self.rows):
            for j in range(self.cols):
                cell_x = j * self.cell_size
                cell_y = i * self.cell_size
                if self.visited[i][j]==-1: #if flag
                    self.window.blit(self.flag_image, (cell_x, cell_y))
                elif not self.visited[i][j]: 
                    self.window.blit(self.unvisited_image, (cell_x, cell_y))
                elif self.visited[i][j]==2: #temporary visited
                    self.window.blit(self.visited_image, (cell_x,cell_y))
                elif self.grid[i][j]==10: #if mine
                    self.window.blit(self.mine_image, (cell_x, cell_y))
                else:
                   self.window.blit(self.numbers[self.grid[i][j]],(cell_x, cell_y))
        if self.gameover:
            if self.gameover==-1 :   
                self.window.blit(self.lost,(0,self.window_height))
            else:
                self.window.blit(self.won,(0,self.window_height))
            self.window.blit(self.again,(self.window_width//2,self.window_height))

    
    def levelselect(self):
        self.window_width=1000
        self.window_height=700
        self.window = pygame.display.set_mode((self.window_width, self.window_height))
        pygame.display.set_caption('Minesweeper ~ Menu')
        self.window.blit(self.menu,(0,0))
        pygame.display.update()
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return False
                elif event.type == pygame.MOUSEBUTTONDOWN:  
                    mouse_pos = pygame.mouse.get_pos()
                    x= mouse_pos[0] / self.window_width
                    y=mouse_pos[1] / self.window_height
                    if x>0.254 and x<0.739:
                        if y>0.285 and y < 0.428:
                            pygame.display.set_caption('Minesweeper ~ Beginner')
                            self.num_mines=10
                            self.rows=9
                            self.cols=9
                            self.window_height=600
                            self.window_width=600
                            return True
                        elif y>0.484 and y<0.628:
                            pygame.display.set_caption('Minesweeper ~ Intermidiate')
                            self.num_mines=40
                            self.rows=16
                            self.cols=16
                            self.window_height=600
                            self.window_width=600
                            return True
                        elif y>0.672 and y<0.815:
                            pygame.display.set_caption('Minesweeper ~ Expert')
                            self.num_mines=99
                            self.rows=15
                            self.cols=30
                            self.window_height=500
                            self.window_width=1000
                            return True
                            
    def reveal_bombs(self):
        for i in range(self.rows):
            for j in range(self.cols):
                if self.grid[i][j]==10:
                    self.visited[i][j]=1
    
    def check(self):# will return 0 if ok, -1 if loss, 1 if win
        flagged_mines=0
        visited_squares=0
        squares=self.cols*self.rows
        for i in range(self.rows):
            for j in range(self.cols):
                if self.visited[i][j]==1:
                    if self.grid[i][j]==10:
                        self.reveal_bombs()
                        self.window = pygame.display.set_mode((self.window_width, self.window_height+100))
                        return -1
                    visited_squares+=1
                elif self.visited[i][j]==-1 and self.grid[i][j]==10:
                    flagged_mines+=1
        if flagged_mines+visited_squares==squares:
            self.window = pygame.display.set_mode((self.window_width, self.window_height+100))
            return 1
        return 0
    
    def get_pos(self):
        mouse_pos = pygame.mouse.get_pos()
        return mouse_pos[1] // self.cell_size, mouse_pos[0] // self.cell_size
    
    def run(self):
        running = self.levelselect()
        if running:
            return self.play()
            
    def play(self):
        self.gameover=0
        running=True
        first_time=True
        holding_down=False
        lasti,lastj=-1,-1
        self.initialize()
        while running and not self.gameover:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif holding_down and event.type == pygame.MOUSEMOTION:
                    i,j=self.get_pos()
                    if not self.valid(i,j): continue
                    self.unvisit_around(lasti,lastj)
                    if self.visited[i][j]==1:
                        lasti,lastj=i,j
                        self.visit_around(i,j,temporary=True)

                elif event.type == pygame.MOUSEBUTTONDOWN and not holding_down:
                    i,j=self.get_pos()
                    if not self.valid(i,j): continue
                    if event.button == 1 and self.visited[i][j]>=0:  # Left-click DOWN                        
                        if first_time:
                            self.prepare_grid(i,j)
                            first_time=False
                            
                        if self.visited[i][j]==1:
                            flags=self.flags_around(i,j)
                            if flags>=self.grid[i][j]:
                                self.visit_around(i,j)
                            else:
                                self.unvisit_around(lasti,lastj)
                                lasti,lastj=i,j
                                self.visit_around(i,j,temporary=True)
                        else:
                            self.visit_around(i,j)
                    elif event.button == 3 and self.visited[i][j]<=0:  # Right-click DOWN
                        if self.visited[i][j]==-1: self.visited[i][j]=0
                        else: self.visited[i][j]=-1
                        
                    holding_down=True
               
                elif event.type == pygame.MOUSEBUTTONUP:
                    holding_down=False
                    i,j=self.get_pos()
                    if self.valid(i,j) and event.button == 1 and self.visited[i][j]!=-1:  # Left-click UP
                        self.unvisit_around(i,j)
                        
            self.window.fill((190, 190, 190))
            self.draw_grid()
            pygame.display.update()
            self.gameover=self.check()
            
        while self.gameover:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()
                    if event.button == 1 and self.visited[i][j]>=0:  # Left-click DOWN
                        x= mouse_pos[0] / self.window_width
                        y=mouse_pos[1] / self.window_height
                        if x>0.5 and y>1:
                            return True
                        
            self.window.fill((190, 190, 190))
            self.draw_grid()
            pygame.display.update()                       


import sys,os # For PyInstaller
if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
    os.chdir(sys._MEIPASS)
if __name__ == '__main__':
    random.seed(time())
    pygame.init()
    play=True
    while play:
        game = Game()
        play=game.run()
    pygame.quit()