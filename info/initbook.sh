#!/bin/bash

cd /Bookinfo/urls

python3 consolidated.py

cd /Bookinfo

nohup python3 -u booking.py > progressbar.log &

/bin/bash
