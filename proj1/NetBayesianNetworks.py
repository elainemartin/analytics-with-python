import json
from numpy import array, append, shape, expand_dims, tile, swapaxes, repeat, multiply, sum

class Net:
     nodeList = []

     def __init__(self, name, nodeList):
            self.name = name
            self.nodeList = nodeList
            print  '---------- Network created: ', name , '----------'

     def displayNetName(self):
            print "Name : ", self.name

     def addNode(self, nodeName, states, cpt, parents):
        print  '---------- Adding new node ----------'
        self.nodeList.append(Node(nodeName, states, cpt, parents))
        print  '---------- Added new node with node name: ', nodeName


     def displayNet(self):
             print self.name

     def jdefault(self,o):
                return o.__dict__

     def getNode(self,inputName):
             print  '---------- Obtaining node:  ----------', inputName
             for node in self.nodeList:
                 if inputName == node.nodeName:
                     print "Node found: ", node.nodeName
                     return node

     def saveJSON(self, filePath):
         print  '---------- Saving JSON to file:  ----------', filePath
         with open(filePath, 'w') as f:
               json.dump(self, f, default=net.jdefault, indent = 4, sort_keys=True)
         print  '---------- JSON object saved successfully at:  ----------', filePath

     def loadJSON(self,filePath):
         print  '---------- Loading JSON from file:  ----------', filePath
         with open(filePath) as json_file:
              json_data = json.load(json_file)
              netName = json_data["name"]
              nodeListJSON = json_data["nodeList"]
              nodeListTemp = []
              nodeList1 = []
              for node in nodeListJSON:
                  nodeListTemp.append(node)
              for value in nodeListTemp:
                 nodeList1.append(Node(value["nodeName"], value["states"], value["cpt"], value["parents"]))
              net1 = Net(netName, nodeList1)
              return net1
         print  '---------- Network object created successfully at:  ----------'

     def postJSON(self):
         for node in self.nodeList:
            node.potential = array(node.cpt)
            node.dimension = array(node.cpt).shape
            node.tmpPot = None
            node.evidenceIndex = -2 #no evidence
         print  '---------- Post JSON processing completed  ----------'

