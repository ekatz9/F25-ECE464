
# read input file

#TODO: create applet to choose input file

with open('hw1.txt','r') as file:
    program = file.read()
    lines = program.split('\n')
    # test that program is reading file correctly
    # for line in lines:
    #     print(line)

    # Data structures for output
    inputs = []
    outputs = []
    gates = []
    #HW02 data structure encoding a circuit representation
    circ = [] #array of tuples (nodeOut,nType,{list of inputs})

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
            nType = line[equal+1:open].strip()
            # node is a logic gate
            # Find how many inputs
            inputCount = 0
            for i in nodeIn:
                if i.isalpha():
                    inputCount += 1
            
            #format string to be "nodeOut InputCount GateType nodeIn"
            gate = nodeOut + ' ' + str(inputCount) + ' ' + nType + ' ' + nodeIn
            gates.append(gate)

            #HW02 circuit representation
            # Python silliness to strip inputs for circ[]
            temp = [t.strip() for t in nodeIn.split(',')]
            elem = (nodeOut,nType,temp)
            circ.append(elem)

        else:
            nType = line[0:open].strip()
            if nType == 'INPUT':
                #node is an input
                inputs.append(line[open+1:close].strip())
                #HW02 circuit representation
                elem = (nodeIn.strip(),'INPUT','')
                circ.append(elem)

            if nType == 'OUTPUT':
                #node is an output
                outputs.append(line[open+1:close].strip())
                #HW02 circuit representation
                elem = ('','OUTPUT',nodeIn.strip())
                circ.append(elem)

    # Print All Inputs
    print("\n           ==INPUT==")
    for i in inputs:
        print(f'           ||  {i}  ||')
    print("           =========\n")

    # Print All Outputs
    print("          ==OUTPUTS==")
    for i in outputs:
        print(f'          ||   {i}   ||')
    print("          ===========\n")

    # Print All Gates
    print("=============GATES==============")
    
    print("==OUT==# INPUT==TYPE=====IN=====")
    for i in gates:
        # Format Gate Data
        data = i.split()
        data[0] = data[0].center(3)
        data[1] = data[1] + "-Input"
        data[2] = data[2].center(4)

        # Combine All Inputs And Center
        index = 4
        s = len(data)
        while index < s:
            data[3] += data[index]
            index += 1
        data[3] = data[3].center(8)

        print(f'||{data[0]}||{data[1]}||{data[2]}||{data[3]}||')
    
    print("================================\n")

####################
# HW02

# create memoization structure (dictionary)
leveldict = {}
# initialize dictionary with lowest level elements (inputs)
for input in inputs:
    leveldict[input] = 0

#function getlevel
#   takes as input Node elem, typically a representation of a circuit element
#   returns as output an integer representation of the circuit level of elem
#   reads and writes to global memoization dictionary leveldict
#   fails for sequential circuits
def getlevel(elem):

    # base case: elem has already been assigned level
    if elem in leveldict:
        return leveldict[elem]

    # find inputs associated with elem
    elemInputs = []
    for c in circ:
        if c[0] == elem:
            elemInputs = c[2]
            break

    # recursively fill leveldict until level of desired element found
    leveldict[elem] = 0
    for input in elemInputs:
        leveldict[elem] = max(leveldict[elem],getlevel(input)+1)

    return leveldict[elem]

#kickstart getlevel for every highest level element (outputs)
maxlevel = 0
for output in outputs:
    maxlevel = max(maxlevel,getlevel(output))

#print(circ)
print(leveldict)
print(maxlevel)
