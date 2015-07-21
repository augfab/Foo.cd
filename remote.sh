#!/bin/bash

print_help() {
	cat <<-EOF
	Usage: $(basename $0) [-h] [-p PIPE]
	Control Foo.cd via this remote interface

	Options:
	    -h               Print this help and exit
	    -p PIPE          Path to a writable named pipe, defaults to ./pipe

	Write following commands to the terminal in order to control Foo.cd:
	    Space, 1         Play/Pause
	    BackSpace, 2     Stop
	    CTRL-D,9         Quit
	    W, A, S, D       Navigate in tree
	    Up, Down         Volume Up/Down
	    Right, Left      Previous/Next song
	    Enter            Play selected song
	    Tab              Append selected song to playlist

	Exit status:
	    Returns 1 if no writable pipe (default ./pipe or inputted with -p) \
exists.
	EOF
}

while [ $# -gt 0 ]
do
	key="$1"
	case $key in
		-h)
			print_help
			exit 0
			;;
		-p)
			shift
			if [ -p "$1" ]
			then
				if [ -w "$1" ]
				then
					$PIPE="$1"
				else
					>&2 echo "$1 does not have write permission"
					>&2 print_help
					exit 1
				fi
			else
				>&2 echo "$1 is not a pipe or does not exist"
				>&2 print_help
				exit 1
			fi
			;;
		*)
			;;
	esac
	shift
done

if [ -z "$PIPE" ]
then
	SCRIPTPATH=$(dirname $(readlink -f $0))
	if [ -p "$SCRIPTPATH/pipe" ] && [ -w "$SCRIPTPATH/pipe" ]
	then
		PIPE="$SCRIPTPATH/pipe"
	else
		>&2 echo "$SCRIPTPATH/pipe is not a writable pipe or does not exist"
		>&2 print_help
		exit 1
	fi
fi


# internal field separator for read
# enables the use of space and tab as normal input characters
IFS=""

while true
do
	read -rsn1 ui
	case "$ui" in
		$'\033') # escape for ^[ Escape key
			read -rsn1 -t 0.01 tmp
			if [ "$tmp" = "[" ]
			then
				read -rsn1 -t 0.01 tmp
				case "$tmp" in
					A) # ^[[A is Up key
						echo Up
						;;
					B)
						echo Down
						;;
					C)
						echo Right
						;;
					D)
						echo Left
						;;
					*)
						;;
				esac
			fi
			;;
		"")
			echo tree_validate > $PIPE
			;;
		z|w)
			echo tree_up > $PIPE
			;;
		s)
			echo tree_down > $PIPE
			;;
		q|a)
			echo tree_left > $PIPE
			;;
		d)
			echo tree_right > $PIPE
			;;
		1|" ")
			echo play_pause > $PIPE
			;;
		$'\177'|2) # escape for ^? Backspace key
			echo stop > $PIPE
			;;
		$'\004'|9) # escape for ^D
			echo quit > $PIPE
			exit 0
	esac
done

exit 0
