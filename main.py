
board = [
    ["♜", "♞", "♝", "♛", "♚", "♝", "♞", "♜"],
    ["♟", "♟", "♟", "♟", "♟", "♟", "♟", "♟"],
    ["·", "·", "·", "·", "·", "·", "·", "·"],
    ["·", "·", "·", "·", "·", "·", "·", "·"],
    ["·", "·", "·", "·", "·", "·", "·", "·"],
    ["·", "·", "·", "·", "·", "·", "·", "·"],
    ["♙", "♙", "♙", "♙", "♙", "♙", "♙", "♙"],
    ["♖", "♘", "♗", "♕", "♔", "♗", "♘", "♖"]
]

white_pieces = ["♙", "♖", "♘", "♗", "♕", "♔"]
black_pieces = ["♟", "♜", "♞", "♝", "♛", "♚"]

files = {
    "a": 0,
    "b": 1,
    "c": 2,
    "d": 3,
    "e": 4,
    "f": 5,
    "g": 6,
    "h": 7
}

turn = "white"
game_running = True
last_move = None

white_king_moved = False
black_king_moved = False

white_queenside_rook_moved = False
white_kingside_rook_moved = False

black_queenside_rook_moved = False   
black_kingside_rook_moved = False


def print_board():

    print("  a b c d e f g h")

    rank = 8

    for row in board:

        print(rank, end=" ")

        for piece in row:
            print(piece, end=" ")

        print()

        rank -= 1

    print("  a b c d e f g h")


def move_piece(board, from_row, from_column, to_row, to_column):

    piece = board[from_row][from_column]

    board[to_row][to_column] = piece
    board[from_row][from_column] = "·"

def promote_pawn(board, row, column):
    piece = board[row][column]
    
    if piece == "♙" and row == 0:

        while True:

            choice = input("Promote pawn to (Q/R/B/N): ").upper()

            if choice == "Q":
                board[row][column] = "♕"
                break

            elif choice == "R":
                board[row][column] = "♖"
                break

            elif choice == "B":
                board[row][column] = "♗"
                break

            elif choice == "N":
                board[row][column] = "♘"
                break

            else:
                print("Invalid choice. Please choose Q, R, B, or N.")

    elif piece == "♟" and row == 7:

        while True:

            choice = input("Promote pawn to (Q/R/B/N): ").upper()

            if choice == "Q":
                board[row][column] = "♛"
                break

            elif choice == "R":
                board[row][column] = "♜"
                break

            elif choice == "B":
                board[row][column] = "♝"
                break

            elif choice == "N":
                board[row][column] = "♞"
                break

            else:
                print("Invalid choice. Please choose Q, R, B, or N.")


def is_valid_pawn_move(
    board,
    piece,
    from_row,
    from_column,
    to_row,
    to_column
):

    if piece == "♙":

        # Move forward one square
        if from_column == to_column:

            if from_row - to_row == 1 and board[to_row][to_column] == "·":
                return True

        # Move forward two squares
        if from_column == to_column:

            if from_row == 6 and from_row - to_row == 2:

                if board[5][from_column] == "·" and board[to_row][to_column] == "·":
                    return True

        # Capture diagonally
        if from_row - to_row == 1 and abs(from_column - to_column) == 1:

            if board[to_row][to_column] in black_pieces:
                return True

        return False


    elif piece == "♟":

        # Move forward one square
        if from_column == to_column:

            if to_row - from_row == 1 and board[to_row][to_column] == "·":
                return True

        # Move forward two squares
        if from_column == to_column:

            if from_row == 1 and to_row - from_row == 2:

                if board[2][from_column] == "·" and board[to_row][to_column] == "·":
                    return True

        # Capture diagonally
        if to_row - from_row == 1 and abs(from_column - to_column) == 1:

            if board[to_row][to_column] in white_pieces:
                return True

        return False

    return False


def is_valid_rook_move(
    board,
    from_row,
    from_column,
    to_row,
    to_column
):

    destination = board[to_row][to_column]

    piece = board[from_row][from_column]

    if piece in white_pieces:

        if destination in white_pieces:
            return False

    if piece in black_pieces:

        if destination in black_pieces:
            return False

    if from_row == to_row and from_column == to_column:
        return False

    if from_column == to_column:

        if to_row > from_row:
            step = 1
        else:
            step = -1

        for row in range(from_row + step, to_row, step):

            if board[row][from_column] != "·":
                return False

        return True


    elif from_row == to_row:

        if to_column > from_column:
            step = 1
        else:
            step = -1

        for column in range(from_column + step, to_column, step):

            if board[from_row][column] != "·":
                return False

        return True

    return False


