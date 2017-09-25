#!/usr/bin/python

from os import environ
from mininet.node import Controller, RemoteController

# Custom Controller
POXDIR = environ[ 'HOME' ] + '/pox'

class POXController( Controller ):                                                                         
    "Custom Controller class to invoke POX forwarding.l2_learning"                                     
    def __init__( self, name, cdir=POXDIR,
            command='python pox.py',
            cargs=( 'openflow.of_01 --port=%s '
                'forwarding.l2_learning' ),
            **kwargs ):
        Controller.__init__( self, name, cdir=cdir, command=command, cargs=cargs, **kwargs )
