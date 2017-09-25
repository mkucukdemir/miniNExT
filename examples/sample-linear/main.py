#!/usr/bin/python

from topology_spec import LinearTopo
from switch_spec import MultiSwitch
from  controller_spec import POXController
from mininet.log import setLogLevel
from mininet.link import TCLink
from mininet.node import CPULimitedHost
from mininet.net import Mininet
from mininet.util import irange,dumpNodeConnections
from mininext.cli import CLI

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
    # print "** Testing bandwidth between h1 and h4"
    # h1, h4 = net.get('h1', 'h4')
    # net.iperf((h1, h4))
    print "** Running CLI"
    CLI(net)
