# assembler-CO-project-IIITD-
this repository contains the code for Computer Organisation(CO) group project of Btech 1st year IIITD. students in the group: Tarandeep Singh, Tanmay Khatri, Sweta Snigdha, Tejas Jaiswal

the provided code converts input in form of assembly language, to machine code
the input is given through stdin and output is displayed in the console
the code main file is "Assembler.py"

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

lastly, if no errors are found the assembly code is printed in the console,
in case errors are found, the error which is detected first according to provided code is printed in the console.


Group Members
Tejas (tejasj228)
Tarandeep (Taran-0107)
Sweta (cypherei00)
Tanmay (TanmayKhatri28)

Contributions
Tejas:
Made a function to write the output and the error into text files and also to track the line number.
Tarandeep:
Made a function to convert instructions to machine code (binary digits).
Sweta:
Made a function for error handling.
Tanmay:
Made a function to take input and classify it.
Overall, the group members worked together effectively to create a functional assembler. Each member made a significant contribution to the project, and their work was essential to the success of the project.

Here are some additional details about each member's contribution:

Tejas: Tejas' function to write the output and the error into text files and also to track the line number was essential for debugging the assembler. This function allowed the group to easily identify and fix errors in the assembler's code.
Tarandeep: Tarandeep's function to convert instructions to machine code (binary digits) was essential for the assembler to be able to run on a computer. This function allowed the group to translate the assembler's code into a format that the computer could understand.
Sweta: Sweta's function for error handling was essential for ensuring that the assembler could run without crashing. This function allowed the group to catch and handle errors that occurred during the execution of the assembler's code.
Tanmay: Tanmay's function to take input and classify it was essential for the assembler to be able to be used to create different types of programs. This function allowed the group to create a versatile assembler that could be used for a variety of tasks.
The group members worked together effectively to create a functional assembler. Each member made a significant contribution to the project, and their work was essential to the success of the project.
