##ANLY503NetworkVisTutorial.R
##Based on
##http://www.kateto.net/wp-content/uploads/2015/06/Polnet%202015%20Network%20Viz%20Tutorial%20-%20Ognyanova.pdf
##To use this, you must install the following
##install.packages("igraph")
##install.packages("network")
##install.packages("sna")
##install.packages("ndtv")

library(igraph)
library(network)
library(sna)
library(ndtv)

##This tutorial will use two datasets

###DATASET1 - edges and nodes
##Dataset1-Media-Example-NODES.csv
##and
##Dataset1-Media-Example-EDGES.csv
##Link to data is here
##http://www.kateto.net/wordpress/wp-content/uploads/2015/06/Polnet2015.zip
##Be sure both datafiles are names as shown above and are
##placed in the CWD for R

nodes <- read.csv("HeroNODES.csv", header=T, as.is=T)
links <- read.csv("HeroEDGES.csv", header=T, as.is=T)

##Examine the data
(nodes)
(head(nodes))
(head(links))
(nrow(nodes))
(nrow(links))
(length(unique(nodes$id)))
(nrow(unique(links[,c("from", "to")])))

##Notice that there are 52 links, but
##only 49 unique from-to links
##We will aggregate repeated from-to links
##by summing the weights

#(links)
## This is another method to aggregate.
#links <- aggregate(links[,3], links[-3],sum)
##The above and below lines of code do the same thing

## Use the weight and sum the weight to combone from, to, and type
## Rename the columns to be from, to, and type (which are the same names)
links<- aggregate(links$weight,by=list(from=links$from, to=links$to, type=links$type),sum)
#(nrow(unique(links[,c("from", "to")])))
## Put the links in order using from and to
links <- links[order(links$from, links$to),]
#Rename column 4 as wright
colnames(links)[4] <- "weight"
#Remove the row names
rownames(links) <- NULL
#Recheck the uniqueness
(nrow(links))
(nrow(unique(links[,c("from", "to")])))
(links)
(nodes)


### DATASET 2 - edges and nodes#####################
#-----------------------------
## IGNORE THIS - ITS FOR SOMETHING ELSE ############
#----------------------------
#nodes2 <- read.csv("Dataset2-Media-User-Example-NODES.csv", header=T, as.is=T)
#links2 <- read.csv("Dataset2-Media-User-Example-EDGES.csv", header=T, row.names=1)
#(head(nodes2))
#(head(links2))
#links2 <- as.matrix(links2)
#dim(links2)
#dim(nodes2)
####################################################
#

############Using igraph and creating a network object#####
## Network Vis: starting with igraph
## Start by converting raw data to an igraph
## network object.
## The graph.data.frame function takes two data frames
## One for the EDGES (called links here)
## One for the NODES (called nodes here)
## For the EDGES col1 is source and col2 is the target
## for each direced edge 
## For nodes (vertices) col1 is the ID, other cols are
## node attributes
#(links)
#(nodes)
## Create a network object called net 
net <- graph.data.frame(links,nodes,directed=T)
(net)

##IGrAPH outputs:
# DNW  for directed, named, weighted graph
## 17  49  for num nodes and edges
##Access to nodes, edges, and attributes
#The edges and vertices of the net object
E(net)
V(net)
E(net)$type
#Vertex median attribute
V(net)$media 
V(net)$media.type

##Accessing the network as a matrix
net[1,]
net[2,3]
#TO see the matrix
net[,]

##What happens if we plot net?
plot(net)
##It does plot a network, but the labels and look
##are not what we want...

## Make it pretty:
## Remove the self-loops
net <- simplify(net,remove.multiple=F, remove.loops=T)
plot(net)


#######    Making it Pretty   ################
#############################################
##Reduce arrow size an remove labels
plot(net, edge.arrow.size=.3, vertex.label=NA)

##Adding fonts and colors
##install.packages("extrafont")
##install.packages("RColorBrewer")
##install.packages("grDevices")
library(extrafont)
library(RColorBrewer)
library(grDevices)

##Examples from above packages
##pch is point symbol shape
## cex is point size
## col is color
plot(x=1:5, y=rep(5,5), pch=19, cex=12, col=rgb(.25,.5,.3,alpha=.5), xlim=c(0,6))

palette1 <- heat.colors(5,alpha=1)
palette2 <- rainbow(5,alpha=.5)
plot(x=1:10, y=1:10, pch=19, cex=5, col=palette2)
plot(x=1:10, y=1:10, pch=19, cex=5, col=palette1)

palette3 <- brewer.pal(10,"Blues")
plot(x=10:1, y=10:1, pch=19, cex=4, col=palette3)

