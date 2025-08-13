# Connect Four Game against AI Bot
#### Video Demo: https://youtu.be/iIkvXqwWUhI
#### Description:
            This is a Connect Four game for player vs AI!
            the game enviroment is created using pygame,sys and the AI bot is made using numpy, random, math libraries. I started by defining some constants such as the board dimensions, screen size, colours etc.

            main():
            This function makes a 2D array to represent the Game board with values like [0(empty), 1(player coin), 2(AI coin)], then I initialized the pygame engine, I displayed the game screen and setuped its background. Then I called the draw_board function which darws a board based on the 2D array. Then I tracked user movements in a while True loop with an condition, If it is player's turn then:
                we showed the coin one mouse however when It was just about to be droped
                we detected when player clicks a coulmn
                placed the piece in the lowest available row in that coulmn.
                Check condition for win, if player wins then desplay a message and end the game else pass the control to AI
            for the AI's moves:
                we did the similar thing and implemented an minimax algorithm to check for the best move, after AI's move I checked again for the win condition, and If AI won, stop the game and print AI wins on the screen else give the turn to the player


            draw_board():
            loopes over the rows and columns to draw the board by calling pygame.draw.react and pygame.draw.circle. I made a transparent serface and then draw the circle on to that and then place that serface on screen using blit to reduce the pixelated look of the circle
            
            create_board():
            this function creates a 2D array to represent the board

            print_board(board):
            this function prints the board at the console. I filped the board with np.flip to ensure that the rows are filled bottom up

            drop_piece(board, row, col, piece):
            drops the piece(RED_COIN || YELLOW_COIN) at the board[row][col] place

            is_valid_location(board, col):
            this function see's if there is space in the coulmn that the player clicked

            get_next_open_row(board, col):
            loops through the row which the player clicked to find it's bottom most empty row/cell

            winning_move(board, piece):
            I used an if condition to match the board[row][col] with piece in a loop for every possible way of winning and returned true if condition is met

            Minimax:
            The thing I am most excited about in this project is the Minimax Algorithm of AI bot. The AI Bot uses the Minimax Algorithm which given any game state, optimally solves every outcome and assigns a numerical score to the end state, then the algorithm based on its configuration, tires to maximies its numerical value and in turn makes the best moves or vice virsa.