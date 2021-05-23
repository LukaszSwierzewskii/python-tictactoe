"""Sample engine implementation"""
from src.game_engine.board import (
    PositionTakenException,
    WrongPlayerException,
    OutsideBoardException,
)


from src.game_engine.engine import instance
from src.opencv_backend.ui import draw_grid, draw_x, draw_circle, cv



game_started = False
img = cv.imread('red.jpg',0)
draw_grid(img)
while not instance.has_won:
    print(instance.get_board_copy())    
    from_usr = input("Type location and symbol to play (example: 0,0,x):\n").split(",")
    if from_usr[0] == "exit":
        exit(0)
    if len(from_usr) < 2:
        print("input error")
        continue
    from_usr[0] = int(from_usr[0])
    from_usr[1] = int(from_usr[1])
    move = {"coordinates": tuple(from_usr[:2]), "symbol": from_usr[2]}
    drawer = list(move["coordinates"])
    drawer.reverse()
    symbol = move['symbol']

    try:
        instance.make_move(move)
        if symbol == 'x': 
            draw_x(img, drawer)
        else :
            draw_circle(img, drawer)
        cv.imshow('image',img)
        cv.waitKey(400)
    except PositionTakenException:
        print("position is already taken by another symbol")
    except WrongPlayerException:
        print("Not your turn.")
    except OutsideBoardException:
        print("Chosen position is ouside the board")
if instance.winner != "DRAW":
    print(instance.winner + "'s have won")
else:
    print(instance.winner)