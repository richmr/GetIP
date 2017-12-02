#!/bin/bash

if [ "$1" != "" ]; then
    echo "Getip will send alert messages to: "$1
    echo "Please make sure your localhost email server is set up."
else
    echo "Please specify an email to send alert messages to."
    echo "Example: "$0" myemail@email.com"
fi


if ! [ $(id -u) = 0 ]; then
   echo "Installing getip for persistent use requires root access"
   echo "You can run this in user space, just ensure the logfile and currentip files are user accessible."
   exit 1
fi

#mkdir /usr/bin/getip
#cp *.py /usr/bin/getip
#mkdir /var/log/getip

#echo -e '#!/bin/bash\n\npython /usr/bin/getip/getip.py --source "ifconfig.me" --alertemail "'$1'"' > /etc/cron.daily/getip
#chmod u+x /etc/cron.daily/getip


