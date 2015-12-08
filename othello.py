
# coding: utf-8

# In[36]:

import numpy as np
import Tkinter
import time
import sys


# In[37]:

class Board:
    """
    rows: board size
    board: a 8x8 matrix of colors
    color: a value in [0,1,2]: none, black, white, respectively.
    move: a array [row,col]
    directions: a set of all nine unit vectors
    olds: stack to keep old boards, which is to undo()
    """
    def __init__(self):
        self.rows = 8
        self.directions = np.array([[-1,0],[-1,1],[0,1],[1,1],[1,0],[1,-1],[0,-1],[-1,-1]], int)
        self.init()
    
    def init(self):
        self.board = [[0 for x in range(self.rows)] for x in range(self.rows)] 
        self.posScore = [[50,-10 ,5  ,5  ,5  ,5 ,-10 ,50],
                        [-10,-25 ,-3  ,-3  ,-3  ,-3  ,-25 ,-10],
                        [5  ,-3   ,2  ,2  ,2  ,2  ,-3   ,5],
                        [5  ,-3   ,2  ,2  ,2  ,2  ,-3   ,5],
                        [5  ,-3   ,2  ,2  ,2  ,2  ,-3   ,5],
                        [5  ,-3   ,2  ,2  ,2  ,2  ,-3   ,5],
                        [-10,-25 ,-3  ,-3  ,-3  ,-3  ,-25 ,-10],
                        [50 ,-10 ,5  ,5  ,5  ,5  ,-10 ,50]]
        self.board[3][3] = 1
        self.board[4][4] = 1
        self.board[3][4] = 2
        self.board[4][3] = 2
        self.olds = []
    
    def getBoardCopy(self):
        """returns a copy of board"""
        return [row[:] for row in self.board]
    
    def put(self, row, col, color):
        """put a score into borad at a given index"""
        self.board[row][col] = color
    
    def get(self, row, col):
        """get a score into borad at a given index"""
        return self.board[row][col]
    
    def getStat(self):
        """returns a statistics which includes:
            1. # of black pieces
            2. # of white pieces"""
        b_score, w_score = 0, 0
        for row in range(self.rows):
            for col in range(self.rows):
                test = self.board[row][col]
                if test == 1:
                    b_score += 1
                elif test == 2:
                    w_score += 1
        return [b_score, w_score]
    
    def getCountScore(self):
        """returns a simple score based on the number of each color"""
        count = 0
        for row in range(self.rows):
            for col in range(self.rows):
                test = self.board[row][col]
                if test == 1:
                    count += 1
                elif test == 2:
                    count -= 1
        return count
    
    def getPosScore(self):
        """returns a score calculated based on the pre-defined positional matrix"""
        score = 0
        for row in range(self.rows):
            for col in range(self.rows):
                test = self.board[row][col]
                if test == 1:
                    score += self.posScore[row][col]
                elif test == 2:
                    score -= self.posScore[row][col]
        return score
    
    def undo(self):
        """move back state to old (top of stack)"""
        lastboard = self.olds.pop()
        self.board = lastboard
        
    def isValidMove(self, move, color):
        validMove = False;
        # flip color
        opposite = (bool(color - 1) ^ bool(1)) + 1 
        
        # check all direction
        for way in self.directions:
            newPos = move + way
            # border checking
            if not self.checkBorder(newPos):
                 continue
            # check this way 
            if (self.board[newPos[0]][newPos[1]] == opposite):
                newPos += way
                # ignore opposites
                while (self.checkBorder(newPos) and self.board[newPos[0]][newPos[1]] == opposite):
                    newPos += way
                # verify move if next is the same
                if self.checkBorder(newPos) and self.board[newPos[0]][newPos[1]] == color:
                    validMove = True;
        return validMove
    
    def checkBorder(self, pos):
        return (pos[0] >= 0 and pos[0] < self.rows and pos[1] >= 0 and pos[1] < self.rows)
    
    def updateBoard(self, move, color):
        # store the current board
        self.olds.append(self.getBoardCopy())
        
        opposite = (bool(color - 1) ^ bool(1)) + 1 
        # check all direction
        for way in self.directions:
            newPos = move + way
            # border checking
            if not self.checkBorder(newPos):
                 continue
            # check this way      
            if (self.board[newPos[0]][newPos[1]] == opposite):
                newPos += way
                # ignore opposites
                while (self.checkBorder(newPos) and self.board[newPos[0]][newPos[1]] == opposite):
                    newPos += way
                # verify move if next is the same
                if self.checkBorder(newPos) and self.board[newPos[0]][newPos[1]] == color:
                    # color flip with backtracking
                    newPos -= way
                    while(not np.array_equal(newPos,move)):
                        self.board[newPos[0]][newPos[1]] = color
                        newPos -= way
                    self.board[newPos[0]][newPos[1]] = color
        
    def getValidMoves(self,color):
        """ returns a vector of moves"""
        moves = []
        for row in range(self.rows):
            for col in range(self.rows):
                move = np.array([row,col])
                if(self.board[row][col] != 0):
                    continue
                if(self.isValidMove(move,color)):
                    moves.append(move)
        return np.array(moves)
    
    def show(self):
        print "   A  B  C  D  E  F  G  H"
        for row in range(self.rows):
            print row,
            for col in range(self.rows):
                if self.board[row][col] == 0:
                    print "| ",
                elif self.board[row][col] == 1:
                    print "|*",
                else:
                    print "|o",
            print "|" 
        sys.stdout.flush()


