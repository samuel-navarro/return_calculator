#!/usr/bin/bash

set -e
set -u

if [ $# -ne  1 ]; then
    echo "Usage: $0 <years_per_run>"
    exit -1
fi

YEARS_PER_RUN=$(($1))

INITIAL_YEAR=1950
END_YEAR=2019

RUN_YEAR=$(($INITIAL_YEAR + $YEARS_PER_RUN))

while [ $RUN_YEAR -le $END_YEAR ]; do
    RETURN=$(python ./index_process.py -f sp500.csv -m 900 -y0 $INITIAL_YEAR -y1 $RUN_YEAR | grep "Average return" | cut -f 2 -d : | sed 's/[^0-9\.]//g' | head -n1)
    echo "Return $INITIAL_YEAR - $RUN_YEAR: $RETURN %"

    INITIAL_YEAR=$(($INITIAL_YEAR + 1))
    RUN_YEAR=$(($RUN_YEAR + 1))
done
