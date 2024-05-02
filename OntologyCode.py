from owlready2 import *
import networkx as nx
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

# Enter file name to read ontology
onto = get_ontology("TestCase2New.rdf").load()

# Node statistics
nSize = 2000
nShape = "o"

# Impact analysis prompt
impact = input("What Node would you like to test the Impact Analysis on? ")

#Beginning of creation of the Graph
G = nx.DiGraph()

for ind in onto.individuals():
    className = str(ind.is_a).split(".")[-1]
    className = className.split("]")[0]
    G.add_node(ind.name, cl  = str(className))
    
    for prop in ind.get_properties():
        # Checking if the property has a value for the individual
        if prop[ind]:
            propName = str(prop).split(".")[-1]
            propName = propName.split("]")[0]
            
            # Add each value of the property as a node and create edges between the individual and its values
            for value in prop[ind]:
                name = str(value)
                value_name = name.split(".")[-1]
                if (ind.name != name):
                    G.add_node(value_name)
                    G.add_edge(ind.name, value_name, label = propName)
               
# Dicts for the class of requirements and defined edges
classes = nx.get_node_attributes(G, 'cl')
edges = nx.get_edge_attributes(G, 'label')

# Setting the colors of the nodes, dependent on type
nColor = {}
for ind in classes:
    if classes[ind] == "Function_Types" or classes[ind] == "Condition_Types" or classes[ind] == "Display_Types":
        color = {ind:"tan"}
        nColor.update(color)
        
    elif classes[ind] == "LL_Requirement":
        color = {ind:"lavender"}
        nColor.update(color)

    elif classes[ind] == "UI_Requirement":
        color = {ind:"skyblue"}
        nColor.update(color)

    elif classes[ind] == "Customer_Requirement":
        color = {ind:"lightgreen"}
        nColor.update(color)

    elif classes[ind] == "Artifact":
        color = {ind:"salmon"}
        nColor.update(color)

    elif classes[ind] == "Sources":
        color = {ind:"lightyellow"}
        nColor.update(color)

    else:
        color = "grey"
        nColor.update(color)


# Setting the impacted node colors        
eColor = {(u,v):"black" for u,v in edges} 
for node in G.nodes():
    if node == impact:
        colorImpact = "red"
        nColorImpact = {impact:colorImpact}
        nColor.update(nColorImpact)
        
        for u,v in edges:
            try:    
                if (edges[(u, impact)] in edges[(u,v)]):
                    if (edges[(u,impact)] == "refers to"):
                        colorImpact = "orange"
                    else:
                        colorImpact = "orange"
                    nColorImpact = {u:colorImpact}
                    eColorImpact = {(u,impact):colorImpact} 
                    nColor.update(nColorImpact)
                    eColor.update(eColorImpact)
                        
            except KeyError:
                continue
            
        for u,v in edges:
            try:    
                     
                if (edges[(impact, v)] in edges[(u,v)]):
                    colorImpact = "orange"
                    nColorImpact = {v:colorImpact}
                    eColorImpact = {(impact,v):colorImpact} 
                    nColor.update(nColorImpact)
                    eColor.update(eColorImpact)
                        
            except KeyError:
                continue
            
    else: 
        colorImpact = "none"

# Enables editing of text within node, if text would overflow
midN = '-\n'
nMod = {n: n.replace(" ","\n") if (" " in n[:len(n)]) else n
        for n in G}
nMod2 = {n: (n[:len(n) // 2] + midN + n[len(n) // 2:]) if ((len(n)*(nSize/6) > nSize) and "\n" not in nMod[n]) else nMod[n] for n in nMod}
nMod.update(nMod2)

# Different types of graph layouts, uncomment to select type
#pos = nx.circular_layout(G, scale=2)
pos = nx.kamada_kawai_layout(G)
#pos = nx.spring_layout(G, seed=42)
#pos = nx.nx_agraph.graphviz_layout(G,"twopi", args = '-Gnodesep=.5')

# Graph generator
plt.figure(figsize=(64, 64))
nx.draw_networkx_edges(G, pos, width = 1, edge_color =[eColor[(u,v)] for u,v in edges], edgelist=edges, arrows=True, node_size = nSize)
nx.draw_networkx_nodes(G, pos, node_size = nSize, node_color = [nColor[node] for node in G.nodes()], node_shape = nShape, edgecolors = "black")
nx.draw_networkx_labels(G, pos, labels = nMod)

plt.title("Graph Created from Actual Trace Data")

# Setting information for the legend
sourceData = mpatches.Patch(color='lightgreen', label='Customer Requirement')
CRData = mpatches.Patch(color='skyblue', label='UI Requirement')
UIData = mpatches.Patch(color='lavender', label='Lower Level Requirement')
AData = mpatches.Patch(color='salmon', label='Artifict')
PropData = mpatches.Patch(color='tan', label='Shared Property')
IData = mpatches.Patch(color='red', label='Analyzed Node')
DData = mpatches.Patch(color='orange', label='Impacted')
plt.legend(title = 'Legend', title_fontsize = 60, prop = {'size':40}, handles=[sourceData, CRData, UIData, AData, PropData, IData, DData])

# Saving graph as a PNG
plt.savefig('Impact Pictures/Impact.png')

# Present Graph
plt.show()
