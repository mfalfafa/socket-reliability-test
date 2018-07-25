### Communication reliability test for multiple raspi3s and computer server using socket protocol through switch.
## Created by MF ALFAFA
## miftahf77@gmail.com
## 24 July 2018

Hardware Requirements :
1. Some Raspi3s (min. 5 Raspi3s)
2. Switch (tp-link TL-SG1016D 16-Port Gigabit Switch)
3. Computer Server

Software Rquirements :
1. Python 3 (3.5.3)
2. Python 3 script for Client and Server 

Configurations: 
For this testing, there are 5 Raspi3s :
1. Raspi 1 -> Client-0 (Wlan:192.168.10.100, Eth0:192.168.20.10)
2. Raspi 2 -> Client-1 (Wlan:192.168.10.101, Eth0:192.168.20.11)
3. Raspi 3 -> Client-2 (Wlan:192.168.10.102, Eth0:192.168.20.12)
4. Raspi 4 -> Client-3 (Wlan:192.168.10.103, Eth0:192.168.20.13)
5. Raspi 5 -> Client-4 (Wlan:192.168.10.104, Eth0:192.168.20.14)

PC Server (Eth:192.168.20.50)

the 5 Raspi3s are connected to a switch using RJ45 Cable. Computer PC is also connected to same switch.