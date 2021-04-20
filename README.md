# MineCryptoOnWifiRouter
 
 <b>Warning! This is still under development. Everything at your own risk.</b>
 
 This is a small Tutorial that shows you how to mine DuinoCoin on a wifi router.  <a href="https://duinocoin.com">DuinoCoin</a> is a crypto that can even be mined on such low power devices.

1. Flash the router you want to use with  <a href="https://openwrt.org">Openwrt</a> . There many guides for your specific router out there. This will void your Warranty!
 If you want buy a router in purpose I wouldt recomend a tplink. You can glash them very easely and theyre cheap.
2. SSH into your router. Under Linux run: "ssh root@[routerip]. Under Windows use Putty. The default port 22 is fine.
3. type: "opkg update", "opkg install python3" and "opkg install coreutils-nohup" to install python and nohup.
4. Now edit the led names in the script. Also change Pichi to your username. There comments.
5. Now use a program like winscp to get the miner.py script onto your router.
6. Then go back to ssh and type "nohup python3 miner.py &".
7. Thats it! Your router is now mining crypto! Happy Mining!

Offically tested Routers:
AVM Fritz!Box 4040: 100kh/s at 2400 difficulty(~15 DUCO per day)
