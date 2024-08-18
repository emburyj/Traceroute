# Name: Josh Embury
# Description: This program accepts a list of hostnames as a command line
# arguments and uses the traceRoute method of the IcmpHelperLibrary class.

from IcmpHelperLibrary import *
import sys

if __name__ == '__main__':
    n = len(sys.argv) # total number of command line args
    try:
        if n > 1:
            print("Attempting to build traceroute for the following hosts:")
            for i in range(1, n):
                print(f"{sys.argv[i]}")
            print()
            for i in range(1, n):
                icmp_traceroute = IcmpHelperLibrary()
                icmp_traceroute.traceRoute(sys.argv[i])

        else:
            print("Please enter a valid host as command line argument!")
    except Exception as e:
       print(e)
       print("Exception occured. Please enter valid host as command line argument!")