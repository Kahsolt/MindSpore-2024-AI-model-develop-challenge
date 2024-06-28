#/bin/bash

date

python test_serving_performance.py --task 1 -X 0.5 -T 3000 -P 8835 -O "./"

date

echo "Done" >> DONE
