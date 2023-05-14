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

labels={}
variables={}

file = open('stdin.txt', 'r')
s=file.read().split('\n')
ff= open('stdout.txt', 'w')
ns=list(filter(None, s))
file.close()

def write_error(error_str):
    ff.close()
    f=open('stdout.txt',"w")
    f.write(error_str)
    f.close()

def assembly_to_binary(words_list,instruction_type,counter,varcount):

    def check_reg(opcode,inst_type,*regslist):
        bool1=opcode=="mov" and inst_type=="C"
        for register in regslist:
            if register not in registers.keys():
                write_error("ERROR:Typos in instruction name or register name"+" at line "+str(counter))
                raise Exception("ERROR:Typos in instruction name or register name")
            elif register=="FLAGS" and not  bool1:
                write_error("ERROR:Illegal use of FLAGS register"+str(counter))
                raise Exception("ERROR:Illegal use of FLAGS register")

    opcode=words_list[0]
    if opcode not in oplist:
        write_error("ERROR:Typos in instruction name or register name"+" at line "+str(counter))
        raise Exception("ERROR:Typos in instruction name or register name")
    if opcode[0]=="j" and words_list[1] not in labels.keys():
        write_error("ERROR:General Syntax Error")
        raise Exception("ERROR:General Syntax Error"+" at line "+str(counter))

    return_str=""

    if instruction_type=="var":
        variables[words_list[1]]=int_to_binary(counter+varcount,7)
        return return_str

    elif instruction_type=="label":
        labels[opcode[0:-1]]=int_to_binary(counter,7)
        return return_str
    

#instructions
    if instruction_type=="B" and  words_list[0]=="mov":
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
            write_error("ERROR:Typos in instruction name or register name"+" at line "+str(counter))
            raise Exception("ERROR:Typos in instruction name or register name")
        num=int(numstr)
        if num>127 or num<0:
            write_error("ERROR:Illegal Immediate values (more than 7 bits)"+" at line "+str(counter))
            raise Exception("ERROR:Illegal Immediate values (more than 7 bits)")
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
                write_error("ERROR:Misuse of labels as variables or vice-versa"+" at line "+str(counter))
                raise Exception("ERROR:Misuse of labels as variables or vice-versa")
            else:
                write_error("ERROR:Illegal Immediate values"+" at line "+str(counter))
                raise Exception("ERROR:Illegal Immediate values")
        return_str+="0"#unused bits
        check_reg(opcode,instruction_type, r1)
        return_str+=registers[r1]+variables[var1]

    elif instruction_type=="E":
        l1=words_list[1]
        if l1 not in labels.keys():
            if var1 in variables.keys():
                write_error("ERROR:Misuse of labels as variables or vice-versa"+" at line "+str(counter))
                raise Exception("ERROR:Misuse of labels as variables or vice-versa")
            else:
                write_error("ERROR:Use of undefined labels"+" at line "+str(counter))
                raise Exception("ERROR:Use of undefined labels")
        return_str+="0000"#unused bits
        return_str+=labels[l1]

    elif instruction_type=="F":
        return_str+="00000000000"#unused bits

    return return_str


count=0
f=True
for i in range(len(ns)):
    wl=ns[i].split()

    if wl[-1][-3:]=="hlt" and i!=len(ns)-1:
        write_error("ERROR: hlt not being used as the last instruction"+" at line "+str(i+1))
        raise Exception("ERROR:hlt not being used as the last instruction")

    if i==len(ns)-1 and wl[-1][-3:]!="hlt":
        write_error("ERROR: Missing hlt instruction")
        raise Exception("ERROR: Missing hlt instructione")

    if wl[0]!="var":
        f=False
    if f==False and wl[0]=="var":
        write_error("ERROR:Variables not declared at the beginning"+" at line "+str(i+1))
        raise Exception("ERROR:Variables not declared at the beginning")
    if f==False:
        count+=1


for i in range(len(ns)):
    wl=ns[i].split()
    if wl[0][-1]==":":
        labels[wl[0][0:-1]]=int_to_binary(count-len(ns)+i,7)

varcount=len(ns)-count
count-=1
linecounter=1
for j in ns:
        cmnd=list((j).split(' '))
        if cmnd[0][-1]==":":
            cmnd=cmnd[1:]
        if cmnd[0]=="var":
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
            elif(cmnd[2] in registers.keys()):
                type="C"
            elif(cmnd[2] in variables.keys()):
                type="D"
            else:
                if cmnd[0] in ("ld","st"):
                    write_error("ERROR:Use of undefined variables"+" at line "+str(linecounter))
                    raise Exception("ERROR:Use of undefined variables")
                else:
                    write_error("ERROR:Typos in instruction name or register name"+" at line "+str(linecounter))
                    raise Exception("ERROR:Typos in instruction name or register name")
            

        
        ff.write(assembly_to_binary(cmnd,type,linecounter,len(ns)-varcount-1))
        if linecounter>varcount:
            ff.write("\n")
        linecounter+=1

print("successfully written to output file, encountered no errors")