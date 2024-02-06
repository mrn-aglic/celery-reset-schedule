#!/bin/sh

echo $1

rm logs.txt

if [ "$1" = 'scheduler' ]
then
    exec celery -A reset_schedule.beat beat -S redbeat.RedBeatScheduler --loglevel info
#    exec celery -A reset_schedule.beat beat --loglevel debug
elif [ "$1" = 'worker' ]
then
    exec celery -A reset_schedule.worker worker -Q default --loglevel info
elif [ "$1" = 'flower' ]
then
    exec celery -A reset_schedule.worker --broker=redis://redis:6379/0 flower --conf=/config/flowerconfig.py
fi

exec "$@"
