#!/bin/bash
# game[n] = [name, win_num, lose_num, draw_num]
awk -v arg="$1" '

function sort_array(ind, x, n) {

if (x == 4) {

#using infinity as -1 as placeholder, its not being compared anywhere, this is just for clarity of thought
 for(i=n-1; i>=0; i--) {
            k=i;
            if(ind[i,1]==0 && ind[i,2]==0) {max = 0;}
            else if (ind[i,2]==0) {max = -1;}
            else {max = ind[i,1]/ind[i,2];}

            for(j=0; j<i; j++) {

                    #if wins and losses are zero; that will be better than win zero and loss one
                    if (ind[j,1] == 0 && ind[j,2] == 0) {
                        if(max==0) {if(ind[k,2]>0) {k=j;}}
                        
                    }

                    #if both have losses zero we see who has won more
                    else if(ind[j,2]==0) {if(ind[k,2] == 0 && ind[k,1] < ind[j,1]) {k=j;}
                                            if(ind[k,2] != 0) {max = -1; k=j;}}

                    #if denominator is not zero, calculated normally
                    else { if (ind[j, 1]/ind[j, 2] > max && ((ind[k,2] != 0) || (ind[k,2] == 0  && ind[k,1] == 0) )) {max = ind[j, 1]/ind[j,2]; k=j;}
                           #if ratios are same, higher no of wins is better 
                           else if (ind[j, 1]/ind[j, 2] == max && ind[j,1] > ind[k,1]) {k=j;} }

            }
            #print ("switching " ind[i,0] " and " ind[k,0])
            for (j=0; j<4;j++) {
               
                temp = ind[i, j];
                ind[i, j] = ind[k, j];
                ind[k, j] = temp; } 
        }

}

else if (x == 5) {

    for(i=n-1; i>=0; i--) {
            k=i;
            max = ind[i,1]+ind[i,2]+ind[i,3];
            for(j=0; j<i; j++) {
                    if (ind[j,1]+ind[j,2]+ind[j,3] > max ) {max = ind[j,1]+ind[j,2]+ind[j,3]; k=j;}
            }
            for (j=0; j<4;j++) {
            temp = ind[i, j];
            ind[i, j] = ind[k, j];
            ind[k, j] = temp; }

}
}
    else { 
        for(i=n-1; i>=0; i--) {
            k=i;
            max = ind[i, x];
            for(j=0; j<i; j++) {
                    if (ind[j, x] > max ) {max = ind[j, x]; k=j;}
            }
            for (j=0; j<4;j++) {
                temp = ind[i, j];
                ind[i, j] = ind[k, j];
                ind[k, j] = temp; } 
        }
}


}

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

#print("Function entered")

printf "%-17s %-13s %-10s %-10s %-10s %-10s\n", "Usernames", "Total played", "Wins", "Losses", "Draws", "Win-loss ratio"
printf "\n"
for (j=i-1; j>=0; j--) {
if(user[j,2] == 0 && user[j,1] == 0) {x=0}
else if(user[j,2] == 0) {x = "inf"}
else {x = user[j,1]/user[j,2]}
printf "%-17s %-13s %-10s %-10s %-10s %-10s\n", user[j,0], user[j,1]+user[j,2]+user[j,3], user[j,1], user[j,2], user[j,3], x

}
}

BEGIN {FS=","; OFS = "\t"; all=0; oth=0; four=0; tic=0
key = 4; #default because ratio is the fairest way to rank
if(arg == "wins") {key = 1}
else if (arg == "losses") {key = 2}
else if (arg == "draws") {key = 3}
else if (arg == "ratio") {key = 4}
else if (arg == "total") {key = 5}

}
{

all = add_row_to_array(allgames, all)

if ($6 == "Othello"){
oth = add_row_to_array(othello, oth) }

else if ($6 == "Tic-Tac-Toe") {
tic = add_row_to_array(tictactoe, tic)} 

else if ($6 == "Connect FOUR") {
four = add_row_to_array(connect, four)}

}
END {

sort_array(allgames, key, all)
sort_array(tictactoe, key, tic)
sort_array(othello, key, oth)
sort_array(connect, key, four)

printf "\nHistory for all games \n"
printing(allgames, all)

printf "\nHistory for Tic-Tac-Toe \n"
printing(tictactoe, tic)

printf "\nHistory for Othello \n"
printing(othello, oth)

printf "\nHistory for Connect four \n"
printing(connect, four)



}


' history.csv


#struggle faced: in sorting 0,0 was not being sorted because i had put deno not equal to zero in the normal ratio comparisions and was also relying on normal ratio comparisions to sort the 0,0 case