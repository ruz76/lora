# TODO cron?
while :
do
  LINE=`python3 generateLine.py 0`; python3 getPosition.py $LINE 0
  LINE=`python3 generateLine.py 1`; python3 getPosition.py $LINE 1
  python3 getPositionFromTrack.py 3
	sleep 10
done
