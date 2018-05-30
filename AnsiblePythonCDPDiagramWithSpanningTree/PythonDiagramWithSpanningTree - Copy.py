#!/usr/bin/python
#Written by Markus Borgenstrand, MABO1602.
#Importing the os and graphviz libraries. OS is for reading the CDP information files and later removing them. Graphviz is for the visual topology.
#This scripts creates topologies as CDP sees it with links blocked by STP removed. If no ports are blocked for a VLAN the topology is the same as the Physical topology, this is to avoid creating a topology for each VLAN when all are the same(Like for VLAN 1002-1005 that is not really used anymore).
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
#    print ("Local: "+str(Local))
#    print ("Remote: "+str(Remote))

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



#Exception to check if there even are any files in the directory.
try:
  ListOfFileNamesSTP=os.listdir('./STP')
except:
  ListOfFileNamesSTP=""


ListOfTopologies=['Physical network',edges]

#Next section of the code is to go through the blocking ports from STP which will pop(remove) them from the dictionary for that particular VLAN.
i=0
for FileName in ListOfFileNamesSTP:
  #Split() can split up a string onto different words, if an argument is used it can split on that instead of space which is standard.
  #Because Ansible creates the files as Node_show_STP.txt it will split up the Node show STP.txt into different elements in a list. Only the first holds the node name.
  CurrentNode=FileName.split('_')[0]+".AnsibleLab"
#Opens the file and reads all the lines in the file.
  CurrentFile=open("STP/"+FileName,"rt")
  CurrentFileLines=CurrentFile.readlines()
  
#Loops through all the lines in the file.  The interface names in the file holds blocking interfaces meaning they should be removed from the topology.
  for Lines in CurrentFileLines:
    CurrentEdges=edges.copy() #Copies the edges dictionary as without it, the two variables will point to the same data so changing CurrentEdges will change the edges.
    CurrentLineTemp=Lines.replace('\n','').split("  ")
    CurrentLineTemp[:]=[item for item in CurrentLineTemp if item!='']

#Below if-statements are to fix the output as CDP ses Gig/Fas but STP only sees Gi/Fa as the start of the interface name. CurrentLineTemp[0] is the VLAN number and CurrentLineTemp[1] is the interface that is blocked in STP.
    if CurrentLineTemp[1][0:3]==' Fa':
      CurrentLineTemp[1]=CurrentLineTemp[1][1:3]+'s'+CurrentLineTemp[1][3:]
    elif CurrentLineTemp[1][0:3]==' Gi':
      CurrentLineTemp[1]=CurrentLineTemp[1][1:3]+'g'+CurrentLineTemp[1][3:]
#Below is the varible that holds the hostname and interface link same way as in edges dictionary. 
    comparing=(CurrentNode,CurrentLineTemp[1])

#Below if-statements checks if the blocked port is in the CurrentEdges dictionary which holds all interfaces according to CDP. If found the dictionary entry is pop'ed which means the key and value is removed from the dictionary.
    if comparing in CurrentEdges.keys():
      CurrentEdges.pop(comparing)

#Below if statement checks if the current link is in the values of the dictionary and will then get the corresponding key and will pop that key.
    if comparing in CurrentEdges.values():
      key= CurrentEdges.keys()[CurrentEdges.values().index(comparing)] #Returns key when the value of the dictionary is comparing, from stack overflow.
      CurrentEdges.pop(key)
    ListOfTopologies.append(CurrentLineTemp[0])
    ListOfTopologies.append(CurrentEdges)

for FileName in ListOfFileNamesSTP:
  os.system("rm STP/"+FileName)




#Below code was copied from https://gist.github.com/floatingstatic/598f5258cd7fa554af785aa7dec4417d but changed a bit for my project. 



def draw_topology(topology,style, output_filename='topology'):
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






#Below goes through all the different sets of topologies and saves the topology as VLAN0001 with its topology according to CDP with STPs blocked ports removed as they are not forwarding traffic.ListOfTopologies[i+1] is the interconnection of the nodes while ListOfTopologies[i] is the filename. VLAN0001.png is the filename for the first VLAN and so on. Complete diagram is called Physical network.
i=0
while i<len(ListOfTopologies):
  styles = {
    'graph': {
        'label': ListOfTopologies[i],
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
  draw_topology(ListOfTopologies[i+1],styles,ListOfTopologies[i])
  i+=2
#draw_topology(edges,'topology2')