def is_valid_knight_move(
    board,
    from_row,
    from_column,
    to_row,
    to_column
):

    destination = board[to_row][to_column]

    piece = board[from_row][from_column]

    if piece in white_pieces:

        if destination in white_pieces:
            return False

    if piece in black_pieces:

        if destination in black_pieces:
            return False

    row_difference = abs(from_row - to_row)
    column_difference = abs(from_column - to_column)

    if row_difference == 2 and column_difference == 1:
        return True

    if row_difference == 1 and column_difference == 2:
        return True

    return False


def is_valid_bishop_move(
    board,
    from_row,
    from_column,
    to_row,
    to_column
):

    if from_row == to_row and from_column == to_column:
        return False

    row_difference = abs(from_row - to_row)
    column_difference = abs(from_column - to_column)

    if row_difference != column_difference:
        return False

    if to_row > from_row:
        row_step = 1
    else:
        row_step = -1

    if to_column > from_column:
        column_step = 1
    else:
        column_step = -1

    row = from_row + row_step
    column = from_column + column_step

    while row != to_row or column != to_column:

        if board[row][column] != "·":
            return False

        row += row_step
        column += column_step

    destination = board[to_row][to_column]

    piece = board[from_row][from_column]

    if piece in white_pieces:

        if destination in white_pieces:
            return False

    if piece in black_pieces:

        if destination in black_pieces:
            return False

    return True


def is_valid_queen_move(
    board,
    from_row,
    from_column,
    to_row,
    to_column
):

    if is_valid_rook_move(
        board,
        from_row,
        from_column,
        to_row,
        to_column
    ):
        return True

    if is_valid_bishop_move(
        board,
        from_row,
        from_column,
        to_row,
        to_column
    ):
        return True

    return False


def is_valid_king_move(
    board,
    from_row,
    from_column,
    to_row,
    to_column
):

    if from_row == to_row and from_column == to_column:
        return False

    row_diff = abs(from_row - to_row)
    col_diff = abs(from_column - to_column)

    if row_diff > 1 or col_diff > 1:
        return False

    destination = board[to_row][to_column]

    piece = board[from_row][from_column]

    if piece in white_pieces:

        if destination in white_pieces:
            return False

    if piece in black_pieces:

        if destination in black_pieces:
            return False

    return True

def is_valid_castling(board, from_row, from_column, to_row, to_column, turn, king_moved, rook_moved):
    if abs(to_column - from_column) != 2:
        return False

    if king_moved:
        return False

    piece = board[from_row][from_column]

    if turn == "white" and piece != "♔":
        return False

    if turn == "black" and piece != "♚":
        return False

    if turn == "white" and from_row != 7:
        return False

    if turn == "black" and from_row != 0:
        return False

    if to_column > from_column:
        king_side = True

    else:
        king_side = False

    if rook_moved:
        return False

    if king_side:
        rook_column = 7

    else:
        rook_column = 0

    rook = board[from_row][rook_column]

    if turn == "white" and rook != "♖":
        return False

    if turn == "black" and rook != "♜":
        return False

        if kingside:

            if board[from_row][5] != "·":
                return False

            if board[from_row][6] != "·":
                return False

    else:

        if board[from_row][1] != "·":
            return False

        if board[from_row][2] != "·":
            return False

        if board[from_row][3] != "·":
            return False


        if is_square_attacked(board, from_row, from_column,  "black" if turn == "white" else "white"):
            return False

        if king_side:
            middle_column = from_column + 1

        else:
            middle_column = from_column - 1

        if is_square_attacked(board, from_row, middle_column, "black" if turn == "white" else "white"):
            return False

        if is_square_attacked(board, to_row, to_column, "black" if turn == "white" else "white"):
            return False

        return True

def is_valid_move(
    board,
    piece,
    from_row,
    from_column,
    to_row,
    to_column,turn,last_move,king_moved,rook_moved
):

    if piece == "♙" or piece == "♟":

        normal_pawn_move =is_valid_pawn_move(
            board,
            piece,
            from_row,
            from_column,
            to_row,
            to_column
        )

        en_passant_move = is_valid_en_passant(board,from_row, from_column, to_row, to_column, turn,last_move)


        return normal_pawn_move or en_passant_move    




    elif piece == "♖" or piece == "♜":

        return is_valid_rook_move(
            board,
            from_row,
            from_column,
            to_row,
            to_column
        )

    elif piece == "♘" or piece == "♞":

        return is_valid_knight_move(
            board,
            from_row,
            from_column,
            to_row,
            to_column
        )

    elif piece == "♗" or piece == "♝":

        return is_valid_bishop_move(
            board,
            from_row,
            from_column,
            to_row,
            to_column
        )

    elif piece == "♕" or piece == "♛":

        return is_valid_queen_move(
            board,
            from_row,
            from_column,
            to_row,
            to_column
        )

    elif piece == "♔" or piece == "♚":

        if abs(to_column - from_column) == 2:

            return is_valid_castling(
                board,
                from_row,
                from_column,
                to_row,
                to_column,
                turn,
                king_moved,
                rook_moved
            )

        return is_valid_king_move(
            board,
            piece,
            from_row,
            from_column,
            to_row,
            to_column
        )


