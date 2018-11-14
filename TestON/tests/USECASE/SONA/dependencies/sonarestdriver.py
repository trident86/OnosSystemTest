#!/usr/bin/env python
"""
Created on 07-08-2015
Copyright 2015 Open Networking Foundation (ONF)

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

"""
import json
import os
import requests
import types
import sys

from drivers.common.api.controllerdriver import Controller


class SonaRestDriver( Controller ):

    def __init__( self ):
        self.pwd = None
        self.user_name = "user"
        super( SonaRestDriver, self ).__init__()
        self.ip_address = "localhost"
        self.port = "8080"
        self.wrapped = sys.modules[ __name__ ]

    def connect( self, **connectargs ):
        try:
            for key in connectargs:
                vars( self )[ key ] = connectargs[ key ]
            self.name = self.options[ 'name' ]
        except Exception as e:
            main.log.exception( e )
        try:
            if os.getenv( str( self.ip_address ) ) is not None:
                self.ip_address = os.getenv( str( self.ip_address ) )
            else:
                main.log.info( self.name + ": ip set to " + self.ip_address )
        except KeyError:
            main.log.info( "Invalid host name," +
                           "defaulting to 'localhost' instead" )
            self.ip_address = 'localhost'
        except Exception as inst:
            main.log.error( "Uncaught exception: " + str( inst ) )

        return super( OnosRestDriver, self ).connect()

    def pprint( self, jsonObject ):
        """
        Pretty Prints a json object

        arguments:
            jsonObject - a parsed json object
        returns:
            A formatted string for printing or None on error
        """
        try:
            if isinstance( jsonObject, str ):
                jsonObject = json.loads( jsonObject )
            return json.dumps( jsonObject, sort_keys=True,
                               indent=4, separators=( ',', ': ' ) )
        except ( TypeError, ValueError ):
            main.log.exception( "Error parsing jsonObject" )
            return None

    def send( self, url, ip = "DEFAULT", port = "DEFAULT", base="/onos", method="GET",
              query=None, data=None, debug=False ):
        """
        Arguments:
            str ip: ONOS IP Address
            str port: ONOS REST Port
            str url: ONOS REST url path.
                     NOTE that this is is only the relative path. IE "/devices"
            str base: The base url for the given REST api. Applications could
                      potentially have their own base url
            str method: HTTP method type
            dict query: Dictionary to be sent in the query string for
                         the request
            dict data: Dictionary to be sent in the body of the request
        """
        # TODO: Authentication - simple http (user,pass) tuple
        # TODO: should we maybe just pass kwargs straight to response?
        # TODO: Do we need to allow for other protocols besides http?
        # ANSWER: Not yet, but potentially https with certificates
        if ip == "DEFAULT":
            main.log.warn( "No ip given, reverting to ip from topo file" )
            ip = self.ip_address
        if port == "DEFAULT":
            main.log.warn( "No port given, reverting to port " +
                           "from topo file" )
            port = self.port

        try:
            path = "http://" + str( ip ) + ":" + str( port ) + base + url
            if self.user_name and self.pwd:
                main.log.info( "user/passwd is: " + self.user_name + "/" + self.pwd )
                auth = ( self.user_name, self.pwd )
            else:
                auth = None
            main.log.info( "Sending request " + path + " using " +
                           method.upper() + " method." )
            response = requests.request( method.upper(),
                                         path,
                                         params=query,
                                         data=data,
                                         auth=auth )
            if debug:
                main.log.debug( response )
            return ( response.status_code, response.text.encode( 'utf8' ) )
        except requests.exceptions:
            main.log.exception( "Error sending request." )
            return None
        except Exception:
            main.log.exception( self.name + ": Uncaught exception!" )
            main.cleanAndExit()

    def setNetCfg( self, cfgJson, ip="DEFAULT", port="DEFAULT",
                   subjectClass=None, subjectKey=None, configKey=None ):
        """
        Description:
            Set a json object with the ONOS network configurations
        Returns:
            Returns main.TRUE for successful requests; Returns main.FALSE
            if error on requests;
            Returns None for exceptions

        """
        try:
            output = None
            if ip == "DEFAULT":
                main.log.warn( "No ip given, reverting to ip from topo file" )
                ip = self.ip_address
            if port == "DEFAULT":
                main.log.warn( "No port given, reverting to port " +
                               "from topo file" )
                port = self.port
            url = "/openstacknode/configure"
            if subjectClass:
                url += "/" + subjectClass
                if subjectKey:
                    url += "/" + subjectKey
                    if configKey:
                        url += "/" + configKey
            response = self.send( method="POST",
                                  url=url, ip = ip, port = port,
                                  data=json.dumps( cfgJson ) )
            if response:
                if 200 <= response[ 0 ] <= 299:
                    main.log.info( self.name + ": Successfully POST cfg" )
                    return main.TRUE
                else:
                    main.log.error( "Error with REST request, response was: " +
                                    str( response ) )
                    return main.FALSE
        except ( AttributeError, TypeError ):
            main.log.exception( self.name + ": Object not as expected" )
            return None
        except Exception:
            main.log.exception( self.name + ": Uncaught exception!" )
            main.cleanAndExit()
