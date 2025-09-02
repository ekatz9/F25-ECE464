

# read input file
with open('input.txt','r') as file:
    program = file.read()
    lines = program.split('\n')
    # test that program is reading file correctly
    # for line in lines:
    #     print(line)

    # Data structures for output
    inputs = []
    outputs = []
    gates = []

    for line in lines:

        # consider each input line conforms to the format
        # 'nodeOut' = 'nType'('nodeIn')

        # find delimiter indices
        equal = line.find('=')
        open = line.find('(')
        close = line.find(')')
        
        # DEBUG: print line from input as reference
        print(line)

        # DEBUG: check delimiter indices
        # print(f'{line} -> {equal},{open},{close}')
        
        # Find appropriate Substrings
        nodeOut = line[0:equal].strip()
        nodeIn = line[open+1:close].strip()

        # input/output declarations do not include '='
        # find() returns -1 if character not found
        if equal > 0:
            nType = line[equal+1:open].strip()
            # node is a logic gate
            print(f'{nodeOut} is an {nType} Gate')
            # TODO: add to data structure
        
        else:
            nType = line[0:open].strip()
            if nType == 'INPUT':
                #node is an input
                print(f'{nodeIn} is an input')
                # TODO: add to data structure

            if nType == 'OUTPUT':
                #node is an output
                print(f'{nodeIn} is an output')
                # TODO: add to data structure

    # TODO: format output

    # Barbaric input sensing
    #for line in lines:
    #    if line[0:5] == 'INPUT':
    #        print(f'input {line[6]} detected')
    #    if line[0:6] == 'OUTPUT':
    #        print(f'output {line[7]} detected')

