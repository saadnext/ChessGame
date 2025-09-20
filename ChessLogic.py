"""
Responslabe for handling chess logic
"

import pygame
import copy
pygame.init()
class BoardState():
    def __init__(self):
        self.board = [
            ["bR","bN","bB","bQ","bK","bB","bN","bR"],
            ["bP","bP","bP","bP","bP","bP","bP","bP"],
            ["--","--","--","--","--","--","--","--"],
            ["--","--","--","--","--","--","--","--"],
            ["--","--","--","--","--","--","--","--"],
            ["--","--","--","--","--","--","--","--"],
            ["wP","wP","wP","wP","wP","wP","wP","wP"],
            ["wR","wN","wB","wQ","wK","wB","wN","wR"]
        ]
        self.MoveSound = pygame.mixer.Sound("assets/sounds/move_piece.mp3")
        self.CaptureSound = pygame.mixer.Sound("assets/sounds/capture_piece.mp3")
        self.check_sound = pygame.mixer.Sound("assets/sounds/move-check.mp3")  
        self.castle_sound = pygame.mixer.Sound("assets/sounds/castle.mp3")  
        self.WhiteToMove = True
        self.GameMoves = []
        self.RedoMoves = []
        self.WhiteKingPos = (7,4)
        self.hasWhiteKingMove = False
        self.hasBlackKingMove = False
        self.hasWhiteRightRookMove = False
        self.hasWhiteLeftRookMove = False
        self.hasBlackRightRookMove = False
        self.hasBlackLeftRookMove = False
        self.WhiteShortCastle = False
        self.WhiteLongCastle = False
        self.BlackShortCastle = False
        self.BlackLongCastle = False
        self.BlackKingPos = (0,4)
        self.CheckMate = False
        self.StaleMate = False
        self.winner = None
        self.WhiteOncheck = False
        self.BlackOncheck = False
    def MovePiece(self, move):
        #self.isKingOnCheck(move)
       
        if  (move.targetRow,move.targetCol) == (7,6) and move.PieceMoved == "wK":
            self.WhiteShortCastle = True
            self.board[7][7] = "--"   
            self.board[7][5] = "wR"
        elif  (move.targetRow,move.targetCol) == (7,2) and move.PieceMoved == "wK":
            self.WhiteLongCastle = True
            self.board[7][0] = "--"   
            self.board[7][3] = "wR"
        elif (move.targetRow,move.targetCol) == (0,6) and move.PieceMoved == "bK":
            self.BlackShortCastle = True
            self.board[0][7] = "--"   
            self.board[0][5] = "bR"
        elif (move.targetRow,move.targetCol) == (0,2) and move.PieceMoved == "bK":
            self.BlackLongCastle = True
            self.board[0][0] = "--"   
            self.board[0][3] = "bR"
        self.board[move.startRow][move.startCol] = "--"
        if move.isEnPassant:
            self.board[self.GameMoves[-1].targetRow][self.GameMoves[-1].targetCol] = "--" 
        if move.PieceMoved[1] == "P"  and( move.startRow == 1 and move.targetRow == 0 or  move.startRow == 6 and move.targetRow == 7):
            if move.PieceMoved[0] == "w" and move.startRow == 1 and move.targetRow == 0:
                self.board[move.targetRow][move.targetCol] = "wQ"
            elif move.PieceMoved[0] == "b" and move.startRow == 6 and move.targetRow == 7:
                self.board[move.targetRow][move.targetCol] = "bQ"
        else:
            self.board[move.targetRow][move.targetCol] = move.PieceMoved
        self.GameMoves.append(move)
        self.WhiteToMove = not self.WhiteToMove
        self.RedoMoves.clear()
        self.HandleSoundEffect(move)
        if move.PieceMoved == "wK":
            self.WhiteKingPos = (move.targetRow, move.targetCol)
            self.hasWhiteKingMove = True
        elif move.PieceMoved == "bK":
            self.BlackKingPos = (move.targetRow, move.targetCol)
            self.hasBlackKingMove = True
        
    def UndoMove(self):
        if self.GameMoves:
            lastMove = self.GameMoves.pop()
            #self.isKingOnCheck(Move((lastMove.targetRow, lastMove.targetCol),(lastMove.startRow, lastMove.startCol),self.board))
            self.RedoMoves.append(lastMove)
            if  (lastMove.targetRow,lastMove.targetCol) == (7,6) and lastMove.PieceMoved == "wK":
                self.WhiteShortCastle = True
                self.board[7][5] = "--"
                self.board[7][7] = "wR"
            elif (lastMove.targetRow,lastMove.targetCol) == (7,2) and lastMove.PieceMoved == "wK":
                self.WhiteLongCastle = True
                self.board[7][0] = "wR"   
                self.board[7][3] = "--"
            elif (lastMove.targetRow,lastMove.targetCol) == (0,6) and lastMove.PieceMoved == "bK":
                self.BlackShortCastle = True
                self.board[0][7] = "bR"   
                self.board[0][5] = "--"
            elif (lastMove.targetRow,lastMove.targetCol) == (0,2) and lastMove.PieceMoved == "bK":
                self.BlackLongCastle = True
                self.board[0][0] = "bR"   
                self.board[0][3] = "--"
            if lastMove.isEnPassant :
                self.board[lastMove.targetRow][lastMove.targetCol] = "--" 
                self.board[lastMove.startRow][lastMove.startCol] = lastMove.PieceMoved
                if lastMove.PieceCaptured == "bP":
                    self.board[lastMove.targetRow+1][lastMove.targetCol] = lastMove.PieceCaptured 
                else:
                    self.board[lastMove.targetRow-1][lastMove.targetCol] = lastMove.PieceCaptured 
            else:
                self.board[lastMove.startRow][lastMove.startCol] = lastMove.PieceMoved
                self.board[lastMove.targetRow][lastMove.targetCol] = lastMove.PieceCaptured
            if lastMove.PieceMoved == "wK":
                self.WhiteKingPos = (lastMove.targetRow, lastMove.targetCol)
                self.hasWhiteKingMove = not self.hasWhiteKingMove
            elif lastMove.PieceMoved == "bK":
                self.BlackKingPos = (lastMove.targetRow, lastMove.targetCol)
                self.hasBlackKingMove = not self.hasBlackKingMove
            self.WhiteToMove = not self.WhiteToMove
            self.winner = None
            self.HandleSoundEffect(lastMove)
    def RedoMove(self):
        if self.RedoMoves:
            lastMove = self.RedoMoves.pop()
            #self.isKingOnCheck(lastMove)

            if  (lastMove.targetRow,lastMove.targetCol) == (7,6) and lastMove.PieceMoved == "wK":
                self.WhiteShortCastle = True
                self.board[7][7] = "--"   
                self.board[7][5] = "wR"
            elif (lastMove.targetRow,lastMove.targetCol) == (7,2) and lastMove.PieceMoved == "wK":
                self.WhiteLongCastle = True
                self.board[7][0] = "--"   
                self.board[7][3] = "wR"
            elif  (lastMove.targetRow,lastMove.targetCol) == (0,6) and lastMove.PieceMoved == "bK":
                self.BlackShortCastle = True
                self.board[0][7] = "--"   
                self.board[0][5] = "bR"
            elif (lastMove.targetRow,lastMove.targetCol) == (0,2) and lastMove.PieceMoved == "bK":
                self.BlackLongCastle = True
                self.board[0][0] = "--"   
                self.board[0][3] = "bR"
            if lastMove.isEnPassant:
                self.board[lastMove.targetRow][lastMove.targetCol] = "--"
                if lastMove.PieceCaptured == "bP":
                    self.board[lastMove.targetRow+1][lastMove.targetCol] ="--"
                else:
                    self.board[lastMove.targetRow-1][lastMove.targetCol] = "--"
            
            # Move the piece again
            self.board[lastMove.startRow][lastMove.startCol] = "--"
            if lastMove.PieceMoved[1] == "P"  and( lastMove.startRow == 1 and lastMove.targetRow == 0 or  lastMove.startRow == 6 and lastMove.targetRow == 7):
                if lastMove.PieceMoved[0] == "w" and lastMove.startRow == 1 and lastMove.targetRow == 0:
                    self.board[lastMove.targetRow][lastMove.targetCol] = "wQ"
                elif lastMove.PieceMoved[0] == "b" and lastMove.startRow == 6 and lastMove.targetRow == 7:
                    self.board[lastMove.targetRow][lastMove.targetCol] = "bQ"
            else:
                self.board[lastMove.targetRow][lastMove.targetCol] = lastMove.PieceMoved

            # 🔥 Add move back to GameMoves 🔥
            self.GameMoves.append(lastMove)

            # Toggle turn
            self.WhiteToMove = not self.WhiteToMove
            self.winner = None
            self.HandleSoundEffect(lastMove)
            if lastMove.PieceMoved == "wK":
                self.WhiteKingPos = (lastMove.targetRow, lastMove.targetCol)
                self.hasWhiteKingMove = not self.hasWhiteKingMove
            elif lastMove.PieceMoved == "bK":
                self.BlackKingPos = (lastMove.targetRow, lastMove.targetCol)
                self.hasBlackKingMove = not self.hasBlackKingMove
    def GetValidMoves(self):
        moves = self.GetAllPossibleMoves()
        for i in range(len(moves)-1,-1,-1):
            if self.isKingUnderAttack(moves[i]):
                moves.remove(moves[i])
                if len(moves) == 0:
                    self.CheckMate = True
                    self.winner  = "Black" if self.WhiteToMove else "White"
                    break
            else:
                if len(moves) == 0:
                    self.StaleMate == True
                    break
        return moves
    def isKingUnderAttack(self,move,testing=True):
        board_copy,king_pos = self.simulateMove(move)
        KingUnderAttackByBishop = self.doseKingUnderAttack(board_copy,king_pos,"B")
        KingUnderAttackByBishop = self.doseKingUnderAttack(board_copy,king_pos,"B")
        KingUnderAttackByRook =self.doseKingUnderAttack(board_copy,king_pos,"R")
        KingUnderAttackByKnight = self.doseKingUnderAttack(board_copy,king_pos,"N")
        KingUnderAttackByPawn =self.doseKingUnderAttack(board_copy,king_pos,"P")
        KingUnderAttackByKing =self.doseKingUnderAttack(board_copy,king_pos,"K")
        isKingOnCheck = (KingUnderAttackByBishop or KingUnderAttackByRook or KingUnderAttackByKnight or KingUnderAttackByPawn or  KingUnderAttackByKing  )
        return isKingOnCheck
    def doseKingUnderAttack(self,board_copy,king_pos,enemy_piece):
        AllyColor = "w" if self.WhiteToMove else "b"
        EnemyColor = "b" if self.WhiteToMove else "w"
        if enemy_piece == "B":
            Directions =((1,1),(-1,-1),(-1,1),(1,-1))
            for dir in Directions:
                for d in range(1,8):
                    row = king_pos[0] + dir[0]*d
                    col  = king_pos[1] +  dir[1]*d
                    if 0<=row<8 and 0<=col<8:
                        if board_copy[row][col] == EnemyColor+ "B" or board_copy[row][col]== EnemyColor+  "Q":
                            print(EnemyColor)
                            return True
                        elif board_copy[row][col] !="--":
                            break
            return False
        elif enemy_piece == "R":
            Directions =((1,0),(-1,0),(0,1),(0,-1))
            for dir in Directions:
                for d in range(1,8):
                    row = king_pos[0] + dir[0]*d
                    col  = king_pos[1] +  dir[1]*d
                    if 0<=row<8 and 0<=col<8:
                        if board_copy[row][col] == EnemyColor+ "R" or board_copy[row][col]== EnemyColor+  "Q":
                            return True
                        elif board_copy[row][col] !="--":
                            break
            return False
        elif enemy_piece == "N":
            Directions =((2,1),(2,-1),(-2,1),(-2,-1),(1,2),(-1,2),(1,-2),(-1,-2))
            for dir in Directions:
                row = king_pos[0] + dir[0]
                col  = king_pos[1] +  dir[1]
                if 0<=row<8 and 0<=col<8:
                    if board_copy[row][col] == EnemyColor+ "N":
                        return True
            return False
        elif enemy_piece == "P":
            Directions =((-1,-1),(-1,1)) if self.WhiteToMove else ((1,1),(1,-1))
            for dir in Directions:
                row = king_pos[0] + dir[0]
                col  = king_pos[1] +  dir[1]
                if 0<=row<8 and 0<=col<8:
                    if board_copy[row][col] == EnemyColor+ "P":
                        return True
        elif enemy_piece == "K":
            Directions = ((1,0),(-1,0),(0,1),(0,-1),(1,1),(-1,-1),(-1,1),(1,-1))
            for dir in Directions:
                row = king_pos[0] + dir[0]
                col  = king_pos[1] +  dir[1]
                if 0<=row<8 and 0<=col<8:
                    if board_copy[row][col] == EnemyColor+ "K":
                        return True
            return False
    def simulateMove(self, move):
        board_copy = copy.deepcopy(self.board)
        king_pos = self.WhiteKingPos if self.WhiteToMove else self.BlackKingPos
        board_copy[move.startRow][move.startCol] = "--"
        if move.isEnPassant:
            board_copy[self.GameMoves[-1].targetRow][self.GameMoves[-1].targetCol] = "--"
        board_copy[move.targetRow][move.targetCol] = move.PieceMoved
        if move.PieceMoved[1] == "K":
            king_pos = (move.targetRow,move.targetCol)
        return board_copy,king_pos
    def HandleSoundEffect(self,move):
        """elif self.isKingUnderAttack(self.GameMoves[-1]) :
            self.check_sound.play()
            if self.WhiteToMove:
                self.WhiteOncheck = True
            else:
                self.BlackOncheck = True"""
        if self.WhiteShortCastle or self.WhiteLongCastle or self.BlackShortCastle or self.BlackLongCastle:
            if self.WhiteShortCastle:
                self.WhiteShortCastle = False
            if self.WhiteLongCastle:
                self.WhiteLongCastle = False
            if self.BlackShortCastle:
                self.BlackShortCastle = False
            if self.BlackLongCastle:
                self.BlackLongCastle = False
            self.castle_sound.play()
        elif move.PieceCaptured !="--":
            self.CaptureSound.play()
        else:
            self.MoveSound.play()
            self.WhiteOncheck = False
            self.BlackOncheck = False
    def GetAllPossibleMoves(self):
        moves = []
        pieces = {
            'P': self.getPawnsMoves,
            'N': self.getKnightMoves,
            'B': self.getBishopMoves,
            'R': self.getRookMoves,
            'Q': self.getQueenMoves,
            'K': self.getKingMoves,

        }
        for row in range(8):
            for col in range(8):
                color = self.board[row][col][0]
                if (color =='w' and self.WhiteToMove) or (color =='b' and not self.WhiteToMove):
                    piece = self.board[row][col][1]
                    pieces[piece](row,col,moves)#Get possible moves for the piece
        return moves
    def getPawnsMoves(self,row,col,moves):
        if self.WhiteToMove:#white pawns moves
            if self.board[row-1][col] == "--":#1 square advance
                moves.append(Move((row,col),(row-1,col),self.board))
                if row == 6 and self.board[row-2][col] == "--": #2 squares advence
                    moves.append(Move((row,col),(row-2,col),self.board))
            #White caputers
            if col >0: #Captures to left
                if self.board[row-1][col-1][0] == 'b':
                    moves.append(Move((row,col),(row-1,col-1),self.board))
                if self.GameMoves:
                    if self.GameMoves[-1].PieceMoved == "bP" and  self.GameMoves[-1].startRow == 1 and  self.GameMoves[-1].targetRow == 3 and  self.GameMoves[-1].targetCol == col -1 and self.GameMoves[-1].targetRow == row:
                        moves.append(Move((row,col),(row-1,col-1),self.board,isEnPassant = True))
            if col < 7: #Captures to right
                if self.board[row-1][col+1][0] == 'b':
                    moves.append(Move((row,col),(row-1,col+1),self.board))
                if self.GameMoves:
                    if self.GameMoves[-1].PieceMoved == "bP" and  self.GameMoves[-1].startRow == 1 and  self.GameMoves[-1].targetRow == 3 and  self.GameMoves[-1].targetCol == col +1 and self.GameMoves[-1].targetRow == row:
                        moves.append(Move((row,col),(row-1,col+1),self.board,isEnPassant = True))
        else:#black pawns moves
            if self.board[row+1][col] == "--":#1 square advance
                moves.append(Move((row,col),(row+1,col),self.board))
                if row == 1 and self.board[row+2][col] == "--":#2 square advance
                    moves.append(Move((row,col),(row+2,col),self.board))
            #Black caputers
            if col >0: #Captures to left
                if self.board[row+1][col-1][0] == 'w':
                    moves.append(Move((row,col),(row+1,col-1),self.board))
                if self.GameMoves:
                    if self.GameMoves[-1].PieceMoved == "wP" and self.GameMoves[-1].startRow == 6 and  self.GameMoves[-1].targetRow == 4 and self.GameMoves[-1].targetCol == col -1  and self.GameMoves[-1].targetRow == row:
                        moves.append(Move((row,col),(row+1,col-1),self.board,isEnPassant = True))
            if col < 7: #Captures to right
                if self.board[row+1][col+1][0] == 'w':
                    moves.append(Move((row,col),(row+1,col+1),self.board))
                if self.GameMoves:
                    if self.GameMoves[-1].PieceMoved == "wP" and self.GameMoves[-1].startRow == 6 and self.GameMoves[-1].targetRow == 4 and self.GameMoves[-1].targetCol == col +1 and self.GameMoves[-1].targetRow == row:
                        moves.append(Move((row,col),(row+1,col+1),self.board,isEnPassant = True))
        return moves
    def getKnightMoves(self,row,col,moves):
        knightDirections = ((2,1),(2,-1),(-2,1),(-2,-1),(1,2),(-1,2),(1,-2),(-1,-2))
        AllyColor = 'w' if self.WhiteToMove else 'b'
        for direction in knightDirections:
            targetRow = row + direction[0]
            targetCol = col + direction[1]
            if 0<=targetRow<8 and 0<=targetCol<8 : #square is on the board
                targetSquare = self.board[targetRow][targetCol]
                if targetSquare[0] != AllyColor:
                    moves.append(Move((row,col),(targetRow,targetCol),self.board))
                    

        return moves
        
    def getBishopMoves(self,row,col,moves):
        BishopDirections = ((1,1),(-1,-1),(-1,1),(1,-1))
        enemyColor = 'b' if self.WhiteToMove else 'w'
        for direction in BishopDirections:
            for distance in range(1,8):
                targetRow = row + direction[0]*distance
                targetCol = col + direction[1]*distance
                if 0<=targetRow<8 and 0<=targetCol<8 : #square is on the board
                    targetSquare = self.board[targetRow][targetCol]
                    if targetSquare == "--": #empty square (move is possible)
                        moves.append(Move((row,col),(targetRow,targetCol),self.board))
                    elif targetSquare[0] == enemyColor:#enemy piece is on the target square
                        moves.append(Move((row,col),(targetRow,targetCol),self.board))
                        break
                    else: 
                        break
                else:
                    break
        return moves
    def getRookMoves(self,row,col,moves):
        RookDirections = ((1,0),(-1,0),(0,1),(0,-1))
        enemyColor = 'b' if self.WhiteToMove else 'w'
        for direction in RookDirections:
            for distance in range(1,8):
                targetRow = row + direction[0]*distance
                targetCol = col + direction[1]*distance
                if 0<=targetRow<8 and 0<=targetCol<8 : #square is on the board
                    targetSquare = self.board[targetRow][targetCol]
                    if targetSquare == "--": #empty square (move is possible)
                        moves.append(Move((row,col),(targetRow,targetCol),self.board))
                    elif targetSquare[0] == enemyColor:#enemy piece is on the target square
                        moves.append(Move((row,col),(targetRow,targetCol),self.board))
                        break
                    else: 
                        break
                else:
                    break
        return moves
    def getQueenMoves(self,row,col,moves):
        self.getRookMoves(row,col,moves)
        self.getBishopMoves(row,col,moves)
    def getKingMoves(self,row,col,moves):
        KingDirections = ((1,0),(-1,0),(0,1),(0,-1),(1,1),(-1,-1),(-1,1),(1,-1))
        AllyColor = 'w' if self.WhiteToMove else 'b'
        for direction in KingDirections:
            targetRow = row + direction[0]
            targetCol = col + direction[1]
            if 0<=targetRow<8 and 0<=targetCol<8 : #square is on the board
                targetSquare = self.board[targetRow][targetCol]
                if targetSquare[0] !=AllyColor:
                    moves.append(Move((row,col),(targetRow,targetCol),self.board))
        if self.WhiteToMove and not self.hasWhiteKingMove and not self.WhiteOncheck:
            if self.board[7][5] =="--" and self.board[7][6] =="--":
                if not self.hasWhiteRightRookMove and  not self.isKingUnderAttack(Move((row,col),(row,5),self.board),testing=False):
                    moves.append(Move((row,col),(row,6),self.board))
                else:
                    self.WhiteShortCastle = False
            else:
                self.WhiteShortCastle = False
            if self.board[7][3] =="--" and self.board[7][2] =="--" and self.board[7][1] =="--":
                if not self.hasWhiteLeftRookMove and not self.isKingUnderAttack(Move((row,col),(row,3),self.board),testing=False):
                    moves.append(Move((row,col),(row,2),self.board))
                else:
                    self.WhiteLongCastle = False
            else:
                self.WhiteLongCastle= False
        elif not self.WhiteToMove and not self.hasBlackKingMove and not self.BlackOncheck:
            if self.board[0][5] =="--" and self.board[0][6] =="--":
                if not self.hasBlackRightRookMove and  not self.isKingUnderAttack(Move((row,col),(row,5),self.board),testing=False):
                    moves.append(Move((row,col),(row,6),self.board))
                else:
                    self.BlackShortCastle = False
            else:
                self.BlackShortCastle = False
            if self.board[0][3] =="--" and self.board[0][2] =="--" and  self.board[0][1] =="--":
                if not self.hasBlackLeftRookMove and not self.isKingUnderAttack(Move((row,col),(row,3),self.board),testing=False):
                    moves.append(Move((row,col),(row,2),self.board))
                else:
                    self.BlackLongCastle = False
            else:
                self.BlackLongCastle= False

    def isKingOnCheck(self,move):
        self.WhiteToMove = not self.WhiteToMove
        isOnCheck = self.isKingUnderAttack(move)
        self.WhiteToMove = not self.WhiteToMove
        if isOnCheck:
            if self.WhiteToMove:
                self.BlackOncheck = True
            else:
                self.WhiteOncheck = True
        else:
            self.WhiteOncheck = False
            self.BlackOncheck = False


class Move():
    def __init__(self,startSq,targetSq,board,isEnPassant = False):
        self.bs = BoardState()
        self.startRow = startSq[0]
        self.startCol = startSq[1]
        self.targetRow = targetSq[0]
        self.targetCol = targetSq[1]
        self.PieceMoved = board[self.startRow][self.startCol]
        self.PieceCaptured = board[self.targetRow][self.targetCol]
        self.MoveId = self.startRow*1000 + self.startCol*100  + self.targetRow*10 + self.targetCol
        self.isEnPassant = isEnPassant # Fix here
        if isEnPassant:
            self.PieceCaptured = "bP" if self.bs.WhiteToMove else "wP"
    def __eq__(self, value):
        if isinstance(value,Move):
            return self.MoveId == value.MoveId
        return False
    def getChessNotation(self):
        startRowNotation = str(8 - self.startRow)
        targetRowNotation = str(8 - self.targetRow)
        startColNotation = chr(self.startCol + 97)
        targetColNotation = chr(self.targetCol + 97)
        MoveNotation = startColNotation + startRowNotation + targetColNotation + targetRowNotation

        return MoveNotation
