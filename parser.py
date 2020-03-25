#!/usr/bin/env python

####################################################################################
#
#   Author: Boyan NAYDENOV
#   Version: 1.0
#   Description: Parses input XML, and stores the data into usable objects.
#
####################################################################################

import xml.etree.ElementTree as ET
import sys
from netClasses import *

# Transforms a string into an integer, while also extracting the number units.
def getDigit(str):
    isUnit = False;
    for i,c in enumerate(str):
        if not c.isdigit():
            isUnit = True;
            break
    number = int(str[:i]) if (isUnit) else int(str[:(i+1)])
    unit =  str[i:] if (isUnit) else '';

    if unit == 'Mbps':
        number *= 1e6;
    elif unit == 'Gbps':
        number *= 1e6;

    return number;

# Parses all the stations from the XML file and creates/returns a dictionary out of it.
def getStations(root):
    stationDict = {};

    for station in root.iter('station'):
        name = station.get('name');
        sp = station.get('service_policy');
        trans_cap = getDigit(station.get('transmission-capacity'));
        x = float(station.get('x'));
        y = float(station.get('y'));

        stationC = Station(name, sp, trans_cap, x, y);

        stationDict[name] = stationC;

    return stationDict;

# Parses all the switches from the XML file and creates/returns a dictionary out of it.
def getSwitches(root):
    switchesDict = {};

    for switch in root.iter('switch'):

        name = switch.get('name');
        sp = switch.get('service_policy');
        trans_cap = getDigit(switch.get('transmission-capacity'));
        tech_lat = int(switch.get('tech-latency'));
        switching_tech = switch.get('switching-technique');
        x = float(switch.get('x'));
        y = float(switch.get('y'));

        switchC = Switch(name, sp, trans_cap, switching_tech, x, y);

        switchesDict[name] = switchC;

    return switchesDict;

# Parses all the links from the XML file and creates/returns a dictionary out of it.
def getLinks(root):
    linksDict = {};

    for link in root.iter('link'):
        name = link.get('name');
        fromN = link.get('from');
        fromPort = int(link.get('fromPort'));
        toN =  link.get('to');
        toPort = int(link.get('toPort'));
        trans_cap = getDigit(link.get('transmission-capacity'));

        linkC = Link(name, fromN, fromPort, toN, toPort, trans_cap);
        linksDict[name] = linkC;

    return linksDict;

# Parses all the flows from the XML file and creates/returns a dictionary out of it.
def getFlows(root):
    flowsDict = {};

    for flow in root.iter('flow'):
        targets = getTargets(flow);

        deadline = int(flow.get('deadline'));
        name = flow.get('name');
        jitter = int(flow.get('jitter'));
        max_pl = getDigit(flow.get('max-payload'));
        min_pl = getDigit(flow.get('min-payload'));
        period = int(flow.get('period'));
        priority = flow.get('priority');
        source = flow.get('source');

        flowC = Flow( name, deadline, jitter, max_pl, min_pl, period, priority, source, targets);
        flowsDict[name] = flowC;

    return flowsDict;

# Parses all the targets for any given flow and creates/returns a dictionary out of it.
def getTargets(flow):
    targetsDict = {};

    for target in flow.iter('target'):
        paths = [];
        for path in target.iter('path'):
            paths.append(path.get('node'));
        name = target.get('name');
        mode =  target.get('mode');

        targetC = Target(name, mode, paths);
        targetsDict[name] = targetC;

    return targetsDict;

# Function that creates parent network node by parsing the input XML.
# It also attaches all other objects as dictionaries to itself.
def getNetwork(filePath):
    tree = ET.parse(filePath);
    root = tree.getroot();

    networkNode = root.find('network');

    name = networkNode.get('name');
    overhead = int(networkNode.get('overhead'));
    spp = networkNode.get('shortest-path-policy');
    technology = networkNode.get('technology');
    capacity = getDigit(networkNode.get('transmission-capacity'));

    network = Network(name, overhead,spp, technology, capacity);

    stations = getStations(root);
    network.setStations(stations);

    switches = getSwitches(root);
    network.setSwitches(switches);

    links = getLinks(root);
    network.setLinks(links);

    flows = getFlows(root);
    network.setFlows(flows);

    return network;