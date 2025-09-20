import pygame
import ChessLogic
width = height = 624
square_size = width//8

images = {}
image_size = (square_size,square_size)
GameFPS = 15
black_mated =pygame.transform.smoothscale(pygame.image.load("assets/images/bKm.png"),(square_size,square_size)) 
white_mated =pygame.transform.smoothscale(pygame.image.load("assets/images/wKm.png"),(square_size,square_size)) 
white_check =pygame.transform.smoothscale(pygame.image.load("assets/images/wKc.png"),(square_size,square_size))
black_check =pygame.transform.smoothscale(pygame.image.load("assets/images/bKc.png"),(square_size,square_size))
def LoadImages():
    pieces = ["wP","wN","wB","wR","wQ","wK","bP","bN","bB","bR","bQ","bK"]
    for piece in pieces:
        image_path = "assets/images/" + piece + ".png"
        images[piece] =pygame.transform.smoothscale(pygame.image.load(image_path),image_size)

def main():
    pygame.init()
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Chess Game by Saad Rabia")
    clock = pygame.time.Clock()
    bs = ChessLogic.BoardState()
    font  = pygame.font.Font(None,30)
    ValidMoves = bs.GetValidMoves()
    moveMade = False
    LoadImages()
    running = True
    Square_Selected = ()
    Player_Click = []
    Draging = False
    DragedPiece = ""
    DragedPiecePos = ()
    DragingPos = (0,0)
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                x,y = pygame.mouse.get_pos()
                row = y//square_size
                col = x//square_size
                if bs.board[row][col] !="--":
                    Draging = True
                    DragedPiece = bs.board[row][col]
                    DragedPiecePos = (row,col)
                if Square_Selected == (row, col) and bs.board[row][col] =="--":
                    Square_Selected = ()
                    Player_Click = []
                else :
                    Square_Selected  = (row, col)
                    Player_Click.append(Square_Selected)
                if len(Player_Click) == 2 :
                    move = ChessLogic.Move(Player_Click[0],Player_Click[1],bs.board)
                    for m in ValidMoves:
                        if m == move:
                            bs.MovePiece(m)
                            print(bs.GameMoves[-1].getChessNotation(),end=" ")
                            moveMade = True
                            Square_Selected = ()
                            Player_Click = []
                            break
                        else:
                            Player_Click = [Square_Selected]
            if event.type == pygame.MOUSEBUTTONUP:
                col,row = (DragingPos[0],DragingPos[1])
                if 0<=row<8 and 0<=col<8 and DragedPiecePos:
                    move = ChessLogic.Move(DragedPiecePos,(row,col),bs.board)
                    for m in ValidMoves:
                        if m == move:
                            bs.MovePiece(m)
                            print(bs.GameMoves[-1].getChessNotation(),end=" ")
                            moveMade = True
                            break
                Draging = False
                DragedPiece = ""
                DragedPiecePos = ()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_z:
                    bs.UndoMove()
                    moveMade = True
                elif event.key == pygame.K_y:
                    bs.RedoMove()
                    moveMade = True
        if moveMade:
            ValidMoves = bs.GetValidMoves()
            moveMade = False
        DrawBoardState(screen,font,Square_Selected,DragedPiece,DragedPiecePos,bs) # Draw board state
        DragingPos = DragPiece(screen,Draging,DragedPiece) # for handling drag Piece
        DrawPossiblePieceMoves(screen,bs,Square_Selected,ValidMoves)# Draw possible moves for a piece
        clock.tick(GameFPS)
        pygame.display.flip()
def DrawBoardState(screen,font,Square_Selected,DragedPiece,DragedPiecePos,bs):
    DrawBoard(screen,font) # Draw squares of the board
    HighlightSquare(screen,Square_Selected,bs) #  Highligh the Square
    HighlightMove(screen,bs)#Highligh the move
    DrawPieces(screen,DragedPiece,DragedPiecePos,bs.board) # Draw pieces in the board
    DrawOncheck(screen,bs)
def DrawOncheck(screen,bs):
    if bs.winner == "White":
        screen.blit(black_mated,(bs.BlackKingPos[1]*square_size,bs.BlackKingPos[0]*square_size))
    elif bs.winner == "Black":
        screen.blit(white_mated,(bs.WhiteKingPos[1]*square_size,bs.WhiteKingPos[0]*square_size))
    elif bs.WhiteOncheck:
        screen.blit(white_check,(bs.WhiteKingPos[1]*square_size,bs.WhiteKingPos[0]*square_size))
    elif bs.BlackOncheck:
        screen.blit(black_check,(bs.BlackKingPos[1]*square_size,bs.BlackKingPos[0]*square_size))
