"""
Copyright 2016 Open Networking Foundation ( ONF )

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
"""
Description: This test is to determine if ONOS can handle
             dynamic scaling of the cluster size.

List of test cases:
CASE1: Compile ONOS and push it to the test machines
CASE2: Assign devices to controllers
CASE21: Assign mastership to controllers
CASE3: Assign intents
CASE4: Ping across added host intents
CASE5: Reading state of ONOS
CASE6: The scaling case.
CASE7: Check state after control plane failure
CASE8: Compare topo
CASE9: Link s3-s28 down
CASE10: Link s3-s28 up
CASE11: Switch down
CASE12: Switch up
CASE13: Clean up
CASE14: start election app on all onos nodes
CASE15: Check that Leadership Election is still functional
CASE16: Install Distributed Primitives app
CASE17: Check for basic functionality with distributed primitives
"""
class HAscaling:

    def __init__( self ):
        self.default = ''

    def CASE1( self, main ):
        """
        CASE1 is to compile ONOS and push it to the test machines

        Startup sequence:
        cell <name>
        onos-verify-cell
        NOTE: temporary - onos-remove-raft-logs
        onos-uninstall
        start mininet
        git pull
        mvn clean install
        onos-package
        onos-install -f
        onos-wait-for-start
        start cli sessions
        start tcpdump
        """
        import re
        main.log.info( "ONOS HA test: Restart all ONOS nodes - " +
                         "initialization" )
        # set global variables
        # These are for csv plotting in jenkins
        main.HAlabels = []
        main.HAdata = []
        try:
            from tests.dependencies.ONOSSetup import ONOSSetup
            main.testSetUp = ONOSSetup()
        except ImportError:
            main.log.error( "ONOSSetup not found. exiting the test" )
            main.cleanAndExit()
        main.testSetUp.envSetupDescription()
        main.Cluster.numCtrls = 1
        try:
            from tests.HA.dependencies.HA import HA
            main.HA = HA()
            # load some variables from the params file
            cellName = main.params[ 'ENV' ][ 'cellName' ]
            main.apps = main.params[ 'ENV' ][ 'appString' ]
            stepResult = main.testSetUp.envSetup( includeCaseDesc=False )
        except Exception as e:
            main.testSetUp.envSetupException( e )
        main.testSetUp.evnSetupConclusion( stepResult )

        main.scaling = main.params[ 'scaling' ].split( "," )
        main.log.debug( main.scaling )
        scale = main.scaling.pop( 0 )
        main.log.debug( scale )
        main.Cluster.setRunningNode( int( re.search( "\d+", scale ).group( 0 ) ) )

        applyFuncs = []
        applyArgs = []
        try:
            if main.params[ 'topology' ][ 'topoFile' ]:
                main.log.info( 'Skipping start of Mininet in this case, make sure you start it elsewhere' )
            else:
                applyFuncs.append( main.HA.startingMininet )
                applyArgs.append( None )
        except (KeyError, IndexError):
                applyFuncs.append( main.HA.startingMininet )
                applyArgs.append( None )

        main.testSetUp.ONOSSetUp( main.Cluster, cellName=cellName,
                                  extraApply=applyFuncs,
                                  applyArgs=applyArgs,
                                  installMax=True,
                                  atomixClusterSize=3,
                                  includeCaseDesc=False )
        main.HA.initialSetUp()

        main.step( 'Set logging levels' )
        logging = True
        try:
            logs = main.params.get( 'ONOS_Logging', False )
            if logs:
                for namespace, level in logs.items():
                    for ctrl in main.Cluster.active():
                        ctrl.CLI.logSet( level, namespace )
        except AttributeError:
            logging = False
        utilities.assert_equals( expect=True, actual=logging,
                                 onpass="Set log levels",
                                 onfail="Failed to set log levels" )

    def CASE2( self, main ):
        """
        Assign devices to controllers
        """
        main.HA.assignDevices( main )

    def CASE102( self, main ):
        """
        Set up Spine-Leaf fabric topology in Mininet
        """
        main.HA.startTopology( main )

    def CASE21( self, main ):
        """
        Assign mastership to controllers
        """
        main.HA.assignMastership( main )

    def CASE3( self, main ):
        """
        Assign intents
        """
        main.HA.assignIntents( main )

    def CASE4( self, main ):
        """
        Ping across added host intents
        """
        main.HA.pingAcrossHostIntent( main )

    def CASE104( self, main ):
        """
        Ping Hosts
        """
        main.case( "Check connectivity" )
        main.step( "Ping between all hosts" )
        pingResult = main.Mininet1.pingall()
        utilities.assert_equals( expect=main.TRUE, actual=pingResult,
                                 onpass="All Pings Passed",
                                 onfail="Failed to ping between all hosts" )

    def CASE5( self, main ):
        """
        Reading state of ONOS
        """
        main.HA.readingState( main )

    def CASE6( self, main ):
        """
        The Scaling case.
        """
        import time
        import re
        assert main, "main not defined"
        assert utilities.assert_equals, "utilities.assert_equals not defined"
        try:
            main.HAlabels
        except ( NameError, AttributeError ):
            main.log.error( "main.HAlabels not defined, setting to []" )
            main.HAlabels = []
        try:
            main.HAdata
        except ( NameError, AttributeError ):
            main.log.error( "main.HAdata not defined, setting to []" )
            main.HAdata = []

        main.case( "Scale the number of nodes in the ONOS cluster" )

        main.step( "Checking ONOS Logs for errors" )
        for ctrl in main.Cluster.active():
            main.log.debug( "Checking logs for errors on " + ctrl.name + ":" )
            main.log.warn( main.ONOSbench.checkLogs( ctrl.ipAddress ) )

        """
        pop # of nodes from a list, might look like 1,3,5,7,5,3...
        install/deactivate node as needed
        """
        try:
            prevNodes = main.Cluster.getRunningPos()
            prevSize = main.Cluster.numCtrls
            scale = main.scaling.pop( 0 )
            main.Cluster.setRunningNode( int( re.search( "\d+", scale ).group( 0 ) ) )
            main.step( "Scaling from {} to {} nodes".format(
                prevSize, main.Cluster.numCtrls ) )
        except IndexError as e:
            main.log.debug( e )
            main.cleanAndExit()

        activeNodes = range( 0, main.Cluster.numCtrls )
        newNodes = [ x for x in activeNodes if x not in prevNodes ]
        deadNodes = [ x for x in prevNodes if x not in activeNodes ]
        main.Cluster.clearActive()
        main.step( "Start new nodes" )  # OR stop old nodes?
        started = main.TRUE
        stopped = main.TRUE
        for i in newNodes:
            main.log.debug( "Starting " + str( main.Cluster.runningNodes[ i ].ipAddress ) )
            started = main.ONOSbench.onosStart( main.Cluster.runningNodes[ i ].ipAddress ) and started
        utilities.assert_equals( expect=main.TRUE, actual=started,
                                 onpass="ONOS started",
                                 onfail="ONOS start NOT successful" )
        for i in deadNodes:
            main.log.debug( "Stopping " + str( main.Cluster.controllers[ i ].ipAddress ) )
            stopped = main.ONOSbench.onosStop( main.Cluster.controllers[ i ].ipAddress ) and stopped
        utilities.assert_equals( expect=main.TRUE, actual=stopped,
                                 onpass="ONOS stopped",
                                 onfail="ONOS stop NOT successful" )

        main.testSetUp.setupSsh( main.Cluster )

        main.testSetUp.checkOnosService( main.Cluster )

        main.Cluster.startCLIs()

        main.step( "Checking ONOS nodes" )
        nodeResults = utilities.retry( main.Cluster.nodesCheck,
                                       False,
                                       attempts=90 )
        utilities.assert_equals( expect=True, actual=nodeResults,
                                 onpass="Nodes check successful",
                                 onfail="Nodes check NOT successful" )

        for i in range( 10 ):
            ready = True
            for ctrl in main.Cluster.active():
                output = ctrl.CLI.summary()
                if not output:
                    ready = False
            if ready:
                break
            time.sleep( 30 )
        utilities.assert_equals( expect=True, actual=ready,
                                 onpass="ONOS summary command succeded",
                                 onfail="ONOS summary command failed" )
        if not ready:
            main.cleanAndExit()

        # Rerun for election on new nodes
        runResults = main.TRUE
        for ctrl in main.Cluster.active():
            run = ctrl.CLI.electionTestRun()
            if run != main.TRUE:
                main.log.error( "Error running for election on " + ctrl.name )
            runResults = runResults and run
        utilities.assert_equals( expect=main.TRUE, actual=runResults,
                                 onpass="Reran for election",
                                 onfail="Failed to rerun for election" )

        main.HA.commonChecks()

    def CASE7( self, main ):
        """
        Check state after ONOS scaling
        """
        main.HA.checkStateAfterEvent( main, afterWhich=1 )

        main.step( "Leadership Election is still functional" )
        # Test of LeadershipElection
        leaderList = []
        leaderResult = main.TRUE

        for ctrl in main.Cluster.active():
            leaderN = ctrl.CLI.electionTestLeader()
            leaderList.append( leaderN )
            if leaderN == main.FALSE:
                # error in response
                main.log.error( "Something is wrong with " +
                                 "electionTestLeader function, check the" +
                                 " error logs" )
                leaderResult = main.FALSE
            elif leaderN is None:
                main.log.error( ctrl.name +
                                 " shows no leader for the election-app." )
                leaderResult = main.FALSE
        if len( set( leaderList ) ) != 1:
            leaderResult = main.FALSE
            main.log.error(
                "Inconsistent view of leader for the election test app" )
            main.log.debug( leaderList )
        utilities.assert_equals(
            expect=main.TRUE,
            actual=leaderResult,
            onpass="Leadership election passed",
            onfail="Something went wrong with Leadership election" )

    def CASE8( self, main ):
        """
        Compare topo
        """
        main.HA.compareTopo( main )

    def CASE9( self, main ):
        """
        Link down
        """
        src = main.params['kill']['linkSrc']
        dst = main.params['kill']['linkDst']
        main.HA.linkDown( main, src, dst )

    def CASE10( self, main ):
        """
        Link up
        """
        src = main.params['kill']['linkSrc']
        dst = main.params['kill']['linkDst']
        main.HA.linkUp( main, src, dst )

    def CASE11( self, main ):
        """
        Switch Down
        """
        # NOTE: You should probably run a topology check after this
        main.HA.switchDown( main )

    def CASE12( self, main ):
        """
        Switch Up
        """
        # NOTE: You should probably run a topology check after this
        main.HA.switchUp( main )

    def CASE13( self, main ):
        """
        Clean up
        """
        main.HA.cleanUp( main )

    def CASE14( self, main ):
        """
        Start election app on all onos nodes
        """
        main.HA.startElectionApp( main )

    def CASE15( self, main ):
        """
        Check that Leadership Election is still functional
            15.1 Run election on each node
            15.2 Check that each node has the same leaders and candidates
            15.3 Find current leader and withdraw
            15.4 Check that a new node was elected leader
            15.5 Check that that new leader was the candidate of old leader
            15.6 Run for election on old leader
            15.7 Check that oldLeader is a candidate, and leader if only 1 node
            15.8 Make sure that the old leader was added to the candidate list

            old and new variable prefixes refer to data from before vs after
                withdrawl and later before withdrawl vs after re-election
        """
        main.HA.isElectionFunctional( main )

    def CASE16( self, main ):
        """
        Install Distributed Primitives app
        """
        main.HA.installDistributedPrimitiveApp( main )

    def CASE17( self, main ):
        """
        Check for basic functionality with distributed primitives
        """
        main.HA.checkDistPrimitivesFunc( main )
