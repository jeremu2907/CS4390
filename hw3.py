#!/usr/bin/python
from mininet.topo import Topo
from mininet.net import Mininet
from mininet.node import Node
from mininet.log import setLogLevel, info
from mininet.cli import CLI


class LinuxRouter(Node):
    def config(self, **params):
        super(LinuxRouter, self).config(**params)
        self.cmd('sysctl net.ipv4.ip_forward=1')

    def terminate(self):
        self.cmd('sysctl net.ipv4.ip_forward=0')
        super(LinuxRouter, self).terminate()


class NetworkTopo(Topo):
    def build(self, **_opts):
        r1 = self.addHost('r1', cls=LinuxRouter, ip='10.0.0.1/8')

        s1 = self.addSwitch('s1')

        # Adding hosts specifying the default route
        h1 = self.addHost(name='h1',
                          ip='10.1.0.252/24',
                          defaultRoute='via 10.1.0.1')
        h2 = self.addHost(name='h2',
                          ip='10.0.0.251/24',
                          defaultRoute='via 10.0.0.1')
        h3 = self.addHost(name='h3',
                          ip='10.0.0.253/24',
                          defaultRoute='via 10.0.0.1')

        # Add host-switch links in the same subnet
        self.addLink(s1,
                     r1,
                     intfName2='r1-eth1',
                     params2={'ip': '10.0.0.1/24'})

        self.addLink(h1,
                     r1,
                     intfName2='r1-eth2',
                     params2={'ip': '10.1.0.1/24'})

        # Add host-switch links
        self.addLink(h2, s1)
        self.addLink(h3, s1)

def run():
    topo = NetworkTopo()
    net = Mininet(topo=topo)
    net.start()

    info(net.pingAll())

    CLI(net)
    net.stop()


if __name__ == '__main__':
    setLogLevel('info')
    run()
