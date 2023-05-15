# assembler-CO-project-IIITD-
this repository contains the code for Computer Organisation(CO) group project of Btech 1st year IIITD. students in the group: Tarandeep Singh, Tanmay Khatri, Sweta Singdha, Tejas Jaiswal

the provided code converts input in form of assembly language, to machine code
the input is given through a file "stdin.txt" and the output is written to the file "stdout.txt"

the code consists of 4 main parts:
first, the dictionary of opcodes and redister adress, having the name as key and it's binary as value.
there is also a dictinary of variables and lables, to which the data is stored later in an iteration of all the lines of code in inout file

then there is a function called assembler_to_binary which converts a single instruction to machine code, 
given the list of words and type of instruction as input. this function is defined in the begining but is called much later in the code
it contains another function called check reg inside it

then there is a for loop iterating through each line of code, calculating the number of variable definitions, 
for use later for  assigning variable adresses and label adresses

lastly there is another iteration through each line, this time cheking the opcode and identifying and
classifying the intructions into type A,B,C,D,E or F and then calling the funtion assembler_to_binary

errors in the code are checked throughout each of the steps mentioned above, in both the iterations and inside the function
