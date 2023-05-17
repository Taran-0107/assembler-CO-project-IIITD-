import sys


#dictionaries of registers and opcodes
registers={"R0":"000","R1":"001","R2":"010","R3":"011","R4":"100","R5":"101","R6":"110","FLAGS":"111"}

opcodes={"add":"00000","sub":"00001","mov$":"00010","mov":"00011",
         "ld":"00100","st":"00101","mul":"00110","div":"00111",
         "rs":"01000","ls":"01001","xor":"01010","or":"01011",
         "and":"01100","not":"01101","cmp":"01110","jmp":"01111",
         "jlt":"11100","jgt":"11101","je":"11111","hlt":"11010"}

oplist=list(opcodes.keys())
oplist.append("var")

#function to convert integer to 7 bit binart
def int_to_binary(num,size):
    b=format(num,"b")
    unused=size-len(b)
    b='0'*unused+b
    return b

#initialising dictionaries for variables and labels to store their adress
labels={}
variables={}

l=[]
s=[]
for i in sys.stdin:
    l.append(i)
for item in l:
    item1=item.replace("\n","")
    s.append(item1)

ff= open('stdout.txt', 'w')
ns=s



#main function to convert assembly code to binary, takes single line as input and produces it's binary
#also checks errors, inputs can be infered from variable names below
def assembly_to_binary(words_list,instruction_type,counter,varcount):

    #creating a return string, which is basically the string of binary of a single line returned by this function
    return_str=""
    
    def check_reg(opcode,inst_type,*regslist):
        bool1=opcode=="mov" and inst_type=="C"
        for register in regslist:
            if register not in registers.keys():
                return ("ERROR:Typos in instruction name or register name"+" at line "+str(counter))
            elif register=="FLAGS" and not  bool1:
                return ("ERROR:Illegal use of FLAGS register"+str(counter))
        return None

    opcode=words_list[0]
    if opcode not in oplist:
        return ("ERROR:Typos in instruction name or register name"+" at line "+str(counter))
    if opcode[0]=="j" and words_list[1] not in labels.keys():
        return ("ERROR:General Syntax Error")


    if instruction_type=="var":
        variables[words_list[1]]=int_to_binary(counter+varcount,7)
        return return_str

    elif instruction_type=="label":
        labels[opcode[0:-1]]=int_to_binary(counter,7)
        return return_str
    

    #checking instructions
    if instruction_type=="B" and  words_list[0]=="mov":
        return_str+=opcodes["mov$"] 
    else:
        return_str+=opcodes[opcode] 

    if instruction_type=="A":
        r1=words_list[1]
        r2=words_list[2]
        r3=words_list[3]
        return_str+="00"#unused bits
        a=check_reg(opcode,instruction_type, r1,r2,r3)
        if a!=None:
            return a
        return_str+=registers[r1]+registers[r2]+registers[r3]
    
    elif instruction_type=="B":
        r1=words_list[1]
        numstr=(words_list[2].replace("$",""))
        if not numstr.isnumeric():
            return("ERROR:Typos in instruction name or register name"+" at line "+str(counter))
 
        num=int(numstr)
        if num>127 or num<0:
            return("ERROR:Illegal Immediate values (more than 7 bits)"+" at line "+str(counter))

        return_str+="0"#unused bitss
        a=check_reg(opcode,instruction_type, r1)
        if a!=None:
            return a
        return_str+=registers[r1]+int_to_binary(num,7)
    
    elif instruction_type=="C":
        r1=words_list[1]
        r2=words_list[2]
        return_str+="00000"#unused bits
        a=check_reg(opcode,instruction_type, r1,r2)
        if a!=None:
            return a
        return_str+=registers[r1]+registers[r2]

    elif instruction_type=="D":
        r1=words_list[1]
        var1=words_list[2]
        if var1 not in variables.keys():
            if var1 in labels.keys():
                return("ERROR:Misuse of labels as variables or vice-versa"+" at line "+str(counter))
            else:
                return("ERROR:Illegal Immediate values"+" at line "+str(counter))
        return_str+="0"#unused bits
        a=check_reg(opcode,instruction_type, r1)
        if a!=None:
            return a
        return_str+=registers[r1]+variables[var1]

    elif instruction_type=="E":
        l1=words_list[1]
        if l1 not in labels.keys():
            if var1 in variables.keys():
                return("ERROR:Misuse of labels as variables or vice-versa"+" at line "+str(counter))
            else:
                return("ERROR:Use of undefined labels"+" at line "+str(counter))
        return_str+="0000"#unused bits
        return_str+=labels[l1]

    elif instruction_type=="F":
        return_str+="00000000000"#unused bits

    return return_str

output=""
count=0
f=True
error=False
#cheking presence of variables and labels and their count using a loop
for i in range(len(ns)):
    wl=ns[i].split()

    if wl[-1][-3:]=="hlt" and i!=len(ns)-1:
        if not error:
            error=True
            output=("ERROR: hlt not being used as the last instruction"+" at line "+str(i+1))

    if i==len(ns)-1 and wl[-1][-3:]!="hlt":
        if not error:
            error=True
            output=("ERROR: Missing hlt instruction")

    if wl[0]!="var":
        f=False
    if f==False and wl[0]=="var":
        if not error:
            error=True
            output=("ERROR:Variables not declared at the beginning"+" at line "+str(i+1))
    if f==False:
        count+=1


for i in range(len(ns)):
    wl=ns[i].split()
    if wl[0][-1]==":":
        labels[wl[0][0:-1]]=int_to_binary(count-len(ns)+i,7)

varcount=len(ns)-count
count-=1
linecounter=1

#main loop that takes input and classifies the instruction into a type, 
#then calls the function mentioned above to covert the assembly code to binary.
for j in ns:
        
        #to remove unwanted characters like spaces and indentations
        cmnd=list((j).split(' '))
        #print (cmnd)
        while cmnd[0]=='':
            cmnd.remove("")

        #checking for label
        if cmnd[0][-1]==":":
            cmnd=cmnd[1:]

        for i in range(len(cmnd)):
            if ":" in cmnd[i]:
                cmnd[i]=cmnd[i][cmnd[i].index(':')+1:]
            if '\t' in cmnd[i]:
                cmnd[i]=cmnd[i].replace("\t","")

        while cmnd[0]=='':
            cmnd.remove("")
        
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
                    if not error:
                        error=True
                        output=("ERROR:Use of undefined variables"+" at line "+str(linecounter))
                        break
                else:
                    if not error:
                        error=True
                        output=("ERROR:Typos in instruction name or register name"+" at line "+str(linecounter))
                        break
            

        
        temp=(assembly_to_binary(cmnd,type,linecounter,len(ns)-varcount-1))
        if "ERROR:" in temp:
            output=temp
            break
        elif not error:
            output+=temp
            if linecounter>varcount:
                output+=("\n")
        linecounter+=1

ff.write(output)
#printing this line in case no errors are found
#print("successfully written to output file, encountered no errors\n")
print(output)
