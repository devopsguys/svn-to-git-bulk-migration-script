#!/bin/bash

# Try and find any directories that only contain .git
# These directories have not been fully checked out and
# are mid-migration

echo "Repositories still in progress"
echo ""

inprogress=0

for D in `find migration/* -maxdepth 0 -type d`; do
subdircount=`find $D -maxdepth 1 | grep -v ".git" | wc -l`
if [ $subdircount -eq 1 ]
then
  let "inprogress++"
  echo $D | awk -F"/" '{printf $2}'
  echo ' [Incomplete]'
else
  echo $D | awk -F"/" '{printf $2}'
  echo -n " | "
  echo -n `cd $D; git log -1 --format=%cd  --date=iso`
  echo
fi

total=`find migration -maxdepth 1 -type d | wc -l`

done

completed=`expr $total - $inprogress`
progress=`echo "scale=3; ($completed / $total) * 100" | bc`

echo ""
echo "In progress: $inprogress"
echo "Total: $total"
echo "Progress: $progress%"
