#!/bin/bash
usage()
{
cat << EOF
usage: $0 options

Use this script to autologin to a remote host. 
(Storing your password in plain text is not a good idea!)

OPTIONS:
   -h      Show this message
   -s      Server address
   -u      Username to login with
   -p      Passord to login with
   -k      Unleash the kracken!
EOF
}

unleashTheKraken()
{
  echo "TODO!"
}

SERVER=
PASSWD=
VERBOSE=
while getopts "hs:u:p:k" OPTION
do
  case $OPTION in
        h)
            usage
            exit 1
            ;;
        s)
            SERVER=$OPTARG
            ;;
        u)  
            USERNAME=$OPTARG
            ;;
        p)
            PASSWORD=$OPTARG
            ;;
        k) 
            unleashTheKraken
            exit 0
            ;;
        ?)
      echo "error"

            usage
            exit
            ;;
     esac
done

if [[ -z $USERNAME ]] || [[ -z $SERVER ]] || [[ -z $PASSWD ]]
then
   /usr/bin/expect -c  "spawn ssh $USERNAME@$SERVER;\
  expect \".*password:\"; \
  send \"$PASSWORD\n \";\
  interact;"
fi

