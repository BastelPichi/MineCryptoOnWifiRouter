# MineCryptoOnWifiRouter
 
 
 This is a short guide that shows you how to mine DuinoCoin on a wifi router.  <a href="https://duinocoin.com">DuinoCoin</a> is a crypto that can even be mined on such low power devices.
 
 <b>Warning! the <a href="https://www.youtube.com/watch?v=n1P3cpXcubQ" target="_blank">YouTube Video</a> is not anymore up to date. Just follow the readme here.</b>
 
1. Flash the router you want to use with  <a href="https://openwrt.org">Openwrt</a> . There many guides for your specific router out there. This will void your Warranty!
 If you want to buy a router in purpose I wouldt recomend a tplink. You can flash them very easely and theyre cheap.
2. SSH into your router. Under Linux run: "ssh root@[routerip]. Under Windows use Putty. The default port 22 is fine.
3. type: "opkg update", "opkg install python3" and "opkg install coreutils-nohup" to install python and nohup.
4. Now edit line 13 to your username, line 14 to the first led and line 15 to the second led. Theyre coments You can get the led names by visiting the openwrt webinterface and going to system -> LED-Configuration. Pick 2 that are free..
5. Now use a program like <a href="https://winscp.net/eng/download.php">Winscp</a> to get the miner.py script onto your router. Select SCP as protocol.
6. Then go back to putty and type "python3 miner.py".
7. If everything seems to work, and the router is mining, press Ctrl + c and type "nohup python3 miner.py &". If it doesnt, open a issue.
8. Thats it! Your router is now mining crypto! Happy Mining!

Offically tested Routers:
AVM Fritz!Box 4040: 100kh/s at 2400 difficulty(~15-20 DUCO per day)

How can I further develop this?
1. Create a fork
2. Change the things you want to change and make shure everything works
3. Open a pull request
