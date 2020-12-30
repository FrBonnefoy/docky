# Consolidate url file

read_files = glob.glob("booking_flag_url*")
with open("consolidatedflagurls.txt", "wb") as outfile:
    for f in read_files:
        with open(f, "rb") as infile:
            outfile.write(infile.read())

#Import logs

flogname='consolidatedflagurls.txt'
with open(flogname) as flogdone:
    done_urls=flogdone.readlines()

done_urls=list(filter(lambda x: 'https://www.booking.com/' in x, done_urls))

with open("booking_flag_url.txt", "wb") as outfile:
    for url in done_urls:
        outfile.write(url)
        outfile.write('\n')
