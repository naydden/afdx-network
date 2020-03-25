#!/usr/bin/env python

####################################################################################
#
#	Author: Boyan NAYDENOV
#	Version: 1.0
#	Description: Calculates the loads of each link
#
####################################################################################

def checkDirect(node1, node2, fromD, toD):
	return True if fromD == node1 and toD == node2 else False;

def checkReverse(node1, node2, fromR, toR):
	return True if fromR == node1 and toR == node2 else False;

# For each link, assign all the flows that pass through it in both directions (direct and reverse)
# and calculate in the end, the link load in each direction.
def calculeLoads(net):
	for link in net.links.values():
		fromDirect = link.fromN;
		fromReverse = link.toN;

		toDirect = link.toN;
		toReverse = link.fromN;

		for flow in net.flows.values():
			# For Source -> X segment, it is always direct
			if flow.source == fromDirect:
				for target in flow.targets.values():
					if toDirect == target.path[0]:
						link.addFlow(flow, 'direct');
						# exit loop since for a link, and from == source of flow,
						# only one targets is enough as its first path is always the same
						break;
			else:
				for target in flow.targets.values():
					for i, path in enumerate(target.path):
						if i < len(target.path) - 1:
							# Checks if the specific target of the flow is indeed going
							# through the studied link. If so, in what direction.
							if checkDirect(target.path[i], target.path[i+1], fromDirect, toDirect):
								# since many targets of the flow may be using this link, we have to add
								# the flow only once.
								if not flow in link.flowsDirect:
									link.addFlow(flow, 'direct');
							elif checkReverse(target.path[i], target.path[i+1], fromReverse, toReverse):
								# since many targets of the flow may be using this link, we have to add
								# the flow only once.
								if not flow in link.flowsReverse:
									link.addFlow(flow, 'reverse');

		# Finally, now that the link has all the flows that are going through, it can compute its load.
		link.calculateLoad(net.overhead);