# In[38]:

class GraphicsMgr:
    def __init__(self, othello):
        self.othello = othello
        self.BOX_HEIGHT = 70
        self.BOX_WIDTH = 70
        self.ROWS = self.othello.board.rows
        self.board = self.othello.board
        self.init()
        
    def init(self):
        self.top = Tkinter.Tk()
        self.top.resizable(0,0)
        self.top.wm_title("Othello")
        self.top.protocol("WM_DELETE_WINDOW", self.quit)
        
        self.level = Tkinter.IntVar()
        self.level2 = Tkinter.IntVar()
        
        self.showBoard()
        self.showMenu()
        
        # bring the window to the front
        self.top.lift()
        self.top.attributes('-topmost', True)
        self.top.attributes('-topmost', 0)
        self.top.focus_force()
        self.top.update()
        
    def getLevel1(self):
        return self.level.get()
    
    def getLevel2(self):
        return self.level2.get()

    def showBoard(self):
        # game canvas
        self.canvas = Tkinter.Canvas(self.top, bg="#46603b", height=560, width=560)
        
        # board lines
        for row in range(1,self.ROWS):
            self.canvas.create_line(0, row*self.BOX_HEIGHT,self.BOX_WIDTH*self.ROWS, row*self.BOX_HEIGHT) 
            self.canvas.create_line(row*self.BOX_WIDTH, 0,row*self.BOX_WIDTH, self.BOX_HEIGHT*self.ROWS)    
        
        # discs
        self.drawDiscs()
        self.canvas.bind("<Button-1>", self.click)
        self.canvas.pack()
    
    def resetBoard(self):
        self.canvas.delete("all")
        for row in range(1,self.ROWS):
            self.canvas.create_line(0, row*self.BOX_HEIGHT,self.BOX_WIDTH*self.ROWS, row*self.BOX_HEIGHT) 
            self.canvas.create_line(row*self.BOX_WIDTH, 0,row*self.BOX_WIDTH, self.BOX_HEIGHT*self.ROWS)    
        
    def showMenu(self):
        
        # message board
        self.message = Tkinter.StringVar()
        Tkinter.Label(self.top, textvariable=self.message).pack()
        
        # buttons
        buttons = Tkinter.Frame(self.top, relief=Tkinter.GROOVE, borderwidth=0)
        buttons.pack(side = Tkinter.LEFT)
        Tkinter.Button(buttons, text="Player vs Player", width=20, command = self.playerMode).pack()
        Tkinter.Button(buttons, text="Player vs CPU", width=20, command = self.cpuMode).pack()
        Tkinter.Button(buttons, text="CPU vs CPU",width=20,  command = self.cpucpuMode).pack()

        # cpu modes
        modes = Tkinter.Frame(self.top, relief=Tkinter.GROOVE, borderwidth=0)
        modes.pack(side = Tkinter.LEFT)
        
        levels = Tkinter.Frame(modes, relief=Tkinter.GROOVE, borderwidth=0)
        levels.pack()
        self.level.set(0)
        Tkinter.Label(levels, text="CPU1 Level",justify = Tkinter.LEFT).pack(side=Tkinter.LEFT)
        for idx, mode in enumerate(['LV.1', 'LV.2', 'LV.3']):
            button = Tkinter.Radiobutton(levels, text=mode, variable=self.level, value=idx, indicatoron=0, command = self.changeLevel1)
            button.pack(pady=5,side=Tkinter.LEFT)
            
        levels2 = Tkinter.Frame(modes, relief=Tkinter.GROOVE, borderwidth=0)
        levels2.pack()
        self.level2.set(0)
        Tkinter.Label(levels2, text="CPU2 Level",justify = Tkinter.LEFT).pack(side=Tkinter.LEFT)
        for idx, mode in enumerate(['LV.1', 'LV.2', 'LV.3']):
            button = Tkinter.Radiobutton(levels2, text=mode, variable=self.level2, value=idx, indicatoron=0, command = self.changeLevel2)
            button.pack(pady=5,side=Tkinter.LEFT)
            
        
        # score board
        scoreframe = Tkinter.Frame(self.top, relief=Tkinter.GROOVE, borderwidth=0)
        scoreframe.pack(side = Tkinter.LEFT)
        self.level.set(0)
        self.score = Tkinter.StringVar()
        Tkinter.Label(scoreframe, textvariable=self.score, font=("Helvetica", 33),width=7).pack()

    def tick(self):
        self.top.update()
        
    def changeLevel1(self):
        if self.othello.player1 != None:
            self.othello.player1.level = self.level.get()
            
    def changeLevel2(self):
        if self.othello.player2 != None:
            self.othello.player2.level = self.level2.get()
        
    def playerMode(self):
        print "Player VS Player MODE"
        self.othello.mode = 0
        self.othello.resetGame = True
        
    def cpuMode(self):
        print "Player VS CPU MODE"
        self.othello.mode = 1
        self.othello.resetGame = True
        
    def cpucpuMode(self):
        print "CPU VS CPU MODE"
        self.othello.mode = 2
        self.othello.resetGame = True
        
    def click(self, event):
        if self.othello.menuMode:
            return
        self.othello.target.moved = True
        self.othello.target.move = np.array([event.y/self.BOX_HEIGHT, event.x/self.BOX_WIDTH])
        self.canvas.focus_set()
        
    def quit(self):
        self.othello.endGame = True
        self.top.destroy()
        
    def drawDiscs(self):
        for row in range(self.ROWS):
            for col in range(self.ROWS):
                color = self.board.get(row,col)
                if color == 1:
                    board_color = "black"
                elif color == 2:
                    board_color = "white"
                else:
                    board_color = None
                    
                if board_color != None:
                    self.canvas.create_oval(col*self.BOX_WIDTH+2, row*self.BOX_HEIGHT+2, (col+1)*self.BOX_WIDTH-2,
                        (row+1)*self.BOX_HEIGHT-2, fill = board_color)
        self.top.update()


