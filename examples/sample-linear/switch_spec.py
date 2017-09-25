#!/usr/bin/python

from mininet.node import OVSSwitch

# Custom Switch
class MultiSwitch( OVSSwitch ):
    "Custom Switch() subclass that connects to different controllers"
    def start( self, controllers ):
        return OVSSwitch.start( self, [ cmap[ self.name ] ] )
