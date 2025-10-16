import os


print('\nF25 ECE 464 Project 01 \nCircuit & Faults')
print('\nMazin Al-Attrash & Eli Katz')
print(f'{'':-<37}\n')

NodeCounter = 0

#Class Node defines a Node in a Circuit
class node:
    def __init__(self, name, type, gate, nodesIn):
        global NodeCounter
        self.id = NodeCounter
        NodeCounter += 1
        self.name = name
        self.type = type
        self.gate = gate
        self.value = ''
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
    if fileInd == 'q':
        os._exit(0)
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
printList = sorted(circuit.items(), key = lambda item: item[1].id)
print(f'\n||{' id ':=^8}||{' name ':=^10}||{' type ':=^10}||{' gate ':=^10}||{' nodes in ':=^15}||')
for listing in printList:
    instring = ''
    for nin in listing[1].nodesIn:
        instring += nin + ', '
    print(f'||{listing[1].id:^8}||{listing[1].name:^10}||{listing[1].type:^10}||{listing[1].gate:^10}||{instring[0:-2]:^15}||')

#################
#1) Fault Listing

# Fault List Data Structures
SA0list = {}
SA1list = {}
#TODO: populate full fault list

######################
#2) Circuit Simulation

# Hash Table for logic with undefined values
# key: Gate
# Value is array of outputs for inputs 00 01 0x 11 1x xx (ascii ascending order)
ulogictable = {
    'AND'   : ('0', '0', '0', '1', 'x', 'x'),
    'NAND'  : ('1', '1', 'x', '0', 'x', 'x'),
    'OR'    : ('0', '1', 'x', '1', '1', 'x'),
    'NOR'   : ('1', '0', 'x', '0', '0', 'x'),
    'XOR'   : ('0', '1', 'x', '0', 'x', 'x'),
    'XNOR'  : ('1', '0', 'x', '1', 'x', 'x')
}

# Get Input Vector
cInputs = sorted(cInputs)
cOutputs = sorted(cOutputs)

temp = ''
for cInput in cInputs:
    temp += cInput + ', '
print('\n2) Circuit Simulation')
print(f'   input test vector for inputs {temp}')
tvector = input('\n   test vector: ')
while(len(tvector) != len(cInputs)):
    tvector = input('      invalid test vector, try again: ')

# assign values for inputs
for i in range(len(cInputs)):
    print(f'assigning {circuit[cInputs[i]].name} value {tvector[i]}')
    circuit[cInputs[i]].value = tvector[i]
print('')

#function getvalue
#   take as input Node elem
#   returns as output value of elem (x,0,1)
#   reads and writes to circuit
def getvalue(elem):

    print(f'getting value for {elem.name}')

    # base case: elem already has a value
    if elem.value != '':
        print(f'   {elem.name} has value {elem.value}')
        return elem.value
    
    # base case: elem has 1 input (NOT Gate)
    if elem.gate == 'NOT':
        currVal = circuit[elem.nodesIn[0]].value
        if currVal == '0':
            elem.value = '1'
        elif currVal == '1':
            elem.value = '0'
        else:
            elem.value = 'x'
        print(f'   {elem} = !{currVal} = {elem.value}')
        return elem.value
    
    # get values of elem inputs
    inputVals = []
    print(f'   inputs = {elem.nodesIn}')
    for elemInput in elem.nodesIn:
        inputVals.append(getvalue(circuit[elemInput]))
    print(f'   inputVals = {inputVals}')

    # use ulogic lookup table
    currVal = inputVals[0]
    print(f'   currVal = {currVal}')
    for i in range(1,len(inputVals)):
        #format for lookup table
        vals = sorted({currVal,inputVals[i]})
        print(f'   vals = {vals}')
        valstring = "".join(vals)
        match valstring:
            case '0':
                currVal = ulogictable[elem.gate][0]
            case '01':
                currVal = ulogictable[elem.gate][1]
            case '0x':
                currVal = ulogictable[elem.gate][2]
            case '1':
                currVal = ulogictable[elem.gate][3]
            case '1x':
                currVal = ulogictable[elem.gate][4]
            case 'x':
                currVal = ulogictable[elem.gate][5]
    elem.value = currVal
    print(f'      {elem.name} = {elem.gate}({elem.nodesIn}) = {elem.gate}({inputVals}) = {elem.value}')
    return elem.value

#kickstart getvalue
for cOutput in cOutputs:
    getvalue(circuit[cOutput])
    

#Debug - Print circuit values
for elem in circuit.items():
    print(f'{elem[1].name} = {elem[1].value}')
    