# In[39]:

class Othello:
    def __init__(self):
        self.board = Board()
        self.graphicsMgr = GraphicsMgr(self)
        self.player1 = None
        self.player2 = None
        self.target = None
        self.menuMode = False
        self.mode = None
        self.endGame = False
        self.resetGame = False
        self.playerToggle = 0
        self.init()
        
    def init(self):
        pass
        
    def getMenuMode(self):
        """get menu mode from console (for debug)
        """
        menuIDs = [0,1]
        print "Menu:"
        print "[0] Player vs Player"
        print "[1] Player vs CPU"

        num = input("> ");
        while(not num in menuIDs):
            num = input("> ");
        
        return num
    
    def start(self):
        """starts a main game loop
        """
        self.graphicsMgr.message.set("Choose mode and play othello!")
        stat = self.board.getStat()
        self.graphicsMgr.score.set("B%d W%d"%(stat[0],stat[1]))
            
        while not self.endGame:
            self.menuMode = True
            while(self.mode == None and not self.endGame):
                self.graphicsMgr.tick()
            self.menuMode = False
            self.resetGame = False
            
            if self.endGame:
                return
            
            # choose who's first
            sys.stdout.flush()
            self.playerToggle = random.getrandbits(1)
                
            if self.mode == 0:
                self.vsPlayerMode()
            elif self.mode == 1:
                self.vsCPUMode()
            else:
                self.CPUvsCPUMode()
            self.mode = None
            
            self.play()
        
    def vsPlayerMode(self):
        self.player1 = Player("P1",1,self.board)
        self.player2 = Player("P2",2,self.board)
        
    def vsCPUMode(self):
        self.player1 = Player("P1",1,self.board)
        self.player2 = Player("CPU2",2,self.board, True, self.graphicsMgr.getLevel1())
        
    def CPUvsCPUMode(self):
        self.player1 = Player("CPU1",1,self.board, True, self.graphicsMgr.getLevel1())
        self.player2 = Player("CPU2",2,self.board, True, self.graphicsMgr.getLevel2())
    
    def getNextPlayer(self):
        """returns a next player
        """
        if  self.playerToggle == 0:
            self.playerToggle = 1
            return self.player1
        else:
            self.playerToggle = 0
            return self.player2
        
    def play(self):
        """starts to play othello
        """
        print "Game start!"
        self.board.init()
        self.graphicsMgr.resetBoard()
        self.board.show()
        self.graphicsMgr.drawDiscs()
        nomovectr = 0
        
        while(not self.endGame):
            # player turn =================================
            self.target = self.getNextPlayer()
            self.graphicsMgr.message.set("%s(%s)" %(self.target.name,self.target.getColorName()))
            player_turn = True
            self.graphicsMgr.drawDiscs()
            self.target.moves = self.board.getValidMoves(self.target.color)
            stat = self.board.getStat()
            self.graphicsMgr.score.set("B%d W%d"%(stat[0], stat[1]))
            
            # no choce ?
            if(self.target.moves.size == 0):
                player_turn = False
                nomovectr += 1
                # is game end?
                if(nomovectr == 2):
                    if stat[0] > stat[1]:
                        self.graphicsMgr.message.set("Black won!")
                    elif stat[0] == stat[1]:
                        self.graphicsMgr.message.set("Even!")
                    else:
                        self.graphicsMgr.message.set("White won!")
                    break
            else:
                nomovectr = 0
            
            while(player_turn):
                while(not self.target.moved and not self.endGame and not self.resetGame):
                    self.graphicsMgr.tick()
                    
                if(self.endGame or self.resetGame):
                    return
                
                move = self.target.getMove()
                if move == None:
                    self.graphicsMgr.top.bell()
                    continue
                
                self.board.updateBoard(move, self.target.color)
                self.board.show()
                self.graphicsMgr.drawDiscs()
                player_turn = False
            


