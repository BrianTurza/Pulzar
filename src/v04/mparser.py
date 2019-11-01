"""
©Pulzar 2018-19
Author: Brian Turza
"""
import constants
from Lib.fmath import *
from Obj.varObject import VarObject
from Obj.builtinObject import BuiltinObject
from Obj.loopObject import LoopObject
from Obj.functionObject import FuncObject
from Obj.conditionalObject import ConditionalObject
from Obj.libObject import libObject

import math
import os

class Parser(object):

    def __init__(self,token_stream,include):
        self.tokens = token_stream
        self.include = include
        self.ast = { 'main_scope' : [] }
        self.symbol_table = []

        self.token_index = 0
        
    
    def parse(self):
        """
        This function takes tokens from lexer and #TODO
        """
        count = 0
        for self.token_index  in range(len(self.tokens)):

            token_type = self.tokens[self.token_index][0]
            token_value = self.tokens[self.token_index][1]

            #If token == echo add tokens to parse_include()
            if token_type == "KEYWORD" and token_value == "include":
                self.parse_include(self.tokens[self.token_index:len(self.tokens)])

            elif token_type == "KEYWORD" and token_value == "Program":
                self.parse_program(self.tokens[self.token_index:len(self.tokens)])
                count += 1
            
            elif token_type == "DATATYPE":
                self.parse_variable(self.tokens[self.token_index:len(self.tokens)],False,True)
            #Check if it was already dececlared
                        
            elif token_type == "IDENTIFIER" and token_value in self.symbol_table:
                self.parse_variable(self.tokens[self.token_index:len(self.tokens)],False,False)


            elif token_type == "BUILT_IN_FUNCTION":
                self.parse_builtin(self.tokens[self.token_index:len(self.tokens)])
            
            elif token_type == "MATH_FUNCTION":
                self.parse_math(self.tokens[self.token_index:len(self.tokens)],False)
                     
            elif token_type == "KEYWORD" and token_value == "if" or token_value == "else" or token_value == "elseif":
                self.parse_conditional_statments(self.tokens[self.token_index:len(self.tokens)])
            
            elif token_type == "KEYWORD" and token_value == "for":
                self.parse_loop(self.tokens[self.token_index:len(self.tokens)])

            
            elif token_type == "KEYWORD" and token_value == "func":
                self.parse_func(self.tokens[self.token_index:len(self.tokens)])
            
            elif token_type == "KEYWORD" and token_value == "run":
                self.find_func(self.tokens[self.token_index:len(self.tokens)])
            
            elif token_type == "COMMENT":
                self.parse_comment(self.tokens[self.token_index:len(self.tokens)])

            elif token_type == "UNDEFINIED":
                #TODO Identify better errors
                self.error_message("SyntaxError: \n Undefinied")

            self.token_index += 1
        #If no Program declaration is found in code, calls a error message
        if count == 0:
             self.error_message("Program Error: \nType must be included in code")
        
        return self.ast
        
    def parse_include(self,token_stream):

        tokens_checked = 0
        list_lib = ["math","tools"]
        lib = ""
        ast = {'Include' : []}
        for token in range(0,len(token_stream)):
			
            token_type = token_stream[tokens_checked][0]
            token_value = token_stream[tokens_checked][1]
            
            if token_type == "SEMIC":break
            
            if token == 1 and token_value == "math":
                lib = "Lib.fmath"
                ast['Include'].append({'libary' : token_value})
            
            elif token == 1 and token_value not in list_lib:
                msg = "IncludeError at line:\n'{}' is not definied".format (token_value)
                self.error_message(msg)
            
            tokens_checked += 1
        
        self.ast['main_scope'].append(ast)

        return [ast, tokens_checked]

        self.token_index += tokens_checked
    
    def parse_math(self,token_stream,):
        
        value = ""
        tokens_checked = 0
        ast = {'math' : []}
        for token in range(0,len(token_stream)):
			
            token_type = token_stream[tokens_checked][0]
            token_value = token_stream[tokens_checked][1]
            
            if token_type == "SEMIC":break

            if token == 0: ast.append({'function' : token_value})
                
            if token == 1 and token_type in ["INT","ID"]:
                value = token_value
                
            elif token == 1 and token_type not in ["INTEGER","IDENTIFIER"]:
                msg = "Error: "+token_value+" must be int"
                self.error_message(msg)

            elif token > 1 and token % 2 == 0:
                value += token_value

            tokens_checked += 1

        ast['math'].append({'arguments' : value})
        self.ast['main_scope'].append(ast)
        
        self.token_index += tokens_checked

        return [ast, tokens_checked]

    def parse_program(self,token_stream):
		
        tokens_checked = 0
        ast = { 'program': [] }

        for token in range(0,len(token_stream)):
            
            token_type = token_stream[tokens_checked][0]
            token_value = token_stream[tokens_checked][1]

            if token_type == "SEMIC": break

            if token == 1 and token_value == "Console":
                ast['program'].append({'type' : token_value})

            elif token == 1 and token_value not in ["Program","Console","Browser"]:
                self.error_message("Program error: undefinied program '{}'".format (token_value))
            
            tokens_checked += 1
                
        self.token_index += tokens_checked

        self.ast['main_scope'].append(ast)

        return [ast, tokens_checked]

    def parse_variable(self, token_stream,inScope,decl):

        if decl == True:
            tokens_checked = 0

            func = ["factorial", "sin"]
            ast = { 'variable_declaration': [] }
            value = ""
            c = False
        
            for token in range(0,len(token_stream)):

                token_type = token_stream[tokens_checked][0]
                token_value = token_stream[tokens_checked][1]

                #If  semic is found loop breaks
                if token_type == "SEMIC": break

                elif token == 0:
                    ast['variable_declaration'].append({'type' : token_value})
                
                elif token == 1 and token_type == "IDENTIFIER":
                    ast['variable_declaration'].append({ 'name': token_value })
                
                elif token == 1 and token_stream[token + 1][0] == "SEMIC":
                    #If the type is integer
                    if token_stream[0][1] == "var":
                        ast['variable_declaration'].append({ "value": '"Undefinied"' })

                    elif token_stream[0][1] == "int": 
                        ast['variable_declaration'].append({ "value": "0" })
                    elif token_stream[0][1] == "str":
                        ast['variable_declaration'].append({ "value": '""' })
                    elif token_stream[0][1] == "bool":
                        ast['variable_declaration'].append({ "value": "None" })
                
                #Invalid variable name <ERROR>
                elif token == 1 and token_type != "IDENTIFIER":
                    msg = ("NameError at line \nInvalid variable name '"+token_value+"'")
                    self.error_message(msg)	
                #Invalid operator Error
                elif token == 2 and token_type != "OPERATOR":
                    msg = "OperatorError\n Invalid operator"
                    print(token_value)
                    self.error_message(msg)
                
                elif token == 3 and token_stream[0][1] != "var" and token_stream[token + 1][0] == "SEMIC": 

                    if token_type == "IDENTIFIER":
                        value = self.get_token_value(token_value)

                        if type(eval(value)) == eval(token_stream[0][1]):
                            try: ast['variable_declaration'].append({ "value": int(token_value) })
                            except ValueError: ast['variable_declaration'].append({ "value": token_value })
                        else:
                            self.error_message("variable value does not match defined type")

                    elif type(eval(token_value)) == eval(token_value) and token_type not in  ["IDENTIFIER", "COMPLEX", "FACTORIAL"] :
                        try: ast['variable_declaration'].append({ "value": int(token_value) })
                        except ValueError: ast['variable'].append({ "value": token_value })
                    else:
                        self.error_message("Variable value does not match defined type")
                
                elif token == 3 and token_type in  ['INTEGER', 'OPERATOR', 'STRING', 'IDENTIFIER','LATEX','COMPLEX_NUMBER']:
                    value = token_value

                elif token == 3 and token_type == token_type == "COMPLEX_NUMBER":
                    value = token_value.replace("i","j")
                    c = True
                
                elif token == 3 and token_type == "STRING":
                    value = token_value.replace("\s", " ")

                elif token  <= 3 and token_type == "IDENTIFIER":
                    value = self.get_token_value(token_value)
                    print(value)

                elif token == 3 and token_type not in ['INTEGER', 'OPERATOR', 'STRING', 'IDENTIFIER','LATEX',"COMPLEX_NUMBER"]:
                    msg = "ValueError at line:\nInvalid Variable value '"+token_value+"'"
                    self.error_message(msg)


                
                elif token > 3:
                    value += token_value
                
                elif token_type == "BRACKET":
                    value += token_value

                tokens_checked += 1

            if type(value) == int:
                try:value = eval(value)
                except:pass

            elif type(value) == float:
                value = float(value)
            
            elif type(value) == complex:
                try: value = complex(value)
                except: pass
            
            ast['variable_declaration'].append({'value' : value})
            
            if inScope == False:
                self.ast['main_scope'].append(ast)

            self.symbol_table.append([ast['variable_declaration'][1]['name'], ast['variable_declaration'][2]['value']])

            self.token_index += tokens_checked
            
            return [ast,tokens_checked]

        elif decl == False:
			
            tokens_checked = 0
            func = ["factorial", "sin",]
            ast = { 'variable': [] }
            value = ""
            c = False
            for token in range(0,len(token_stream)):
                
                token_type = token_stream[tokens_checked][0]
                token_value = token_stream[tokens_checked][1]
                #If  semic is found loop breaks

                if token_type == "SEMIC": break
                
                elif token == 1 and token_type == "IDENTIFIER":
                    print(token_value)
                    ast['variable'].append({ 'name': token_value })
                #Invalid operator Error
                elif token == 2 and token_type != "OPERATOR":
                    msg = "OperatorError\nInvalid operator"
                    self.error_message(msg)
                
                elif token == 3 and token_stream[token + 1][0] == "SEMIC": 

                    if token_type == "IDENTIFIER":
                        value = self.get_token_value(token_value)

                        if type(eval(value)) == eval(token_stream[0][1]):
                            try: ast['variable_declaration'].append({ "value": int(token_value) })
                            except ValueError: ast['variable_declaration'].append({ "value": token_value })
                        else:
                            self.error_message("variable value does not match defined type")

                    elif type(eval(token_value)) == eval(token_stream[0][1]) and token != "IDENTIFIER":
                        try: ast['variable_declaration'].append({ "value": int(token_value) })
                        except ValueError: ast['variable_declaration'].append({ "value": token_value })
                    else:
                        self.error_message("Variable value does not match defined type")
                
                elif token == 3 and token_type in  ['INTEGER', 'OPERATOR', 'STRING', 'IDENTIFIER','LATEX','COMPLEX_NUMBER']:
                    value = token_value

                elif token == 3 and token_type == token_type == "COMPLEX_NUMBER":
                    value = token_value.replace("i","j")
                    c = True
                
                elif token == 3 and token_type == "STRING":
                    value = token_value.replace("\s", " ")

                elif token  <= 3 and token_type == "IDENTIFIER":
                    value = self.get_token_value(token_value)
                    print(value)

                elif token == 3 and token_type not in ['INTEGER', 'OPERATOR', 'STRING', 'IDENTIFIER','LATEX',"COMPLEX_NUMBER"]:
                    msg = "ValueError at line:\nInvalid Variable value '"+token_value+"'"
                    self.error_message(msg)
                
                elif token > 3:
                    value += token_value
                
                elif token_type == "BRACKET":
                    value += token_value

                tokens_checked += 1

            if type(value) == int:
                try:value = eval(value)
                except:pass

            elif type(value) == float:
                value = float(value)
            
            elif type(value) == complex:
                try: value = complex(value)
                except: pass
            
            ast['variable_declaration'].append({'value' : value})

            self.ast['main_scope'].append(ast)

            self.token_index += tokens_checked


    def get_scope(self, token_stream):

        nesting_count = 1
        tokens_checked = 0
        body_tokens = []

        for token in token_stream:

            tokens_checked += 1

            token_value = token[1]
            token_type  = token[0] 

            if token_type == "SCOPE_DEFINER" and token_value == "{": nesting_count += 1
            elif token_type == "SCOPE_DEFINER" and token_value == "}": nesting_count -= 1

            if nesting_count == 0: 
                body_tokens.append(token)
                break

            else: body_tokens.append(token)

        return [body_tokens, tokens_checked,nesting_count]


    def parse_scope(self,token_stream, ast):
        ast = {'body' : []}
        tokens_checked = 0
        nesting_count = 0

        for tokens_checked  in range(len(token_stream)):

            token_type = token_stream[tokens_checked][0]
            token_value = token_stream[tokens_checked][1]

            #If token is echo add tokens to parse_include()
            if token_type == "KEYWORD" and token_value == "include":
                include = self.parse_include(self.tokens[self.token_index:len(self.tokens)])
                ast['body'].append(include[0])
                tokens_checked += include[1]
            
            elif token_type == "DATATYPE":
                var = self.parse_variable(self.tokens[self.token_index:len(self.tokens)],True,True)
                ast['body'].append(var[0])
                tokens_checked += var[1]

            #Check if it was already dececlared
            elif token_type == "IDENTIFIER" and token_value in self.symbol_table:
                var = self.parse_variable(self.tokens[self.token_index:len(self.tokens)],True,False)
                ast['body'].append(var[0])
                tokens_checked += var[1]

            elif token_type == "BUILT_IN_FUNCTION":
                builtin = self.parse_builtin(self.tokens[self.token_index:len(self.tokens)])
                ast['body'].append(builtin[0])
                tokens_checked += builtin[1]
            
            elif token_type == "MATH_FUNCTION":
                math = self.parse_math(self.tokens[self.token_index:len(self.tokens)],True)
                ast['body'].append(math[0])
                tokens_checked += math[1]
                     
            elif token_type == "KEYWORD" and token_value == "if" or token_value == "else" or token_value == "elseif":
                condtitional = self.parse_conditional_statments(self.tokens[self.token_index:len(self.tokens)],True)
                ast['body'].append(condtitional[0])
                tokens_checked += condtitional[1] - 1

            elif token_type == "KEYWORD" and token_value == "for":
                loop = self.parse_loop(self.tokens[self.token_index:len(self.tokens)],True)
                ast['body'].append(loop[0])
                tokens_checked += loop[1]

            elif token_type == "KEYWORD" and token_value == "while":
                loop = self.parse_loop(self.tokens[self.token_index:len(self.tokens)],True)
                ast['body'].append(loop[0])
                tokens_checked += loop[1]
            
            elif token_type == "KEYWORD" and token_value == "func":
                function = self.parse_func(self.tokens[self.token_index:len(self.tokens)],True)
                ast['body'].append(function[0])
                tokens_checked += function[1]

            elif token_type == "KEYWORD" and token_value == "run":
                run = self.find_func(self.tokens[self.token_index:len(self.tokens)],True)
                ast['body'].append(run[0])
                tokens_checked += run[1]
            
            elif token_type == "COMMENT":
                comment = self.parse_comment(self.tokens[self.token_index:len(self.tokens)],True)
                ast['body'].append(comment[0])
                tokens_checked += comment[1]

            elif token_type == "UNDEFINIED":
                #TODO Identify better errors
                self.error_message("SyntaxError: \n Undefinied")

        self.token_index += nesting_count + 1

        statement_ast[astName].append(ast)
        self.ast.append(statement_ast[astName])
    
    def parse_builtin(self,token_stream):

        tokens_checked = 0
        value = ""
        ast = {'builtin_function' : []}
        for token in range(0,len(token_stream)):
            
            token_type = token_stream[tokens_checked][0]
            token_value = token_stream[tokens_checked][1]

            if token_type == "SEMIC": break

            if token == 0:
                ast['builtin_function'].append({'function' : token_value})
        
            if token == 1 and token_type =="IDENTIFIER":
                #TODO value = self.get_token_value(token_value)
                value = token_value
                    
            elif token > 1:
                value += token_value

            tokens_checked += 1
        
        if type(value) == int:
            try:value = eval(value)
            except:pass

        elif type(value) == float:
            value = float(value)
        
        elif type(value) == complex:
            try: value = complex(value)
            except: pass

        ast['builtin_function'].append({'argument' : value})

        self.ast['main_scope'].append(ast)

        self.token_index += tokens_checked

        return [ast,tokens_checked]
        
    def parse_conditional_statments(self,token_stream):

        tokens_checked = 0
        condition = ""
        els = False
        tokens = []
        ast = {'conditional_Statment' : []}
        
        for token in range(0,len(token_stream)):

            token_type = token_stream[tokens_checked][0]
            token_value = token_stream[tokens_checked][1]

            if token_type == "SCOPE_DEFINIER" and token_value == "{":
                self.get_scope(token_stream[tokens_checked + 1:len(token_stream)])
                break

            elif token == 0 and token_value == "if":
                ast['conditional_Statment'].append({'keyword' : token_value})
            
            elif token == 0 and token_value == "else":
                ast['conditional_Statment'].append({'keyword' : token_value})
                els = True       
            
            elif token == 1:
                condition = token_value

            elif token > 1 and token <= 3:
                condition += token_value

            elif token_stream[tokens_checked + 1][0] == "SCOPE_DEFINIER":
                msg = "CondtionalError:\nelse function doesnt take arguments"
                print(token_stream[tokens_checked + 1][0])
                self.error_message(msg)
            
            tokens_checked += 1
            
        if els == False:
            ast['conditional_Statment'].append({'condition' : condition})

        self.ast['main_scope'].append(ast)

        scope_tokens =  self.get_scope(token_stream[tokens_checked:len(token_stream)])

        print(scope_tokens)
        self.parse_scope(scope_tokens[0], ast)

        tokens_checked += scope_tokens[1]

        self.token_index += tokens_checked

        return [ast, tokens_checked]

    def get_token_value(self,token):
        for variable in self.symbol_table:
            if variable[0] == token: return variable[1]

    def parse_loop(self,token_stream):
	#for x :: x < 10 :: x++ {
        tokens_checked = 0
        value = ""
        increment = ""
        var_decl = False
        ast = {'loop' : []}
        
        for token in range(0,len(token_stream)):

            token_type = token_stream[tokens_checked][0]
            token_value = token_stream[tokens_checked][1]
                          
            if token_type == "SCOPE" and token_value == "{":
                break

            if token == 0:
                ast['loop'].append({'keyword' : token_value})
            
            if token == 1 and token_type in "IDENTIFIER":
                value = token_value
                ast['loop'].append({'name' : token_value})
                ast['loop'].append({'start_value' : self.get_token_value(token_value)})
            
            elif token == 1 and token_type == "DATATYPE":
                #check variale declaration
                if token_stream[token + 1][0] == "IDENTIFIER" and token_stream[token + 2][0] == "OPERATOR" and token_stream[token + 3][0] in ["INTEGER","IDENTIFIER",]:
                    ast['loop'].append({'name' : token_value})
                    ast['loop'].append({'start_value' :token_stream[token + 3][1]})
                    var_decl = True

            elif token == 2 and token_type != "SEPARATOR" and var_decl == False:
                msg = "SEPARATORError: at line:\nMust be '::'"
                self.error_message(msg)

            elif token == 5 and token_type != "SEPARATOR" and var_decl:
                msg = "SEPARATORError: at line:\nMust be '::'"
                self.error_message(msg)
			
            elif (token == 3 and token_value != value):
                print(token_value, [ast['loop'][2]['start_value']])
                msg = ("ValueError: at line:\nMust be same as ",[ast['loop'][2]['start_value']])
                self.error_message(msg)
            
            elif token == 4 and token_type != "COMPARTION_OPERATOR" :
                msg = "OperatorError at line:\nMust be operator"
                self.error_message(msg)

            
            elif token == 5 and token_type in ["INTEGER","IDENTIFIER"]:
                ast['loop'].append({'end_value' : token_value})
            
            elif token == 6 and token_type != "SEPARATOR":
                msg = "SeparatorError: at line:\nMust be '::'"
                self.error_message(msg)
            
            elif token == 7 and token_value == value + "++":
                ast['loop'].append({'increment' : "1"})
            
            elif token == 7 and token_value == value + "--":
                ast['loop'].append({'increment' : "-1"})
                       
            tokens_checked += 1

        self.ast['main_scope'].append(ast)

        self.token_index += tokens_checked

        return [ast,tokens_checked]
    
    def parse_func(self,token_stream):
        tokens_checked = 0
        value = ""
        ast = {'function_declaration' : []}
        
        for token in range(0,len(token_stream)):

            token_type = token_stream[tokens_checked][0]
            token_value = token_stream[tokens_checked][1]

            if  token_type == "SCOPE_DEFINIER" and token_value == "{":break
            
            if  token_type == "SCOPE_DEFIENIER" and token_value == "}":break

            if token == 1 and token_type == "IDENTIFIER":
                ast['function_declaration'].append({'name' : token_value})

            elif token == 2 and token_type != "COLON":
                self.error_message("Error:")
            
            elif token == 3 and token_value == "0":
                value = token_value

            elif token == 3 and token_type in ["IDENTIFIER","COMMA"]:
                value = token_value
            
            elif token > 3 and token_type in ["IDENTIFIER","COMMA"]:
                value += token_value
            
            tokens_checked += 1

        self.token_index += tokens_checked
        
        ast['function_declaration'].append({'argument' : value})
        
        self.ast['main_scope'].append(ast)

        return [ast,tokens_checked]

    def parse_comment(self,token_stream,isScope):
        tokens_checked = 0
        comment_str = ""
        ast = {'comment': []}
        
        for token in range(0,len(token_stream)):

            token_type = token_stream[tokens_checked][0]
            token_value = token_stream[tokens_checked][1]

            if  token_type == "COMMENT" and token_value == "**|": break
        
            if token >= 1:
                comment_str += str(token_value) + " "

            tokens_checked+=1
        ast['comment'].append({'Comment_str' : comment_str})

        if inScope == False:
            self.ast['main_scope'].append(ast)
        
        self.token_index += tokens_checked

        return [ast, tokens_checked]
        
    def parse_macros(self,token_stream):
        """TODO
		macros
		{
			define _var x_ {
				x = 0;
			}
			redefine @echo {
                _print_					
			}
		}
        """
        tokens_checked = 0
        
        for token in range(0, len(token_stream)):
			
            ast = {'macros' : []}
            
            if token == 2 and token_type == "SCOPE_DEFINIER":
                pass

