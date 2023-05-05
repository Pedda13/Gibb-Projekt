while true 
do
UserIPAddress=$(zenity --entry --text="Please enter IP-Adress to Remote control")
UserUsername=$(zenity --entry --text="Please enter the Username which has root permissions on the remote Computer")
UserChoice=$(zenity --list --title="Choose what you want to do" --column "Choose" Restart Shutdown)

echo $UserChoice
if [ $UserChoice == "Restart" ]
then
	ssh -t $UserUsername@$UserIPAddress "shutdown now -r"
	UserAgain=$(zenity --entry --text="Do you want to use another IP?(y/n)")
	if [ $UserAgain == "y" ]
		then
			continue
		else
			break
	fi
else
	ssh -t $UserUsername@$UserIPAddress "shutdown now"
	UserAgain=$(zenity --entry --text="Do you want to use another IP?(y/n)")
	if [ $UserAgain == "y" ]
	then
		continue
	else
		break
	fi
fi
done