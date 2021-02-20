#################################################################
# ex7 - recursion
# login: raz.perry
# id : 208613190
# full name: raz perry
# others (students, webs, notes):
# in function 2 i chose to return -1 (when there are only 1/0 and -1 cells
# because the function get only the variations for a row (or col) but that
# unknown cell affected also from the col (or row) blocks and maybe there
# the third option will be the chosen one. in that case i would create wrong
# board and have to return recursively.
# students - toot avrach (discuss on function 5)
#################################################################
from copy import deepcopy
BLACK = 1
WHITE = 0
UNKNOWN = -1


def num2list(row, num):
    """The function gets row and number and returns the number counts in a row
    in a new list"""
    lst = []
    counter = 0
    for cell in row:
        if cell == num:
            counter += 1
        elif counter != 0:
            lst.append(counter)
            counter = 0
    if counter != 0:
        lst.append(counter)
    return lst


def make2zero(row):
    """The function gets a row and replace all -1 to 0"""
    for i in range(len(row)):
        if row[i] == UNKNOWN:
            row[i] = WHITE
            

def update_row(row, index, number):
    """The function gets a row, index and number and update the cell value to
    the number"""
    row[index] = number
    return row


def add_block(index, lst, block):
    """The function gets col index, list and its current block and update the
    list to the block (change values to 1) and returns the list and the next
    index. also add to the end 0"""
    for i in range(block):
        lst[index + i] = BLACK
    if len(lst) - index < block:
        lst[index + i + 1] = WHITE
        index += 1
    return lst, index + block


def valid_add_block(row, index, block):
    """The function checks if its legal to create a block - no zero and the
    after char cant be one"""
    if WHITE not in row[index:index + block]:
        if len(row) > index + block:
            if row[index + block] == BLACK:
                return False
        return True
    return False


def variations_helper(row, blocks, options, col_index, block_index):
    """The function gets a row its blocks, options list and col index. If the
    row is same with blocks its add the row to the options. recursively its
    changes more values in the row till the end of it"""
    if block_index == len(blocks):
        if num2list(row, BLACK) == blocks:
            make2zero(row)
            options.append(row)
        return options
    if len(row) - col_index < blocks[block_index]:
        return options
    if row[col_index] in (UNKNOWN, BLACK):
        if valid_add_block(row, col_index, blocks[block_index]):
            new_row, new_index = add_block(col_index, row[:], blocks[block_index])
            variations_helper(new_row, blocks, options, new_index, block_index + 1)
        if row[col_index] == -1:
            variations_helper(update_row(row, col_index, WHITE), blocks, options, col_index + 1, block_index)
    else:
        variations_helper(row, blocks, options, col_index + 1, block_index)
    return options


def get_row_variations(row, blocks):
    """The function gets a row and its blocks and returns all options by using
    variarions_helper function"""
    return variations_helper(row[:], blocks, [], 0, 0)


def get_intersection_row(rows):
    """The function gets list of rows and returns a row of their intersection.
    if unknown it returns -1"""
    if not rows:
        return []
    lst = []
    for i in range(len(rows[0])):
        if len(set([row[i] for row in rows])) == 1:
            lst.append(rows[0][i])
        else:
            lst.append(UNKNOWN)
    return lst


def create_mat(rows_amount, cols_amount):
    """The function gets rows and cols amount and returns a new matrix of -1
    values in the input size"""
    new_mat = []
    for i in range(rows_amount):
        new_mat.append([])
        for j in range(cols_amount):
            new_mat[i].append(UNKNOWN)
    return new_mat


def update_game_column(board, index, new_col):
    """The function gets a board, col index and new col and it updates the
    board column according to the input column"""
    for i in range(len(board)):
        board[i][index] = new_col[i]


def column(board, col_index):
    """The function gets board and col index and returns the column as list"""
    return [board[i][col_index] for i in range(len(board))]


