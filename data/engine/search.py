import random
from data.engine.evaluate import score as eval_score


def random_move_search(moves):
    return moves[random.randint(0, len(moves)-1)]


def minimax(game, depth, maximizing_player):
    if depth == 0 or game.end:
        return eval_score(game.state)

    if maximizing_player:
        max_eval = float('-inf')
        moves = game.generate_pseudo_legal_moves()
        for move in moves:
            game.make_move(move)
            if not game.end:
                try:
                    game.duck_move(random_move_search(game.generate_duck_moves()))
                except KeyError:
                    game.unmake_move()
                    return eval_score(game.state)
            eval = minimax(game, depth - 1, False)
            max_eval = max(max_eval, eval)
            game.unmake_move()
        return max_eval
    else:
        min_eval = float('inf')
        moves = game.generate_pseudo_legal_moves()
        for move in moves:
            game.make_move(move)
            if not game.end:
                try:
                    game.duck_move(random_move_search(game.generate_duck_moves()))
                except KeyError:
                    game.unmake_move()
                    return eval_score(game.state)
            eval = minimax(game, depth - 1, True)
            min_eval = min(min_eval, eval)
            game.unmake_move()
        return min_eval


def search(game, is_duck=True, color="White"):
    best_move = None
    best_eval = -9999 if color == "White" else 9999
    moves = game.generate_pseudo_legal_moves()
    for move in moves:
        game.make_move(move)
        if not game.end:
            if is_duck:
                try:
                    game.duck_move(random_move_search(game.generate_duck_moves()))
                except KeyError:
                    game.unmake_move()
                    continue
            else:
                game.duck_place(random_move_search(game.generate_duck_moves()).end)
        eval = minimax(game, 2, False) if color == "White" else minimax(game, 2, True)
        game.unmake_move()

        if color == "White":
            if eval > best_eval:
                best_eval = eval
                best_move = move
        else:
            if eval < best_eval:
                best_eval = eval
                best_move = move

    if best_move is None:
        moves = game.generate_pseudo_legal_moves()
        best_move = random_move_search(moves)

    return best_move