def is_square_attacked(
    board,
    target_row,
    target_column,
    attacking_color
):

    if attacking_color == "white":

        rook = "♖"
        knight = "♘"
        bishop = "♗"
        queen = "♕"
        pawn = "♙"
        king = "♔"

    else:

        rook = "♜"
        knight = "♞"
        bishop = "♝"
        queen = "♛"
        pawn = "♟"
        king = "♚"


    for row in range(8):

        for column in range(8):

            if board[row][column] == rook:

                if is_valid_rook_move(
                    board,
                    row,
                    column,
                    target_row,
                    target_column
                ):
                    return True


            if board[row][column] == knight:

                if is_valid_knight_move(
                    board,
                    row,
                    column,
                    target_row,
                    target_column
                ):
                    return True


            if board[row][column] == bishop:

                if is_valid_bishop_move(
                    board,
                    row,
                    column,
                    target_row,
                    target_column
                ):
                    return True


            if board[row][column] == queen:

                if is_valid_queen_move(
                    board,
                    row,
                    column,
                    target_row,
                    target_column
                ):
                    return True


            if board[row][column] == pawn:

                if attacking_color == "white":

                    if (
                        target_row == row - 1
                        and abs(target_column - column) == 1
                    ):
                        return True

                else:

                    if (
                        target_row == row + 1
                        and abs(target_column - column) == 1
                    ):
                        return True


            if board[row][column] == king:

                row_difference = abs(row - target_row)
                column_difference = abs(column - target_column)

                if row_difference <= 1 and column_difference <= 1:

                    if row_difference != 0 or column_difference != 0:
                        return True


    return False


def is_in_check(board, color):

    if color == "white":
        king = "♔"
        opponent = "black"
    else:
        king = "♚"
        opponent = "white"


    for row in range(8):

        for column in range(8):

            if board[row][column] == king:

                return is_square_attacked(
                    board,
                    row,
                    column,
                    opponent
                )

    return False


def has_legal_move(board, color, last_move):

    if color == "white":
        own_pieces = white_pieces
    else:
        own_pieces = black_pieces


    for row in range(8):

        for column in range(8):

            piece = board[row][column]

            if piece not in own_pieces:
                continue


            for to_row in range(8):

                for to_column in range(8):

                    valid_move = is_valid_move(
                        board,
                        piece,
                        row,
                        column,
                        to_row,
                        to_column,color, last_move, False, False
                    )

                    if not valid_move:
                        continue


                    moving_piece = board[row][column]
                    captured_piece = board[to_row][to_column]


                    move_piece(
                        board,
                        row,
                        column,
                        to_row,
                        to_column
                    )


                    if not is_in_check(board, color):

                        board[row][column] = moving_piece
                        board[to_row][to_column] = captured_piece

                        return True

                    else:

                        board[row][column] = moving_piece
                        board[to_row][to_column] = captured_piece


    return False

def was_two_square_pawn_move(last_move):

    if last_move is None:
        return False

    if last_move["piece"] not in ["♙", "♟"]:
        return False

    if abs(last_move["to_row"] - last_move["from_row"]) != 2:
        return False

    return True

def is_valid_en_passant(board, from_row, from_column, to_row, to_column, turn, last_move):

    if not was_two_square_pawn_move(last_move):
        return False

    moving_piece = board[from_row][from_column]

    if turn == "white" and moving_piece != "♙":
        return False

    if turn == "black" and moving_piece != "♟":
        return False

    if abs(to_column - from_column) != 1:
        return False

    if board[to_row][to_column] != "·":
        return False

    if turn == "white" and to_row != from_row - 1:
        return False

    if turn == "black" and to_row != from_row + 1:
        return False

    captured_row = from_row
    captured_column = to_column

    captured_piece = board[captured_row][captured_column]

    if turn == "white" and captured_piece != "♟":
        return False

    if turn == "black" and captured_piece != "♙":
        return False

    if last_move["to_row"] != captured_row:
        return False

    if last_move["to_column"] != captured_column:
        return False

    return True