# In[40]:

import random
class Player:
    # for debug
    nums = {"0","1","2","3","4","5","6","7"}
    alpha = {"A","B","C","D","E","F","G","H"}
    
    def __init__(self, name, color, board, isCpu = False, level = 0):
        """
        name: "Player1" or "Player2"
        color: black(1) or white(2)
        isCpu: True or False
        level: cpu level [0,1,2]
        move: next move
        moves: a set of next valid moves
        moved: Does player choose the next move
        depth: a maximum depth of mini max tree
        """
        self.name = name
        self.color = color
        self.isCpu = isCpu
        self.level = level
        self.move = None
        self.moves = None
        if self.isCpu:
            self.moved = True
        else:
            self.moved = False
        self.depth = 4
        
        self.board = board
        self.minmax = MinMax(self.board)
        
    def setCPULevel(self, level):
        self.cpuLevel = level
        
    def getColorName(self):
        if self.color == 1:
            return "Black"
        elif self.color == 2:
            return "White"
        else:
            return ""
    
    def getMove(self):
        """returns a valid move if possible based on player type,
        assuming that valid moves are already set in moves variable
        and for player a user's move is already set in move variable
        """
        next_move = None
        
        # Player plays
        if self.isCpu == False:
            found = False
            for test in self.moves:
                if(np.array_equal(test,self.move)):
                    found = True
                    break
            if found:
                next_move = self.move
            self.move = None
            self.moved = False
        
        # CPU plays
        else:
            next_move = self.play()
        
        print "%s: %s" %(self.name, str(next_move))
        return next_move
        
    def readInput(self):
        """read input from console (for debug)"""
        string = raw_input("%s: " %(self.name))
        string = list(string)
        row = int(string[0])
        col = ord(string[1]) - ord('A')
        return np.array([row,col])
    
    def randomPlay(self):
        """returns one of the valid moves randomly, 
         assuming that some valid choices are already set in moves
         """
        next_move = random.choice(self.moves)
        return next_move
    
    def play(self):
        """returns a valid move based on CPU level,
        assuming that some valid choices are already set in moves
        """
        if self.level == 0:
            return self.randomPlay()
        elif self.level == 1:
            return self.minmax.getBestMove(self.depth, self.color, self.moves, self.board.getCountScore)
        else:      
            return self.minmax.getBestMove(self.depth, self.color, self.moves, self.board.getPosScore)
        


