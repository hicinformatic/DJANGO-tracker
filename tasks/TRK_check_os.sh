#!/bin/bash

#
# Configuration system
#
DIRECTORY=$(dirname $0)
CANCONTINUE=0
SCRIPT=$1
TIMEOUT=$2
PIDFILE="${DIRECTORY}/${SCRIPT}.pid"
START="http://localhost/tracker/start/${1}/"

[[ $CHECKSSL -eq 0 ]] && CURLCMD="curl -sk" || CURLCMD="curl -s"
STATUS=$(curl -s $START)
[[ "$STATUS" =~ ^(OK).*$ ]] && STATUS=1 || STATUS=0

# Verification des doublons de processus automatisé
if [ -f $PIDFILE ]; then
    FILEPID=$(cat $PIDFILE)
    PIDPROC=$(ps aux | grep "$FILEPID" | grep -v "grep" | wc -l)
    if [ $PIDPROC -gt 0 ]; then
        CANCONTINUE=1
        if [ $STATUS == 1 ]; then
            $(kill -9 $FILEPID > /dev/null)
            $(rm $PIDFILE)
            CANCONTINUE=0
        else
            CANCONTINUE=1
        fi
    fi
fi

# Verification de doublon de processus avec erreurs
SCRIPTPROC=$(ps aux | grep "${SCRIPT}.py" | grep -v "grep" | wc -l)
if [ $SCRIPTPROC -gt 0 ]; then
    CANCONTINUE=1
    ALLPROC=$(ps -ewo pid,etimes,cmd | grep "${SCRIPT}.py" | grep -v "grep")
    while read pid etimes cmd
    do
        if [ "$etimes" -gt $TIMEOUT ]; then
            if [ $STATUS == 1 ]; then
                $(kill -9 $pid > /dev/null)
                CANCONTINUE=0
            fi
        fi
    done <<< "$(echo -e "$ALLPROC")"
fi

$(rm -f ${PIDFILE})
exit $CANCONTINUE