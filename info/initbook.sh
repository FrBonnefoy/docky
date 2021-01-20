
#!/bin/bash
python3 /Bookinfo/urls/consolidated.py
nohup python3 -u /Bookinfo/booking.py > progressbar.log &

/bin/bash
