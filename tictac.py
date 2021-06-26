
def MakeTicTacTable():
    table = [[0,0,0],
         [0,0,0],
         [0,0,0]]
    return table

def ShowTable(table):
    for i in range(0,3) :
        for j in range(0,3) :
            print(table[i][j],end ="")
        print()
def Select_Table(table,row,column,player):
    if(player == 1):
        if(table[row][column] == 0):
            table[row][column] = "X"
        else:
            print("Not empty !!")
            return False
    else:
        if(table[row][column] == 0):
            table[row][column] = "O"
        else:
            print("Not empty !!")
            return False
    return table

def CheackRepeate(table,row,column):
    if(table[row][column] == 0 ):
        return True
    return False

def SelectPlayer(player):
    if(player == 1):
        return "X"
    return "O"


    
def CalculatorScoore(table):
    win = 0 
    for player in range(1,3):
        if(row_win(table,player) or col_win(table,player) or
           diag_win(table,player)):
            win = player
    is_zero = 0
    for i in range (len(table)):
        for j in range(len(table)):
            if(table[i][j]== 0):
                is_zero +=1
    if is_zero == 0 and win ==0 :
        win =-1
    return win



  
def game_is_over(board):
    for i in range(3):

        if board[i][0] == board[i][1] == board[i][2] \
            and board[i][0] != 0 :
            print(board[i][0] + " wins!")
            return board[i][0]
        

        if board[0][i] == board[1][i] == board[2][i] \
            and board[0][i] != 0:
            print(board[0][i] + " wins!")
            return board[0][i]
        

    if board[0][0] == board[1][1] == board[2][2] \
        and board[0][0] != 0:
        print(board[0][0] + " wins!")
        return board[0][0]
    
    if board[2][0] == board[1][1] == board[0][2] \
        and board[2][0] != 0:
        print(board[2][0] + " wins!")
        return board[2][0]
    
    
    if 0 not in board[0] and 0 not in board[1] \
        and 0 not in board[2]:
        print("Tie game!")
        return 0
    
    return False
      

def is_valid(px,py,table):
    if px < 0 or px >2 or py < 0 or py > 2:
        return False
    elif table[px][py]  != 0:
        return False
    else:
        return True


def play(table):
    player = "X"
    ShowTable(table)
    
    if player == "X":
        while True:
            (m,qx,qy) = min(table)
            px,py = input("Input [ ] [ ]  : ").split()
            px = int(px)
            py = int(py)
            (qx,qy) = (px,py)
            
            if(is_valid(px,py,table)):
                table[px][py] = "X"
                player = "O"
                break
            else:
                print("The move is not valid ! Try again")
    else :
        (m,px,py) = max(table)
        table[px][py] = "O"
        player = "X"
        
        
            
        
    
 
def play_game():   
    countscore = 0
    is_game = True
    table = MakeTicTacTable()
    ShowTable(table)
    while(is_game == True):
        
        for player in range(1,3):
            correct_input = True
            print("You are Player : " , player)
            while(correct_input == True):
                if(player == 1):
                    m,qx,qy = min(table)
                    a,b = input("Choose Tictac Table in row and column : " ).split()
                    qx,qy = int(a),int(b)
                    if is_valid(int(a),int(b),table):
                        table[int(a)][int(b)] = "X"
                        ShowTable(table)
                        correct_input = False
                        
                    else:
                        print("Tablyouselected not empty")
                elif (player == 2):
                    m,px,py = max(table)
                    table[px][py] = "O"
                    ShowTable(table)
                    correct_input = False
                    
            winner = game_is_over(table)
            if winner == "X":
                correct_input = False
                is_game = False
                countscore += 1
                break
            elif winner == "O":
                correct_input = False
                is_game = False
                countscore -= 1

def max(table):
    maxv = -2
    px = None
    py = None
    
    result = game_is_over(table)
    if result == 'X':
        return (-1, 0, 0)
    elif result == 'O':
        return (1, 0, 0)
    elif result == 0:
        return (0, 0, 0)
    
    for i in range(0,3):
        for j in range (0,3):
            if table[i][j] == 0:
                table[i][j] == "0"
                (m,min_i,min_j) = min(table)
                if m > maxv :
                    maxv = m
                    px = i 
                    py = j
                table[i][j] = 0
    return (maxv,px,py)

def min (table):
    minv =2
    qx = None
    qy = None
    
    result = game_is_over(table)
    
    if result == 'X':
        return(-1,0,0)
    elif result == 'O':
        return (1,0,0)
    elif result == 0:
        return (0,0,0)
    
    for i in range (0,3):
        for j in range (0,3):
            if table[i][j] == 0:
                table[i][j] = "X"
                (m,max_i,max_j) = max()
                if m < minv:
                    minv = m 
                    qx = i 
                    qy = j
                table[i][j] = 0
    return (minv,qx,qy)

play_game()

            
    
