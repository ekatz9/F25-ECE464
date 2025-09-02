

# read input file
with open('input.txt','r') as file:
    program = file.read()
    lines = program.split('\n')
    # test that program is reading file correctly
    # for line in lines:
    #     print(line)

# categorize inputs & outputs & gates
    inputs = []
    outputs = []
    gates = []

    # parse each line into
    # 'nodeOut' = 'nType'('nodeIn')
    for line in lines:

        # find delimiter indices
        equal = line.find('=')
        open = line.find('(')
        close = line.find(')')
        print(line)
        # print(f'{line} -> {equal},{open},{close}')
        
        nodeOut = line[0:equal].strip()
        nodeIn = line[open+1:close].strip()

        if equal > 1:
            nType = line[equal+1:open]
            # node is a logic gate
            print(f'{nodeOut} is an {nType} Gate')
        else:
            nType = line[0:open].strip()
            if nType == 'INPUT':
                #node is an input
                print(f'{nodeIn} is an input')
            if nType == 'OUTPUT':
                #node is an output
                print(f'{nodeIn} is an output')

    for gate in gates:
        print(gate)

    # Barbaric input sensing
    #for line in lines:
    #    if line[0:5] == 'INPUT':
    #        print(f'input {line[6]} detected')
    #    if line[0:6] == 'OUTPUT':
    #        print(f'output {line[7]} detected')

