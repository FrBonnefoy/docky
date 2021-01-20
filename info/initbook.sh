
#!/bin/bash
python3 /Bookinfo/urls/consolidated.py
cd /Bookinfo
nohup python3 -u booking.py > progressbar.log &

/bin/bash
