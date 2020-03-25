#!/usr/bin/env python

####################################################################################
#
#	Author: Boyan NAYDENOV
#	Version: 1.0
#	Description: Script that evaluates the performance of AFDX networks
#				 by calculating their loads and its end-to-end delay bounds
#				 for transimtted flows.
#			Input: Path of XML with the charactersitcs of the network.
#			STDOUT Output: XML with the delay bounds and loads for the given input.
#	Requirements: >Python 3
#
####################################################################################

import sys

from parser import getNetwork
from load import calculeLoads
from delays import iterativeDelays
from serialiser import generateOutput
from parser_compare import compareResults

def isStable(net):
	isStable = True;
	for link in net.links.values():
		if link.loadDirect > 1 or link.loadReverse > 1:
			isStable = False;

	if not isStable:
		# If network is not stable, program exits here
		print("Net is not stable!!");
		exit();

# Gets the path of the INPUT xml file
filePath = sys.argv[1];

# Get the network object. It contains all the stations, switches, links and flows
net = getNetwork(filePath)

## Compute links LOADS ##
calculeLoads(net);

## Check STABILITY of network ##
isStable(net);

## Compute flow DELAYS ##
iterativeDelays(net);

## Generate output XML into stdout ##
generateOutput(net, filePath);

compareResults(net, filePath)