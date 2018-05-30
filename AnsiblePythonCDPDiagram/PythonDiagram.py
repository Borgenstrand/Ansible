#!/usr/bin/python
#Written by Markus Borgenstrand, MABO1602.
#Importing the os and graphviz libraries. OS is for reading the CDP information files and later removing them. Graphviz is for the visual topology.
import os
import graphviz

#Exception to check if there even are any files in the directory.
try:
  ListOfFileNames=os.listdir('./CDP')
except:
  ListOfFileNames=""

NodesConnected={}

i=0
for FileName in ListOfFileNames:
  #Split() can split up a string onto different words, if an argument is used it can split on that instead of space which is standard.
  #Because Ansible creates the files as Node_show_CDP.txt it will split up the Node show CDP.txt into different elements in a list. Only the first holds the node name.
  CurrentNode=FileName.split('_')[0]+".AnsibleLab"
#Opens the file and reads all the lines in the file.
  CurrentFile=open("CDP/"+FileName,"rt")
  CurrentFileLines=CurrentFile.readlines()

#The reason why it starts at j=1 is that the first line is not interesting as it holds this information:
#Device ID        Local Intrfce     Holdtme    Capability  Platform  Port ID
#It is good to have for trouble shooting purposes but not needed in the topology.
  j=1
#This loop loops through all the neighbours in each Node_show_CDP.txt file and adds them to the list, incase there are multiple by the same interface it will add another entry in the dictionary, this is due to the fact that a device might be connected to multiple devices through one link.
  while j<len(CurrentFileLines):
#Below temporary variable removes the \n from the files if it exists, as different devices handle rows in different ways it was added here. 
    CurrentLineTemp=CurrentFileLines[j].replace('\n','').split("  ")
    CurrentLine=[]
    for element in CurrentLineTemp:
      if element != '':
        CurrentLine.append(element)

    j+=1
    try:
      NodesConnected[CurrentNode]+=[CurrentNode,CurrentLine[1],CurrentLine[0],CurrentLine[-1]]
    except:
      NodesConnected[CurrentNode]=[CurrentNode,CurrentLine[1],CurrentLine[0],CurrentLine[-1]]

  CurrentFile.close()

#NodesConnected now holds all the data about the connections. The structure is Local device, Local interface, Remote device, remote interface.

#Now to remove the loaded files(I like to be modular so each section does something and then it is easier to test then just throw everything in at once)
#One reason for this to be done is so that old configurations files will not be added in the graph incase of the node being down.
#Scenario: If R1 is connected to R2 who is connected to R3 who is connected to R1, if R3 goes down the link is only R1 to R2, but if the files are not removed Ansible will not remove them(only update R1 and R2 file) and then R3 will magically be shown in the graph anyway. This can of course be commenteded out for troubleshooting purposes.
for FileName in ListOfFileNames:
  os.system("rm CDP/"+FileName)


NodesKeys=sorted(NodesConnected.keys())
edges={}
#print NodesKeys
for Nodes in NodesKeys:
  i=0
  while i<len(NodesConnected[Nodes]):
#Need a bit of magic to show the linknames correctly as sometimes it takes a space in the name from the show cdp neighbour file.
#First splitting up the string by seperating everythign with a space between.
#Then emptying the empty elements and only keeping the elements with something in it. Doing this for the Local and Remote link.
#The reason for this is that the tuples ('R1.AnsibleLab', 'Ser 1/2') and ('R1.AnsibleLab', ' Ser 1/2') are different due to the "Ser 1/2" and " Ser 1/2" being different. 
    LocalLink=NodesConnected[Nodes][i+1].split(" ")
    #print ("LocalLink Before: "+str(LocalLink))
    LocalLink[:]=[item for item in LocalLink if item!='']
    LocalLink=str(LocalLink[0]+LocalLink[1])
    RemoteLink=NodesConnected[Nodes][i+3].split(" ")
    #print ("RemoteLink Before: "+str(RemoteLink))
    RemoteLink[:]=[item for item in RemoteLink if (item!='' and item!="WS-C3750-")]#This is to avoid issues with C3750 taking up a lot of space in show cdp neighbor output
    RemoteLink=str(RemoteLink[0]+RemoteLink[1])
    #print ("LocalLink: "+LocalLink)
    #print ("RemoteLink: "+RemoteLink)
#The Local variable holds the current Local node and its interface in a tuple, the Remote holds the remote node and its interface. This will then be compared against the edges dictionary so duplicate nodes and links will not show up in the graph. Edges will otherwise show both link from R1 to R3 and the same link from R3 to R1 even though it is one and the same.
    Local=(NodesConnected[Nodes][i],LocalLink)
    Remote=(NodesConnected[Nodes][i+2],RemoteLink)
    print ("Local: "+str(Local))
    print ("Remote: "+str(Remote))

    if(Local in edges.keys() and Remote in edges.values()):
      pass
      #Below print statement is kept for troubleshooting purposes
      #print("Duplicated local in keys remote in values")
    elif(Remote in edges.keys() and Local in edges.values()):
      pass
      #Below print statement is kept for troubleshooting purposes
      #print("Duplicated Remote in keys Local in values")
    else:
      edges[Local]=Remote
    i+=4

#Below is only for troubleshooting if needed or if we need data for manually creating the topology using CDP as the data source.
#print (edges)
#print (edges.keys())
#print (edges.values())


#Below code was copied from https://gist.github.com/floatingstatic/598f5258cd7fa554af785aa7dec4417d but changed a bit for my project. 

def draw_topology(topology, output_filename):
    style = {
      'graph': {
        'label': output_filename,
        'fontsize': '16',
        'fontcolor': 'white',
        'bgcolor': '#333333',
        'rankdir': 'BT',
      },
      'nodes': {
        'fontname': 'Helvetica',
        'shape': 'box',
        'fontcolor': 'white',
        'color': '#006699',
        'style': 'filled',
        'fillcolor': '#006699',
        'margin': '0.4',
      },
      'edges': {
        'style': 'dashed',
        'color': 'green',
        'arrowhead': 'open',
        'fontname': 'Courier',
        'fontsize': '10',
        'fontcolor': 'white',
      }
    }

    nodes = set([key[0] for key in topology.keys() + topology.values()])

    g = graphviz.Graph(format='png')

    for node in nodes:
        g.node(node)

    for key, value in topology.iteritems():
        head, t_label = key
        tail, h_label = value
        g.edge(head, tail, headlabel=h_label, taillabel=t_label, label=" "*12)

    g.graph_attr.update(
        ('graph' in style and style['graph']) or {}
    )
    g.node_attr.update(
        ('nodes' in style and style['nodes']) or {}
    )
    g.edge_attr.update(
        ('edges' in style and style['edges']) or {}
    )

    g.render(filename=output_filename)







draw_topology(edges,'Network diagram')


