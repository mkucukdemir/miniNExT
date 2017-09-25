#!/usr/bin/python

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
