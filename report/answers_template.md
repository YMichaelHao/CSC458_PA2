# CSC458 PA2 Report

Names / UTORids:

## Part 0 - Mininet introduction and the forwarding/control-plane bridge

1. **Mininet components.** In your own words, define a Mininet host, switch, link, and controller. What Linux mechanisms make it possible to emulate many hosts on one VM?

 - A Mininet host is like a virtual computer, it's a process with it's own private network namespace, interfaces, IP/MAC addresess, so it can run normal linux commands.

 - A Switch is a software switch that forwards frames betweens it ports based on th rules in it flow table

 - A Link are essentially virtual cables which transfer data.

 - The Controller is the program that decides how the switches should forward traffic.

 - The Linux Mechanisms that make it possible to emulate many hosts on one VM are the network namespaces, they give each host its own isolated network stack while all hosts share one kernel, which is much lighter than running one VM per host. Open vSwitch brideges acts as the switches.

2. **CLI orientation.** Include the output of `net` and `links` for the original one-host/one-switch topology. Give one command that you ran inside `h1` from the Mininet CLI and explain how it differs from an `mn` launcher command.

```
mininet> net
h1 h1-eth0:s1-eth1
s1 lo:  s1-eth1:h1-eth0
c0
mininet> links
h1-eth0<->s1-eth1 (OK OK) 


mininet> h1 ip addr
1: lo: <LOOPBACK,UP,LOWER_UP> mtu 65536 qdisc noqueue state UNKNOWN group default qlen 1000
    link/loopback 00:00:00:00:00:00 brd 00:00:00:00:00:00
    inet 127.0.0.1/8 scope host lo
       valid_lft forever preferred_lft forever
    inet6 ::1/128 scope host 
       valid_lft forever preferred_lft forever
2: h1-eth0@if7: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc noqueue state UP group default qlen 1000
    link/ether 7e:58:8e:2d:2c:00 brd ff:ff:ff:ff:ff:ff link-netnsid 0
    inet 10.0.0.1/8 brd 10.255.255.255 scope global h1-eth0
       valid_lft forever preferred_lft forever
    inet6 fe80::7c58:8eff:fe2d:2c00/64 scope link 
       valid_lft forever preferred_lft forever
```
 - One command I ran inside `h1` from the mininet CLI was `ip addr`. It runs an ordinary Linux command insider host `h1`, in a network that already exists, the output shows only h1's own interfaces which shows it ran insde h1's private network namespace. It differs from the mn launcher command because the mn launcher is run from the normal VM shell and builds the whole network from the options given, then open the Mininet CLI.

3. **Task 1 - more hosts.** Show that your one-switch/five-host topology has the expected five links and 0% `pingall` loss before link constraints are introduced.
```
mininet> links
h1-eth0<->s1-eth1 (OK OK) 
h2-eth0<->s1-eth2 (OK OK) 
h3-eth0<->s1-eth3 (OK OK) 
h4-eth0<->s1-eth4 (OK OK) 
h5-eth0<->s1-eth5 (OK OK) 
mininet> net
h1 h1-eth0:s1-eth1
h2 h2-eth0:s1-eth2
h3 h3-eth0:s1-eth3
h4 h4-eth0:s1-eth4
h5 h5-eth0:s1-eth5
s1 lo:  s1-eth1:h1-eth0 s1-eth2:h2-eth0 s1-eth3:h3-eth0 s1-eth4:h4-eth0 s1-eth5:h5-eth0
c0
mininet> pingall
*** Ping: testing ping reachability
h1 -> h2 h3 h4 h5 
h2 -> h1 h3 h4 h5 
h3 -> h1 h2 h4 h5 
h4 -> h1 h2 h3 h5 
h5 -> h1 h2 h3 h4 
*** Results: 0% dropped (20/20 received)
```
4. **Task 2 - more switches.** Show the final two-switch/ten-host structure and the inter-switch link. Briefly describe how you refactored the topology Python code to avoid repetition.
```
mininet> net
h1 h1-eth0:s1-eth1
h2 h2-eth0:s1-eth2
h3 h3-eth0:s1-eth3
h4 h4-eth0:s1-eth4
h5 h5-eth0:s1-eth5
h6 h6-eth0:s2-eth1
h7 h7-eth0:s2-eth2
h8 h8-eth0:s2-eth3
h9 h9-eth0:s2-eth4
h10 h10-eth0:s2-eth5
s1 lo:  s1-eth1:h1-eth0 s1-eth2:h2-eth0 s1-eth3:h3-eth0 s1-eth4:h4-eth0 s1-eth5:h5-eth0 s1-eth6:s2-eth6
s2 lo:  s2-eth1:h6-eth0 s2-eth2:h7-eth0 s2-eth3:h8-eth0 s2-eth4:h9-eth0 s2-eth5:h10-eth0 s2-eth6:s1-eth6
c0
mininet> links
h1-eth0<->s1-eth1 (OK OK) 
h2-eth0<->s1-eth2 (OK OK) 
h3-eth0<->s1-eth3 (OK OK) 
h4-eth0<->s1-eth4 (OK OK) 
h5-eth0<->s1-eth5 (OK OK) 
h6-eth0<->s2-eth1 (OK OK) 
h7-eth0<->s2-eth2 (OK OK) 
h8-eth0<->s2-eth3 (OK OK) 
h9-eth0<->s2-eth4 (OK OK) 
h10-eth0<->s2-eth5 (OK OK) 
s1-eth6<->s2-eth6 (OK OK) 
mininet> pingall
*** Ping: testing ping reachability
h1 -> h2 h3 h4 h5 h6 h7 h8 h9 h10 
h2 -> h1 h3 h4 h5 h6 h7 h8 h9 h10 
h3 -> h1 h2 h4 h5 h6 h7 h8 h9 h10 
h4 -> h1 h2 h3 h5 h6 h7 h8 h9 h10 
h5 -> h1 h2 h3 h4 h6 h7 h8 h9 h10 
h6 -> h1 h2 h3 h4 h5 h7 h8 h9 h10 
h7 -> h1 h2 h3 h4 h5 h6 h8 h9 h10 
h8 -> h1 h2 h3 h4 h5 h6 h7 h9 h10 
h9 -> h1 h2 h3 h4 h5 h6 h7 h8 h10 
h10 -> h1 h2 h3 h4 h5 h6 h7 h8 h9 
*** Results: 0% dropped (90/90 received)
```
For the refactor i looped over the hosts, and kept a hosts per switch constant such that i can attach a certain numbers of hosts to each switch.


