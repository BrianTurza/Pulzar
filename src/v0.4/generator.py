"""
©Pulzar 2018-20

#Author : Brian Turza
version: 0.4
#Created : 14/9/2019
"""
from Lib.fmath import *
from Obj.varObject import VarObject
from Obj.builtinObject import BuiltinObject
from Obj.loopObject import LoopObject
from Obj.functionObject import FuncObject, RunFuncObject
from Obj.conditionalObject import ConditionalObject
from Obj.libObject import libObject
from Obj.returnObject import ReturnObject
from Obj.scopeObject import ScopeObject

import math
import os


class Generation:
    def __init__(self, source_ast, isConsole):
        self.transpiled_code = ""
        self.isConsole = isConsole

        self.source_ast = source_ast['main_scope']

    def generate(self):
        if self.isConsole == True:
            for ast in self.source_ast:
                if self.check_ast('variable_declaration', ast):
                    var = VarObject(ast)
                    self.transpiled_code += var.transpile() + "\n"

                if self.check_ast('conditional_statement', ast):
                    condition = ConditionalObject(ast, 1)
                    self.transpiled_code += condition.transpile() + "\n"

                if self.check_ast('builtin_function', ast):
                    builtin = BuiltinObject(ast)
                    self.transpiled_code += builtin.transpile() + "\n"

                if self.check_ast('loop', ast):
                    loop = LoopObject(ast, 1)
                    self.transpiled_code += loop.transpile() + "\n"

                if self.check_ast('function_declaration', ast):
                    func = FuncObject(ast, 1)
                    self.transpiled_code += func.transpile() + "\n"

                if self.check_ast('call_function', ast):
                    func = RunFuncObject(ast)
                    self.transpiled_code += func.transpile() + "\n"

                if self.check_ast('return', ast):
                    return_ = ReturnObject(ast)
                    self.transpiled_code += return_.transpile() + "\n"
        else:
            self.transpiled_code = """
from flask import Flask
app = Flask(__name__)

@app.route("/")
def hello():
"""
            for ast in self.source_ast:
                if self.check_ast('variable_declaration', ast):
                    var = VarObject(ast)
                    self.transpiled_code += "\t" + var.transpile() + "\n"

                if self.check_ast('conditional_statement', ast):
                    condition = ConditionalObject(ast, 1)
                    self.transpiled_code += "\t" + condition.transpile() + "\n"

                if self.check_ast('builtin_function', ast):
                    builtin = BuiltinObject(ast)
                    self.transpiled_code += "\t" + builtin.transpile() + "\n"

                if self.check_ast('loop', ast):
                    loop = LoopObject(ast, 1)
                    self.transpiled_code += "\t" + loop.transpile() + "\n"

                if self.check_ast('function_declaration', ast):
                    func = FuncObject(ast, 1)
                    self.transpiled_code += "\t" + func.transpile() + "\n"

                if self.check_ast('call_function', ast):
                    func = RunFuncObject(ast)
                    self.transpiled_code += "\t" + func.transpile() + "\n"

                if self.check_ast('return', ast):
                    return_ = ReturnObject(ast)
                    self.transpiled_code += "\t" + return_.transpile() + "\n"

        if self.isConsole == False:
            self.transpiled_code += """
if __name__ == "__main__":
    app.run()
"""
        return self.transpiled_code

    def check_ast(self, astName, ast):
        try:
            if ast[astName]: return True
        except:
            return False
