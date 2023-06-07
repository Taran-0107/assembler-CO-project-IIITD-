reg_addr={"R0":"000","R1":"001","R2":"010","R3":"011","R4":"100","R5":"101","R6":"110","FLAGS":"111"}
rv={"000":0,"001":0,"010":0,"011":0,"100":0,"101":0,"110":0,"111":0}
flags=list("0000000000000000")

def get_flags():
    tempstr=''
    for i in flags:
        tempstr+=i
    return tempstr

var={}
labels=[]
opcodes=["00000","00001","00010",
"00011","00100","00101","00110",
"00111","01000","01001","01010",
"01011","01100","01101","01110",
"01111","11100","11101","11111","11010"]

def int_to_binary(num,size):
    b=format(num,"b")
    unused=size-len(b)
    b='0'*unused+b
    return b

def inst_type_list(str):
    opcode=str[:5]
    l=[]
    args=[]
    A=[0,1,6,10,11,12]
    B=[2,8,9]
    C=[3,7,13,14]
    D=[4,5]
    E=[15,16,17,18]
    F=[19]

    if opcode in [e for i, e in enumerate(opcodes) if i in A]:
        l=l+[str[:5],str[5:7],str[7:10],str[10:13],str[13:]]
        args=args+l[-3:]

    elif opcode in [e for i, e in enumerate(opcodes) if i in B]:
        l=l+[str[:5],str[5:6],str[6:9],str[9:]]
        args=args+l[-2:]
    
    elif opcode in [e for i, e in enumerate(opcodes) if i in C]:
        l=l+[str[:5],str[5:10],str[10:13],str[13:]]
        args=args+l[-2:]
    
    elif opcode in [e for i, e in enumerate(opcodes) if i in D]:
        l=l+[str[:5],str[5:6],str[6:9],str[9:]]
        args=args+l[-2:]
        var[l[-1]]=0
    
    elif opcode in [e for i, e in enumerate(opcodes) if i in E]:
        l=l+[str[:5],str[5:9],str[9:]]
        args=args+l[-1:]
        labels.append(l[-1])
    
    elif opcode in [e for i, e in enumerate(opcodes) if i in F]:
        l=l+[str[:5],str[5:]]
    
    return l,args

def ld(r1,mem_addr):
    rv[r1]=var[mem_addr]

def st(r1,mem_addr):
    var[mem_addr]=rv[r1]

def movim(r1,imm):
    rv[r1]=int(imm,2)

def lshift(r1,imm):
    num=int(imm,2)
    bin_num=int_to_binary(rv[r1],16)
    if num>=16:
        rv[r1]=0
    else:
        bin_num=bin_num[num:]+"0"*num
        rv[r1]=int(bin_num,2)

def rshift(r1,imm):
    num=int(imm,2)
    bin_num=int_to_binary(rv[r1],16)
    if num>=16:
        rv[r1]=0
    else:
        bin_num=bin_num[0:16-num]
        rv[r1]=int(bin_num,2)

#type A
def add(r1,r2,r3):
    rv[r1]=rv[r2]+rv[r3]
    check_overflow(r1)
def sub(r1,r2,r3):
    rv[r1]=rv[r2]-rv[r3]
    check_overflow(r1)
def mul(r1,r2,r3):
    rv[r1]=rv[r2]+rv[r3]
    check_overflow(r1)
def div(reg3,reg4):
    if(rv[reg4]==0):
        flags[-4]="1"
        rv["000"]=0
        rv["001"]=0
        return
    rv["000"]=reg3/reg4
    rv["001"]=reg3%reg4

def xor(r1,r2,r3):
    rv[r1]=rv[r2]^rv[r3]
def orr(r1,r2,r3):
    rv[r1]=rv[r2]|rv[r3]
def andd(r1,r2,r3):
    rv[r1]=rv[r2]&rv[r3]
#type c
def movreg(r1,r2):
    if r2=="111":
        rv[r1]=int(get_flags(),2)
    else:
        rv[r1]=rv[r2]

