#!/usr/bin/bash


d=("keyboard" "pathfinding" "image" "numpy" "colorama")

for str in ${d[@]}; do
  pip3 install $str
done

version=$(python -V 2>&1 | grep -Po '(?<=Python )(.+)')

if [[ -z "$version" ]]
then
    echo -e "\nNo Python!" 
fi


treeFidi=`echo ${version//./} | cut -c1-4`

if [[ "$treeFidi" -lt "3110" && "$treeFidi" -ge "3100" ]]
then 
    echo -e "\nValid version ${version}\n\nRun program with ./main.py or python main.py"
else
    echo -e "\nInvalid version ${version}"
fi