#!/usr/bin/python

from os import environ
import os
from subprocess import call
from mininet.topo import Topo
from mininet.net import Mininet
from mininet.node import CPULimitedHost
from mininet.link import TCLink
from mininet.util import irange,dumpNodeConnections
from mininet.log import setLogLevel
from mininext.cli import CLI
from mininet.node import OVSSwitch, Controller, RemoteController

# Link Declarations
"""
bw:             bandwidth in b/s (e.g. '10m')
delay:          transmit delay (e.g. '1ms' )
jitter:         jitter (e.g. '1ms')
loss:           loss (e.g. '1' )
gro:            enable GRO (False)
txo:            enable transmit checksum offload (True)
rxo:            enable receive checksum offload (True)
speedup:        experimental switch-side bw option
use_hfsc:       use HFSC scheduling
use_tbf use:    TBF scheduling
latency_ms:     TBF latency parameter
enable_ecn:     enable ECN (False)
enable_red:     enable RED (False)
max_queue_size: queue limit parameter for netem Helper method: bool -> 'on'/'off'
use_htb:        Hierarchical Token Bucket rate limiter
"""
link_fastEthernet = {
            'bw':1000,
            'delay':'1ms',
            'loss':0,
            'max_queue_size':1000
        }

link_ethernet = {
            'bw':10,
            'delay':'1ms',
            'loss':0,
            'max_queue_size':1000,
            'use_htb':True
        }

link_3g = {
            'bw':2,
            'delay':'75ms',
            'loss':2,
            'max_queue_size':1000
        }

link_wifi = {
            'bw':2,
            'delay':'5ms',
            'loss':3,
            'max_queue_size':1000
        }

# Custom COntroller
POXDIR = environ[ 'HOME' ] + '/pox'

class POXController( Controller ):                                                                         
    "Custom Controller class to invoke POX forwarding.l2_learning"                                     
    def __init__( self, name, cdir=POXDIR,
            command='python pox.py',
            cargs=( 'openflow.of_01 --port=%s '
                'forwarding.l2_learning' ),
            **kwargs ):
        Controller.__init__( self, name, cdir=cdir, command=command, cargs=cargs, **kwargs )

# Default OpenFlow controller
# c0 = Controller( 'c0', port=6633 )

# A remote controller
# c0 = RemoteController( 'c0', ip='127.0.0.1', port=6633 )

# Custom Controller
c0 = POXController( 'c0',  port=6633 )

# Default OpenFlow controller
# c1 = Controller( 'c1', port=6634 )

# A remote controller
# c1 = RemoteController( 'c1', ip='127.0.0.1', port=6634 )

# Custom Controller
c1 = POXController( 'c1', port=6634 )

# Switch :: COntroller mapping
cmap = { 's1': c0, 's2': c0, 's3': c1, 's4': c1 }

# Custom Switch
class MultiSwitch( OVSSwitch ):
    "Custom Switch() subclass that connects to different controllers"
    def start( self, controllers ):
        return OVSSwitch.start( self, [ cmap[ self.name ] ] )

# Network Topology
class LinearTopo(Topo):
    "Linear topology of k switches, with one host per switch."

    def __init__(self, k=2, **opts):
        """Init.
            k: number of switches (and hosts)
            hconf: host configuration options
            lconf: link configuration options"""

        super(LinearTopo, self).__init__(**opts)

        self.k = k

        lastSwitch = None
        for i in irange(1, k):
            host = self.addHost('h%s' % i, cpu=.5/k)
            switch = self.addSwitch('s%s' % i)
            # 10 Mbps, 5ms delay, 1% loss, 1000 packet queue
            self.addLink( host, switch, **link_fastEthernet)
            if lastSwitch:
                self.addLink(switch, lastSwitch, **link_fastEthernet)
            lastSwitch = switch

if __name__ == '__main__':
    setLogLevel('info')
    "Create network and run simple performance test"
    topo = LinearTopo(k=4)
    net = Mininet(topo=topo,host=CPULimitedHost, link=TCLink, switch=MultiSwitch, build=False )
    for c in [ c0, c1 ]:
        net.addController(c)
    net.build()
    net.start()
    print "** Dumping host connections"
    dumpNodeConnections(net.hosts)
    print "** Testing network connectivity"
    net.pingAll()
    print "** Testing bandwidth between h1 and h4"
    h1, h4 = net.get('h1', 'h4')
    net.iperf((h1, h4))
    net.iperf((h1, h4))
    net.iperf((h1, h4))
    net.iperf((h1, h4))
    net.iperf((h1, h4))
    print "** Running CLI"
    CLI(net)
