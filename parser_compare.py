#!/usr/bin/env python

####################################################################################
#
#   Author: Boyan NAYDENOV
#   Version: 1.0
#   Description: Parses output XML, and compares WoPANets delays and loads to computed ones
#
####################################################################################

import xml.etree.ElementTree as ET
import sys


def getFlows(results):

    flowsDict = {};
    for flow in results.iter('flow'):
        targets = getTargets(flow);
        name = flow.get('name');
        flowsDict[name] = targets;

    return flowsDict;


def getTargets(flow):

    targetsDict = {};
    for target in flow.iter('target'):
        name = target.get('name');
        delay =  float(target.get('value'));

        targetsDict[name] = delay;

    return targetsDict;

def getEdges(edges):

    edgesDict = {};
    for edge in edges.iter('edge'):
        name = edge.get('name');
        loads = getLoads(edge);

        edgesDict[name] = loads;
    return edgesDict;

def getLoads(edge):
    direct = 0;
    reverse = 0;
    for usage in edge.iter('usage'):
        if usage.get("type") == "direct":
            direct = float(usage.get("value"));
        else:
            reverse = float(usage.get("value"));
    loadDict = {
        'direct' : direct,
        'reverse' : reverse
    }
    return loadDict;

def compareResults(net, filePath):
    fileName = filePath.split("/");
    fileName = fileName[len(fileName) - 1];
    fileName = fileName.split(".")[0];

    tree = ET.parse('./samples/'+fileName+'_res.xml');
    root = tree.getroot();

    delaysNode = root.find('delays');
    flows_original = getFlows(delaysNode);

    loadsNode = root.find('load');
    loadsOriginal = getEdges(loadsNode);

    flows_calculated = net.flows;

    for f_oName, f_oTargets in flows_original.items():
        f_cTargets = flows_calculated[f_oName].targets;
        print("Flow ", f_oName)
        for t_oName, t_oDelay in f_oTargets.items():
            t_cDelay = f_cTargets[t_oName].delay;
            print("     Target ", t_oName, " delta delay of ", t_oDelay - t_cDelay)

    loads_calculated = net.links;
    for l_oName, l_oLoads in loadsOriginal.items():
        for loadType, load in l_oLoads.items():
            l_cloadD = loads_calculated[l_oName].loadDirect*net.capacity;
            l_cloadR = loads_calculated[l_oName].loadReverse*net.capacity;
            print("Load ", l_oName)
            print("     Reverse delta ", l_cloadR - l_oLoads['reverse'], " Direct delta ", l_cloadD - l_oLoads['direct'] )