def perform_en_passant(board, from_row, from_column, to_row, to_column):

    captured_row = from_row
    captured_column = to_column

    board[to_row][to_column] = board[from_row][from_column]
    board[from_row][from_column] = "·"
    board[captured_row][captured_column] = "·"

def perform_castling(
    board,
    from_row,
    from_column,
    to_row,
    to_column
):

    # Move the king
    board[to_row][to_column] = board[from_row][from_column]
    board[from_row][from_column] = "·"

    # Kingside castling
    if to_column > from_column:

        rook_from_column = 7
        rook_to_column = 5

    # Queenside castling
    else:

        rook_from_column = 0
        rook_to_column = 3

    # Move the rook
    board[from_row][rook_to_column] = board[from_row][rook_from_column]
    board[from_row][rook_from_column] = "·"



while game_running:

    print()

    print_board()

    print()

    print(f"Current turn: {turn}")

    print()

    from_square = input("Move from: ")

    if from_square == "quit":

        print("Game ended.")
        break

    to_square = input("Move to: ")

    print()


    # Translate starting square

    from_file = from_square[0]
    from_rank = int(from_square[1])

    from_column = files[from_file]
    from_row = 8 - from_rank

    piece = board[from_row][from_column]


    # Translate destination square

    to_file = to_square[0]
    to_rank = int(to_square[1])

    to_column = files[to_file]
    to_row = 8 - to_rank


    # Check whether there is a piece

    if piece == "·":

        print("There is no piece at that square.")
        continue


    # Check whose piece it is

    if turn == "white":

        if piece not in white_pieces:

            print("It's white's turn. You can only move white pieces.")
            continue

    else:

        if piece not in black_pieces:

            print("It's black's turn. You can only move black pieces.")
            continue


    if turn == "white":
        king_moved = white_king_moved

    else:
        king_moved = black_king_moved

    if turn == "white":
        if to_row > from_row:
            rook_moved = white_kingside_rook_moved
        else:
            rook_moved = white_queenside_rook_moved

    else:
        if to_row > from_row:
            rook_moved = black_kingside_rook_moved
        else:
            rook_moved = black_queenside_rook_moved

    valid_move = is_valid_move(
        board,
        piece,
        from_row,
        from_column,
        to_row,
        to_column,turn,last_move, king_moved, rook_moved
    )


    if not valid_move:

        print("Invalid move for that piece.")
        continue


    # Save pieces

    moving_piece = board[from_row][from_column]
    captured_piece = board[to_row][to_column]


    en_passant_move = is_valid_en_passant(board, from_row, from_column, to_row, to_column, turn, last_move)

    if en_passant_move:

        captured_row = from_row
        captured_column = to_column
        en_passant_captured_piece = board[captured_row][captured_column]


    else:
        captured_row = None
        captured_column = None
        en_passant_captured_piece = None

    if en_passant_move:

        perform_en_passant(
            board,
            from_row,
            from_column,
            to_row,
            to_column
        )

    else:

        move_piece(
            board,
            from_row,
            from_column,
            to_row,
            to_column
        )

    if is_in_check(board, turn):

        board[from_row][from_column] = moving_piece
        board[to_row][to_column] = captured_piece

        if en_passant_move:
            board[captured_row][captured_column] = en_passant_captured_piece

        print("You cannot make that move because your king would be in check.")
        continue

    last_move = {
        "piece" : moving_piece,
        "from_row" : from_row,
        "to_row" : to_row,
        "from_column" : from_column,
        "to_column" : to_column,
    }
        



    promote_pawn(board, to_row, to_column)

    if en_passant_move:
        print(f"{moving_piece} captured {en_passant_captured_piece} en passant on {to_square}.")



    elif captured_piece != "·":

        print(
            f"{moving_piece} captured "
            f"{captured_piece} on {to_square}."
        )

    else:

        print(
            f"Moved {moving_piece} "
            f"from {from_square} to {to_square}."
        )


    # Switch turns

    if turn == "white":
        turn = "black"
    else:
        turn = "white"


    # Check for checkmate or check

    if is_in_check(board, turn):

        if not has_legal_move(board, turn):

            print(f"Checkmate! {turn} has lost.")
            game_running = False

        else:

            print(f"{turn.capitalize()} is in check!")


    # Check for stalemate

    else:

        if not has_legal_move(board, turn, last_move):

            print("Stalemate!")
            game_running = False