# In[41]:

class MinMax():
    def __init__(self,board):
        """
        board: Board obj
        """
        self.board = board
        
    def getBestMove(self, depth, current_color, moves, score_func):
        """Assuming there is at least one valid move in moves,
        among them returns the best move using minimax algorithm 
        with alpha beta pruninggiven, given a score function
        """
        # both starts with lowest possible scores
        alpha = None # a value of best move found so far for MAX = -inf
        beta = None  # a value of best move found so far for MIN = +inf
        
        bestmove = None
        maxply_color = (bool(current_color - 1) ^ bool(1)) + 1
        
        for move in moves:
            # self.board.show()
            if alpha is not None:
                beta = -1 * alpha
            
            self.board.updateBoard(move,current_color)
            test = self.getBestMoveHelper(depth-1, maxply_color, 0, score_func, alpha, beta, maxply_color)
            
            if beta == None or test < beta:
                beta = test
                bestmove = move
            self.board.undo() # undo
            
        return bestmove
    
    def getBestMoveHelper(self, depth, current_color, nomovectr, score_func, alpha, beta, maxply_color):
        """returns a heuristic value at the specified depth or the endgame
        """
        next_color = (bool(current_color - 1) ^ bool(1)) + 1
        
        # if depth == 0 or a terminal node (game end)
        # returns the heuristic value of node
        if nomovectr == 2 or depth == 0:
            score = score_func()
            if maxply_color == 2:
                score *= -1
            #print "[L] ========"
            #self.board.show()
            #print "color: %d" % (current_color)
            #print "[L] Score: %d" % (score)
            return score
        
        # is there any possible movement for the player?
        moves = self.board.getValidMoves(current_color)
        
        if moves.size == 0:
            return self.getBestMoveHelper(depth-1, next_color, nomovectr+1, score_func, alpha, beta, maxply_color)
        else:
            for move in moves:
                # self.board.show()
                self.board.updateBoard(move, current_color)
                test = self.getBestMoveHelper(depth-1, next_color, 0, score_func, alpha, beta, maxply_color)
                self.board.undo() # undo
                
                # maxplayer
                if(maxply_color == current_color):
                    if alpha == None or test > alpha:
                        alpha = test
                # minplayer
                else:
                    if beta == None or test < beta:
                        beta = test
                
                #print "color: %d" % (current_color)
                #print "s = %d" % (test)
                #if alpha != None:
                #    print "a = %d" % (alpha)
                #if beta != None:
                #    print "b = %d" % (beta)
                
                # pruning
                if (alpha != None) and (beta != None) and beta <= alpha:
                    # print "pruned!"
                    break
    
        if(maxply_color == current_color):
            return alpha
        return beta


# In[42]:

othello = Othello()
othello.start()


# In[ ]:



