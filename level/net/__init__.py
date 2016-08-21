from level.net.node import Node
from level.net.linkage import Linkage, Straight


def from_xml(xml):
    nodes = dict()
    for n in xml.findall('node'):
        node = Node.from_xml(n)
        nodes[node.name] = node

    links = [Straight.from_xml(l, nodes) for l in xml.findall('link')]
    return nodes, links


def draw(net_data, surface, camera):
    nodes, links = net_data

    for l in links:
        l.draw(surface, camera)

    for n in nodes.values():
        n.draw(surface, camera)
