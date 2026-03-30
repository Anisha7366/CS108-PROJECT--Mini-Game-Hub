#!/bin/bash

#possible additions: trim users to keep "vimes" and "vimes " same; password visibility; disapprove empty strings as user/pass; 

touch users.tsv

sed -i 's/\r$//' users.tsv

escape_regex() {
    printf '%s\n' "$1" | sed 's/[][\\.^$*]/\\&/g'
}

check_user() {
    local x=$(escape_regex "$1")

    if grep -q "^${x}"$'\t' users.tsv; then
        echo "Exists"
    else 
        echo "Does not exist"
    fi
}

check_pass() {
    local p=$(escape_regex "$1")
    local u=$(escape_regex "$2")

    if grep -q "^${u}"$'\t'"${p}$" users.tsv; then
        echo "Match"
    else 
        echo "Issue"
    fi
}

add_user() {
    local us=$1
    local pa=$2

    u=$(check_user "${us}")
    if [[ ${u} == "Exists" ]]; then 
        echo "Fail"
    else
        echo "${us}"$'\t'"${pa}" >> users.tsv
    fi
}



read -p "Press r for login and n to make a new account: " key

while [[ ${key} == 'n' ]]
do
    read -p "Enter username: " user
    read -p "Enter password for ${user}: " pass
    hash=$(echo -n ${pass} | sha256sum | awk '{print $1}') 

    t=$(add_user "${user}" "${hash}")
    if [[ ${t} == "Fail" ]]; then
        echo "This username already exists! Try again."
    else
        echo "User created successfully!"
        read -p "Press r for login, n to make a new account and q to quit: " key
    fi 
    
done


#the works for player 1

#echo ${key}

while [[ ${key} == 'r' ]]
do
read -p "Enter username of Player 1: " user1
read -p "Enter password for ${user1}: " pass1

#read -p "Enter username of Player 2: " user2
#read -p "Enter password for ${user2}: " pass2 


hash1=$(echo -n ${pass1} | sha256sum | awk '{print $1}') 

#echo "The hash for password 1 is: ${hash1}"

#hash2=$(echo -n ${pass2} | sha256sum | awk '{print $1}') 

#echo "The hash for password 2 is: ${hash2}"

#echo ${user1} ${pass1}


u1=$(check_user "${user1}")
p1=$(check_pass "${hash1}" "${user1}") 

if [[ ${p1} == "Match" ]]; then
    echo "Successful!"
    key=q 
elif [[ ${u1} == "Exists" ]]; then
    read -p "Either username or password are incorrect. Press r to enter again and q to quit. " key
else 
    read -p "No such account exists. Press r to enter again, n to make a new account and q to quit. " key
fi

if [[ ${key} == n ]]; then
    add_user "${user1}" "${hash1}"
fi 

done




#the works for player2

key2='r'

while [[ ${key2} == 'r' && ${key} != 'q' ]]
do
#read -p "Enter username of Player 1: " user1
#read -p "Enter password for ${user1}: " pass1

read -p "Enter username of Player 2: " user2
read -p "Enter password for ${user2}: " pass2 


#hash1=$(echo -n ${pass1} | sha256sum | awk '{print $1}') 

#echo "The hash for password 1 is: ${hash1}"

hash2=$(echo -n ${pass2} | sha256sum | awk '{print $1}') 

#echo "The hash for password 2 is: ${hash2}"

#echo ${user1} ${pass1}


u2=$(check_user "${user2}")
p2=$(check_pass "${hash2}" "${user2}") 

if [[ ${p2} == "Match" ]]; then
    echo "Successful!"
    key2=q 
elif [[ ${u2} == "Exists" ]]; then
    read -p "Either username or password are incorrect. Press r to enter again and q to quit. " key2
else 
    read -p "No such account exists. Press r to enter again, n to make a new account and q to quit. " key2
fi

if [[ ${key2} == n ]]; then
    add_user "${user2}" "${hash2}"
fi 

done

#add_user "Sam Vimes" "123" 