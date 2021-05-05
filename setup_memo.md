
# setup machine
- ssh
- user
- wifi
- i2c

# install grovepi

```
sudo apt-get install libatlas-base-dev 
sudo pip3 install --default-timeout=10000 numpy
```

GrovePi Script install.sh
user が pi じゃない場合、install.sh / update.sh のユーザー部分を書き換える必要がある。
https://qiita.com/yukataoka/items/9df2c74f7cd514e04b97#grove-pi%E3%81%AE%E3%83%A9%E3%82%A4%E3%83%96%E3%83%A9%E3%83%AA%E3%82%A3%E4%B8%8D%E5%85%B7%E5%90%88

# setup display

https://101010.fun/iot/raspi-oled.html

```
sudo pip3 install adafruit-blinka
sudo pip3 install adafruit-pillow
sudo pip3 install adafruit-circuitpython-ssd1306
sudo apt-get install libopenjp2-7
sudo apt-get install libtiff5
```

