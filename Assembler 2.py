registers={"R0":"000","R1":"001","R2":"010","R3":"011","R4":"100","R5":"101","R6":"110","FLAGS":"111"}

opcodes={"add":"00000","sub":"00001","mov":"00010","mov1":"00011",
         "ld":"00100","st":"00101","mul":"00110","div":"00111",
         "rs":"01000","ls":"01001","xor":"01010","or":"01011",
         "and":"01100","not":"01101","cmp":"01110","jmp":"01111",
         "jlt":"11100","jgt":"11101","je":"11111","hlt":"11010"}

oplist=list(opcodes.keys())
oplist.append("var")

def int_to_binary(num,size):
    b=format(num,"b")
    unused=size-len(b)
    b='0'*unused+b
    return b

counter=0
labels={}
variables={}

def assembly_to_binary(words_list,instruction_type):
    opcode=words_list[0]
    if opcode not in oplist:
        raise Exception("typo error")
    if opcode[0]=="j" and words_list[1] not in labels:
        raise Exception("jump error")

    return_str=""

    if instruction_type=="var":
        variables[opcode[0]]=int_to_binary(counter,7)

    elif instruction_type=="label":
        labels[opcode[0:-1]]=int_to_binary(counter,7)

#instructions
    if opcode!="var":
        return_str+=opcodes[opcode] 

    if instruction_type=="A":
        return_str+="00"#unused bits
        return_str+=registers[words_list[1]]+registers[words_list[2]]+registers[words_list[3]]
    
    elif instruction_type=="B":
        return_str+="0"#unused bits
        return_str+=registers[words_list[1]]+int_to_binary(int(words_list[2].replace("$","")),7)
    
    elif instruction_type=="C":
        return_str+="00000"#unused bits
        return_str+=registers[words_list[1]]+registers[words_list[2]]

    elif instruction_type=="D":
        return_str+="0"#unused bits
        return_str+=registers[words_list[1]]+variables[words_list[2]]

    elif instruction_type=="E":
        return_str+="0000"#unused bits
        return_str+=labels[words_list[1]]

    elif instruction_type=="F":
        return_str+="00000000000"#unused bits

    return return_str

file = open('stdin.txt', 'r')
s=file.read().split('\n')
ff= open('stdout.txt', 'w')
ns=list(filter(None, s))
if "hlt" not in ns:
    ff.write("ERROR: missing hlt instruction")
if ns[0][0:3]!="var":
    ff.write("ERROR: variables not declared at the beginning")
elif ns[-1][-3:]!="hlt":
    ff.write("ERROR: hlt not being used as the last instruction")
else:
    for j in ns:
        cmnd=list((j).split(' '))
        if cmnd[0] == (oplist[0 or 1 or 6 or 10 or 11 or 12]):
            type="A"
        elif cmnd[0] == (oplist[2 or 8 or 9]):
            type="B"
        elif cmnd[0] == (oplist[3 or 7 or 13 or 14]):
            type="C"
        elif cmnd[0] == (oplist[4 or 5]):
            type="D"
        elif cmnd[0] == (oplist[15 or 16 or 17 or 18]):
            type="E"
        elif cmnd[0] == (oplist[19]):
            type="F"
        ff.write(assembly_to_binary(cmnd,type))
        ff.write("\n")