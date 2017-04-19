#!/bin/bash

#
# Configuration system
#
RUNNING=0
DIRECTORY=$(dirname $0)
PIDFILE="$DIRECTORY/exportftp.pid"
CSVFILE="$DIRECTORY/exportftp.csv"
START="$PROTOCOL://$HOST/SendinBlue/start/2/"
STOP="$PROTOCOL://$HOST/SendinBlue/stop/2/"
EXPORT="$PROTOCOL://$HOST/SendinBlue/export/delta/"

[[ $CHECKSSL -eq 0 ]] && CURLCMD="curl -sk" || CURLCMD="curl -s"
STATUS=$($CURLCMD -H "username:$USERNAME" -H  "password:$PASSWORD" $START)
[[ "$STATUS" =~ ^(OK).*$ ]] && STATUS=1 || STATUS=0

# Verification des doublons de processus automatisé
if [ -f $PIDFILE ]; then
    FILEPID=$(cat $PIDFILE)
    PIDPROC=$(ps aux | grep "$FILEPID" | grep -v "grep" | wc -l)
    if [ $PIDPROC -gt 0 ]; then
        if [ $STATUS == 1 ]; then
            $(kill -9 $FILEPID)
        else
            RUNNING=1
        fi
    fi
fi

# Verification de doublon de processus avec erreurs
SCRIPTPROC=$(ps aux | grep "$0" | grep -v "grep" | wc -l)
if [ $SCRIPTPROC -gt 2 ]; then
    RUNNING=1
    ALLPROC=$(ps -ewo pid,etimes,cmd | grep "$0" | grep -v "grep")
    while read pid etimes cmd
    do
        if [ "$etimes" -gt 10 ]; then
            if [ $STATUS == 1 ]; then
                RUNNING=0
                $(kill -9 $pid > /dev/null)
            fi
        fi
    done <<< "$(echo -e "$ALLPROC")"
fi