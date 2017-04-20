#!/bin/bash

#
# Configuration system
#
CANCONTINUE=0
DIRECTORY=$(dirname $0)

TASKS = ('sort(Recurring)''report(Hourly)' 'report(Daily)' 'report(Monthly)' 'report(Annually)' 'purge(Report)' 'purge(Visit)' 'purge(Task)')
TASK = ${TASKS[$1]}
PIDFILE="${DIRECTORY}/${SCRIPT}.pid"

START="$PROTOCOL://$HOST/tracker/start/${1}/"
RUNNING="$PROTOCOL://$HOST/tracker/running/${1}/"
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
            $(kill -9 $FILEPID > /dev/null)
            $(rm $PIDFILE)
        else
            CANCONTINUE=1
        fi
    fi
fi

# Verification de doublon de processus avec erreurs
SCRIPTPROC=$(ps aux | grep "${TASK}.pid" | grep -v "grep" | wc -l)
if [ $SCRIPTPROC -gt 1 ]; then
    CANCONTINUE=1
    ALLPROC=$(ps -ewo pid,etimes,cmd | grep "${TASK}.py" | grep -v "grep")
    while read pid etimes cmd
    do
        if [ "$etimes" -gt $2 ]; then
            if [ $STATUS == 1 ]; then
                $(kill -9 $pid > /dev/null)
                CANCONTINUE=0
            fi
        fi
    done <<< "$(echo -e "$ALLPROC")"
fi

echo $CANCONTINUE
exit($CANCONTINUE)