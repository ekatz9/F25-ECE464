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
        self.fault = ''
        self.nodesIn = nodesIn

    def __str__(self):
        return self.value
    
class fault:
    def __init__(self, id, name, type,):
        self.id = id
        self.name = name,
        self.type = type
        self.detected = False

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
    if fileInd == -1:
        print('   Program quit')
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
        openbr = line.find('(')
        close = line.find(')')

        # Find appropriate Substrings
        nodeOut = line[0:equal].strip()
        nodeIn = line[openbr+1:close].strip()

        # input/output declarations do not include '='
        # find() returns -1 if character not found
        if equal > 0:
            # node is a logic gate
            nType = line[equal+1:openbr].strip()

            # Python silliness to strip inputs for circ[]
            inputs = [t.strip() for t in nodeIn.split(',')]
            
            # update circuit{}
            if nodeOut in circuit:
                circuit[nodeOut].gate = nType
                circuit[nodeOut].nodesIn = inputs
            else:
                circuit[nodeOut] = node(nodeOut, '', nType, inputs)
        
        else:
            nType = line[0:openbr].strip()
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

faultlist = []
print('\n1) Full Fault List')
input('   press enter to continue')
#TODO: populate full fault list
faultcounter = 0
printList = sorted(circuit.items(), key = lambda item: item[1].name)
print(f'\n||{' count ':=^10}||{' location ':=^10}||{' fault ':=^10}')
for listing in printList:
    faults = f'{listing[1].name}-SA0, {listing[1].name}-SA1'
    
    faultlist.append(fault(listing[1].name,listing[1].name,'SA0'))
    faultlist.append(fault(listing[1].name,listing[1].name,'SA1'))

    faultcounter += 2
    carriage = 3
    for faultType in {'SA0', 'SA1'}:
        for ninput in listing[1].nodesIn:
            if carriage % 7 == 0:
                faults += f'\n||{faultcounter:^10}||{'':^10}||'
                carriage = 1
            faults += f', {listing[1].name}-{ninput}-{faultType}'
            #print(f'{listing[1].name} has input {ninput}')
            faultlist.append(fault(listing[1].name,ninput,faultType))

            faultcounter += 1
            carriage += 1
    print(f'||{faultcounter:^10}||{listing[1].name:^10}||{faults}')
print(f'{faultcounter} faults total')

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
    if(tvector == '-1'):
        print('   program quit')
        os._exit(0)
    tvector = input('      invalid test vector, try again: ')
    

# assign values for inputs
for i in range(len(cInputs)):
    # print(f'assigning {circuit[cInputs[i]].name} value {tvector[i]}')
    circuit[cInputs[i]].value = tvector[i]
print('')

#function getvalue
#   take as input Node elem
#   returns as output value of elem (x,0,1)
#   reads and writes to circuit
def getvalue(elem):

    # print(f'getting value for {elem.name}')

    # base case: elem already has a value
    if elem.value != '':
        # print(f'   {elem.name} has value {elem.value}')
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
        # print(f'   {elem} = !{currVal} = {elem.value}')
        return elem.value
    
    # get values of elem inputs
    inputVals = []
    # print(f'   inputs = {elem.nodesIn}')
    for elemInput in elem.nodesIn:
        inputVals.append(getvalue(circuit[elemInput]))
    # print(f'   inputVals = {inputVals}')

    # use ulogic lookup table
    currVal = inputVals[0]
    # print(f'   currVal = {currVal}')
    for i in range(1,len(inputVals)):
        #format for lookup table
        vals = sorted({currVal,inputVals[i]})
        # print(f'   vals = {vals}')
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
    # print(f'      {elem.name} = {elem.gate}({elem.nodesIn}) = {elem.gate}({inputVals}) = {elem.value}')
    return elem.value

#kickstart getvalue
for cOutput in cOutputs:
    getvalue(circuit[cOutput])
    
# Print Circuit Analysis
for coutput in cOutputs:
    print(f'output {coutput} = {circuit[coutput].value}')

# terminal buffer insufficient, print to output.txt
with open('output.txt','w') as z:
    printList = sorted(circuit.items(), key = lambda item: item[1].name)
    print(f'\n||{' id ':=^8}||{' name ':=^10}||{' value ':=^9}||')
    print(f'\n||{' id ':=^8}||{' name ':=^10}||{' value ':=^9}||', file = z)
    for listing in printList:
        print(f'||{listing[1].id:^8}||{listing[1].name:^10}||{listing[1].value:^9}||')
        print(f'||{listing[1].id:^8}||{listing[1].name:^10}||{listing[1].value:^9}||', file = z)

#####################
# 3) Fault Simulation

#function getvalue
#   take as input Node elem
#   returns as output value of elem (x,0,1)
#   reads and writes to circuit
def getfault(elem,cfault):

    #stupid fault stuff
    # base case: output fault
    # is fault at this gate
    if elem.name[0] == cfault.id:
        #is fault at outputf
        if cfault.id == cfault.name[0]:
            # return fault type
            if faultType == 'SA0':
                return '0'
            else:
                return '1'
            
    # base case: elem already has a value
    if elem.fault != '':
        # print(f'   {elem.name} has value {elem.fault}')
        return elem.fault
    
    # base case: elem has 1 input (NOT Gate)
    if elem.gate == 'NOT':
        currVal = circuit[elem.nodesIn[0]].fault
        if currVal == '0':
            elem.fault = '1'
        elif currVal == '1':
            elem.fault = '0'
        else:
            elem.fault = 'x'
        # print(f'   {elem} = !{currVal} = {elem.fault}')
        return elem.fault
    
    # get values of elem inputs
    inputVals = []
    # # print(f'   inputs = {elem.nodesIn}')
    for elemInput in elem.nodesIn:
        thisval = getfault(circuit[elemInput],cfault)
        # is fault at this gate
        if elem.name == cfault.id:
            # is fault at this input
            print(f'{elemInput} == {cfault.name[0]}')
            if elemInput == cfault.name[0]:
                print(f'ping! {cfault.id}-{cfault.name}-{cfault.type}')
                # what is fault type
                if cfault.type == 'SA0':
                    thisval = '0'
                else:
                    thisval = '1'
        inputVals.append(thisval)

    # print(f'   inputVals = {inputVals}')

    # use ulogic lookup table
    currVal = inputVals[0]
    # print(f'   currVal = {currVal}')
    for i in range(1,len(inputVals)):
        #format for lookup table
        vals = sorted({currVal,inputVals[i]})
        # # print(f'   vals = {vals}')
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
    elem.fault = currVal
    # print(f'      {elem.name} = {elem.gate}({elem.nodesIn}) = {elem.gate}({inputVals}) = {elem.fault}')
    return elem.fault

def clearfaults():
    for elem in circuit:
        circuit[elem].fault = ''

for cfault in faultlist:
    #assign starting values
    for i in range(len(cInputs)):
        circuit[cInputs[i]].fault = tvector[i]

    for coutput in cOutputs:
        print(f'{getfault(circuit[coutput],cfault)[0]}, expected {circuit[coutput].value}')
        if getfault(circuit[coutput],cfault)[0] != circuit[coutput].value:
            cfault.detected = True

    clearfaults()

for cfault in faultlist:
    if cfault.detected == True:
        print(f'{cfault.id}-{cfault.name[0]}-{cfault.type} = {cfault.detected}')
    

    