5. **Basic testing.** For an unconstrained `h1 -> h8` path, report `ping -c 5` packet loss and average RTT, and report one `iperf3` throughput measurement. Was the first ping slower than later pings? If so, connect this observation to mechanisms such as PA1 ARP resolution and switch learning.
```
mininet> h1 ping -c 5 h8
PING 10.0.0.8 (10.0.0.8) 56(84) bytes of data.
64 bytes from 10.0.0.8: icmp_seq=1 ttl=64 time=22.0 ms
64 bytes from 10.0.0.8: icmp_seq=2 ttl=64 time=0.428 ms
64 bytes from 10.0.0.8: icmp_seq=3 ttl=64 time=0.121 ms
64 bytes from 10.0.0.8: icmp_seq=4 ttl=64 time=0.082 ms
64 bytes from 10.0.0.8: icmp_seq=5 ttl=64 time=0.104 ms

--- 10.0.0.8 ping statistics ---
5 packets transmitted, 5 received, 0% packet loss, time 4051ms
rtt min/avg/max/mdev = 0.082/4.541/21.974/8.717 ms
```
Packet loss was 0% and the average RTT was 4.541 ms.
```
mininet> h8 iperf3 -s &
mininet> h1 iperf3 -c h8 -p 5201
Connecting to host 10.0.0.8, port 5201
[  5] local 10.0.0.1 port 57866 connected to 10.0.0.8 port 5201
[ ID] Interval           Transfer     Bitrate         Retr  Cwnd
[  5]   0.00-1.00   sec  1008 MBytes  8.45 Gbits/sec    2   8.17 MBytes       
[  5]   1.00-2.00   sec  1.17 GBytes  10.0 Gbits/sec    3   8.17 MBytes       
[  5]   2.00-3.00   sec  1.21 GBytes  10.4 Gbits/sec    5   8.17 MBytes       
[  5]   3.00-4.00   sec  1.20 GBytes  10.3 Gbits/sec    3   8.17 MBytes       
[  5]   4.00-5.00   sec  1.11 GBytes  9.55 Gbits/sec    3   8.17 MBytes       
[  5]   5.00-6.00   sec  1.16 GBytes  10.0 Gbits/sec    1   8.17 MBytes       
[  5]   6.00-7.00   sec  1.18 GBytes  10.2 Gbits/sec    3   8.17 MBytes       
[  5]   7.00-8.00   sec  1.21 GBytes  10.4 Gbits/sec    3   8.17 MBytes       
[  5]   8.00-9.00   sec  1.23 GBytes  10.6 Gbits/sec    0   8.17 MBytes       
[  5]   9.00-10.00  sec  1.17 GBytes  10.1 Gbits/sec    2   8.17 MBytes       
- - - - - - - - - - - - - - - - - - - - - - - - -
[ ID] Interval           Transfer     Bitrate         Retr
[  5]   0.00-10.00  sec  11.6 GBytes  9.99 Gbits/sec   25             sender
[  5]   0.00-20.06  sec  11.6 GBytes  4.98 Gbits/sec                  receiver

iperf Done.
```
iperf3 measured 9.99 Gbits/sec at the sender.