plot(net, vertex.size=30, vertex.label.family="Arial Black")

##########

## Plotting Networks : Parameters of the Plot
## Example: Node have color, shape, size, label, etc.
## Edges have color, width, size, etc...

##Examples....
## 1)
plot(net,edge.arrow.size=.4, edge.curved=.1)

## 2)
plot(net,edge.arrow.size=.2, edge.color="orange", vertex.size=30,
     vertex.color="orange", vertex.frame.color="#ffffff",
     vertex.label=V(net)$media, vertex.label.color="black")

##Generate colors based on media type
colrs <- c("light blue", "tomato", "gold")
V(net)$color <- colrs[V(net)$media.type]
(V(net)$color)

## Use node degree to set node size
##(degree.distribution(net))
##NOTE!! Could not get degree to work without
## calling igraph::degree explicitly and degree is in + out
deg<-igraph::degree(net)
(deg)
V(net)$size <-deg*3
E(net)$arrow.size <- .2
E(net)$edge.color <- "gray80"
E(net)$width <- 1 +E(net)$weight/12
plot(net,edge.arrow.size=.2, vertex.frame.color="#ffffff",vertex.label=V(net)$media, vertex.label.color="black")

##Adding a legend
legend(x=-1.5, y=-1.1, c("Newspaper","TV", "Online"),
       pch=21,col="#777777", pt.bg=colrs,pt.cex=2,cex=.8, bty="n",
       ncol=1)

##plotting without nodes
plot(net,vertex.shape="none", vertex.label=V(net)$media,
     vertex.label.font=2, vertex.label.color="gray40",
     vertex.label.cex=.6,edge.color="blue")

##Color the edges by the node they exit
##Get the starting node using igraph get.edges
##Here again, I needed to explicitly use
##igraph::get.edges
edge.start <- igraph::get.edges(net,1:ecount(net))[,1]
(edge.start)
edge.col <- V(net)$color[edge.start]
plot(net,edge.color=edge.col, edge.curved=.2,
     vertex.label=V(net)$media,vertex.label.cex=.5)

#####Network Layouts#######
##Network layouts are algorithsm that return coordinates
##for each node in the network.
##barabasi.game is a function that generates
##a simple graph starting from one node adding
##more nodes/links based on "level of preference 
## for attachment" between the nodes. 
net.bg <- barabasi.game(40)
(net.bg)
V(net.bg)
E(net.bg)
V(net.bg)$frame.color <- "white"
V(net.bg)$color <-"orange"
V(net.bg)$label <-""
##vertex size
V(net.bg)$size <-14
E(net.bg)$arrow.mode <-5
##random layout
#plot(net.bg, layout=layout.random)
par(mfrow=c(2,3), mar=c(.5,.5,.5,.5,.5,.5))
##layout options
lay1 <- layout.circle(net.bg)
lay2 <- layout.sphere(net.bg)
lay3 <- layout.star(net.bg)

plot(net.bg, layout=lay1, main="Circle Layout")
plot(net.bg, layout=lay2, main=" SphereLayout")
plot(net.bg, layout=lay3, main="Star Layout")

##fruchterman-reingold layout
##nodes are "electrically charged and so repulse
##each other to create a balanced network
lay4 <- layout.fruchterman.reingold(net.bg)
## kamada.kawai layout is also a force
##directed algorithm.
lay5 <- layout.kamada.kawai(net.bg)
lay6 <- layout.spring(net.bg, mass=.5)
##plot two figures with 1 row and 3 cols
##par(mfrow=c(1,3), mar=c(0,0,0,0))
plot(net.bg, layout=lay4, main="Fruchterman-Reingold")
plot(net.bg,layout=lay5, main="Kamada-Kawai Layout")
plot(net.bg,layout=lay6, main="Spring Layout")

##Manual rescaling and normalization
lay7 <- layout.fruchterman.reingold(net.bg)
#lay7 <- layout.circle(net.bg)
lay8 <- layout.norm(lay7, ymin=1, ymax=-1, xmax=1)
par(mfrow=c(1,2), mar=c(0,0,0,0))
plot(net.bg, rescale=F, layout=lay7, main="fruchterman.reingold")
plot(net.bg, rescale=F, layout=lay7*.5, main="rescaled by .5")
par(mfrow=c(1,2), mar=c(0,0,0,0))
plot(net.bg, rescale=F, layout=lay8, main="normalized and not rescaled")
plot(net.bg, rescale=F, layout=lay8 *.5, main="normalized and rescaled by .5")