def DrawBoard(screen,font):
    colors = ["#EEEED2","#769656"]
    #colors = ["#b58763", "#f0dab5"]
    #colors = ["grey", "white"]
    for row in range(8):
        for col in range(8):
            color = colors[(row+col) %2]
            pygame.draw.rect(screen,color,(col*square_size,row*square_size,square_size,square_size))
            if row == 7:
                color = 1 if (row+col) %2 == 0 else 0
                text = font.render(chr(col+97),True,colors[color])
                screen.blit(text,(col*square_size+square_size-14,row*square_size+square_size-20)) 
        color = 1 if (row) %2 == 0 else 0
        text = font.render(str(8-row),True,colors[color])
        screen.blit(text,(2,row*square_size))
def DrawPieces(screen,DragedPiece,DragedPiecePos,board):
    for row in range(8):
        for col in range(8):
            if board[row][col] != "--" :
                piece = board[row][col]
                if piece != DragedPiece or (row,col) != DragedPiecePos:
                    screen.blit(images[piece],(col*square_size,row*square_size))
def HighlightMove(screen,bs):
    if bs.GameMoves:
        move = bs.GameMoves[-1]
        transparent_screen  = pygame.Surface((width,height),pygame.SRCALPHA)
        pygame.draw.rect(transparent_screen,(255,79,0,70),(move.startCol*square_size,move.startRow*square_size,square_size,square_size))
        pygame.draw.rect(transparent_screen,(255,79,0,70),(move.targetCol*square_size,move.targetRow*square_size,square_size,square_size))
        screen.blit(transparent_screen,(0,0))
def HighlightSquare(screen,Square_Selected,bs):
    if len(Square_Selected) != 0 and bs.board[Square_Selected[0]][Square_Selected[1]] != "--":
            transparent_screen  = pygame.Surface((width,height),pygame.SRCALPHA)
            pygame.draw.rect(transparent_screen,(255,79,0,70),(Square_Selected[1]*square_size,Square_Selected[0]*square_size,square_size,square_size))
            screen.blit(transparent_screen,(0,0))
def DrawPossiblePieceMoves(screen,bs,Square_Selected,ValidMoves):
    if Square_Selected :
        if bs.board[Square_Selected[0]][Square_Selected[1]] != "--":
            piece = bs.board[Square_Selected[0]][Square_Selected[1]]
            for move in ValidMoves:
                if move.PieceMoved == piece and move.startRow == Square_Selected[0] and move.startCol == Square_Selected[1]:
                    transparent_screen  = pygame.Surface((width,height),pygame.SRCALPHA)
                    if (move.PieceCaptured =="--" and not move.isEnPassant):
                        pygame.draw.circle(transparent_screen,(0,0,0,30),(move.targetCol*square_size+square_size//2,move.targetRow*square_size+square_size//2),square_size//4)
                    else :
                        pygame.draw.circle(transparent_screen,(0,0,0,30),(move.targetCol*square_size+square_size//2,move.targetRow*square_size+square_size//2),square_size//2,6)
                    screen.blit(transparent_screen,(0,0))
                    #pygame.draw.rect(screen,"light grey",(move.targetCol*square_size,move.targetRow*square_size,square_size,square_size))
    

def DragPiece(screen,Draging,DragedPiece):
    if Draging:
            transparent_screen  = pygame.Surface((width,height),pygame.SRCALPHA)
            x,y = pygame.mouse.get_pos()
            row,col = (x,y)
            ScalImage = pygame.transform.smoothscale(images[DragedPiece],(square_size,square_size))
            screen.blit(ScalImage,(row-square_size//2,col-square_size//2))
            DragingPos = (row//square_size,col//square_size)
            """zzpygame.draw.circle(transparent_screen,(0,0,0,70),(DragingPos[0]*square_size+square_size//2,DragingPos[1]*square_size+square_size//2),square_size*0.75)
            screen.blit(transparent_screen,(0,0))"""
            return DragingPos
    return (0,0)



if __name__ == "__main__":
    main()