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

        Traceroute to (google.com) 172.217.15.238
          TTL=1    RTT=2.01 ms    Type=11    Code=0 (TTL expired)    10.0.0.1
          TTL=2    RTT=15.37 ms    Type=11    Code=0 (TTL expired)    10.27.164.115
          TTL=3    RTT=12.31 ms    Type=11    Code=0 (TTL expired)    96.216.77.9
          TTL=4    RTT=13.98 ms    Type=11    Code=0 (TTL expired)    24.124.175.33
          TTL=5    RTT=13.23 ms    Type=11    Code=0 (TTL expired)    24.124.175.41
          TTL=6    RTT=11.19 ms    Type=11    Code=0 (TTL expired)    24.124.175.214
          TTL=7    RTT=16.35 ms    Type=11    Code=0 (TTL expired)    69.241.15.222
          TTL=8    RTT=16.96 ms    Type=11    Code=0 (TTL expired)    142.251.64.231
          TTL=9    RTT=12.75 ms    Type=11    Code=0 (TTL expired)    216.239.54.189
          TTL=10    RTT=13.54 ms    Type=0    Code=0 (echo reply)        Identifier=1097    Sequence Number=0    172.217.7.46
        Traceroute to (myspace.com) 34.111.176.156
          TTL=1    RTT=1.97 ms    Type=11    Code=0 (TTL expired)    10.0.0.1
          TTL=2    RTT=14.68 ms    Type=11    Code=0 (TTL expired)    10.27.164.115
          TTL=3    RTT=10.47 ms    Type=11    Code=0 (TTL expired)    96.216.77.13
          TTL=4    RTT=10.24 ms    Type=11    Code=0 (TTL expired)    24.124.175.85
          TTL=5    RTT=18.22 ms    Type=11    Code=0 (TTL expired)    24.124.175.25
          TTL=6    RTT=12.15 ms    Type=11    Code=0 (TTL expired)    24.124.175.226
          TTL=7    RTT=12.68 ms    Type=11    Code=0 (TTL expired)    68.87.78.178
          TTL=8    RTT=14.11 ms    Type=11    Code=0 (TTL expired)    172.253.50.81
          TTL=9    RTT=13.96 ms    Type=11    Code=0 (TTL expired)    216.239.48.235
          TTL=10    RTT=13.78 ms    Type=0    Code=0 (echo reply)        Identifier=1097    Sequence Number=0    34.111.176.156
