#!/bin/bash
python cleanup.py;
for i in {1..1000};
do
    python classify.py;
    python cleanup.py;
done