#---------------------------BROWSER------------------------------------

    def parse_alert(self,token_stream):

        tokens_checked = 0
        value = ""
        
        for token in range(0,len(token_stream)):

            token_type = token_stream[tokens_checked][0]
            token_value = token_stream[tokens_checked][1]

            if token == 2 and token_type == "SEMIC":break
             
            if token == 1 and token_type == 'STRING':
                value = token_value
            else:
                value = token_value
            
            tokens_checked+=1

        echoObj = BuiltinObject()
        self.transpiled_code += echoObj.transpile_alert(value)

        self.token_index += tokens_checked
#-------------------------------CALL FUNCTION------------------------------
    def find_func(self,token_stream):
        tokens_checked = 0
        
        name = ""
        argument = ""
        
        for token in range(0,len(token_stream)):

            token_type = token_stream[tokens_checked][0]
            token_value = token_stream[tokens_checked][1]
            
            if  token_type == "SEMIC":break

            elif token == 1  and token_type != "IDENTIFIER":
                self.error_message("Error")

            elif token == 1 and token_type == "IDENTIFIER":
                name = token_value
            
            elif token == 3 and token_type in ["IDENTIFIER","INTEGER","STRING","BOOLEAN"]:
                argument = token_value
            

            tokens_checked+=1


        funcObj = FuncObject()
        self.transpiled_code += funcObj.transpile_run_func(name,argument)

        self.token_index += tokens_checked
#--------------------------------------------------------------------------

    def error_message(self,msg):
        print(msg)
        quit()
