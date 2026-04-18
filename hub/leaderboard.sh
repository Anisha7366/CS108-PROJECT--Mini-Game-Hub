#!/bin/bash
# game[n] = [name, win_num, lose_num, draw_num]
awk '

function add_row_to_array(user, i) {

#creating an array and filling out the data in an array for all the player 1s
    exists = "No"

    for(j = 0; j<i; j++) {
        if (user[j, 0] == $1) {
            exists = "Yes"
            if($2 == "winner") {
                user[j, 1]++;
            }  
            else if($2 == "loser") {
                user[j, 2]++;
            }
            else if($2 == "draw") {
                user[j, 3]++;
            } 
            break
        }
        
    }

    if (exists == "No") {

            user[i, 0] = $1
            user[i, 1] = 0
            user[i, 2] = 0
            user[i, 3] = 0
        
            if($2 == "winner") {
                user[i, 1]++;
            }  
            else if($2 == "loser") {
                user[i, 2]++;
            }
            else if($2 == "draw") {
                user[i,3]++;
            } 
        
        i++;

        }

#doing pretty much the same thing for all the player 2s

exists = "No"

    for(j = 0; j<i; j++) {
        if (user[j, 0] == $3) {
            exists = "Yes"
            if($4 == "winner") {
                user[j, 1]++;
            }  
            else if($4 == "loser") {
                user[j, 2]++;
            }
            else if($4 == "draw") {
                user[j, 3]++;
            } 
            break
        }
        
    }

    if (exists == "No") {

            user[i, 0] = $3
            user[i, 1] = 0
            user[i, 2] = 0
            user[i, 3] = 0
        
            if($4 == "winner") {
                user[i, 1]++;
            }  
            else if($4 == "loser") {
                user[i, 2]++;
            }
            else if($4 == "draw") {
                user[i,3]++;
            } 
        
        i++;

        }
return i;

}

function printing(user, i) {

printf "%-20s %-10s %-10s %-10s\n", "Usernames", "Wins", "Losses", "Draws"
printf "\n"
for (j=0; j<i; j++) {
printf "%-20s %-10s %-10s %-10s\n", user[j,0], user[j,1], user[j,2], user[j,3]

}
}

BEGIN {FS=","; OFS = "\t"; i=0; oth=0; four=0; tic=0}
{

i = add_row_to_array(user, i)

if ($6 == "Othello"){
oth = add_row_to_array(othello, oth) }

else if ($6 == "Tic-Tac-Toe") {
tic = add_row_to_array(tictactoe, tic)} 

else if ($6 == "Connect FOUR") {
four = add_row_to_array(connect, four)}

}
END {


printf "\nHistory for all games \n"
printing(user, i)

printf "\nHistory for Tic-Tac-Toe \n"
printing(tictactoe, tic)

printf "\nHistory for Othello \n"
printing(othello, oth)

printf "\nHistory for Connect four \n"
printing(connect, four)



}


' history.csv