#######Comparing layouts###########
##The layout used by igraph is layout.auto
##which automatically selects an algorithm based on 
##properties.
##Look for all layoutsin igraphs
layouts <- grep("^layout\\.", ls("package:igraph"), value=TRUE)
##Remove some layouts
layouts <- layouts[!grepl("bipartite|merge|norm|sugiyama|spring", layouts)]
par(mfrow=c(3,3), mar=c(.5,0,.5,0))
for (layout in layouts){
  print(layout)
  layholder <- do.call(layout, list(net))
  plot(net,edge.arrow.mode=0,layout=layholder,main=layout)
}


#####Highlighting Aspects of a network#######
h<-hist(links$weight)
m<-mean(links$weight)
s<-sd(links$weight)

##Edges can be removed with delete.edges
threshold <- m
net.sp <- igraph::delete.edges(net,E(net)[weight<threshold])
lay9 <- layout.fruchterman.reingold(net.sp)
plot(net.sp,layout=lay9)

##Color edges by type
E(net)$width <-1.5
plot(net,edge.color=c("dark red", "gray")[(E(net)$type=="hyperlink")+1], 
     vertex.color="gray40", layout=layout.circle)


##Other ways to delete edges
net.m <-net - E(net)[E(net)$type=="hyperlink"]
net.h <-net - E(net)[E(net)$type=="mention"]
par(mfrow=c(1,2))
plot(net.h, vertex.color="orange", main="Tie: Hyperlink")
plot(net.m, vertex.color="blue", main="Tie: Mention")


###SHowing COMMUNITIES in networks #############
V(net)$community <- optimal.community(net)$membership
colrs <- adjustcolor(c("gray50", "tomato", "gold", "yellowgreen"), alpha=.6)
plot(net,vertex.color=colrs[V(net)$community])

## Highlighting nodes or links
dist.from.NYT <- shortest.paths(net,algorithm = "unweighted")[1,]
oranges <- colorRampPalette(c("dark red", 'gold'))
col <- oranges(max(dist.from.NYT)+1)[dist.from.NYT+1]
plot(net,vertex.color=col, vertex.label=dist.from.NYT, 
     edge.arrow.size=.6, vertex.label.color="white")


##Using for/in loops
#RE:http://estebanmoro.org/2012/11/
## temporal-networks-with-igraph-and-r-with-20-lines-of-code/
par(mfrow=c(2,2),mar=c(0,0,0,0), oma=c(0,0,0,0))
g = watts.strogatz.game(1,20,3,0.4)
for(i in 1:4) plot(g,layout=layout.fruchterman.reingold,margin=0)


##Neighbors
##The neighbors function finds all nodes one step out from the 
##focal.
##The function, incident, finds all edges for a node

col <- rep("grey40", vcount(net)) #repeat grey forall nodes
#(col)
#change node color from gray for those with WSJ
col[V(net)$media=="Wall Street Journal"] <- "#ff5100"
neigh.nodes <- neighbors(net,V(net)[media=="Wall Street Journal"], mode="out")
col[neigh.nodes]<-"#ff9d00"
plot(net,vertex.color=col)

##Marking groups of nodes
plot(net,mark.groups=c(1,4,5,8), mark.col="light blue",
     mark.border=NA)

##Mark multiple groups
plot(net,mark.groups = list(c(1,2,3), c(7:9)), 
     mark.col=c("light blue", "light green"), 
     mark.border = NA)

##Highlight a path in the graph
news.path <- get.shortest.paths(net,V(net)[media=="MSNBC"],
            V(net)[media=="New York Post"], mode="all",
            output="both")

ecol <- rep("gray80", ecount(net))
ecol[unlist(news.path$epath)] <- "orange"

ew <-rep(2,ecount(net))
ew[unlist(news.path$epath)] <-5

vcol <-rep("gray40", vcount(net))
vcol[unlist(news.path$vpath)] <- "gold"

plot(net,vertex.color=vcol, edge.color=ecol,
     edge.width=ew, edge.arrow.mode=0)


###########################################
######Interactive Plotting With tkplot

#R and igraph allow for interactive plotting of networks

#tkid is the id of the tkplot that will open
tkid <- tkplot(net)
#get coords from tkplot
lay10 <- tkplot.getcoords(tkid) 
plot(net,lay10)

##############

##Random Graphs and measures and review of concepts
G <- erdos.renyi.game(20,.2)
plot(G)
diameter((G))
average.path.length(G)
##The vertices and edges
V(G)
E(G)
get.edgelist(G)
#adj matrix
get.adjacency(G)

################################
##Other Network Types

###Heatmaps
netm <- get.adjacency(net,attr="weight", sparse=F)
colnames(netm) <- V(net)$media
rownames(netm) <- V(net)$media

