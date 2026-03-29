#!/bin/bash

#sed -i 's/\r$//' users.tsv

check_user() {
    local x=$1

    if grep -q "^${x}"$'\t' users.tsv; then
        echo "Exists"
    else 
        echo "Does not exist"
    fi
}

check_pass() {
    local p=$1
    local u=$2

    if grep -q "^${u}"$'\t'"${p}$" users.tsv; then
        echo "Match"
    else 
        echo "Issue"
    fi
}


read -p "Enter username of Player 1: " user1
read -p "Enter password for ${user1}: " pass1

#read -p "Enter username of Player 2: " user2
#read -p "Enter password for ${user2}: " pass2 


#hash1=$(echo -n ${pass1} | sha256sum | awk '{print $1}') 

echo "The hash for password 1 is: ${hash1}"

hash2=$(echo -n ${pass2} | sha256sum | awk '{print $1}') 

#echo "The hash for password 2 is: ${hash2}"

#echo ${user1} ${pass1}


u1=$(check_user "${user1}")
p1=$(check_pass "${hash1}" "${user1}") 

if [[ ${p1} == "Match" ]]; then
    echo "Successful!" 
elif [[ ${u1} == "Exists" ]]; then
    echo "Either username or password are incorrect."
else 
    echo "No such account exists."
fi




