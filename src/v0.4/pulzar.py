"""
©Pulzar 2018-20

#Author : Brian Turza
version: 0.4
#Created : 14/9/2019 (this version)
"""

import lexer
import mparser
import generator

import os
import platform
import sys
from time import perf_counter
#Check Platform
#If windows
if platform.system() == "Windows":
    os.system("title Pulzar v0.4")
#If linux or mac os
elif platform.system() == "linux" or platform.system() == "darwin":
    sys.stdout.write("\x1b]2;Pulzar v0.4\x07")

def main():
    arguments_length = len(sys.argv)
    if arguments_length == 1:
        import shell
        shell.shell()

    arg = sys.argv

    #If file doesnt have .plz file extension, it will raise an error
    if arg[1][-4:] != ".plz":
        print("FileError at file '{}':\nMust be .plz file".format (sys.argv[1]))
        quit()
    # Looks for second argument
    elif arguments_length == 2:
        with open(arg[1], "r") as f:
            code = f.read()
            #Lexer
            lex = lexer.Lexer(code)
            tokens = lex.tokenize()
            #Parser
            parse = mparser.Parser(tokens,False)
            ast = parse.parse(tokens)
            if ast[2] == True: # There was an error
                quit()
            obj = generator.Generation(ast[0], ast[1]) # 1 parameter: ast; 2 parameter: isConsole (True or False)
            gen = obj.generate()
            exec(gen)
            return

    elif arguments_length > 2 and sys.argv[arguments_length - 1] in ["-t", "--tools"]:
        with open(sys.argv[1], "r", encoding="utf-8") as f:
            code = f.read()
        print("ORIGINAL CODE:")
        print(code)
        #Lexer
        print("-------------- LEXICAL ANALYSYS ---------------------\n")
        lex = lexer.Lexer(code)
                    
        tokens = lex.tokenize()
        print(tokens)
        #Parser
        print(22*"-" + " PARSER " + 22*"-")

        parse = mparser.Parser(tokens, True)
        ast = parse.parse(tokens)
        if ast[2] == True:  # There was an error
            quit()

        print("Abstract Syntax Tree:")
        print(ast[0])
        print(17*"-" + "CODE GENERATION" + 18*"-")
        obj = generator.Generation(ast[0], ast[1]) # 1 parameter: ast; 2 parameter: isConsole (True or False)
        gen = obj.generate()
        print(gen)
        print("#"*21,"OUTPUT","#"*21)
        exec(gen)

    elif arguments_length > 2 and ("-c" in sys.argv or  "--compile" in sys.argv) and ("-t" not in sys.argv or "--tools" not in sys.argv):
        import subprocess

        with open(sys.argv[1], "r", encoding="utf-8") as f:
            code = f.read()
        print("ORIGINAL CODE:")
        print(code)
        # Lexer
        print("-------------- LEXICAL ANALYSYS ---------------------\n")
        lex = lexer.Lexer(code)

        tokens = lex.tokenize()
        print(tokens)
        # Parser
        print(22 * "-" + " PARSER " + 22 * "-")

        parse = mparser.Parser(tokens, True)
        ast = parse.parse(tokens)
        print("Abstract Syntax Tree:")
        print(ast[0])
        print(17 * "-" + "CODE GENERATION" + 18 * "-")
        obj = generator.Generation(ast[0], ast[1], True)  # 1 parameter: ast; 2 parameter: isConsole (True or False)
        gen = obj.generate()
        print(gen)
        print("#" * 21, "OUTPUT", "#" * 21)
        f = open(sys.argv[1][:-4] + ".cpp", 'w')
        f.write(gen)
        f.close()
        if subprocess.call(["g++", f"{sys.argv[1][:-4]}.cpp", "-o", f"{sys.argv[1][:-4]}"]) == 0:
            if "-r" in sys.argv or "--run" in sys.argv:
                PATH = os.getcwd()
                filename = sys.argv[1][:-4].split('/')
                os.chdir("".join([str(i) + "/" for i in filename[:-1]]))
                subprocess.call([f"{filename[-1]}.exe"], shell=True)
                os.system(f"cd {PATH}")
            else:
                print("Compilation successful")
        else:
            print("Compilation errors")

#---------------------------------------------------------------------------

if __name__ == "__main__":
    start_time = perf_counter()
    main()
    end_time = perf_counter()
    print("\nExecuted in: %s seconds" % (end_time - start_time))