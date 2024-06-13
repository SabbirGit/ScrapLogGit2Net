#! /usr/bin/env python3

# Transforms a network of individuals  Graphml File into a network of Organization Graphml file 
# Edge between of org. networks is the sum of developers that worked together
#
#  Example:
#  Nokia and Apple have three developers co-editing the same files
#  Nokia and Apple are then connected with a edge weight of 3 
# 


#Example of use verbose,fitering and only top firms
# ./transform-nofi-2-nofo-GraphML.py -v test-data/icis-2024-wp-networks-graphML/tensorFlowGitLog-2022-git-log-outpuyt-by-Jose.IN.NetworkFile.graphML

print ("")
print ("transform-nofi-2-nofo-GraphML.py - transforming unweighted networks of individuals into weighted networks of organizations since June 2024")
print ("Let's go")
print ("")


"we need to handle networks"
import networkx as nx

"we need system and operating systems untils"
import sys
import os

"we need to parse arguments" 
import argparse



"filtering of firms is not implemented yet" 
# top_firms_that_matter = ['google','microsoft','ibm','amazon','intel','amd','nvidia','arm','meta','bytedance']
# top_firms_that_matter = ['microsoft','ibm','amazon','intel','amd','nvidia','arm','meta','bytedance']
# top_firms_that_do_not_matter = ['users','tensorflow','google']
# top_firms_that_do_not_matter = ['users','tensorflow','gmail']


def printGraph_as_dict_of_dicts(graph):
    print (nx.to_dict_of_dicts(graph))


def printGraph_notes_and_its_data(graph):
    
    for node, data in G.nodes(data=True):
        print (node)
        print (data)


parser = argparse.ArgumentParser()

parser.add_argument("file", type=str, help="the network file")
parser.add_argument("-v", "--verbose", action="store_true",
                    help="increase output verbosity")

parser.add_argument("-t", "--top-firms-only", action="store_true",
                    help="only top_firms_that_matter")

parser.add_argument("-f", "--filter-by-org", action="store_true",
                    help="top_firms_that_do_not_matter")

args = parser.parse_args()



if args.verbose:
    print("In verbose mode")


if args.top_firms_only:
    print()
    print("In top-firms only mode")
    print("Not implemented yet")
    sys.exit()

if  args.filter_by_org:
    print()
    print("In filtering by org mode")
    print("Not implemented yet")
    sys.exit()



# Lets read the graph then 
input_file_name = args.file

G = nx.read_graphml(input_file_name)


print ("Graph imported successfully")
print ("Number_of_nodes="+str(G.number_of_nodes()))
print ("Number_of_edges="+str(G.number_of_edges()))
print ("Number_of_isolates="+str(nx.number_of_isolates(G)))


if args.verbose:
    print() 
    print("printing graph:")
    printGraph_as_dict_of_dicts(G)
    print() 
    print("printing graph and its data:")
    printGraph_notes_and_its_data(G)
    print() 


print ("")
print ("Checking for isolates")

    
isolate_ids=[]
for isolate in nx.isolates(G):
    isolate_ids.append(isolate)

if (isolate_ids != []):
    print("\t Isolates:")
    for node, data in G.nodes(data=True):
        if node in isolate_ids:
            print ("\t",node,data['e-mail'],data['affiliation'])

    print ("")
    print ("WARNING: Removing for isolates")
    print ("WARNING: Networks created with scraplog should only capture collaborative relationships (i.e., no isolates)")

    G.remove_nodes_from(isolate_ids)


print ("")
print ("Isolates removed successfully")
print ("Number_of_nodes="+str(G.number_of_nodes()))
print ("Number_of_edges="+str(G.number_of_edges()))
print ("Number_of_isolates="+str(nx.number_of_isolates(G)))

    
print ("")
print ("We have network of individuals")
print ("We don't have isolates")
print ("Lets transform it into a network of organizations")
print ("")


"G is the individual network"
"orgG is the organizational network"
"The edges in orgG have a atribute n equal to number of dev. that collaborated among organizations" 

orgG= nx.Graph()

# 
# TO TRANSFORM the following algorith is applied
# For each edge in G:
# If edge nodes are connected to developer of another companirs  then add OrgX with weight 1.0 except if that relation was already modelled
#



# G.add_edge("a", "b", weight=0.6)


for edge in G.edges(data=True):
    if args.verbose:
        print("\t Edge info: "+ str(edge) + " FROM node id" + edge[0] + " TO node id" + edge[1] )
        org_affiliation_from = nx.get_node_attributes(G, "affiliation")[edge[0]]
        org_affiliation_to 
        
        print("\t " + org_affiliation_from + " <--> " +nx.get_node_attributes(G, "affiliation")[edge[1]])
        orgG.add_edge(2, 3, weight=1)  


