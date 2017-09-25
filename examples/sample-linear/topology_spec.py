#!/usr/bin/python

import link_spec
from mininet.topo import Topo
from mininet.node import CPULimitedHost
from mininet.link import TCLink
from mininet.node import OVSSwitch

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
            self.addLink( host, switch, **link_ethernet)
            if lastSwitch:
                self.addLink(switch, lastSwitch, **link_ethernet)
            lastSwitch = switch
