NOTATION_TO_POS_HINT = {
            'a8': (0, .875), 'b8': (.125, .875), 'c8': (.250, .875), 'd8': (.375, .875), 'e8': (.500, .875), 'f8': (.625, .875), 'g8': (.750, .875), 'h8': (.875, .875),
            'a7': (0, .750), 'b7': (.125, .750), 'c7': (.250, .750), 'd7': (.375, .750), 'e7': (.500, .750), 'f7': (.625, .750), 'g7': (.750, .750), 'h7': (.875, .750),
            'a6': (0, .625), 'b6': (.125, .625), 'c6': (.250, .625), 'd6': (.375, .625), 'e6': (.500, .625), 'f6': (.625, .625), 'g6': (.750, .625), 'h6': (.875, .625),
            'a5': (0, .500), 'b5': (.125, .500), 'c5': (.250, .500), 'd5': (.375, .500), 'e5': (.500, .500), 'f5': (.625, .500), 'g5': (.750, .500), 'h5': (.875, .500),
            'a4': (0, .375), 'b4': (.125, .375), 'c4': (.250, .375), 'd4': (.375, .375), 'e4': (.500, .375), 'f4': (.625, .375), 'g4': (.750, .375), 'h4': (.875, .375),
            'a3': (0, .250), 'b3': (.125, .250), 'c3': (.250, .250), 'd3': (.375, .250), 'e3': (.500, .250), 'f3': (.625, .250), 'g3': (.750, .250), 'h3': (.875, .250),
            'a2': (0, .125), 'b2': (.125, .125), 'c2': (.250, .125), 'd2': (.375, .125), 'e2': (.500, .125), 'f2': (.625, .125), 'g2': (.750, .125), 'h2': (.875, .125),
            'a1': (0, 0), 'b1': (.125, 0), 'c1': (.250, 0), 'd1': (.375, 0), 'e1': (.500, 0), 'f1': (.625, 0), 'g1': (.750, 0), 'h1': (.875, 0)
}
NOTATION_TO_POS_HINT_FLIPPED = {
            'h1': (0, .875), 'g1': (.125, .875), 'f1': (.250, .875), 'e1': (.375, .875), 'd1': (.500, .875), 'c1': (.625, .875), 'b1': (.750, .875), 'a1': (.875, .875),
            'h2': (0, .750), 'g2': (.125, .750), 'f2': (.250, .750), 'e2': (.375, .750), 'd2': (.500, .750), 'c2': (.625, .750), 'b2': (.750, .750), 'a2': (.875, .750),
            'h3': (0, .625), 'g3': (.125, .625), 'f3': (.250, .625), 'e3': (.375, .625), 'd3': (.500, .625), 'c3': (.625, .625), 'b3': (.750, .625), 'a3': (.875, .625),
            'h4': (0, .500), 'g4': (.125, .500), 'f4': (.250, .500), 'e4': (.375, .500), 'd4': (.500, .500), 'c4': (.625, .500), 'b4': (.750, .500), 'a4': (.875, .500),
            'h5': (0, .375), 'g5': (.125, .375), 'f5': (.250, .375), 'e5': (.375, .375), 'd5': (.500, .375), 'c5': (.625, .375), 'b5': (.750, .375), 'a5': (.875, .375),
            'h6': (0, .250), 'g6': (.125, .250), 'f6': (.250, .250), 'e6': (.375, .250), 'd6': (.500, .250), 'c6': (.625, .250), 'b6': (.750, .250), 'a6': (.875, .250),
            'h7': (0, .125), 'g7': (.125, .125), 'f7': (.250, .125), 'e7': (.375, .125), 'd7': (.500, .125), 'c7': (.625, .125), 'b7': (.750, .125), 'a7': (.875, .125),
            'h8': (0, 0), 'g8': (.125, 0), 'f8': (.250, 0), 'e8': (.375, 0), 'd8': (.500, 0), 'c8': (.625, 0), 'b8': (.750, 0), 'a8': (.875, 0)
}
NOTATION_TO_GAME_STATE = {
            'a8': (0, 0), 'b8': (0, 1), 'c8': (0, 2), 'd8': (0, 3), 'e8': (0, 4), 'f8': (0, 5), 'g8': (0, 6), 'h8': (0, 7),
            'a7': (1, 0), 'b7': (1, 1), 'c7': (1, 2), 'd7': (1, 3), 'e7': (1, 4), 'f7': (1, 5), 'g7': (1, 6), 'h7': (1, 7),
            'a6': (2, 0), 'b6': (2, 1), 'c6': (2, 2), 'd6': (2, 3), 'e6': (2, 4), 'f6': (2, 5), 'g6': (2, 6), 'h6': (2, 7),
            'a5': (3, 0), 'b5': (3, 1), 'c5': (3, 2), 'd5': (3, 3), 'e5': (3, 4), 'f5': (3, 5), 'g5': (3, 6), 'h5': (3, 7),
            'a4': (4, 0), 'b4': (4, 1), 'c4': (4, 2), 'd4': (4, 3), 'e4': (4, 4), 'f4': (4, 5), 'g4': (4, 6), 'h4': (4, 7),
            'a3': (5, 0), 'b3': (5, 1), 'c3': (5, 2), 'd3': (5, 3), 'e3': (5, 4), 'f3': (5, 5), 'g3': (5, 6), 'h3': (5, 7),
            'a2': (6, 0), 'b2': (6, 1), 'c2': (6, 2), 'd2': (6, 3), 'e2': (6, 4), 'f2': (6, 5), 'g2': (6, 6), 'h2': (6, 7),
            'a1': (7, 0), 'b1': (7, 1), 'c1': (7, 2), 'd1': (7, 3), 'e1': (7, 4), 'f1': (7, 5), 'g1': (7, 6), 'h1': (7, 7)
}

