rsync -r -e "ssh -i /Users/ryota/.ssh/rpi_id_rsa -p 2222" \
  --exclude '.git' \
  --exclude 'sync.sh' \
  ./src/* rpi@raspberrypi.local:/home/rpi/water/