palf <- colorRampPalette(c("gold", "dark orange"))
heatmap(netm[,17:1], Rowv=NA, Colv=NA, col=palf(100),
        scale="none", margins=c(10,10))


#############Using your own dataset to create a network##

##Reminder of R Matrices
##Make a small matrix with rbind
MAT <- rbind(c(0,1,0), c(1,0,1), c(1,0,0))
Names <- c("A", "B", "C")
##To get the same labels for rows and cols if you wish
dimnames(MAT) <- list(Names,Names)
(MAT)

##Matrix multiplication
(MAT %*% MAT)

##Building a matrix that represents EDGES (and Adj matrix)
EdgeList <- rbind(c("A", "B"), c("B", "C"), c("C", "A"))
#Above we define these edges: A -- B, B--C, C--A
#Direction assumed
(EdgeList)

##Recall that igraph is a datastructure for storing networks (graphs)
#Simple Example, where "++" is both directions and "-+" is directed
MyG <- graph_from_literal(A++B, B-+C, C-+A)
V(MyG)$size <- 35
V(MyG)$color <- "light blue"
plot(MyG)

##Three options for igraph objects
EdgeList <- rbind(c("A", "B"), c("B", "C"), c("C", "A"))
MAT <- rbind(c(0,1,0), c(1,0,1), c(1,0,0))
G_edges <- graph_from_edgelist(EdgeList)
New_df <-as.data.frame(EdgeList)
G_df <- graph_from_data_frame(New_df, directed=T)
G_adjMAT <- graph_from_adjacency_matrix(MAT)
par(mfrow=c(2,2), mar=c(0,0,0,0))
plot(G_edges)
plot(G_df)
plot(G_adjMAT)

##Making Trees and Full graphs and other layouts
#Binary tree with 20 nodes and 2 children each
par(mfrow=c(3,3), mar=c(0,0,0,0))
Tree_G <- make_tree(20, children=2)
Full_G <- make_full_graph(n=5)
Lattice_G <- make_lattice(dimvector=c(4,3),circular = F)
Star_G <- make_star(n=15, mode="undirected")
plot(Tree_G)
plot(Full_G)
plot(Lattice_G)
plot(Star_G)

###############Networks and DataFrames
## In many cases, data can be read into R as a df
## There are many options for reading data into networks

##Example 1: Edge Lists and DataFrames
#https://cran.r-project.org/web/packages/igraphdata/igraphdata.pdf
##install.packages("igraphdata")
library(igraphdata)
AirPortData <- data("USairports")
(USairports)
##Attributes: attr: name (g/c), name (v/c), City (v/c), Position (v/c), Carrier (e/c),
## Departures (e/n), Seats (e/n), Passengers (e/n), Aircraft (e/n), Distance (e/n)
(V(USairports))
(E(USairports))
(head(V(USairports)$City))
(head(V(USairports)$Position))
(head(E(USairports)$Aircraft))
(head(E(USairports)$Distance))
(vertex_attr_names(USairports))
#(vertex_attr(USairports,"City"))
(edge_attr_names(USairports))
#(edge_attr(USairports,"Carrier"))
V(USairports)$size=10
(V(USairports)[["DCA"]]) #attributes of DCA
(V(USairports)[1:10]$City)
(unique(E(USairports)["DCA" %->% "BOS"]$Carrier))
DCA_edges<-unique(E(USairports)["DCA" %->% "BOS"]$Carrier)


###Pretend Dataset from Ami #####################################################
##These are from a dataset that I invented. 
nodes3 <- read.csv("NetworkWorkersExample-NODES.csv", header=T, as.is=T)
links3 <- read.csv("NetworkWorkersExample-EDGES.csv", header=T, as.is=T)
##Examine the data
(nodes3)
(head(nodes3))
(head(links3[,1]))
(nrow(nodes3))
(nrow(links3))
(length(unique(nodes3$id)))
(nrow(unique(links3[,c("from", "to")])))
#Make and plot the network
Workers_net <- graph.data.frame(links3,nodes3,directed=T)
(V(Workers_net)$Degree)
(E(Workers_net)$years_on_team)
(E(Workers_net)$to)
plot(Workers_net)


###########NetworkD3###########
##install.packages("networkD3")
# Load package
library(networkD3)
#D3Net <- data.frame(source, target)
Workers_net_D3 <- data.frame(links3[,1],links3[,2])
(mode(Workers_net_D3)) 
simpleNetwork(Workers_net_D3)
###Put it online
# See: http://drgates.georgetown.domains/NetTest1.html
##install.packages("magrittr")
library(magrittr)
simpleNetwork(Workers_net_D3) %>%
  saveNetwork(file = 'NetTest1.html')



