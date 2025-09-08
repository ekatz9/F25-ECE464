

# read input file
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
    circ = [] #HW02 array of tuples (nodeOut,nType,{list of inputs})

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
            elem = (nodeOut,nType,nodeIn.split(','))
            circ.append(elem)


        else:
            nType = line[0:open].strip()
            if nType == 'INPUT':
                #node is an input
                inputs.append(line[open+1:close].strip())
                elem = (nodeIn,'INPUT','u')
                circ.append(elem)

            if nType == 'OUTPUT':
                #node is an output
                outputs.append(line[open+1:close].strip())
                elem = ('u','OUTPUT',nodeIn)
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

# create memoization table
leveldict = {}
# initialize dictionary inputs
for input in inputs:
    leveldict[input] = 0

def getlevel(elem):
    
    # base case: elem has already been assigned level
    if elem in leveldict:
        return leveldict[elem]
    
    # recursively fill leveldict
    elemInputs = circ
    for input in :
        leveldict[elem] = max(leveldict[elem],getlevel(input)+1)
    return leveldict[elem]

#start recursive filling of library
maxlevel = 0
for output in outputs:
    maxlevel = max(maxlevel,getlevel(output))

print(leveldict)