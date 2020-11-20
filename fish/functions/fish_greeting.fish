# # Set probabilty to be 1 in 5
function fish_greeting 

	echo
    set_color magenta
	echo -e (uname -ro | awk '{print " \\\\e[1mOS: \\\\e[0;32m"$0"\\\\e[0m"}')
    set_color magenta
	echo -e (uptime -p | sed 's/^up //' | awk '{print " \\\\e[1mUptime: \\\\e[0;32m"$0"\\\\e[0m"}')
    set_color magenta
	echo -e (uname -n | awk '{print " \\\\e[1mHostname: \\\\e[0;32m"$0"\\\\e[0m"}')
	echo

 if [ (math (random)'%100') -le 5 ]
        weather city Delhi IN
    end 


        todo
	echo ""  
   

end