def full_board(board):
    """The function gets a board and check if it full - if there are more -1
    values"""
    for row in board:
        if not full_list(row):
            return False
    return True


def full_list(lst):
    """The function gets a list and return if there are values of -1"""
    if UNKNOWN in lst:
        return False
    return True


def paint(lst, cons):
    """The function gets a list and blocks and if the blocks are legal its
    returns the new list according to the intersection of the variations. if
    the blocks illegal its returns the original list"""
    new_list = get_intersection_row(get_row_variations(lst, cons))
    if new_list:
        return new_list
    else:
        return lst


def easy_helper(rows_cons, cols_cons, board):
    """The function gets rows and cols constraints and a game board and it
    keep solving the board until there is no more changes or the board is
    complete"""
    had_change = True
    while not full_board(board) and had_change:
        had_change = False
        for row_index, row_cons in enumerate(rows_cons):
            if not full_list(board[row_index]):
                new_row = paint(board[row_index], row_cons)
                if board[row_index] != new_row:
                    board[row_index] = new_row
                    had_change = True
        for col_index, col_cons in enumerate(cols_cons):
            col = column(board, col_index)
            if not full_list(col):
                new_col = paint(col, col_cons)
                if col != new_col:
                    update_game_column(board, col_index, new_col)
                    had_change = True
    return board


def solve_easy_nonogram(constraints):
    """The function gets constraints and returns solve board game as posible by
    using easy_helper function"""
    rows_cons = constraints[0]
    cols_cons = constraints[1]
    game_board = create_mat(len(rows_cons), len(cols_cons))
    return easy_helper(rows_cons, cols_cons, game_board)


def update_board(index, row, board):
    """The function gets a new row and update it to the board according to the
    input index"""
    board[index] = row
    return board


def valid_row(row, blocks):
    """The function gets a row and its blocks and return if there are enough
    valid cells"""
    valid_cells = row.count(UNKNOWN) + row.count(BLACK)
    if valid_cells < sum(blocks):
        return False
    return True


def valid_col(board, cols_cons):
    """The function gets a board and columns constraints and checks if the
    board is legal acoording to the cons"""
    for i in range(len(board[0])):
        if not valid_row(column(board, i), cols_cons[i]):
            return False
    return True


def valid_cols(board, cols_cons):
    """The function gets board and cols constraints and check if the board
    paint is legal"""
    for i in range(len(board[0])):
        if num2list(column(board, i), BLACK) != cols_cons[i]:
            return False
    return True


def nono_helper(rows_cons, cols_cons, board, answers, row_index):
    """The function gets rows and cols constraints, board, answers list and row
     index and add the current board to the answers list if it is full and
     valid. if valid but still not full it calling the function recursively
     with each option of the current unfull row"""
    if not valid_col(board, cols_cons):
        return
    if full_board(board):
        if valid_cols(board, cols_cons):
            answers.append(board)
            return answers
    options = get_row_variations(board[row_index], rows_cons[row_index])
    for op in options:
        nono_helper(rows_cons, cols_cons, update_board(row_index, op,
                                                       deepcopy(board)),
                    answers, row_index + 1)
    return answers


def solve_nonogram(constraints):
    """The function gets constraints and return the all board options by using
    easy solution to create the start board and than using the nono_helper
    function to create all boards"""
    rows_cons = constraints[0]
    cols_cons = constraints[1]
    return nono_helper(rows_cons, cols_cons, solve_easy_nonogram(constraints),
                       [], 0)


def factorial(n):
    """The function calculate the factorial of a number"""
    if n == 0:
        return 1
    else:
        return factorial(n-1) * n


def count_row_variations(length, blocks):
    """The function get a length and blocks and returns the count of row
    variations in that length, using factorial func and n choose k formula"""
    k = length - (sum(blocks) + len(blocks) - 1)
    n = len(blocks) + 1
    if k < 0:
        return 0
    return int(factorial(n + k - 1) / (factorial(n - 1)*factorial(k)))
