import os

#class loc defines a loaction in the circuit
class loc:
    def __init__(self,output,type,input):
        self.output = output
        self.gate = type
        self.input = input
    
    def __str__(self):
        return self.output

# Choose input files
fileList = []
for file in os.listdir(os.getcwd()):
    if file.endswith('.bench'):
        fileList.append(file)

print('\nF25 ECE 464 Project 01 \nCircuit & Faults')
print('\nMazin Al-Attrash & Eli Katz\n')

print('Choose Input File:')
for i in range(0,len(fileList)):
    print(f'   ({i}) {fileList[i]}')

fileInd = int(input('\nfile #: '))
print(f'Opening {fileList[fileInd]}')

#Circuit Representation
inputs = []
outputs = []
circ = []

# Read Input File
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
            circ.append(loc(nodeOut,nType,inputs))
        
        else:
            nType = line[0:open].strip()
            if nType == 'INPUT':
                #node is an input
                inputs.append(line[open+1:close].strip())
                circ.append(loc(nodeIn.strip(),'INPUT',''))

            if nType == 'OUTPUT':
                #node is an output
                outputs.append(line[open+1:close].strip())
                #HW02 circuit representation
                elem = (loc(nodeIn.strip(),'OUTPUT',nodeIn.strip()))
                circ.append(elem)

#test circuit representation
print(f'\n{'label':^10}|{'type':^10}|{'inputs':^15}')
print(f'{'':-<37}')
for input in inputs:
    print(f'\n{input:^10}|{'INPUT':^10}|{'':^15}')
for elem in circ:
    if (elem.gate != 'INPUT' or elem.gate != 'OUTPUT'):
        print(f'\n{elem.output:^10}|{elem.gate:^10}|{elem.input:^15}')
for output in outputs:
    print(f'\n{output:^10}|{'OUTPUT':^10}|{output:^15}')
