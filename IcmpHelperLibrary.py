# Name: Josh Embury
# OSU Email: emburyj@oregonstate.edu
# Course: CS372 - Intro to Networks
# Assignment: Programming Project 3 Traceroute
# Due Date: 8/11/2024
# Description: Raw socket implementation of ping and traceroute.

# #################################################################################################################### #
# Citation for IcmpHelperLibrary.py:
# Date: 08/11/2024
# Adapted from the provided skeleton code:
# https://canvas.oregonstate.edu/courses/1967031/assignments/9713458?module_item_id=24526095
# #################################################################################################################### #

# #################################################################################################################### #
# Imports                                                                                                              #
#                                                                                                                      #
#                                                                                                                      #
#                                                                                                                      #
#                                                                                                                      #
# #################################################################################################################### #
import os
from socket import *
import struct
import time
import select


# #################################################################################################################### #
# Class IcmpHelperLibrary                                                                                              #
#                                                                                                                      #
#                                                                                                                      #
#                                                                                                                      #
#                                                                                                                      #
#                                                                                                                      #
#                                                                                                                      #
#                                                                                                                      #
#                                                                                                                      #
#                                                                                                                      #
#                                                                                                                      #
#                                                                                                                      #
#                                                                                                                      #
#                                                                                                                      #
#                                                                                                                      #
# #################################################################################################################### #
class IcmpHelperLibrary:
    # ################################################################################################################ #
    # Class IcmpPacket                                                                                                 #
    #                                                                                                                  #
    # References:                                                                                                      #
    # https://www.iana.org/assignments/icmp-parameters/icmp-parameters.xhtml                                           #
    #                                                                                                                  #
    #                                                                                                                  #
    #                                                                                                                  #
    #                                                                                                                  #
    #                                                                                                                  #
    #                                                                                                                  #
    #                                                                                                                  #
    #                                                                                                                  #
    #                                                                                                                  #
    #                                                                                                                  #
    # ################################################################################################################ #
    class IcmpPacket:
        # ############################################################################################################ #
        # IcmpPacket Class Scope Variables                                                                             #
        #                                                                                                              #
        #                                                                                                              #
        #                                                                                                              #
        #                                                                                                              #
        # ############################################################################################################ #
        __icmpTarget = ""               # Remote Host
        __destinationIpAddress = ""     # Remote Host IP Address
        __header = b''                  # Header after byte packing
        __data = b''                    # Data after encoding
        __dataRaw = ""                  # Raw string data before encoding
        __icmpType = 0                  # Valid values are 0-255 (unsigned int, 8 bits)
        __icmpCode = 0                  # Valid values are 0-255 (unsigned int, 8 bits)
        __packetChecksum = 0            # Valid values are 0-65535 (unsigned short, 16 bits)
        __packetIdentifier = 0          # Valid values are 0-65535 (unsigned short, 16 bits)
        __packetSequenceNumber = 0      # Valid values are 0-65535 (unsigned short, 16 bits)
        __ipTimeout = 30
        __ttl = 255                     # Time to live
        __errorDescription = {
                                (0, 0): "echo reply",
                                (3, 0): "destination network unreachable",
                                (3, 1): "destination host unreachable",
                                (3, 2): "destination protocol unreachable",
                                (3, 3): "destination port unreachable",
                                (3, 6): "destination network unknown",
                                (3, 7): "destination host unknown",
                                (11, 0): "TTL expired",
        }
        responseAddr = None
        __DEBUG_IcmpPacket = False      # Allows for debug output

        # ############################################################################################################ #
        # IcmpPacket Class Getters                                                                                     #
        #                                                                                                              #
        #                                                                                                              #
        #                                                                                                              #
        #                                                                                                              #
        # ############################################################################################################ #
        def getIcmpTarget(self):
            return self.__icmpTarget

        def getDataRaw(self):
            return self.__dataRaw

        def getIcmpType(self):
            return self.__icmpType

        def getIcmpCode(self):
            return self.__icmpCode

        def getPacketChecksum(self):
            return self.__packetChecksum

        def getPacketIdentifier(self):
            return self.__packetIdentifier

        def getPacketSequenceNumber(self):
            return self.__packetSequenceNumber

        def getTtl(self):
            return self.__ttl

        def getRtt(self):
            return self.__rtt

        def getResponseReceived(self):
            return self.__responseReceived

        def getDestinationIPAddress(self):
            return self.__destinationIpAddress

        def getErrorDescription(self, codeTuple):
            return self.__errorDescription[codeTuple]

        def getResponseAddr(self):
            return self.responseAddr

        # ############################################################################################################ #
        # IcmpPacket Class Setters                                                                                     #
        #                                                                                                              #
        #                                                                                                              #
        #                                                                                                              #
        #                                                                                                              #
        # ############################################################################################################ #
        def setIcmpTarget(self, icmpTarget):
            self.__icmpTarget = icmpTarget
            # Only attempt to get destination address if it is not whitespace
            if len(self.__icmpTarget.strip()) > 0:
                self.__destinationIpAddress = gethostbyname(self.__icmpTarget.strip())
            self.__rtt = None
            self.__responseReceived = False

        def setIcmpType(self, icmpType):
            self.__icmpType = icmpType

        def setIcmpCode(self, icmpCode):
            self.__icmpCode = icmpCode

        def setPacketChecksum(self, packetChecksum):
            self.__packetChecksum = packetChecksum

        def setPacketIdentifier(self, packetIdentifier):
            self.__packetIdentifier = packetIdentifier

        def setPacketSequenceNumber(self, sequenceNumber):
            self.__packetSequenceNumber = sequenceNumber

        def setTtl(self, ttl):
            self.__ttl = ttl

        def setRtt(self, rtt):
            self.__rtt = rtt

        def setResponseReceived(self, booleanValue):
            self.__responseReceived = booleanValue

        def setResponseAddr(self, address):
            self.responseAddr = address

        # ############################################################################################################ #
        # IcmpPacket Class Private Functions                                                                           #
        #                                                                                                              #
        #                                                                                                              #
        #                                                                                                              #
        #                                                                                                              #
        # ############################################################################################################ #
        def __recalculateChecksum(self):
            print("calculateChecksum Started...") if self.__DEBUG_IcmpPacket else 0
            packetAsByteData = b''.join([self.__header, self.__data])
            checksum = 0

            # This checksum function will work with pairs of values with two separate 16 bit segments. Any remaining
            # 16 bit segment will be handled on the upper end of the 32 bit segment.
            countTo = (len(packetAsByteData) // 2) * 2

            # Calculate checksum for all paired segments
            print(f'{"Count":10} {"Value":10} {"Sum":10}') if self.__DEBUG_IcmpPacket else 0
            count = 0
            while count < countTo:
                thisVal = packetAsByteData[count + 1] * 256 + packetAsByteData[count]
                checksum = checksum + thisVal
                checksum = checksum & 0xffffffff        # Capture 16 bit checksum as 32 bit value
                print(f'{count:10} {hex(thisVal):10} {hex(checksum):10}') if self.__DEBUG_IcmpPacket else 0
                count = count + 2

            # Calculate checksum for remaining segment (if there are any)
            if countTo < len(packetAsByteData):
                thisVal = packetAsByteData[len(packetAsByteData) - 1]
                checksum = checksum + thisVal
                checksum = checksum & 0xffffffff        # Capture as 32 bit value
                print(count, "\t", hex(thisVal), "\t", hex(checksum)) if self.__DEBUG_IcmpPacket else 0

            # Add 1's Complement Rotation to original checksum
            checksum = (checksum >> 16) + (checksum & 0xffff)   # Rotate and add to base 16 bits
            checksum = (checksum >> 16) + checksum              # Rotate and add

            answer = ~checksum                  # Invert bits
            answer = answer & 0xffff            # Trim to 16 bit value
            answer = answer >> 8 | (answer << 8 & 0xff00)
            print("Checksum: ", hex(answer)) if self.__DEBUG_IcmpPacket else 0

            self.setPacketChecksum(answer)

        def __packHeader(self):
            # The following header is based on http://www.networksorcery.com/enp/protocol/icmp/msg8.htm
            # Type = 8 bits
            # Code = 8 bits
            # ICMP Header Checksum = 16 bits
            # Identifier = 16 bits
            # Sequence Number = 16 bits
            self.__header = struct.pack("!BBHHH",
                                   self.getIcmpType(),              #  8 bits / 1 byte  / Format code B
                                   self.getIcmpCode(),              #  8 bits / 1 byte  / Format code B
                                   self.getPacketChecksum(),        # 16 bits / 2 bytes / Format code H
                                   self.getPacketIdentifier(),      # 16 bits / 2 bytes / Format code H
                                   self.getPacketSequenceNumber()   # 16 bits / 2 bytes / Format code H
                                   )

        def __encodeData(self):
            data_time = struct.pack("d", time.time())               # Used to track overall round trip time
                                                                    # time.time() creates a 64 bit value of 8 bytes
            dataRawEncoded = self.getDataRaw().encode("utf-8")

            self.__data = data_time + dataRawEncoded

        def __packAndRecalculateChecksum(self):
            # Checksum is calculated with the following sequence to confirm data in up to date
            self.__packHeader()                 # packHeader() and encodeData() transfer data to their respective bit
                                                # locations, otherwise, the bit sequences are empty or incorrect.
            self.__encodeData()
            self.__recalculateChecksum()        # Result will set new checksum value
            self.__packHeader()                 # Header is rebuilt to include new checksum value

        def __validateIcmpReplyPacketWithOriginalPingData(self, icmpReplyPacket):
            # This method determines if the reply packet contains values consistent with
            # values sent by packet.
            print("\n******************************\n") if self.__DEBUG_IcmpPacket else 0
            print("Validate ICMP Reply Packet with Original Ping Data [DEBUG MODE]:") if self.__DEBUG_IcmpPacket else 0
            # compare sequence numbers
            sentSequenceNum = self.getPacketSequenceNumber()
            receivedSequenceNum = icmpReplyPacket.getIcmpSequenceNumber()
            seqCheck = sentSequenceNum == receivedSequenceNum
            icmpReplyPacket.setIcmpSequence_isValid(seqCheck)
            icmpReplyPacket.setExpectedPacketData("Sequence", sentSequenceNum)
            print(f"Sequence number\nExpected:{sentSequenceNum}\nActual:{receivedSequenceNum}\n") if self.__DEBUG_IcmpPacket else 0

            # compare identifiers
            sentIdentifier = self.getPacketIdentifier()
            receivedIdentifier = icmpReplyPacket.getIcmpIdentifier()
            IdCheck = sentIdentifier == receivedIdentifier
            icmpReplyPacket.setIcmpIdentifier_isValid(IdCheck)
            icmpReplyPacket.setExpectedPacketData("Identifier", sentIdentifier)
            print(f"Identifier\nExpected:{sentIdentifier}\nActual:{receivedIdentifier}\n") if self.__DEBUG_IcmpPacket else 0

            # compare raw data
            sentData = self.getDataRaw()
            receivedData = icmpReplyPacket.getIcmpData()
            dataCheck = sentData == receivedData
            icmpReplyPacket.setIcmpData_isValid(dataCheck)
            icmpReplyPacket.setExpectedPacketData("Data", sentData)
            print(f"Raw Data\nExpected:{sentData}\nActual:{receivedData}\n") if self.__DEBUG_IcmpPacket else 0
            print("******************************") if self.__DEBUG_IcmpPacket else 0
            if seqCheck and IdCheck and dataCheck:
                icmpReplyPacket.setIsValidResponse(True)
            else:
                icmpReplyPacket.setIsValidResponse(False)

        # ############################################################################################################ #
        # IcmpPacket Class Public Functions                                                                            #
        #                                                                                                              #
        #                                                                                                              #
        #                                                                                                              #
        #                                                                                                              #
        # ############################################################################################################ #
        def buildPacket_echoRequest(self, packetIdentifier, packetSequenceNumber):
            self.setIcmpType(8)
            self.setIcmpCode(0)
            self.setPacketIdentifier(packetIdentifier)
            self.setPacketSequenceNumber(packetSequenceNumber)
            self.__dataRaw = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"
            self.__packAndRecalculateChecksum()

        def sendEchoRequest(self):
            if len(self.__icmpTarget.strip()) <= 0 | len(self.__destinationIpAddress.strip()) <= 0:
                self.setIcmpTarget("127.0.0.1")

            # print("Pinging (" + self.__icmpTarget + ") " + self.__destinationIpAddress)

            mySocket = socket(AF_INET, SOCK_RAW, IPPROTO_ICMP)
            mySocket.settimeout(self.__ipTimeout)
            mySocket.bind(("", 0))
            mySocket.setsockopt(IPPROTO_IP, IP_TTL, struct.pack('I', self.getTtl()))  # Unsigned int - 4 bytes
            try:
                mySocket.sendto(b''.join([self.__header, self.__data]), (self.__destinationIpAddress, 0))
                timeLeft = 30
                pingStartTime = time.time()
                startedSelect = time.time()
                whatReady = select.select([mySocket], [], [], timeLeft)
                endSelect = time.time()
                howLongInSelect = (endSelect - startedSelect)
                if whatReady[0] == []:  # Timeout
                    print("  *        *        *        *        *    Request timed out.")
                recvPacket, addr = mySocket.recvfrom(1024)  # recvPacket - bytes object representing data received
                # addr  - address of socket sending data
                timeReceived = time.time()
                timeLeft = timeLeft - howLongInSelect

                if timeLeft <= 0:
                    print("  *        *        *        *        *    Request timed out (By no remaining time left).")

                else:
                    # Fetch the ICMP type and code from the received packet
                    icmpType, icmpCode = recvPacket[20:22]

                    if icmpType == 3 or icmpType == 11:                         # Destination Unreachable or TTL exceeded
                        print(f"  TTL={self.getTtl()}    RTT={(timeReceived - pingStartTime) * 1000:.2f} ms    Type={icmpType}    Code={icmpCode} ({self.getErrorDescription((icmpType, icmpCode))})    {addr[0]}")

                    elif icmpType == 0:                         # Echo Reply
                        if len(addr) > 1:
                            self.setResponseAddr(addr[0])
                        icmpReplyPacket = IcmpHelperLibrary.IcmpPacket_EchoReply(recvPacket)
                        icmpReplyPacket.setPingTimeSent(pingStartTime)
                        self.__validateIcmpReplyPacketWithOriginalPingData(icmpReplyPacket)
                        icmpReplyPacket.printResultToConsole(self.getTtl(), timeReceived, addr)
                        if icmpReplyPacket.isValidResponse():
                            self.setResponseReceived(True)
                            self.setRtt(1000 * (timeReceived - pingStartTime))
                        # print(f"This is a valid response: {icmpReplyPacket.isValidResponse()}!") # for test
                        return      # Echo reply is the end and therefore should return

                    else:
                        print("error")
            except timeout:
                print("  *        *        *        *        *    Request timed out (By Exception).")
            finally:
                mySocket.close()

        def printIcmpPacketHeader_hex(self):
            print("Header Size: ", len(self.__header))
            for i in range(len(self.__header)):
                print("i=", i, " --> ", self.__header[i:i+1].hex())

        def printIcmpPacketData_hex(self):
            print("Data Size: ", len(self.__data))
            for i in range(len(self.__data)):
                print("i=", i, " --> ", self.__data[i:i + 1].hex())

        def printIcmpPacket_hex(self):
            print("Printing packet in hex...")
            self.printIcmpPacketHeader_hex()
            self.printIcmpPacketData_hex()

    # ################################################################################################################ #
    # Class IcmpPacket_EchoReply                                                                                       #
    #                                                                                                                  #
    # References:                                                                                                      #
    # http://www.networksorcery.com/enp/protocol/icmp/msg0.htm                                                         #
    #                                                                                                                  #
    #                                                                                                                  #
    #                                                                                                                  #
    #                                                                                                                  #
    #                                                                                                                  #
    #                                                                                                                  #
    #                                                                                                                  #
    #                                                                                                                  #
    #                                                                                                                  #
    #                                                                                                                  #
    # ################################################################################################################ #
    class IcmpPacket_EchoReply:
        # ############################################################################################################ #
        # IcmpPacket_EchoReply Class Scope Variables                                                                   #
        #                                                                                                              #
        #                                                                                                              #
        #                                                                                                              #
        #                                                                                                              #
        # ############################################################################################################ #
        __recvPacket = b''
        __isValidResponse = False

        # ############################################################################################################ #
        # IcmpPacket_EchoReply Constructors                                                                            #
        #                                                                                                              #
        #                                                                                                              #
        #                                                                                                              #
        #                                                                                                              #
        # ############################################################################################################ #
        def __init__(self, recvPacket):
            self.__recvPacket = recvPacket
            self.IcmpIdentifier_isValid = None
            self.IcmpSequence_isValid = None
            self.IcmpData_isValid = None
            self.pingTimeSent = None
            self.expectedPacketData = {"Sequence": None, "Identifier": None, "Data": None}


        # ############################################################################################################ #
        # IcmpPacket_EchoReply Getters                                                                                 #
        #                                                                                                              #
        #                                                                                                              #
        #                                                                                                              #
        #                                                                                                              #
        # ############################################################################################################ #
        def getIcmpType(self):
            # Method 1
            # bytes = struct.calcsize("B")        # Format code B is 1 byte
            # return struct.unpack("!B", self.__recvPacket[20:20 + bytes])[0]

            # Method 2
            return self.__unpackByFormatAndPosition("B", 20)

        def getIcmpCode(self):
            # Method 1
            # bytes = struct.calcsize("B")        # Format code B is 1 byte
            # return struct.unpack("!B", self.__recvPacket[21:21 + bytes])[0]

            # Method 2
            return self.__unpackByFormatAndPosition("B", 21)

        def getIcmpHeaderChecksum(self):
            # Method 1
            # bytes = struct.calcsize("H")        # Format code H is 2 bytes
            # return struct.unpack("!H", self.__recvPacket[22:22 + bytes])[0]

            # Method 2
            return self.__unpackByFormatAndPosition("H", 22)

        def getIcmpIdentifier(self):
            # Method 1
            # bytes = struct.calcsize("H")        # Format code H is 2 bytes
            # return struct.unpack("!H", self.__recvPacket[24:24 + bytes])[0]

            # Method 2
            return self.__unpackByFormatAndPosition("H", 24)

        def getIcmpSequenceNumber(self):
            # Method 1
            # bytes = struct.calcsize("H")        # Format code H is 2 bytes
            # return struct.unpack("!H", self.__recvPacket[26:26 + bytes])[0]

            # Method 2
            return self.__unpackByFormatAndPosition("H", 26)

        def getDateTimeSent(self):
            # This accounts for bytes 28 through 35 = 64 bits
            return self.__unpackByFormatAndPosition("d", 28)   # Used to track overall round trip time
                                                               # time.time() creates a 64 bit value of 8 bytes

        def getIcmpData(self):
            # This accounts for bytes 36 to the end of the packet.
            return self.__recvPacket[36:].decode('utf-8')

        def isValidResponse(self):
            return self.__isValidResponse

        def getIcmpIdentifier_isValid(self):
            return self.IcmpIdentifier_isValid

        def getIcmpSequence_isValid(self):
            return self.IcmpSequence_isValid

        def getIcmpData_isValid(self):
            return self.IcmpData_isValid

        def getExpectedPacketData(self, key):
            return self.expectedPacketData[key]

        def getPingTimeSent(self):
            return self.pingTimeSent

        # ############################################################################################################ #
        # IcmpPacket_EchoReply Setters                                                                                 #
        #                                                                                                              #
        #                                                                                                              #
        #                                                                                                              #
        #                                                                                                              #
        # ############################################################################################################ #
        def setIsValidResponse(self, booleanValue):
            self.__isValidResponse = booleanValue

        def setIcmpIdentifier_isValid(self, booleanValue):
            self.IcmpIdentifier_isValid = booleanValue

        def setIcmpSequence_isValid(self, booleanValue):
            self.IcmpSequence_isValid = booleanValue

        def setIcmpData_isValid(self, booleanValue):
            self.IcmpData_isValid = booleanValue

        def setExpectedPacketData(self, key, value):
            self.expectedPacketData[key] = value

        def setPingTimeSent(self, time):
            self.pingTimeSent = time

        # ############################################################################################################ #
        # IcmpPacket_EchoReply Private Functions                                                                       #
        #                                                                                                              #
        #                                                                                                              #
        #                                                                                                              #
        #                                                                                                              #
        # ############################################################################################################ #
        def __unpackByFormatAndPosition(self, formatCode, basePosition):
            numberOfbytes = struct.calcsize(formatCode)
            return struct.unpack("!" + formatCode, self.__recvPacket[basePosition:basePosition + numberOfbytes])[0]

        # ############################################################################################################ #
        # IcmpPacket_EchoReply Public Functions                                                                        #
        #                                                                                                              #
        #                                                                                                              #
        #                                                                                                              #
        #                                                                                                              #
        # ############################################################################################################ #
        def printResultToConsole(self, ttl, timeReceived, addr):
            bytes = struct.calcsize("d")
            # timeSent = struct.unpack("d", self.__recvPacket[28:28 + bytes])[0] # this value is not correct ping start time
            timeSent = self.getPingTimeSent()
            print(
                    f"  TTL={ttl}    RTT={(timeReceived - timeSent) * 1000:.2f} ms"
                    f"    Type={self.getIcmpType()}    Code={self.getIcmpCode()} (echo reply)"
                    f"        Identifier={self.getIcmpIdentifier()}    "
                    f"Sequence Number={self.getIcmpSequenceNumber()}    {addr[0]}"
                 )
            if not self.getIcmpIdentifier_isValid():
                print(f"ERROR: Invalid Identifier!\nExpected:{self.getExpectedPacketData('Identifier')}\nActual:{self.getIcmpIdentifier()}\n")

            if not self.getIcmpSequence_isValid():
                print(f"ERROR: Invalid Sequence!\nExpected:{self.getExpectedPacketData('Sequence')}\nActual:{self.getIcmpSequenceNumber()}\n")

            if not self.getIcmpData_isValid():
                print(f"ERROR: Invalid Data!\nExpected:{self.getExpectedPacketData('Data')}\nActual:{self.getIcmpData()}\n")
    # ################################################################################################################ #
    # Class IcmpHelperLibrary                                                                                          #
    #                                                                                                                  #
    #                                                                                                                  #
    #                                                                                                                  #
    #                                                                                                                  #
    # ################################################################################################################ #

    # ################################################################################################################ #
    # IcmpHelperLibrary Class Scope Variables                                                                          #
    #                                                                                                                  #
    #                                                                                                                  #
    #                                                                                                                  #
    #                                                                                                                  #
    # ################################################################################################################ #
    __DEBUG_IcmpHelperLibrary = False                  # Allows for debug output

    # ################################################################################################################ #
    # IcmpHelperLibrary Private Functions                                                                              #
    #                                                                                                                  #
    #                                                                                                                  #
    #                                                                                                                  #
    #                                                                                                                  #
    # ################################################################################################################ #
    def __sendIcmpEchoRequest(self, host, ttl, num_of_pings):
        print("sendIcmpEchoRequest Started...") if self.__DEBUG_IcmpHelperLibrary else 0
        rtt = []
        if ttl > 50:
            print(f"Pinging ({host})")
        for i in range(num_of_pings):
            # Build packet
            icmpPacket = IcmpHelperLibrary.IcmpPacket()
            icmpPacket.setTtl(ttl)
            randomIdentifier = (os.getpid() & 0xffff)      # Get as 16 bit number - Limit based on ICMP header standards
                                                           # Some PIDs are larger than 16 bit

            packetIdentifier = randomIdentifier
            packetSequenceNumber = i

            icmpPacket.buildPacket_echoRequest(packetIdentifier, packetSequenceNumber)  # Build ICMP for IP payload
            icmpPacket.setIcmpTarget(host)
            if ttl == 1:
                print(f"Traceroute to ({host}) {icmpPacket.getDestinationIPAddress()}")
            icmpPacket.sendEchoRequest()                                                # Build IP
            if icmpPacket.getRtt():
                rtt.append(icmpPacket.getRtt())
            icmpPacket.printIcmpPacketHeader_hex() if self.__DEBUG_IcmpHelperLibrary else 0
            icmpPacket.printIcmpPacket_hex() if self.__DEBUG_IcmpHelperLibrary else 0
            if ttl < 50 and icmpPacket.getResponseAddr() == icmpPacket.getDestinationIPAddress():
                # print("Destination reached!")
                return 0
            # we should be confirming values are correct, such as identifier and sequence number and data
        if ttl > 50:
            if len(rtt) == 0:
                minRtt = "inf"
                maxRtt = "inf"
                avgRtt = "inf"
            else:
                minRtt = min(rtt)
                maxRtt = max(rtt)
                avgRtt = sum(rtt) / len(rtt)

            print(f"--- {icmpPacket.getIcmpTarget()} ping statistics ---")
            print(f"{num_of_pings} packets transmitted, {len(rtt)} received, {100*(1-(len(rtt) // num_of_pings))}% packet loss")
            if len(rtt) == 0:
                print(f"rtt min/avg/max = {minRtt}/{avgRtt}/{maxRtt}")
            else:
                print(f"rtt min/avg/max = {minRtt:.2f}/{avgRtt:.2f}/{maxRtt:.2f} ms")

    def __sendIcmpTraceRoute(self, host):
        print("sendIcmpTraceRoute Started...") if self.__DEBUG_IcmpHelperLibrary else 0
        # Build code for trace route here

        ttlMax = 50
        for i in range(1, ttlMax + 1):
            destination_flag = self.__sendIcmpEchoRequest(host, i, 1)
            if destination_flag == 0:
                break

    # ################################################################################################################ #
    # IcmpHelperLibrary Public Functions                                                                               #
    #                                                                                                                  #
    #                                                                                                                  #
    #                                                                                                                  #
    #                                                                                                                  #
    # ################################################################################################################ #
    def sendPing(self, targetHost):
        print("ping Started...") if self.__DEBUG_IcmpHelperLibrary else 0
        self.__sendIcmpEchoRequest(targetHost, 255, 4)

    def traceRoute(self, targetHost):
        print("traceRoute Started...") if self.__DEBUG_IcmpHelperLibrary else 0
        self.__sendIcmpTraceRoute(targetHost)


# #################################################################################################################### #
# main()                                                                                                               #
#                                                                                                                      #
#                                                                                                                      #
#                                                                                                                      #
#                                                                                                                      #
# #################################################################################################################### #
def main():
    icmpHelperPing = IcmpHelperLibrary()


    # Choose one of the following by uncommenting out the line
    # sacramento
    # icmpHelperPing.sendPing("209.233.126.254")
    # icmpHelperPing.traceRoute("209.233.126.254")

    # icmpHelperPing.sendPing("www.google.com")
    # icmpHelperPing.traceRoute("www.google.com")

    # Brazil
    # icmpHelperPing.sendPing("200.10.227.250")
    # icmpHelperPing.traceRoute("200.10.227.250")

    # boston
    icmpHelperPing.sendPing("gaia.cs.umass.edu")
    # icmpHelperPing.traceRoute("gaia.cs.umass.edu")

    # south africa
    # icmpHelperPing.sendPing("164.151.129.20")
    # icmpHelperPing.traceRoute("164.151.129.20")

    # new zealand
    # icmpHelperPing.sendPing("122.56.99.243")
    # icmpHelperPing.traceRoute("122.56.99.243")


if __name__ == "__main__":
    main()