NOTATION_TO_GAME_STATE_FLIPPED = {
            'h1': (0, 0), 'g1': (0, 1), 'f1': (0, 2), 'e1': (0, 3), 'd1': (0, 4), 'c1': (0, 5), 'b1': (0, 6), 'a1': (0, 7),
            'h2': (1, 0), 'g2': (1, 1), 'f2': (1, 2), 'e2': (1, 3), 'd2': (1, 4), 'c2': (1, 5), 'b2': (1, 6), 'a2': (1, 7),
            'h3': (2, 0), 'g3': (2, 1), 'f3': (2, 2), 'e3': (2, 3), 'd3': (2, 4), 'c3': (2, 5), 'b3': (2, 6), 'a3': (2, 7),
            'h4': (3, 0), 'g4': (3, 1), 'f4': (3, 2), 'e4': (3, 3), 'd4': (3, 4), 'c4': (3, 5), 'b4': (3, 6), 'a4': (3, 7),
            'h5': (4, 0), 'g5': (4, 1), 'f5': (4, 2), 'e5': (4, 3), 'd5': (4, 4), 'c5': (4, 5), 'b5': (4, 6), 'a5': (4, 7),
            'h6': (5, 0), 'g6': (5, 1), 'f6': (5, 2), 'e6': (5, 3), 'd6': (5, 4), 'c6': (5, 5), 'b6': (5, 6), 'a6': (5, 7),
            'h7': (6, 0), 'g7': (6, 1), 'f7': (6, 2), 'e7': (6, 3), 'd7': (6, 4), 'c7': (6, 5), 'b7': (6, 6), 'a7': (6, 7),
            'h8': (7, 0), 'g8': (7, 1), 'f8': (7, 2), 'e8': (7, 3), 'd8': (7, 4), 'c8': (7, 5), 'b8': (7, 6), 'a8': (7, 7)
}

RANKS = {
    "1": '8', "2": '7', "3": '6', "4": '5', "5": '4', "6": '3', "7": '2', "8": '1'
}
FILES = {
    "a": 'h', "b": 'g', "c": 'f', "d": 'e', "e": 'd', "f": 'c', "g": 'b', "h": 'a'
}

POS_HINT_TO_NOTATION = {v: k for k, v in NOTATION_TO_POS_HINT.items()}
POS_HINT_TO_NOTATION_FLIPPED = {v: k for k, v in NOTATION_TO_POS_HINT_FLIPPED.items()}
GAME_STATE_TO_NOTATION = {v: k for k, v in NOTATION_TO_GAME_STATE.items()}
GAME_STATE_TO_NOTATION_FLIPPED = {v: k for k, v in NOTATION_TO_GAME_STATE_FLIPPED.items()}

columns = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']

rows = ['1', '2', '3', '4', '5', '6', '7', '8']

