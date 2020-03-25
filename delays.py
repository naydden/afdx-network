#!/usr/bin/env python

####################################################################################
#
#	Author: Boyan NAYDENOV
#	Version: 1.0
#	Description: Calculates the delay bounds for each target of each flow
#
####################################################################################


from netClasses import *
import copy
import math

# Auxiliary function that prints the arrival curve of each path, per target of a flow.
def checkCA(flow):
	for target in flow.targets.values():
		print("Flow ", flow.name, " Target ", target.name, 'Target Delay', target.delay);
		for i,path in enumerate(target.path):
			print("		Path ", path);
			print("			b ", target.cArrive[path]['b']," tau ", target.cArrive[path]['tau'],\
			  " delay ", target.cArrive[path]['delai']);

# Auxiliary function that prints the links that a switch has attached.
def checkSwitchLinks(net):
	for switch in net.switches.values():
		print("Switch ", switch.name);
		for link in switch.links:
			print("Links attached ", link.name)

# Appends all links going into or coming out of a switch
def assignLinksToSwitches(net):
	for switch in net.switches.values():
		for link in net.links.values():
			# Links coming out of the switch
			if link.fromN == switch.name:
				switch.links.append(link);
			# Links going into the switch
			elif link.toN == switch.name:
				switch.links.append(link);

# Auxiliary function that computes the delay due to the existence of several flows coming out
# of the same source
def getDelayOtherFlows(net, flow):
	b = 0;
	tau = 0;
	for f in net.flows.values():
		if f.source == flow.source:
			b_f = (8*f.max_pl+8*67);
			tau_f = b/(f.period*1e-3);
			b += b_f;
			tau += tau_f;
	delay = b/net.capacity;
	return delay;

# Initialisation of arrival curve for each path of each target for each flow
# This arrival curve will be updated during the iterations of iterativeDelays()
# The initialisation value of the curve is the same as its value for the first path
def initialiseCarrive(net):
	for flow in net.flows.values():
		# the 8 is transforming bytes into bits
		b = (8*flow.max_pl+8*net.overhead);
		tau = b/(flow.period*1e-3);
		# gets the delay of the flow which may be higher due to other flows passing through
		delayInit = getDelayOtherFlows(net,flow);
		cA = {
			'b' : b + tau * delayInit ,
			'tau' : tau,
			'delai' : delayInit
		}
		for target in flow.targets.values():
			for i,path in enumerate(target.path):
					target.cArrive[path] = cA;

# Updates arrival curve at each iteration
def updateFlow(net, link, flows, toN, swName):
	delay = 0;
	b_e = 0;
	tau_e = 0;

	# for every flow going out of the switch,
	# compute the delay it gets by passing through the switch
	for outFlow in flows:
		b_t = 0;
		tau_t = 0;
		for target in outFlow.targets.values():
			# select only one of the targets, by looking at its paths and comparing to
			# destination of link we are studying. We have to avoid considering more than
			# one target per flow, passing through the same switch and going to the same link
			if toN in target.path:
				b_t = target.cArrive[swName]['b'];
				tau_t = target.cArrive[swName]['tau'];
		b_e += b_t;
		tau_e += tau_t;

	# compute switch input delay
	capacity = net.capacity;
	delay = b_e/capacity;

	b_s = b_e + tau_e * delay;
	tau_s = tau_e;

	# update arrival curve of each flux when going out of the switch
	for outFlow in flows:
		for target in outFlow.targets.values():
			for i,path in enumerate(target.path):
				# update cA for only those targets that have the destination in its path
				if toN == path:
					cA_prev = target.cArrive[target.path[i-1]].copy();
					cA = {
						'b' : cA_prev['b'] + cA_prev['tau']*delay ,
						'tau' : cA_prev['tau'],
						'delai' : delay
					}
					target.cArrive[toN] = cA ;
		net.flows[outFlow.name] = outFlow;

def iterativeDelays(net):

	# Initalisation of the arrival curve for each path, of each target, of each flow
	initialiseCarrive(net);
	# Assignation to the switch to all links coming out or going into it.
	assignLinksToSwitches(net);

	i = 0;
	while True:

		# Go through all switches and update the arrival curve for each output flow.
		for switch in net.switches.values():
			for link in switch.links:
				# select only output flows. And we need both direct and reverse
				# flows going out of the switch
				if link.fromN == switch.name:
					updateFlow(net,link,link.flowsDirect,link.toN, switch.name);
				elif link.toN == switch.name:
					updateFlow(net,link,link.flowsReverse,link.fromN, switch.name);

		converged = True;
		# Update target delays and check for convergence
		for flow in net.flows.values():
			for target in flow.targets.values():

				target.delay = 0;
				# Obtains the delay of a target by adding delays per path
				for cA in target.cArrive.values():
					target.delay += cA['delai']*1e6;
				target.delay = math.ceil(target.delay);

				# check for covergence
				if abs(target.delay - target.delayPrev) > 0.000001:
					target.delayPrev = target.delay;
					# since there is already one that has not converged we don't need to check the rest
					converged = False;
					break;
				target.delayPrev = target.delay;
			if not converged:
				break;

		if converged:
			break;
		i += 1;

	# for flow in net.flows.values():
	# 	checkCA(flow);
	# print(i)