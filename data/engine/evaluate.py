
black_pawn_positioning = [
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1],
            [0.15, 0.15, 0.15, 0.15, 0.15, 0.15, 0.15, 0.15],
            [0.15, 0.15, 0.15, 0.15, 0.15, 0.15, 0.15, 0.15],
            [0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2],
            [0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25],
            [0, 0, 0, 0, 0, 0, 0, 0]
]
white_pawn_positioning = [
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25],
            [0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2],
            [0.15, 0.15, 0.15, 0.15, 0.15, 0.15, 0.15, 0.15],
            [0.15, 0.15, 0.15, 0.15, 0.15, 0.15, 0.15, 0.15],
            [0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0]
]
knight_positioning = [
            [-0.5,          0,     -0.3,        -0.3,      -0.3,       -0.3,         0,      -0.5],
            [-0.4,        -.2,        0,           0,         0,          0,      -0.2,      -0.4],
            [-0.3,          0,      0.1,         0.1,       0.1,        0.1,         0,      -0.3],
            [-0.3,          0,      0.1,         0.2,       0.2,        0.1,         0,      -0.3],
            [-0.3,          0,      0.1,         0.2,       0.2,        0.1,         0,      -0.3],
            [-0.3,          0,      0.1,         0.1,       0.1,        0.1,         0,      -0.3],
            [-0.4,       -0.2,        0,           0,         0,          0,      -0.2,      -0.4],
            [-0.5,          0,     -0.3,        -0.3,      -0.3,       -0.3,         0,      -0.5]
]
bishop_rook_queen_positioning = [
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0],
            [0, 0.05,  0.1,  0.1,  0.1,  0.1, 0.05, 0],
            [0, 0.05,  0.1, 0.15, 0.15,  0.1, 0.05, 0],
            [0, 0.05,  0.1, 0.15, 0.15,  0.1, 0.05, 0],
            [0, 0.05,  0.1,  0.1,  0.1,  0.1, 0.05, 0],
            [0, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0],
            [0, 0, 0, 0, 0, 0, 0, 0]
]


def positioning(piece, row, col):
    if piece == "pW":
        return white_pawn_positioning[row][col]
    elif piece == "pB":
        return black_pawn_positioning[row][col]
    elif piece == "nW" or piece == "nB":
        return knight_positioning[row][col]
    elif piece[0] == "b" or piece[0] == "r" or piece[0] == "q":
        return bishop_rook_queen_positioning[row][col]
    else:
        return 0


piece_points = {"p": 1, "n": 3, 'b': 3, 'r': 5, 'q': 9, 'k': 1000}


def score(state):
    evaluate_score = 0.0
    for row_index, row in enumerate(state):
        for col_index, col in enumerate(row):
            piece = col[0]
            piece_color = 1 if col[1] == 'W' else -1
            if piece in piece_points.keys():
                pos_score = (piece_points[piece] * piece_color
                             + positioning(col, row_index, col_index) * piece_color)
                evaluate_score = round(evaluate_score, 2) + pos_score
    return evaluate_score
