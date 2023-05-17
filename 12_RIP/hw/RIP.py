import json
import os

import pprint
from typing import Dict, Union, List
from collections import namedtuple

# aliases
NodeIp = int
# NamedTuples
DistNode = namedtuple('Point', ['dist', 'node_ip'])


NETWORK_DIAMETR = 15
PATH_TO_NETWORKS_DIR = os.path.join(os.path.dirname(__file__), "networks")

class Network:
    def __init__(self) -> None:
        self.nodes : Dict[NodeIp : Node] = dict()

    def add_node(self, node_ip : NodeIp):
        if node_ip not in self.nodes:
            self.nodes[node_ip] = Node(node_ip, self)
        else:
            # change or raise exception ?
            pass
    
    def add_edge(self, node_ip_1 : NodeIp, node_ip_2 : NodeIp):
        self.nodes[node_ip_1].add_neighbor(node_ip_2)
        self.nodes[node_ip_2].add_neighbor(node_ip_1)

    def get_node(self, node_ip : NodeIp) -> Union["Node", None]:
        if node_ip in self.nodes:
            return self.nodes[node_ip]
        else:
            return None
    
    def update_network(self):
        is_updated : bool = False
        for node_ip in self.nodes:
            is_updated |= self.nodes[node_ip].update()
        return is_updated != 0

class Node:
    def __init__(self, node_ip : NodeIp, network : Network) -> None:
        self.network = network
        self.node_ip = node_ip
        self.routing_table : Dict[NodeIp, DistNode] = {
            self.node_ip : DistNode(dist=0, node_ip=self.node_ip)
        }

    def add_neighbor(self, node_ip : NodeIp):
        self.routing_table[node_ip] = DistNode(dist=1, node_ip=node_ip)

    def _update_node(self, node_ip : NodeIp):
        is_updated = False
        cur_node = self.network.get_node(node_ip)
        if cur_node is None:
            print(f"This node={node_ip} is not existed!")
            return

        for nb_node_ip, nb_dist_node in cur_node.routing_table.items():
            if nb_node_ip not in self.routing_table:
                self.routing_table[nb_node_ip] = DistNode(dist=nb_dist_node.dist + 1, node_ip=cur_node.node_ip)
                is_updated = True
            else:
                if self.routing_table[nb_node_ip].dist > nb_dist_node.dist + 1:
                    self.routing_table[nb_node_ip] = DistNode(dist=nb_dist_node.dist + 1, node_ip=cur_node.node_ip)
                    is_updated = True
        return is_updated

    def update(self):
        neighbors = [node_ip for node_ip, dist_node in self.routing_table.items() if dist_node.dist == 1]
        is_updated = False
        for node_ip in neighbors:
            is_updated |= self._update_node(node_ip=node_ip)
        return is_updated


class RIP:
    def __init__(self, network_json : Dict[NodeIp, List[NodeIp]],
                  network_diametr : int = NETWORK_DIAMETR) -> None:
        self.network_diametr = network_diametr
        # self.number_step = 1

        self._prepared_graph(network_json=network_json)

    
    def _prepared_graph(self, network_json : Dict[NodeIp, List[NodeIp]]):
        self.network = Network()
        for cur_v, list_to_v in network_json.items():
            self.network.add_node(cur_v)
            for to_v in list_to_v:
                self.network.add_node(to_v)
                self.network.add_edge(cur_v, to_v)
    
    def run(self):
        step = 1
        while self.network.update_network() and step <= self.network_diametr:
            for node_ip in self.network.nodes:
                print(f"Simulation step {step} of router {node_ip}")
                print(f'{"[Source IP]":20} {"[Destination IP]":20} {"[Next Hop]":20} {"Metric":20}')

                for out_node_ip, out_dist_node in self.network.get_node(node_ip).routing_table.items():
                    if node_ip != out_node_ip:
                        print(f'{node_ip:20} {out_node_ip:20} {out_dist_node.node_ip:20} {out_dist_node.dist:20}')
                print()

            step += 1

        for node_ip in self.network.nodes:
            print(f'Final state of router {node_ip}')
            print(f'{"[Source IP]":20} {"[Destination IP]":20} {"[Next Hop]":20} {"Metric":20}')
            for out_node_ip, out_dist_node in self.network.get_node(node_ip).routing_table.items():
                if out_node_ip != node_ip:
                    print(f'{node_ip:20} {out_node_ip:20} {out_dist_node.node_ip:20} {out_dist_node.dist:20 }')
            print()


if __name__ == "__main__":
    network_json = json.load(open(os.path.join(PATH_TO_NETWORKS_DIR, "network.json"), "r"))
    rip = RIP(network_json=network_json)

    rip.run()


