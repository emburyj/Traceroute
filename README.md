# Traceroute

## Description of the Program

These programs, titled "Traceroute" (traceroute.py) and "Ping" (ping.py), are python projects developed by Josh Embury for CS372 Section 400 at Oregon State University. The code provided in the IcmpHelperLibrary.py file includes implementation of the traceroute and ping programs, similar to the programs found on Linux operating systems. Traceroute is implemented by sending packets toward a destination host with the ICMP protocol and varying the time-to-live (TTL) field in the packet header as packets are sent to hop routers along the router path to the destination host. By sending an ICMP packet having a TTL value of 1 to a hop router, a response packet containing error message is be sent from the current hop router back to the source host, giving information about the hop router. This is how we obtain the IP addresses and RTT for each of the hop routers along the route path.
The Traceroute program accepts a list of hostnames as a command line arguments and uses the traceRoute method of the IcmpHelperLibrary class.
The Ping program accepts a hostname as a command line arguments and uses the sendPing method of the IcmpHelperLibrary class.

### Here's an example of how the program works:

Here is a sample input/output of the ping program:

        >>>sudo python3 ping.py google.com
        Pinging (google.com)
        TTL=255    RTT=19.68 ms    Type=0    Code=0 (echo reply)        Identifier=1094    Sequence Number=0    172.217.164.14
        TTL=255    RTT=12.79 ms    Type=0    Code=0 (echo reply)        Identifier=1094    Sequence Number=1    142.250.65.110
        TTL=255    RTT=13.49 ms    Type=0    Code=0 (echo reply)        Identifier=1094    Sequence Number=2    172.217.0.78
        TTL=255    RTT=16.65 ms    Type=0    Code=0 (echo reply)        Identifier=1094    Sequence Number=3    172.217.15.238
        --- google.com ping statistics ---
        4 packets transmitted, 4 received, 0% packet loss
        rtt min/avg/max = 12.79/15.66/19.68 ms

Here is a sample input/output of the traceroute program:

        >>>sudo python3 traceroute.py google.com myspace.com
        Attempting to build traceroute for the following hosts:
        google.com
        myspace.com
        
        Traceroute to (google.com) 142.250.69.206
          TTL=1    RTT=48.12 ms    Type=11    Code=0 (TTL expired)    10.192.5.2
          TTL=2    RTT=44.39 ms    Type=11    Code=0 (TTL expired)    10.194.222.17
          TTL=3    RTT=45.57 ms    Type=11    Code=0 (TTL expired)    10.192.89.97
          TTL=4    RTT=44.19 ms    Type=11    Code=0 (TTL expired)    128.193.107.20
          TTL=5    RTT=45.29 ms    Type=11    Code=0 (TTL expired)    128.193.6.212
          TTL=6    RTT=48.45 ms    Type=11    Code=0 (TTL expired)    128.193.88.57
          TTL=7    RTT=47.62 ms    Type=11    Code=0 (TTL expired)    207.98.127.244
          TTL=8    RTT=46.67 ms    Type=11    Code=0 (TTL expired)    207.98.126.62
          TTL=9    RTT=46.05 ms    Type=11    Code=0 (TTL expired)    207.98.127.246
          *        *        *        *        *    Request timed out.
          *        *        *        *        *    Request timed out (By Exception).
          TTL=11    RTT=51.80 ms    Type=11    Code=0 (TTL expired)    192.178.105.129
          TTL=12    RTT=53.92 ms    Type=11    Code=0 (TTL expired)    142.251.48.213
          TTL=13    RTT=48.23 ms    Type=0    Code=0 (echo reply)        Identifier=1411    Sequence Number=0    142.250.69.206
        Traceroute to (myspace.com) 34.111.176.156
          TTL=1    RTT=44.18 ms    Type=11    Code=0 (TTL expired)    10.192.5.2
          TTL=2    RTT=43.87 ms    Type=11    Code=0 (TTL expired)    10.194.222.17
          TTL=3    RTT=48.63 ms    Type=11    Code=0 (TTL expired)    10.192.89.97
          TTL=4    RTT=47.78 ms    Type=11    Code=0 (TTL expired)    128.193.107.20
          TTL=5    RTT=45.92 ms    Type=11    Code=0 (TTL expired)    128.193.6.212
          TTL=6    RTT=44.87 ms    Type=11    Code=0 (TTL expired)    128.193.88.57
          TTL=7    RTT=44.12 ms    Type=11    Code=0 (TTL expired)    207.98.127.244
          TTL=8    RTT=49.20 ms    Type=11    Code=0 (TTL expired)    207.98.126.62
          TTL=9    RTT=47.03 ms    Type=11    Code=0 (TTL expired)    207.98.127.246
          *        *        *        *        *    Request timed out.
          *        *        *        *        *    Request timed out (By Exception).
          TTL=11    RTT=55.30 ms    Type=11    Code=0 (TTL expired)    192.178.105.35
          TTL=12    RTT=54.70 ms    Type=11    Code=0 (TTL expired)    142.251.241.137
          TTL=13    RTT=53.10 ms    Type=0    Code=0 (echo reply)        Identifier=1411    Sequence Number=0    34.111.176.156