Yes, the first ping (22 ms) was much slower because h1 only knows h8's ip address but not h8's MAC address, so it has to use ARP to find h8's MAC address. The switches also haven't learned where h8 is yet, so the first packets are sent to the controller, which floods them and installs forwarding rules in s1 and s2. After that, h1 has h8's MAC chached and the switches already have the rules, so later pings are forwarded immediately.
6. **Multiple topologies.** State the second topology name you added to the `topos` dictionary and show the `mn` command that launches it.

The second topology name i added was constrainedTopology, the command that launches it is: `sudo mn --custom ./topology.py --topo constrainedTopology --switch ovs`


7. **TCLink.** Configure the `s1-s2` link for 50 Mbit/s, 30 ms delay, and 10% loss. Report a `ping` observation and an `iperf3` observation and explain how they differ from the unconstrained baseline. Do not expect an exact TCP throughput under loss.
```
mininet> h1 ping -c 5 h8
PING 10.0.0.8 (10.0.0.8) 56(84) bytes of data.
64 bytes from 10.0.0.8: icmp_seq=2 ttl=64 time=63.0 ms
64 bytes from 10.0.0.8: icmp_seq=4 ttl=64 time=60.9 ms
64 bytes from 10.0.0.8: icmp_seq=5 ttl=64 time=61.1 ms

--- 10.0.0.8 ping statistics ---
5 packets transmitted, 3 received, 40% packet loss, time 4023ms
rtt min/avg/max/mdev = 60.892/61.666/63.018/0.959 ms
```
```
mininet> h8 iperf3 -s &
mininet> h1 iperf3 -c h8 -p 5201
Connecting to host 10.0.0.8, port 5201
[  5] local 10.0.0.1 port 57060 connected to 10.0.0.8 port 5201
[ ID] Interval           Transfer     Bitrate         Retr  Cwnd
[  5]   0.00-1.00   sec   332 KBytes  2.72 Mbits/sec   11   7.07 KBytes       
[  5]   1.00-2.00   sec  63.6 KBytes   521 Kbits/sec    4   7.07 KBytes       
[  5]   2.00-3.00   sec   127 KBytes  1.04 Mbits/sec    3   9.90 KBytes       
[  5]   3.00-4.00   sec  63.6 KBytes   521 Kbits/sec    8   5.66 KBytes       
[  5]   4.00-5.00   sec   191 KBytes  1.56 Mbits/sec    5   9.90 KBytes       
[  5]   5.00-6.00   sec  63.6 KBytes   521 Kbits/sec    7   2.83 KBytes       
[  5]   6.00-7.00   sec  0.00 Bytes  0.00 bits/sec    5   4.24 KBytes       
[  5]   7.00-8.00   sec  63.6 KBytes   522 Kbits/sec    4   5.66 KBytes       
[  5]   8.00-9.00   sec  63.6 KBytes   521 Kbits/sec    5   2.83 KBytes       
[  5]   9.00-10.00  sec  63.6 KBytes   522 Kbits/sec    4   5.66 KBytes       
- - - - - - - - - - - - - - - - - - - - - - - - -
[ ID] Interval           Transfer     Bitrate         Retr
[  5]   0.00-10.00  sec  1.01 MBytes   846 Kbits/sec   56             sender
[  5]   0.00-10.18  sec   896 KBytes   721 Kbits/sec                  receiver

iperf Done.
```
On the contstrained baseline, for ping: RTT rose from 4.5ms to 61.7ms because the 30ms is applied in both directions on the s1-s2 link and loss rose form 0% to 40% because each direction randomly drops 10% of the packets
For iperf3: TCP throughput went from 9.99 Gbits/sec at the sender to 846 Kbits/sec at the sender because TCP treats each loss as congestion and keeps shrinking its sending window.

8. **Remote controller / SDN.** Describe what happened when you used the remote reference controller and what happened after the controller was stopped or unavailable. Distinguish the switch data plane from the controller control plane. If the final course VM does not expose the `controller` command, record that fact and explain the experiment you would perform; no mark is lost for that VM-specific absence.

