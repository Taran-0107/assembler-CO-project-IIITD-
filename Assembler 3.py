registers={"R0":"000","R1":"001","R2":"010","R3":"011","R4":"100","R5":"101","R6":"110","FLAGS":"111"}

opcodes={"add":"00000","sub":"00001","mov$":"00010","mov":"00011",
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

def assembly_to_binary(words_list,instruction_type,counter):

    def check_reg(opcode,inst_type,*regslist):
        bool1=opcode=="mov" and inst_type=="C"
        for register in regslist:
            if register not in registers.keys():
                raise Exception("typo error")
            elif register=="FLAGS" and not  bool1:
                raise Exception("illegal use of flag")

    opcode=words_list[0]
    if opcode not in oplist:
        raise Exception("typo error")
    if opcode[0]=="j" and words_list[1] not in labels:
        raise Exception("jump error")

    return_str=""

    if instruction_type=="var":
        variables[words_list[1]]=int_to_binary(counter,7)
        return return_str

    elif instruction_type=="label":
        labels[opcode[0:-1]]=int_to_binary(counter,7)
        return return_str

#instructions
    if instruction_type=="B"and  words_list[2]=="mov":
        return_str+=opcodes["mov$"] 
    else:
        return_str+=opcodes[opcode] 

    if instruction_type=="A":
        r1=words_list[1]
        r2=words_list[2]
        r3=words_list[3]
        return_str+="00"#unused bits
        check_reg(opcode,instruction_type, r1,r2,r3)
        return_str+=registers[r1]+registers[r2]+registers[r3]
    
    elif instruction_type=="B":
        r1=words_list[1]
        numstr=(words_list[2].replace("$",""))
        if not numstr.isnumeric():
            raise Exception("typo error")
        num=int(numstr)
        if num>127 or num<0:
            raise Exception("illegal value")
        return_str+="0"#unused bitss
        check_reg(opcode,instruction_type, r1)
        return_str+=registers[r1]+int_to_binary(num,7)
    
    elif instruction_type=="C":
        r1=words_list[1]
        r2=words_list[2]
        return_str+="00000"#unused bits
        check_reg(opcode,instruction_type, r1,r2)
        return_str+=registers[r1]+registers[r2]

    elif instruction_type=="D":
        r1=words_list[1]
        var1=words_list[2]
        if var1 not in variables.keys():
            if var1 in labels.keys():
                raise Exception("variables and lables used interchangebly")
            else:
                raise Exception("invalid variable")
        return_str+="0"#unused bits
        check_reg(opcode,instruction_type, r1)
        return_str+=registers[r1]+variables[var1]

    elif instruction_type=="E":
        l1=words_list[1]
        if l1 not in labels.keys():
            if var1 in variables.keys():
                raise Exception("variables and lables used interchangebly")
            else:
                raise Exception("invalid label")
        return_str+="0000"#unused bits
        return_str+=labels[l1]

    elif instruction_type=="F":
        return_str+="00000000000"#unused bits

    return return_str

file = open('stdin.txt', 'r')
s=file.read().split('\n')
ff= open('stdout.txt', 'w')
ns=list(filter(None, s))
if "hlt" not in ns:
    ff.write("ERROR: missing hlt instruction")
elif ns[0][0:3]!="var":
    ff.write("ERROR: variables not declared at the beginning")
elif ns[-1][-3:]!="hlt":
    ff.write("ERROR: hlt not being used as the last instruction")
else:
    for j in ns:
        cmnd=list((j).split(' '))
        print(cmnd[0])
        if cmnd[0]=="var":
            #print("hello")
            type="var"
        elif(len(cmnd)==1):
            type="F"
        elif(len(cmnd)==2):
            type="E"
        elif(len(cmnd)==4):
            type="A"
        elif(len(cmnd)==3):
            if(cmnd[2][0]=="$"):
                type ="B"
            elif(len(cmnd[2])==(2 or 5) ):
                type="C"
#can't diffreneciate undefined variable from a typo, probably have to take input first and check for typo later
            elif(cmnd[2] in variables.keys()):
                type="D"
            else:
                if cmnd[0] in ("ld","st"):
                    raise Exception("invalid variables")
                else:
                    raise Exception("typo error")
            
        print(type)
        ff.write(assembly_to_binary(cmnd,type,counter))
        ff.write("\n")