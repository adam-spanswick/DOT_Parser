#!/usr/bin/python

# Adam Spanswick
#
# Lab 2, Part 1
# DOT file parser
#
# This script reads in a DOT file and outputs a custom mininet startup script which initializes
# mininet with the topology of the DOTfile.

from mininet.net import Mininet
from mininet.node import Controller, OVSBridge
from mininet.nodelib import LinuxBridge
from mininet.cli import CLI
from mininet.log import setLogLevel, info

graph = []
hosts = []
switches = []
links = []

with open("example.dot", "r") as dot_file:
    graph = list(dot_file)

# Remove unneeded information from DOT file
graph.pop(0)
graph.pop(-1)

for i in graph:
    if len(i) == 3:
        if i[0] == 's':
            switches.append(i)
        elif i[0] == 'h':
            hosts.append(i)
    elif len(i) > 3:
        left = i[0] + i[1]
        right = i[-3] + i[-2]
        links.append(left + " -- " + right)

class MyBridge(OVSBridge):
    "Custom OVSBridge."
    def __init__(self, *args, **kwargs):
        kwargs.update(stp='True')
        OVSBridge.__init__(self, *args, **kwargs)

# NOTE - to use LinuxBridge instead of OVSBridge, you must install:
# sudo apt-get install bridge-utils
class MyBridge2(LinuxBridge):
    "Custom LinuxBridge."
    def __init__(self, name, stp=True, prio=None, **kwargs):
        LinuxBridge.__init__(self, name, stp, prio, **kwargs)

def emptyNet():
    "Create an empty network and add nodes to it."

    setLogLevel("info")
    #setLogLevel("debug")

    net = Mininet( controller=None, switch=MyBridge )

    #info( '*** Adding controller\n' )
    #net.addController( 'c0' )

    info( '*** Adding hosts\n' )
    # Create h + int for the number of hosts read in from DOT file
    createdHosts = []
    for h in range(len(hosts)):
        host = 'h' + str(h+1)
        host = net.addHost(host, ip='10.0.0.' + str(h+1))
        createdHosts.append(host)

    info( '*** Adding switch\n' )
    createdSwitches = []
    for s in range(len(switches)):
        switch = 's' + str(s+1)
        switch = net.addSwitch(switch)
        createdSwitches.append(switch)

    info( '*** Creating links\n' )
    for l in range(len(links)):
        temp1 = links[l]
        temp2 = temp1[0] + temp1[1]
        temp3 = temp1[-2] + temp1[-1]
        net.addLink(temp2, temp3)

    info( '*** Starting network\n')
    net.start()
    #net.staticArp()
    net.waitConnected() # https://github.com/mininet/mininet/wiki/FAQ

    info( '*** Running CLI\n' )
    CLI( net )

    info( '*** Stopping network' )
    net.stop()

if __name__ == '__main__':
    emptyNet()