def invert(r1,r2):
    bin_num=int_to_binary(rv[r2],16)
    for i in range(len(bin_num)):
        if bin_num[i]=="0":
            bin_num[i]="1"
        else:
            bin_num[i]="0"
    
    rv[r1]=int(bin_num,2)

def cmp(r1,r2):
    
    if(rv[r1]==rv[r2]):
        flags[-1]="1"
    elif(rv[r1]>rv[r2]):
        flags[-2]="1"
    else:
        flags[-3]="1"

def jmp(mem_addr):
    return int(mem_addr,2)
def jlt(mem_addr):
    if flags[-3]=="1":
        return int(mem_addr,2)
def jgt(mem_addr):
    if flags[-2]=="1":
        return int(mem_addr,2)
def je(mem_addr):
    if flags[-1]=="1":
        return int(mem_addr,2)

def muladd(r1, r2, r3, r4):
    rv[r4] = rv[r1]*rv[r2] + rv[r3]
    check_overflow(r4)

def bitr(r1, r2):
    rv[r2] = int(int_to_binary(rv[r1], 16)[::-1], 2)

def cntz(r1, r2):
    rv[r2] = int_to_binary(rv[r1], 16).rstrip('0').count('0')

def check_overflow(register):
    value=rv[register]
    if value<0 or value>(2**16)-1:
        flags[-4]="1"
        rv[register]=0

func_dict = {"00000": add, "00001": sub, "00110": mul, "00111": div, "01010": xor, "01011": orr, "01100": andd, 
             "00011": movreg, "01101": invert, "01110": cmp, "00100": ld, "00101": st, "00010": movim, 
             "01001": lshift, "01000": rshift, "01111": jmp, "11100": jlt, "11101": jgt, "11111": je, 
             "10100": muladd, "10110": bitr, "10111": cntz}

def execute(inst_tup):
    global flags
    
    inst=inst_tup[0]
    args=inst_tup[1]
    retval=func_dict[inst[0]](*args)
    #print(flags)
    if(inst[0]!="01110"):
        flags=list("0000000000000000")
    return retval

inst_list=[]
lines_data=[]
hlt=False

#memory dump function
def dump_mem(adress):
    i=int(adress)
    bin_i=int_to_binary(adress,7)
    if(i<len(lines_data)):
        print(lines_data[i])

    elif bin_i in var.keys():
        print(int_to_binary(var[bin_i],16))
    
    else:
        print(int_to_binary(0,16))

inend =False
while not inend:
    bin_inst=input().replace("\r","")
    l,args=inst_type_list(bin_inst)
    lines_data.append(bin_inst)
    inst_list.append((l,args))
    if(bin_inst[0:5]=="11010"):
        #print("stop")
        inend=False
        break
    
count=0
while not hlt:
    #print(count)
    instruction=inst_list[count]
    #print(instruction[0][0])
    if(instruction[0][0]=="11010"):
        hlt=True
        print(f"{int_to_binary(count,7)}        {int_to_binary(rv['000'],16)} {int_to_binary(rv['001'],16)} {int_to_binary(rv['010'],16)} {int_to_binary(rv['011'],16)} {int_to_binary(rv['100'],16)} {int_to_binary(rv['101'],16)} {int_to_binary(rv['110'],16)} {get_flags()}")
        break

    if instruction[0][0] not in func_dict.keys():
        pass
    else:
        c=execute(instruction)
        print(f"{int_to_binary(count,7)}        {int_to_binary(rv['000'],16)} {int_to_binary(rv['001'],16)} {int_to_binary(rv['010'],16)} {int_to_binary(rv['011'],16)} {int_to_binary(rv['100'],16)} {int_to_binary(rv['101'],16)} {int_to_binary(rv['110'],16)} {get_flags()}")
        
        if c!=None:
            count=c
        else:
            count+=1
        

for i in range(128):
    dump_mem(i)
    #execute(instruction)

#print("completeed")

#print(rv)
#print(flags)
#print(var)
#print(labels)