#!/usr/bin/bash

DIR="$( cd "$( dirname "$0" )" && pwd )"

echo "The chats listed below will be read:"

cd $DIR/Chats
for entry in *;
do
	if [ "$entry" = "empty.txt" ]; then
		continue
	else
		echo "${entry[0]}"
	fi
done
