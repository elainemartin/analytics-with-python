from numpy import array, append, shape, zeros
from collections import OrderedDict

def calculate(subscripts, *operands):
    inputoutput = subscripts.split('->')
    inputs = inputoutput[0].split(',')

    mapper = OrderedDict()
    for index, operand in enumerate(operands):
        dim = operand.shape
        for i in inputs[index]:
            mapper[i] = dim[inputs[index].index(i)]
            
    dimlist = ''.join(mapper.keys())
    combos = combo(mapper.values())

    if len(inputoutput)==1 or (len(inputs)==1 and len(inputoutput)==1):
        out = 0
    else:
        out = zeros(shape=([mapper[i] for i in inputoutput[1]]))

    for c in combos:
        multiplied = 1
        for index, operand in enumerate(operands):
            multiplied  *= operand[tuple(c[dimlist.index(i)] for i in inputs[index])]
        if len(inputoutput)==1 or (len(inputs)==1 and len(inputoutput)==1):
            out += multiplied
        else:
            out[tuple(c[dimlist.index(i)] for i in inputoutput[1])] += multiplied
        
    return out

def combo(n):
    r = [0]*len(n)
    while True: #
        yield tuple(r)
        p=len(r)-1
        r[p]+=1
        while r[p]==n[p]:
            r[p]=0
            p-=1
            if p == -1:
                return
            r[p]+=1
