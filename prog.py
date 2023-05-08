import DICTIONARY as d

register_values={"R0":"0000000000000000","R1":"0000000000000000",
    "R2":"0000000000000000","R3":"0000000000000000","R4":"0000000000000000",
    "R5":"0000000000000000","R6":"0000000000000000","FLAGS":"0000000000000000"}

counter=0
labels={}
variables={}

def assembly_to_binary(words_list,instruction_type):
    opcode=words_list[0]
    if opcode not in d.opcodes.keys():
        raise Exception("typo error")
    if opcode[0]=="j" and opcode[1] not in labels:
        raise Exception("jump error")

    return_str=""

    if instruction_type=="var":
        variables[opcode[0]]=d.int_to_binary(counter,7)

    elif instruction_type=="label":
        labels[opcode[0:-1]]=d.int_to_binary(counter,7)

#instructions
    return_str+=d.opcodes[opcode] 

    if instruction_type=="A":
        return_str+="00"#unused bits
        return_str+=d.registers[words_list[1]]+d.registers[words_list[2]]+d.registers[words_list[3]]
    
    elif instruction_type=="B":
        return_str+="0"#unused bits
        return_str+=d.registers[words_list[1]]+d.int_to_binary(int(words_list[2]),7)
    
    elif instruction_type=="C":
        return_str+="00000"#unused bits
        return_str+=d.registers[words_list[1]]+d.registers[words_list[2]]

    elif instruction_type=="D":
        return_str+="0"#unused bits
        return_str+=d.registers[words_list[1]]+variables[words_list[2]]

    elif instruction_type=="E":
        return_str+="0000"#unused bits
        return_str+=labels[words_list[1]]

    elif instruction_type=="F":
        return_str+="00000000000"#unused bits

    return return_str