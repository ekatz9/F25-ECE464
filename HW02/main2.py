import os

print('\nF25 ECE 464 Project 01 \nCircuit & Faults')
print('\nMazin Al-Attrash & Eli Katz')
print(f'{'':-<37}\n')

NodeCounter = 0

#Class Node defines a Node in a Circuit
class node:
    def __init__(self, name, type, gate, nodesIn):
        self.id = NodeCounter
        global NodeCounter += 1
        self.name = name
        self.type = type
        self.gate = gate
        self.value = 'x'
        self.nodesIn = nodesIn
    
    def __str__(self):
        return self.value

# Choose input files
fileList = []
for file in os.listdir(os.getcwd()):
    if file.endswith('.bench'):
        fileList.append(file)

print('Choose Input File:')
for i in range(0,len(fileList)):
    print(f'   ({i}) {fileList[i]}')

fileInd = int(input('\nfile #: '))
while fileInd >= len(fileList) or fileInd < 0:
    fileInd = int(input('   invalid file index, try again: '))
print(f'   Opening {fileList[fileInd]}')

#Node data structures
cInputs = []
cOutputs = []
circuit = {}

#Read Input File
with open(fileList[fileInd],'r') as file:
    program = file.read()
    lines = program.split('\n')

    #Populate Circ
    for line in lines:
        
        # consider each input line conforms to the format
        # 'nodeOut' = 'nType'('nodeIn')

        # find delimiter indices
        equal = line.find('=')
        open = line.find('(')
        close = line.find(')')

        # Find appropriate Substrings
        nodeOut = line[0:equal].strip()
        nodeIn = line[open+1:close].strip()

        # input/output declarations do not include '='
        # find() returns -1 if character not found
        if equal > 0:
            # node is a logic gate
            nType = line[equal+1:open].strip()

            # Python silliness to strip inputs for circ[]
            inputs = [t.strip() for t in nodeIn.split(',')]
            
            # update circuit{}
            if nodeOut in circuit:
                circuit[nodeOut].gate = nType
                circuit[nodeOut].nodesIn = inputs
            else:
                circuit[nodeOut] = node(nodeOut, '', nType, inputs)
        
        else:
            nType = line[0:open].strip()
            if nType == 'INPUT':
                #node is an input
                cInputs.append(nodeIn)

                #update circuit{}
                if nodeIn in circuit:
                    circuit[nodeIn].type = nType
                else:
                    circuit[nodeIn] = node(nodeIn,'INPUT','','')

            if nType == 'OUTPUT':
                #node is an output
                cOutputs.append(nodeIn)

                #update circuit{}
                if nodeIn in circuit:
                    circuit[nodeIn].type = nType
                else:
                    circuit[nodeIn] = node(nodeIn,'OUTPUT','','')

###############
# Print Circuit
printList = sorted(circuit, key = lambda node:node.id)
print(f'||{'id':=^5}||{'name':=^7}||{'type':=^10}||{'gate':=^7}||{'nodes in':=^15}||')
for item in printList:
    instring = ''
    for nin in item.nodesIn:
        instring += nin + ', '
    print(f'||{item.id:=^5}||{item.name:=^7}||{item.type:=^10}||{item.gate:=^7}||{instring[0:-2]:=^15}||')

                
                