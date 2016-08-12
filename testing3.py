import geni.rspec.pg as PG
import geni.rspec.egext as EGX
import geni.rspec.igext as IGX
import community
import networkx as nx
import matplotlib.pyplot as plt
import seaborn as sns

r = PG.Request()
G = nx.Graph(nx.drawing.nx_pydot.read_dot("topology.dot.plain")) #newfile.dot

links = []
edgeno = 0

for edge in G.edges():
    links.insert(edgeno, PG.LAN('lan%d' % edgeno))
    links[edgeno].bandwidth = 10000
    edgeno += 1

nodeno = 0
ifaceCounter = 0
vms = []
for node in G.nodes():
	if G.degree(node) > 10:
		#will name supernode-x if it has over 10 links attached to it
		igvm = IGX.XenVM("supernode-%d" % nodeno)
	else:
		igvm = IGX.XenVM("node-%d" % nodeno)
	vms.insert(nodeno, igvm)
	nodeno += 1
	#not sure if the code under this will work
	for neighbor in G.neighbors(node):
        iface = igvm.addInterface("if%d" % ifaceCounter) 
        ifaceCounter += 1
        iface.addAddress(PG.IPv4Address("%d" % (node), "255.255.255.0")) 
        links[edgeno].addInterface(iface) 
        #ifacecounter is not defined error????