class Node():
    'Common base class for all nodes'

    def __init__(self, nodeName, states, prob, parents=None):
        self.nodeName = nodeName
        self.states = states
        self.parents = parents
        self.cpt = prob



    def setChildPotential(self,net,parentWithEvidence):
        variables = sorted(net.nodeList,key=lambda x: x.nodeName)
        remDimension = -2
        for var in variables:
            if var.parents is not None:
                for parent in var.parents:
                    if parent == variables[parentWithEvidence].nodeName:
                        remDimension = var.parents.index(parent)
                if remDimension == 0:
                    var.potential = array([row[variables[parentWithEvidence].evidenceIndex] for row in var.potential])
                elif remDimension == 1:
                    var.potential = var.potential[variables[parentWithEvidence].evidenceIndex]
                #print remDimension
                #print var.potential
                var.dimension = var.potential.shape

    def setEvidence(self,stateName,net):
        for state in self.states:
            if state == stateName:
                self.evidenceIndex = self.states.index(state)
                if self.parents is None:
                    #set own potential
                    self.potential = self.potential[self.evidenceIndex]
                    self.dimension = tuple([1,])
                    #set child's potential
                    self.setChildPotential(net,sorted(net.nodeList,key=lambda x: x.nodeName).index(self))

                else:
                    numrows = self.dimension[0]
                    for d in range(1,len(self.dimension)-1):
                        numrows = numrows*self.dimension[d]
                    temparray = self.potential.reshape(numrows,self.dimension[-1])
                    potentialarray = array([row[self.evidenceIndex] for row in temparray])
                    self.potential = potentialarray.reshape(self.dimension[0:-1])
                print  '---------- Evidence set for   ----------', stateName

    def clearEvidence(self,net):
        self.potential = array(self.cpt)
        self.dimension = self.potential.shape
        self.evidenceIndex = -2
        if self.parents is not None:
            parentWithEvidence = self.parentHasEvidence(self.parents,net)
            if parentWithEvidence != -2:
                self.setChildPotential(net,parentWithEvidence)


    def getBelief(self, net):
        variables = sorted(net.nodeList,key=lambda x: x.nodeName)
        jd = 1
        sumout = range(0,len(net.nodeList))
        for var in variables:

            dimlist = []

            if var.parents is None: # add all dimensions except self
                for i in range(0,len(net.nodeList)):
                    if var == variables[i]:
                        dimlist.append(1)
                        if i==0:
                            var.tmpPot = var.potential
                    else:
                        if i==0:
                            var.tmpPot = expand_dims(var.potential,axis=i)
                        else:
                            var.tmpPot = expand_dims(var.tmpPot,axis=i)
                        dimlist.append(variables[i].dimension[-1])

            else: # add self, skip existing
                names = []
                names = var.parents
                dimNames = reversed(names)
                parentEvidence = self.parentHasEvidence(names,net)
                #print parentEvidence
                dimlist = repeat(1, len(net.nodeList)).tolist()
                if sorted(dimNames) is not dimNames and parentEvidence == -2:
                    var.tmpPot = swapaxes(var.potential,0,1) # only handles 2 axes - what if more than 2 parents?
                    var.tmpPot = expand_dims(var.tmpPot, axis=variables.index(var))
                    dimlist[variables.index(var)] = var.dimension[-1]
                else:
                    if var.evidenceIndex != -2:
                        for i in range(0,len(net.nodeList)-1):
                            if i == 0:
                                var.tmpPot = expand_dims(var.potential, axis=variables.index(var))
                            else:
                                var.tmpPot = expand_dims(var.tmpPot, axis=variables.index(var))
                        dimlist[variables.index(var)] = var.dimension[-1]
                    else:
                        var.tmpPot = expand_dims(var.potential, axis=parentEvidence)
                        dimlist[parentEvidence] = variables[parentEvidence].dimension[-1]
                    #print var.tmpPot.shape

            print '---------- Printing Dimension List for ',var.nodeName,': ', dimlist

            var.tmpPot = tile(var.tmpPot,dimlist) #replicate
            #print var.tmpPot

            jd = multiply(jd, var.tmpPot)

            if var.nodeName == self.nodeName:
                del(sumout[variables.index(var)])

        unnormalizedTmp = sum(jd,axis=(tuple(sumout)))
        return unnormalizedTmp/sum(unnormalizedTmp)

    def parentHasEvidence(self,names,net):
        variables = sorted(net.nodeList,key=lambda x: x.nodeName)
        for name in names:
            for v in variables:
                if name == v.nodeName:
                    if v.evidenceIndex != -2:
                        return variables.index(v)
        return -2

'''
Below input code can be used to test the library:

nodeListInitializer = []
net = Net("Sample net",nodeListInitializer)
A = net.addNode('A',['a1','a2'],[0.9,0.1],None)
C = net.addNode('C',['c1','c2','c3','c4'],[0.1,0.2,0.3,0.4],None)
probB = [
                     [ [0.2,0.4,0.4] , [0.33,0.33,0.34 ] ] ,
                     [ [0.1,0.5,0.4] , [0.3,0.1,0.6 ] ] ,
                     [ [0.01,0.01,0.98] , [0.2,0.7,0.1 ] ] ,
                     [ [0.2,0.1,0.7] , [0.9,0.05,0.05 ] ]
                 ]
B = net.addNode('B',['b1','b2','b3'], probB,['A','C'])


filePath = 'C:/Users/shrilata/Dropbox/MSiA/Spring 2014/Python/test.json'
net.saveJSON(filePath)
newNet = net.loadJSON(filePath)
newNet.postJSON()
B2 = newNet.getNode("B")
B2.setEvidence('b3',newNet)

A2 = newNet.getNode("A")

aAfterSettingB = A2.getBelief(newNet);
print("P(A|B=b3) =",aAfterSettingB)

C2 = newNet.getNode("C")
C2.setEvidence('c4',newNet)
aAfterSettingBC = A2.getBelief(newNet);
print("P(A|B=b3,C=c4) =",aAfterSettingBC)

B2.clearEvidence(newNet)
aAfterSettingC = A2.getBelief(newNet);
print("P(A|C=c4) =",aAfterSettingC)

'''







