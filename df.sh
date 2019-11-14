#!/bin/sh
: <<desc
Shows the top of /etc/passwd on the terminal for 1 second 
and then restores the terminal to exactly how it was
desc

tput smcup #save previous state

head -n$(tput lines) /etc/passwd #get a screenful of lines
sleep 1

tput rmcup #restore previous state
