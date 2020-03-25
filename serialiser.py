#!/usr/bin/env python

####################################################################################
#
#	Author: Boyan NAYDENOV
#	Version: 1.0
#	Description: Transofrms the obtained results into a string XML that is printed to STDOUT.
#
####################################################################################

import xml.etree.ElementTree as ET

# Recursive function that adds spaces and end of lines to an xml in order to print it in
# a prettier way. Extracted from http://effbot.org/zone/element-lib.htm#prettyprint
def prettify(elem, level=0):
	i = "\n" + level*"  "
	if len(elem):
		if not elem.text or not elem.text.strip():
			elem.text = i + "  "
		if not elem.tail or not elem.tail.strip():
			elem.tail = i
		for elem in elem:
			prettify(elem, level+1)
		if not elem.tail or not elem.tail.strip():
			elem.tail = i
	else:
		if level and (not elem.tail or not elem.tail.strip()):
			elem.tail = i

# Serialises the computed data into a xml string. It follows WoPANets xml standard
def generateOutput(net, filePath):
	results = ET.Element('results')

	# Delays and Jitters
	delays = ET.SubElement(results, 'delays')
	jitters = ET.SubElement(results, 'jitters')

	for flow in net.flows.values():
		flow_d = ET.SubElement(delays, "flow", name=flow.name);
		flow_j = ET.SubElement(jitters, "flow", name=flow.name);
		for target in flow.targets.values():
			target_d = ET.SubElement(flow_d, "target", name=target.name, value=str(target.delay));
			target_j = ET.SubElement(flow_j, "target", name=target.name, value=str(target.jitter));

	# Backlogs
	backlogs = ET.SubElement(results, 'backlogs')

	for s in net.switches.values():
		switch = ET.SubElement(backlogs, "switch", name=s.name)
		for link in s.links:
			port = ET.SubElement(switch, "port", num=str(0), backlog=str(0), delay=str(0))
		total = ET.SubElement(switch, "total", backlog=str(0), buffer=str(0), percent=str(0));

	# Loads
	load = ET.SubElement(results, 'load')

	for link in net.links.values():
		edge = ET.SubElement(load, 'edge', name=link.name);
		loadStrD = str(round(link.loadDirect*100,1))+"%"
		loadDirect = ET.SubElement(edge, 'usage', type="direct", value="{:.4e}".format(link.loadDirect*link.trans_cap), percent=loadStrD)
		loadStrR = str(round(link.loadReverse*100,1))+"%"
		loadReverse = ET.SubElement(edge, 'usage', type="reverse", value="{:.4e}".format(link.loadReverse*link.trans_cap), percent=loadStrR)

	prettify(results);
	tree = ET.ElementTree(results)
	# fileName = filePath.split("/");
	# fileName = fileName[len(fileName) - 1];
	# fileName = fileName.split(".")[0];
	# tree.write("./results/"+fileName+"_res.xml", xml_declaration=True, encoding='UTF-8', method="xml");
	print(ET.tostring(results, encoding='utf8').decode('utf8'))