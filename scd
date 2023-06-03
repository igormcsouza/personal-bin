#!/bin/bash

# Check if argument is provided
if [ -z "$1" ]
then
  echo "Usage: . scd <directory>"
  return 1
fi

# Check if the argument is a valid directory in the current working directory
if [ -d "./$1" ]
then
  cd "./$1"
  return 0
fi

# Check if the argument is a valid directory in any of the directories listed in .smartcdfolders
if [ -s "$HOME/.smartcdfolders" ]
then
  while read -r dir
  do
    if [ -d "$dir/$1" ]
    then
      cd "$dir/$1"
      return 0
    fi
  done < "$HOME/.smartcdfolders"
fi

# If the argument is not a valid directory, print an error message
echo "Directory not found"
return 1

