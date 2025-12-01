#!/bin/bash

input_file="logs.txt" #path of input file
output_file="results.txt" #path to save the output

exec > "$output_file"

declare -A domain_status

while IFS=";" read status domain loginfo; do
    status=$(echo $status | xargs)
    domain=$(echo $domain | xargs)
    loginfo=$(echo $loginfo | xargs)

    if [[ $status -eq 255 ]]; then
        domain_status[$domain]="255"
    elif [[ $status -eq 44 && ${domain_status[$domain]} == "255" ]]; then
        domain_status[$domain]="255_to_44"
    fi

    if [[ $status -eq 255 && ${domain_status[$domain]} != "255_to_44" ]]; then
        echo "CRITICAL :: $domain : $loginfo"
    elif [[ ${domain_status[$domain]} == "255_to_44" ]]; then
        echo "OK :: $domain : $loginfo"
    elif [[ $status -ne 255 ]]; then
        echo "OK :: $domain : $loginfo"
    fi
done < "$input_file"




'''
Read the input file; saving the output in output file; splits the log as status, domain and loginfo; set variable domain_status; Removes space from the splitted log;
Check the status with 255 and set domain_status as 255 if true; If false, the domain_status is empty, check the status with 255 and domain_status with 255, if true,
domain_status will be 255_to_44; Based on the domain_status and status, the output will be saved in given path of output file.
'''