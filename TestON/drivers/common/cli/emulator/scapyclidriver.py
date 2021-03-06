#!/usr/bin/env python
"""
2015-2016
Copyright 2016 Open Networking Foundation (ONF)

Please refer questions to either the onos test mailing list at <onos-test@onosproject.org>,
the System Testing Plans and Results wiki page at <https://wiki.onosproject.org/x/voMg>,
or the System Testing Guide page at <https://wiki.onosproject.org/x/WYQg>

TestON is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 2 of the License, or
( at your option ) any later version.

TestON is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with TestON.  If not, see <http://www.gnu.org/licenses/>.

ScapyCliDriver is the basic driver which will handle the Scapy functions

TODO: Add Explanation on how to install scapy
"""
import pexpect
import re
import sys
import types
import os
from drivers.common.cli.emulatordriver import Emulator


class ScapyCliDriver( Emulator ):

    """
       ScapyCliDriver is the basic driver which will handle
       the Scapy functions"""
    def __init__( self ):
        super( ScapyCliDriver, self ).__init__()
        self.handle = self
        self.name = None
        self.home = None
        self.wrapped = sys.modules[ __name__ ]
        self.flag = 0
        # TODO: Refactor driver to use these everywhere
        self.hostPrompt = "\$"
        self.scapyPrompt = ">>>"

    def connect( self, **connectargs ):
        """
           Here the main is the TestON instance after creating
           all the log handles."""
        try:
            for key in connectargs:
                vars( self )[ key ] = connectargs[ key ]
            self.home = self.options[ 'home' ] if 'home' in self.options.keys() else "~/"
            self.name = self.options[ 'name' ]
            self.ifaceName = self.options[ 'ifaceName' ] if 'ifaceName' in self.options.keys() else self.name + "-eth0"
            try:
                if os.getenv( str( self.ip_address ) ) is not None:
                    self.ip_address = os.getenv( str( self.ip_address ) )
                else:
                    main.log.info( self.name +
                                   ": Trying to connect to " +
                                   self.ip_address )

            except KeyError:
                main.log.info( "Invalid host name," +
                               " connecting to local host instead" )
                self.ip_address = 'localhost'
            except Exception as inst:
                main.log.error( "Uncaught exception: " + str( inst ) )

            self.handle = super(
                ScapyCliDriver,
                self ).connect(
                user_name=self.user_name,
                ip_address=self.ip_address,
                port=None,
                pwd=self.pwd )

            if self.handle:
                main.log.info( "Connection successful to the host " +
                               self.user_name +
                               "@" +
                               self.ip_address )
                return self.handle
            else:
                main.log.error( "Connection failed to the host " +
                                self.user_name +
                                "@" +
                                self.ip_address )
                main.log.error( "Failed to connect to the Mininet Host" )
                return main.FALSE
        except pexpect.EOF:
            main.log.error( self.name + ": EOF exception found" )
            main.log.error( self.name + ":     " + self.handle.before )
            main.cleanAndExit()
        except Exception:
            main.log.exception( self.name + ": Uncaught exception!" )
            main.cleanAndExit()

    def disconnect( self ):
        """
        Called at the end of the test to stop the scapy component and
        disconnect the handle.
        """
        response = main.TRUE
        try:
            if self.handle:
                self.handle.sendline( "exit" )
                self.handle.expect( "closed" )
        except pexpect.EOF:
            main.log.error( self.name + ": EOF exception found" )
            main.log.error( self.name + ":     " + self.handle.before )
        except Exception:
            main.log.exception( self.name + ": Connection failed to the host" )
            response = main.FALSE
        return response

    def startScapy( self, mplsPath="" ):
        """
        Start the Scapy cli
        optional:
            mplsPath - The path where the MPLS class is located
            NOTE: This can be a relative path from the user's home dir
        """
        mplsLines = [ 'import imp',
                      'imp.load_source( "mplsClass", "{}mplsClass.py" )'.format( mplsPath ),
                      'from mplsClass import MPLS',
                      'bind_layers(Ether, MPLS, type = 0x8847)',
                      'bind_layers(MPLS, MPLS, bottom_of_label_stack = 0)',
                      'bind_layers(MPLS, IP)' ]

        try:
            self.handle.sendline( "sudo scapy" )
            self.handle.expect( self.scapyPrompt )
            self.handle.sendline( "conf.color_theme = NoTheme()" )
            self.handle.expect( self.scapyPrompt )
            if mplsPath:
                main.log.info( "Adding MPLS class" )
                main.log.info( "MPLS class path: " + mplsPath )
                for line in mplsLines:
                    main.log.info( "sending line: " + line )
                    self.handle.sendline( line )
                    self.handle.expect( self.scapyPrompt )
            return main.TRUE
        except pexpect.TIMEOUT:
            main.log.exception( self.name + ": Command timed out" )
            return main.FALSE
        except pexpect.EOF:
            main.log.exception( self.name + ": connection closed." )
            main.cleanAndExit()
        except Exception:
            main.log.exception( self.name + ": Uncaught exception!" )
            main.cleanAndExit()

    def stopScapy( self ):
        """
        Exit the Scapy cli
        """
        try:
            self.handle.sendline( "exit()" )
            self.handle.expect( self.hostPrompt )
            return main.TRUE
        except pexpect.TIMEOUT:
            main.log.exception( self.name + ": Command timed out" )
            return main.FALSE
        except pexpect.EOF:
            main.log.exception( self.name + ": connection closed." )
            main.cleanAndExit()
        except Exception:
            main.log.exception( self.name + ": Uncaught exception!" )
            main.cleanAndExit()

    def buildEther( self, **kwargs ):
        """
        Build an Ethernet frame

        Will create a frame class with the given options. If a field is
        left blank it will default to the below value unless it is
        overwritten by the next frame.
        Default frame:
        ###[ Ethernet ]###
          dst= ff:ff:ff:ff:ff:ff
          src= 00:00:00:00:00:00
          type= 0x800

        Returns main.TRUE or main.FALSE on error
        """
        try:
            # Set the Ethernet frame
            cmd = 'ether = Ether( '
            options = []
            for key, value in kwargs.iteritems():
                if isinstance( value, str ):
                    value = '"' + value + '"'
                options.append( str( key ) + "=" + str( value ) )
            cmd += ", ".join( options )
            cmd += ' )'
            self.handle.sendline( cmd )
            self.handle.expect( self.scapyPrompt )
            if "Traceback" in self.handle.before:
                # KeyError, SyntaxError, ...
                main.log.error( "Error in sending command: " + self.handle.before )
                return main.FALSE
            self.handle.sendline( "packet = ether" )
            self.handle.expect( self.scapyPrompt )
            if "Traceback" in self.handle.before:
                # KeyError, SyntaxError, ...
                main.log.error( "Error in sending command: " + self.handle.before )
                return main.FALSE
            return main.TRUE
        except pexpect.TIMEOUT:
            main.log.exception( self.name + ": Command timed out" )
            return main.FALSE
        except pexpect.EOF:
            main.log.exception( self.name + ": connection closed." )
            main.cleanAndExit()
        except Exception:
            main.log.exception( self.name + ": Uncaught exception!" )
            main.cleanAndExit()

    def buildIP( self, **kwargs ):
        """
        Build an IP frame

        Will create a frame class with the given options. If a field is
        left blank it will default to the below value unless it is
        overwritten by the next frame.
        Default frame:
        ###[ IP ]###
          version= 4
          ihl= None
          tos= 0x0
          len= None
          id= 1
          flags=
          frag= 0
          ttl= 64
          proto= hopopt
          chksum= None
          src= 127.0.0.1
          dst= 127.0.0.1
          \options\

        Returns main.TRUE or main.FALSE on error
        """
        try:
            # Set the IP frame
            cmd = 'ip = IP( '
            options = []
            for key, value in kwargs.iteritems():
                if isinstance( value, str ):
                    value = '"' + value + '"'
                options.append( str( key ) + "=" + str( value ) )
            cmd += ", ".join( options )
            cmd += ' )'
            self.handle.sendline( cmd )
            self.handle.expect( self.scapyPrompt )
            if "Traceback" in self.handle.before:
                # KeyError, SyntaxError, ...
                main.log.error( "Error in sending command: " + self.handle.before )
                return main.FALSE
            self.handle.sendline( "packet = ether/ip" )
            self.handle.expect( self.scapyPrompt )
            if "Traceback" in self.handle.before:
                # KeyError, SyntaxError, ...
                main.log.error( "Error in sending command: " + self.handle.before )
                return main.FALSE
            return main.TRUE
        except pexpect.TIMEOUT:
            main.log.exception( self.name + ": Command timed out" )
            return main.FALSE
        except pexpect.EOF:
            main.log.exception( self.name + ": connection closed." )
            main.cleanAndExit()
        except Exception:
            main.log.exception( self.name + ": Uncaught exception!" )
            main.cleanAndExit()

    def buildIPv6( self, **kwargs ):
        """
        Build an IPv6 frame

        Will create a frame class with the given options. If a field is
        left blank it will default to the below value unless it is
        overwritten by the next frame.
        Default frame:
        ###[ IPv6 ]###
          version= 6
          tc= 0
          fl= 0
          plen= None
          nh= No Next Header
          hlim= 64
          src= ::1
          dst= ::1

        Returns main.TRUE or main.FALSE on error
        """
        try:
            # Set the IPv6 frame
            cmd = 'ipv6 = IPv6( '
            options = []
            for key, value in kwargs.iteritems():
                if isinstance( value, str ):
                    value = '"' + value + '"'
                options.append( str( key ) + "=" + str( value ) )
            cmd += ", ".join( options )
            cmd += ' )'
            self.handle.sendline( cmd )
            self.handle.expect( self.scapyPrompt )
            if "Traceback" in self.handle.before:
                # KeyError, SyntaxError, ...
                main.log.error( "Error in sending command: " + self.handle.before )
                return main.FALSE
            self.handle.sendline( "packet = ether/ipv6" )
            self.handle.expect( self.scapyPrompt )
            if "Traceback" in self.handle.before:
                # KeyError, SyntaxError, ...
                main.log.error( "Error in sending command: " + self.handle.before )
                return main.FALSE
            return main.TRUE
        except pexpect.TIMEOUT:
            main.log.exception( self.name + ": Command timed out" )
            return main.FALSE
        except pexpect.EOF:
            main.log.exception( self.name + ": connection closed." )
            main.cleanAndExit()
        except Exception:
            main.log.exception( self.name + ": Uncaught exception!" )
            main.cleanAndExit()

    def buildTCP( self, ipVersion=4, **kwargs ):
        """
        Build an TCP frame

        Will create a frame class with the given options. If a field is
        left blank it will default to the below value unless it is
        overwritten by the next frame.

        NOTE: Some arguments require quotes around them. It's up to you to
        know which ones and to add them yourself. Arguments with an asterisk
        do not need quotes.

        Options:
        ipVersion - Either 4 (default) or 6, indicates what Internet Protocol
                    frame to use to encapsulate into
        Default frame:
        ###[ TCP ]###
          sport= ftp_data *
          dport= http *
          seq= 0
          ack= 0
          dataofs= None
          reserved= 0
          flags= S
          window= 8192
          chksum= None
          urgptr= 0
          options= {}

        Returns main.TRUE or main.FALSE on error
        """
        try:
            # Set the TCP frame
            cmd = 'tcp = TCP( '
            options = []
            for key, value in kwargs.iteritems():
                options.append( str( key ) + "=" + str( value ) )
            cmd += ", ".join( options )
            cmd += ' )'
            self.handle.sendline( cmd )
            self.handle.expect( self.scapyPrompt )
            if "Traceback" in self.handle.before:
                # KeyError, SyntaxError, ...
                main.log.error( "Error in sending command: " + self.handle.before )
                return main.FALSE
            if str( ipVersion ) is '4':
                self.handle.sendline( "packet = ether/ip/tcp" )
            elif str( ipVersion ) is '6':
                self.handle.sendline( "packet = ether/ipv6/tcp" )
            else:
                main.log.error( "Unrecognized option for ipVersion, given " +
                                repr( ipVersion ) )
                return main.FALSE
            self.handle.expect( self.scapyPrompt )
            if "Traceback" in self.handle.before:
                # KeyError, SyntaxError, ...
                main.log.error( "Error in sending command: " + self.handle.before )
                return main.FALSE
            return main.TRUE
        except pexpect.TIMEOUT:
            main.log.exception( self.name + ": Command timed out" )
            return main.FALSE
        except pexpect.EOF:
            main.log.exception( self.name + ": connection closed." )
            main.cleanAndExit()
        except Exception:
            main.log.exception( self.name + ": Uncaught exception!" )
            main.cleanAndExit()

    def buildUDP( self, ipVersion=4, **kwargs ):
        """
        Build an UDP frame

        Will create a frame class with the given options. If a field is
        left blank it will default to the below value unless it is
        overwritten by the next frame.

        NOTE: Some arguments require quotes around them. It's up to you to
        know which ones and to add them yourself. Arguments with an asterisk
        do not need quotes.

        Options:
        ipVersion - Either 4 (default) or 6, indicates what Internet Protocol
                    frame to use to encapsulate into
        Default frame:
        ###[ UDP ]###
          sport= domain *
          dport= domain *
          len= None
          chksum= None

        Returns main.TRUE or main.FALSE on error
        """
        try:
            # Set the UDP frame
            cmd = 'udp = UDP( '
            options = []
            for key, value in kwargs.iteritems():
                options.append( str( key ) + "=" + str( value ) )
            cmd += ", ".join( options )
            cmd += ' )'
            self.handle.sendline( cmd )
            self.handle.expect( self.scapyPrompt )
            if "Traceback" in self.handle.before:
                # KeyError, SyntaxError, ...
                main.log.error( "Error in sending command: " + self.handle.before )
                return main.FALSE
            if str( ipVersion ) is '4':
                self.handle.sendline( "packet = ether/ip/udp" )
            elif str( ipVersion ) is '6':
                self.handle.sendline( "packet = ether/ipv6/udp" )
            else:
                main.log.error( "Unrecognized option for ipVersion, given " +
                                repr( ipVersion ) )
                return main.FALSE
            self.handle.expect( self.scapyPrompt )
            if "Traceback" in self.handle.before:
                # KeyError, SyntaxError, ...
                main.log.error( "Error in sending command: " + self.handle.before )
                return main.FALSE
            return main.TRUE
        except pexpect.TIMEOUT:
            main.log.exception( self.name + ": Command timed out" )
            return main.FALSE
        except pexpect.EOF:
            main.log.exception( self.name + ": connection closed." )
            main.cleanAndExit()
        except Exception:
            main.log.exception( self.name + ": Uncaught exception!" )
            main.cleanAndExit()

    def buildSCTP( self, ipVersion=4, **kwargs ):
        """
        Build an SCTP frame

        Will create a frame class with the given options. If a field is
        left blank it will default to the below value unless it is
        overwritten by the next frame.

        NOTE: Some arguments require quotes around them. It's up to you to
        know which ones and to add them yourself. Arguments with an asterisk
        do not need quotes.

        Options:
        ipVersion - Either 4 (default) or 6, indicates what Internet Protocol
                    frame to use to encapsulate into
        Default frame:
        ###[ SCTP ]###
          sport= domain *
          dport= domain *
          tag = None
          chksum = None

        Returns main.TRUE or main.FALSE on error
        """
        try:
            # Set the SCTP frame
            cmd = 'sctp = SCTP( '
            options = [ ]
            for key, value in kwargs.iteritems( ):
                options.append( str( key ) + "=" + str( value ) )
            cmd += ", ".join( options )
            cmd += ' )'
            self.handle.sendline( cmd )
            self.handle.expect( self.scapyPrompt )
            if "Traceback" in self.handle.before:
                # KeyError, SyntaxError, ...
                main.log.error( "Error in sending command: " + self.handle.before )
                return main.FALSE
            if str( ipVersion ) is '4':
                self.handle.sendline( "packet = ether/ip/sctp" )
            elif str( ipVersion ) is '6':
                self.handle.sendline( "packet = ether/ipv6/sctp" )
            else:
                main.log.error( "Unrecognized option for ipVersion, given " +
                                repr( ipVersion ) )
                return main.FALSE
            self.handle.expect( self.scapyPrompt )
            if "Traceback" in self.handle.before:
                # KeyError, SyntaxError, ...
                main.log.error( "Error in sending command: " + self.handle.before )
                return main.FALSE
            return main.TRUE
        except pexpect.TIMEOUT:
            main.log.exception( self.name + ": Command timed out" )
            return main.FALSE
        except pexpect.EOF:
            main.log.exception( self.name + ": connection closed." )
            main.cleanAndExit()
        except Exception:
            main.log.exception( self.name + ": Uncaught exception!" )
            main.cleanAndExit()

    def buildARP( self, **kwargs ):
        """
        Build an ARP frame

        Will create a frame class with the given options. If a field is
        left blank it will default to the below value unless it is
        overwritten by the next frame.

        NOTE: Some arguments require quotes around them. It's up to you to
        know which ones and to add them yourself. Arguments with an asterisk
        do not need quotes.

        Default frame:
        ###[ ARP ]###
        hwtype     : XShortField          = (1)
        ptype      : XShortEnumField      = (2048)
        hwlen      : ByteField            = (6)
        plen       : ByteField            = (4)
        op         : ShortEnumField       = (1)
        hwsrc      : ARPSourceMACField    = (None)
        psrc       : SourceIPField        = (None)
        hwdst      : MACField             = ('00:00:00:00:00:00')
        pdst       : IPField              = ('0.0.0.0')

        Returns main.TRUE or main.FALSE on error
        """
        try:
            # Set the ARP frame
            cmd = 'arp = ARP( '
            options = []
            for key, value in kwargs.iteritems( ):
                if isinstance( value, str ):
                    value = '"' + value + '"'
                options.append( str( key ) + "=" + str( value ) )
            cmd += ", ".join( options )
            cmd += ' )'
            self.handle.sendline( cmd )
            self.handle.expect( self.scapyPrompt )
            if "Traceback" in self.handle.before:
                # KeyError, SyntaxError, ...
                main.log.error( "Error in sending command: " + self.handle.before )
                return main.FALSE
            self.handle.sendline( "packet = ether/arp" )
            self.handle.expect( self.scapyPrompt )
            if "Traceback" in self.handle.before:
                # KeyError, SyntaxError, ...
                main.log.error( "Error in sending command: " + self.handle.before )
                return main.FALSE
            return main.TRUE
        except pexpect.TIMEOUT:
            main.log.exception( self.name + ": Command timed out" )
            return main.FALSE
        except pexpect.EOF:
            main.log.exception( self.name + ": connection closed." )
            main.cleanAndExit()
        except Exception:
            main.log.exception( self.name + ": Uncaught exception!" )
            main.cleanAndExit()

    def buildICMP( self, ipVersion=4, **kwargs ):
        """
        Build an ICMP frame

        Will create a frame class with the given options. If a field is
        left blank it will default to the below value unless it is
        overwritten by the next frame.
        Default frame:
        ###[ ICMP ]###
          type= echo-request
          code= 0
          chksum= None
          id= 0x0
          seq= 0x0

        Options:
        ipVersion - Either 4 (default) or 6, indicates what Internet Protocol
                    frame to use to encapsulate into

        Returns main.TRUE or main.FALSE on error
        """
        try:
            # Set the ICMP frame
            if str( ipVersion ) is '4':
                cmd = 'icmp = ICMP( '
            elif str( ipVersion ) is '6':
                cmd = 'icmp6 = ICMPv6EchoReply( '
            else:
                main.log.error( "Unrecognized option for ipVersion, given " +
                                repr( ipVersion ) )
                return main.FALSE
            options = []
            for key, value in kwargs.iteritems( ):
                if isinstance( value, str ):
                    value = '"' + value + '"'
                options.append( str( key ) + "=" + str( value ) )
            cmd += ", ".join( options )
            cmd += ' )'
            self.handle.sendline( cmd )
            self.handle.expect( self.scapyPrompt )
            if "Traceback" in self.handle.before:
                # KeyError, SyntaxError, ...
                main.log.error( "Error in sending command: " + self.handle.before )
                return main.FALSE

            if str( ipVersion ) is '4':
                self.handle.sendline( "packet = ether/ip/icmp" )
            elif str( ipVersion ) is '6':
                self.handle.sendline( "packet = ether/ipv6/icmp6" )
            else:
                main.log.error( "Unrecognized option for ipVersion, given " +
                                repr( ipVersion ) )
                return main.FALSE
            self.handle.expect( self.scapyPrompt )
            if "Traceback" in self.handle.before:
                # KeyError, SyntaxError, ...
                main.log.error( "Error in sending command: " + self.handle.before )
                return main.FALSE
            return main.TRUE
        except pexpect.TIMEOUT:
            main.log.exception( self.name + ": Command timed out" )
            return main.FALSE
        except pexpect.EOF:
            main.log.exception( self.name + ": connection closed." )
            main.cleanAndExit()
        except Exception:
            main.log.exception( self.name + ": Uncaught exception!" )
            main.cleanAndExit()

    def sendPacket( self, iface=None, packet=None, timeout=1 ):
        """
        Send a packet with either the given scapy packet command, or use the
        packet saved in the variable 'packet'.

        Examples of a valid string for packet:

        Simple IP packet
        packet='Ether(dst="a6:d9:26:df:1d:4b")/IP(dst="10.0.0.2")'

        A Ping with two vlan tags
        packet='Ether(dst='ff:ff:ff:ff:ff:ff')/Dot1Q(vlan=1)/Dot1Q(vlan=10)/
                IP(dst='255.255.255.255', src='192.168.0.1')/ICMP()'

        Returns main.TRUE or main.FALSE on error
        """
        try:
            # TODO: add all params, or use kwargs
            sendCmd = 'srp( '
            if packet:
                sendCmd += packet
            else:
                sendCmd += "packet"
            if iface:
                sendCmd += ", iface='{}'".format( iface )

            sendCmd += ', timeout=' + str( timeout ) + ')'
            self.handle.sendline( sendCmd )
            self.handle.expect( self.scapyPrompt )
            # main.log.warn( "Send packet response: {}".format( self.handle.before ) )
            if "Traceback" in self.handle.before:
                # KeyError, SyntaxError, ...
                main.log.error( "Error in sending command: " + self.handle.before )
                return main.FALSE
            # TODO: Check # of packets sent?
            return main.TRUE
        except pexpect.TIMEOUT:
            main.log.exception( self.name + ": Command timed out" )
            return main.FALSE
        except pexpect.EOF:
            main.log.exception( self.name + ": connection closed." )
            main.cleanAndExit()
        except Exception:
            main.log.exception( self.name + ": Uncaught exception!" )
            main.cleanAndExit()

    def startFilter( self, ifaceName=None, sniffCount=1, pktFilter="ip" ):
        """
        Listen for packets using the given filters

        Options:
        ifaceName - the name of the interface to listen on. If none is given,
                    defaults to self.ifaceName which is <host name>-eth0
        pktFilter - A string in Berkeley Packet Filter (BPF) format which
                    specifies which packets to sniff
        sniffCount - The number of matching packets to capture before returning

        Returns main.TRUE or main.FALSE on error
        """
        try:
            # TODO: add all params, or use kwargs
            ifaceName = str( ifaceName ) if ifaceName else self.ifaceName
            # Set interface
            self.handle.sendline( 'conf.iface = "' + ifaceName + '"' )
            self.handle.expect( self.scapyPrompt )
            cmd = 'pkt = sniff(count = ' + str( sniffCount ) +\
                  ', filter = "' + str( pktFilter ) + '")'
            main.log.info( "Filter on " + self.name + ' > ' + cmd )
            self.handle.sendline( cmd )
            self.handle.expect( '"\)\r\n' )
            # Make sure the sniff function didn't exit due to failures
            i = self.handle.expect( [ self.scapyPrompt, pexpect.TIMEOUT ], timeout=3 )
            if i == 0:
                # sniff exited
                main.log.error( self.name + ": sniff function exited" )
                main.log.error( self.name + ":     " + self.handle.before )
                return main.FALSE
            # TODO: parse this?
            return main.TRUE
        except pexpect.TIMEOUT:
            main.log.exception( self.name + ": Command timed out" )
            return main.FALSE
        except pexpect.EOF:
            main.log.exception( self.name + ": connection closed." )
            main.cleanAndExit()
        except Exception:
            main.log.exception( self.name + ": Uncaught exception!" )
            main.cleanAndExit()

    def checkFilter( self, timeout=10 ):
        """
        Check that a filter returned and returns the reponse
        """
        try:
            i = self.handle.expect( [ self.scapyPrompt, pexpect.TIMEOUT ], timeout=timeout )
            if i == 0:
                return main.TRUE
            else:
                return main.FALSE
        except pexpect.EOF:
            main.log.exception( self.name + ": connection closed." )
            main.cleanAndExit()
        except Exception:
            main.log.exception( self.name + ": Uncaught exception!" )
            main.cleanAndExit()

    def killFilter( self ):
        """
        Kill a scapy filter
        """
        try:
            self.handle.send( "\x03" )  # Send a ctrl-c to kill the filter
            self.handle.expect( self.scapyPrompt )
            return self.handle.before
        except pexpect.TIMEOUT:
            main.log.exception( self.name + ": Command timed out" )
            return None
        except pexpect.EOF:
            main.log.exception( self.name + ": connection closed." )
            main.cleanAndExit()
        except Exception:
            main.log.exception( self.name + ": Uncaught exception!" )
            main.cleanAndExit()

    def readPackets( self ):
        """
        Read all the packets captured by the previous filter
        """
        try:
            self.handle.sendline( "for p in pkt: p \n")
            self.handle.expect( "for p in pkt: p \r\n... \r\n" )
            self.handle.expect( self.scapyPrompt )
        except pexpect.TIMEOUT:
            main.log.exception( self.name + ": Command timed out" )
            return None
        except pexpect.EOF:
            main.log.exception( self.name + ": connection closed." )
            main.cleanAndExit()
        except Exception:
            main.log.exception( self.name + ": Uncaught exception!" )
            main.cleanAndExit()
        return self.handle.before

    def updateSelf( self, IPv6=False ):
        """
        Updates local MAC and IP fields
        """
        self.hostMac = self.getMac()
        if IPv6:
            self.hostIp = self.getIp( IPv6=True )
        else:
            self.hostIp = self.getIp()

    def getMac( self, ifaceName=None ):
        """
        Save host's MAC address
        """
        try:
            ifaceName = str( ifaceName ) if ifaceName else self.ifaceName
            cmd = 'get_if_hwaddr("' + str( ifaceName ) + '")'
            self.handle.sendline( cmd )
            self.handle.expect( self.scapyPrompt )
            pattern = r'(([0-9a-f]{2}[:-]){5}([0-9a-f]{2}))'
            match = re.search( pattern, self.handle.before )
            if match:
                return match.group()
            else:
                # the command will have an exception if iface doesn't exist
                return None
        except pexpect.TIMEOUT:
            main.log.exception( self.name + ": Command timed out" )
            return None
        except pexpect.EOF:
            main.log.exception( self.name + ": connection closed." )
            main.cleanAndExit()
        except Exception:
            main.log.exception( self.name + ": Uncaught exception!" )
            main.cleanAndExit()

    def getIp( self, ifaceName=None, IPv6=False ):
        """
        Save host's IP address

        Returns the IP of the first interface that is not a loopback device.
        If no IP could be found then it will return 0.0.0.0.

        If IPv6 is equal to True, returns IPv6 of the first interface that is not a loopback device.
        If no IPv6 could be found then it will return :: .

        """
        def getIPofInterface( ifaceName ):
            cmd = 'get_if_addr("' + str( ifaceName ) + '")'
            if IPv6:
                cmd = 'get_if_raw_addr6("' + str( ifaceName ) + '")'
            self.handle.sendline( cmd )
            self.handle.expect( self.scapyPrompt )

            pattern = r'(((2[0-5]|1[0-9]|[0-9])?[0-9]\.){3}((2[0-5]|1[0-9]|[0-9])?[0-9]))'
            if IPv6:
                pattern = r'(\\x([0-9]|[a-f]|[A-F])([0-9]|[a-f]|[A-F])){16}'
            match = re.search( pattern, self.handle.before )
            if match:
                # NOTE: The command will return 0.0.0.0 if the iface doesn't exist
                if IPv6 is not True:
                    if match.group() == '0.0.0.0':
                        main.log.warn( 'iface {0} has no IPv4 address'.format( ifaceName ) )
                return match.group()
            else:
                return None
        try:
            if not ifaceName:
                # Get list of interfaces
                ifList = self.getIfList()
                if IPv6:
                    for ifaceName in ifList:
                        if ifaceName == "lo":
                            continue
                        ip = getIPofInterface( ifaceName )
                        if ip is not None:
                            newip = ip
                            tmp = newip.split( "\\x" )
                            ip = ""
                            counter = 0
                            for i in tmp:
                                if i != "":
                                    counter = counter + 1
                                    if counter % 2 == 0 and counter < 16:
                                        ip = ip + i + ":"
                                    else:
                                        ip = ip + i
                            return ip
                    return "::"
                else:
                    for ifaceName in ifList:
                        if ifaceName == "lo":
                            continue
                        ip = getIPofInterface( ifaceName )
                        if ip != "0.0.0.0":
                            return ip
                    return "0.0.0.0"
            else:
                return getIPofInterface( ifaceName )

        except pexpect.TIMEOUT:
            main.log.exception( self.name + ": Command timed out" )
            return None
        except pexpect.EOF:
            main.log.exception( self.name + ": connection closed." )
            main.cleanAndExit()
        except Exception:
            main.log.exception( self.name + ": Uncaught exception!" )
            main.cleanAndExit()

    def getIfList( self ):
        """
        Return List of Interfaces
        """
        try:
            self.handle.sendline( 'get_if_list()' )
            self.handle.expect( self.scapyPrompt )
            ifList = self.handle.before.split( '\r\n' )
            ifList = ifList[ 1 ].replace( "'", "" )[ 1:-1 ].split( ', ' )
            return ifList

        except pexpect.TIMEOUT:
            main.log.exception( self.name + ": Command timed out" )
            return None
        except pexpect.EOF:
            main.log.exception( self.name + ": connection closed." )
            main.cleanAndExit()
        except Exception:
            main.log.exception( self.name + ": Uncaught exception!" )
            main.cleanAndExit()

if __name__ != "__main__":
    sys.modules[ __name__ ] = ScapyCliDriver()