With the remote controller running i get:
```
mininet> pingall
*** Ping: testing ping reachability
h1 -> h2 h3 h4 h5 h6 h7 h8 h9 h10 
h2 -> h1 h3 h4 h5 h6 h7 h8 h9 h10 
h3 -> h1 h2 h4 h5 h6 h7 h8 h9 h10 
h4 -> h1 h2 h3 h5 h6 h7 h8 h9 h10 
h5 -> h1 h2 h3 h4 h6 h7 h8 h9 h10 
h6 -> h1 h2 h3 h4 h5 h7 h8 h9 h10 
h7 -> h1 h2 h3 h4 h5 h6 h8 h9 h10 
h8 -> h1 h2 h3 h4 h5 h6 h7 h9 h10 
h9 -> h1 h2 h3 h4 h5 h6 h7 h8 h10 
h10 -> h1 h2 h3 h4 h5 h6 h7 h8 h9 
*** Results: 0% dropped (90/90 received)
```
But after i stopped the controller, pingall dropped 100% because the switches flow table can only forward using rules already installed, and without the controller no new rules could be added.
```
mininet> pingall
*** Ping: testing ping reachability
h1 -> X X X X X X X X X 
h2 -> X X X X X X X X X 
h3 -> X X X X X X X X X 
h4 -> X X X X X X X X X 
h5 -> X X X X X X X X X 
h6 -> X X X X X X X X X 
h7 -> X X X X X X X X X 
h8 -> X X X X X X X X X 
h9 -> X X X X X X X X X 
h10 -> X X X X X X X X X 
*** Results: 100% dropped (0/90 received)
```

9. **Bridge to PA2 routing.** In `tools/mininet_intro.py`, why does `h1` initially fail to reach `h3` even though the physical links are up? Paste the final `ip route` output from R1/R2/R3 after you install correct static routes. After `link r2 r3 down`, which entries remain and why does reachability fail? Relate this to why a dynamic routing protocol is needed.

`h1` fails to reach `h3` because each router only has routes to its connected subnets, so R1 has no route to 10.3.0.0/24 and drops h1's packet, even though the links are up

```
mininet> r1 ip route
10.1.0.0/24 dev r1-stub proto kernel scope link src 10.1.0.1 
10.2.0.0/24 via 10.254.0.6 dev r1-r2 
10.3.0.0/24 via 10.254.0.6 dev r1-r2 
10.254.0.4/30 dev r1-r2 proto kernel scope link src 10.254.0.5 
mininet> r2 ip route
10.1.0.0/24 via 10.254.0.5 dev r2-r1 
10.2.0.0/24 dev r2-stub proto kernel scope link src 10.2.0.1 
10.3.0.0/24 via 10.254.1.154 dev r2-r3 
10.254.0.4/30 dev r2-r1 proto kernel scope link src 10.254.0.6 
10.254.1.152/30 dev r2-r3 proto kernel scope link src 10.254.1.153 
mininet> r3 ip route
10.1.0.0/24 via 10.254.1.153 dev r3-r2 
10.2.0.0/24 via 10.254.1.153 dev r3-r2 
10.3.0.0/24 dev r3-stub proto kernel scope link src 10.3.0.1 
10.254.1.152/30 dev r3-r2 proto kernel scope link src 10.254.1.154
```

After link r2 r3 down, R1 still sends h3's traffic to R2 which has lost its route to R3 and since static routes can't adapt to failures, then a dynamic routing protocol is needed to recompute routes automatically

10. **PA1 reuse.** Explain the separation among: (a) PA1 longest-prefix forwarding lookup, (b) a PA2 DV/LS route computation for a destination prefix, and (c) the Linux FIB entry installed by the staff runtime.


(a) PA1 longest-prefix forwarding lookup: this looks up each packet's destintion and picks the most specific matching route
(b) a PA2 DV/LS route computation for a destination prefix: this figures ou the best next hop for each destination using messaging from neighboring routers
(c) the Linux FIB entry installed by the staff runtime: this is the ruote that DV/LS chose, which is install into the kernel so (a) csan use it for every packet


## Part III - DV/LS experiments

### A. Correctness and forwarding

Provide one DV and one LS example showing that the protocol state, Linux `ip route`, `ping`, and `traceroute` agree with the expected shortest path.

### B. Failure convergence

Fill in the table for `failure_alt.json`.

| Protocol | DV mode | Initial convergence (s) | Reconvergence (s) | Control messages during event | Control bytes during event |
|---|---|---:|---:|---:|---:|
| DV | basic | | | | |
| DV | poison reverse | | | | |
| LS | - | | | | |

Explain the path before and after the R2-R4 failure.

### C. Count to infinity

Run `count_to_infinity.json` with DV basic and poison reverse. From the generated control-plane capture/status, give at least three successive metrics that illustrate count-to-infinity in basic DV. Explain why poison reverse changes this behavior.

### D. Cost change

Run `cost_change.json` with DV and LS. State the R1 -> 10.4.0.0/24 route before and after the cost change, and compare how the two protocols disseminate the new information.

### E. DV versus LS

In 200-300 words, compare what each router knows, what is carried in control messages, control overhead, convergence behavior, and the failure modes you observed. Refer to your own measurements.
