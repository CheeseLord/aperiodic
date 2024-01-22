#!/bin/bash
python cleanup.py;
for i in {1..1000};
do
    python cover.py;
    if [ $? -eq 0 ]
    then
        mkdir shapes/temp;
        mv shapes/working/* shapes/temp/;
        python basis.py;
    fi
    python cleanup.py;
    rm -r shapes/temp;
done

