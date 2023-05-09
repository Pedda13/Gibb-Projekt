while true 
do
UserIPAddress=$(zenity --entry --text="Please enter IP-Adress to Remote control")
UserName=$(zenity --entry --text="Please enter an Username which has enough permissions")
UserChoice=$(zenity --list --title="Choose what you want to do" --column "Choose" Restart Shutdown Custom)



echo $UserChoice
if [ $UserChoice == "Restart" ]
then
	ssh -t $UserName@$UserIPAddress "sudo shutdown now -r"
	UserAgain=$(zenity --entry --text="Do you want to use another IP?(y/n)")
	if [ $UserAgain == "y" ]
	then
		continue
	else
		break
	fi
fi
if [ $UserChoice == "Shutdown" ]
then
	ssh -t $UserName@$UserIPAddress "sudo shutdown now"
	UserAgain=$(zenity --entry --text="Do you want to use another IP?(y/n)")
	if [ $UserAgain == "y" ]
	then
		continue
	else
		break
	fi
fi
if [ $UserChoice == "Custom" ]
then
	Usercommand=$(zenity --entry --text="Please enter the command you want to use")
	ssh -t $UserName@$UserIPAddress "$Usercommand"
	UserAgain=$(zenity --entry --text="Do you want to use another IP?(y/n)")
	if [ $UserAgain == "y" ]
	then
		continue
	else
		break
	fi
fi
done
