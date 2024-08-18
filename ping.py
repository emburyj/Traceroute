# Name: Josh Embury
# Description: This program accepts a hostname as a command line argument and
# uses the sendPing method of the IcmpHelperLibrary class.

from IcmpHelperLibrary import *
import sys

if __name__ == '__main__':
    n = len(sys.argv) # total number of command line args
    try:
        if n == 2:
            icmp_traceroute = IcmpHelperLibrary()
            icmp_traceroute.sendPing(sys.argv[1])
        else:
            print("Please enter a valid host as command line argument!")

    except Exception as e:
       print(e)
       print("Exception occured. Please enter valid host as command line argument!")