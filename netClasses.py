#!/usr/bin/env python

####################################################################################
#
#   Author: Boyan NAYDENOV
#   Version: 1.0
#   Description: Auxiliary classes for storing the AFDX network elements.
#
####################################################################################


# Parent class that contains the network characteristics as well as all stations,
# switches, links and flows.
class Network:
    def __str__(self):
        return str(self.__class__) + ": " + str(self.__dict__)

    def __init__(self, name, overhead, spp, technology, capacity):
        self.name = name
        self.overhead = overhead
        self.spp = spp
        self.technology = technology
        self.capacity = capacity

    def setStations(self, stations):
        self.stations = stations;

    def setSwitches(self, switches):
        self.switches = switches;

    def setLinks(self, links):
        self.links = links;

    def setFlows(self, flows):
        self.flows = flows;

    def print_c(self):
        print("{ overhead }", self.overhead + 1)

# Class that contains all the data  of an AFDX station
class Station:
    def __str__(self):
        return str(self.__class__) + ": " + str(self.__dict__)

    def __init__(self, name, sp, trans_cap, x, y):
        self.name = name
        self.sp = sp
        self.trans_cap = trans_cap
        self.x = x
        self.y = y

# Class that contains all the data  of an AFDX switch
class Switch:
    def __str__(self):
        return str(self.__class__) + ": " + str(self.__dict__)

    def __init__(self, name, sp, trans_cap, switching_tech, x, y):
        self.name = name
        self.sp = sp
        self.trans_cap = trans_cap
        self.x = x
        self.y = y
        self.links = []
        self.exitFlows = []
        self.enterFlows = []

# Class that contains all the data  of an AFDX link
class Link:
    def __str__(self):
        return str(self.__class__) + ": " + str(self.__dict__)

    def __init__(self, name, fromN, fromPort, toN, toPort, trans_cap):

        self.name = name
        self.fromN = fromN;
        self.fromPort = fromPort;
        self.toN =  toN;
        self.toPort = toPort;
        self.trans_cap = trans_cap;

        # Edge -> Switch : direct
        self.flowsDirect = [];
        self.loadDirect = 0;

        # Switch -> Edge : reverse
        self.flowsReverse = [];
        self.loadReverse = 0;

    def addFlow(self, flow, typeFlow):
        if typeFlow == 'direct':
            self.flowsDirect.append(flow);
        else:
            self.flowsReverse.append(flow);

    # performs the load computation of the link
    def calculateLoad(self, overhead):
        # Direct Load
        load = 0;
        for flow in self.flowsDirect:
            flux = (8*flow.max_pl+8*overhead)/(flow.period*1e-3);
            load += flux;
        self.loadDirect = load/self.trans_cap;

        # Reverse Load
        load = 0;
        for flow in self.flowsReverse:
            flux = (8*flow.max_pl+8*overhead)/(flow.period*1e-3);
            load += flux;
        self.loadReverse = load/self.trans_cap;

# Class that contains all the data of an AFDX flow
class Flow:
    def __str__(self):
        return str(self.__class__) + ": " + str(self.__dict__)

    def __init__(self, name, deadline, jitter, max_pl, min_pl, period, priority, source, targets):
        self.name = name;
        self.deadline = deadline;
        self.jitter = jitter;
        self.max_pl = max_pl;
        self.min_pl = min_pl;
        self.period = period;
        self.priority = priority;
        self.source = source;
        self.targets = targets;
        self.delay = 0;

# Class that contains all the data of an AFDX flow target
class Target:
    def __str__(self):
        return str(self.__class__) + ": " + str(self.__dict__)

    def __init__(self, name, mode, path):
        self.name = name;
        self.mode = mode;
        self.path = path;
        self.delay = 0;
        self.delayPrev = 0;
        self.jitter = 0;
        self.cArrive = {};