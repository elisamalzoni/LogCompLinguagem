import re
import sys

reserved = ['IMPRIMA', 'FIM', 'NAO', 'E', 'OU', 'ENQUANTO', 'ENQUANTOFIM', 'SE', 'ENTAO', 'SENAO', 'ENTRADA', 'INICIALIZE', 'COMO', 'INTEIRO', 'BOOLEANO', 'SUBROTINA', 'VERDADEIRO', 'FALSO', 'FUNCAO', 'CHAME']

class SymbolTable():
    def __init__(self, ancestor):
        self.table = {}
        self.ancestor = ancestor
    
    def declareVariable(self, variable_name, variable_type):
        self.table[variable_name] = [None, variable_type]

    def setVariable(self, variable_name, variable_value):
        if variable_name in self.table:
            if self.table[variable_name][1] == variable_value[1]:
                self.table[variable_name][0] = variable_value[0]
            else:
                raise Exception('tipo declarado e tipo setado são diferentes')

        else:
            raise Exception(f'Variavel nao existe',  variable_name)

    def getVariable(self, variable_name):
        if variable_name in self.table:
            if self.table[variable_name][0] == None:
                if self.ancestor == None:
                    raise Exception(f'Variavel nao setada', variable_name)
                else:
                    return self.ancestor.getVariable(variable_name)
            return self.table[variable_name]
        else:
            if self.ancestor == None:
                raise Exception(f'Variavel nao inicializada', variable_name)
            else:
                return self.ancestor.getVariable(variable_name)

class Node():
    def __init__(self):
        self.value = None
        self.children = []

    def Evaluate(self, st):
        pass

class BinOp(Node):
    def __init__(self, value, children):
        self.value = value
        self.children = children

    def Evaluate(self, st):

        if self.children[0].Evaluate(st)[1] == 'INTEIRO' and self.children[1].Evaluate(st)[1] == 'INTEIRO':
            if self.value == '-':
                return (self.children[0].Evaluate(st)[0] - self.children[1].Evaluate(st)[0], 'INTEIRO')

            elif self.value == '+':
                return (self.children[0].Evaluate(st)[0] + self.children[1].Evaluate(st)[0], 'INTEIRO')
            
            elif self.value == '*':
                return (self.children[0].Evaluate(st)[0] * self.children[1].Evaluate(st)[0], 'INTEIRO')

            elif self.value == '/':
                return (self.children[0].Evaluate(st)[0] // self.children[1].Evaluate(st)[0], 'INTEIRO')

            elif self.value == '<':
                return (self.children[0].Evaluate(st)[0] < self.children[1].Evaluate(st)[0], 'BOOLEANO')
            
            elif self.value == '>':
                return (self.children[0].Evaluate(st)[0] > self.children[1].Evaluate(st)[0], 'BOOLEANO')

            elif self.value == '=':
                return (self.children[0].Evaluate(st)[0] == self.children[1].Evaluate(st)[0], 'BOOLEANO')

        elif self.children[0].Evaluate(st)[1] == 'BOOLEANO' and self.children[1].Evaluate(st)[1] == 'BOOLEANO':
            if self.value == '=':
                return (self.children[0].Evaluate(st)[0] == self.children[1].Evaluate(st)[0], 'BOOLEANO')

            elif self.value == 'OU':
                return (self.children[0].Evaluate(st)[0] or self.children[1].Evaluate(st)[0], 'BOOLEANO')

            elif self.value == 'E':
                return (self.children[0].Evaluate(st)[0] and self.children[1].Evaluate(st)[0], 'BOOLEANO')
        else:
            raise Exception('BinOP nao suporta tipos diferentes')

class UnOp(Node):
    def __init__(self, value, children):
        self.value = value
        self.children = children

    def Evaluate(self, st):
        if self.value == '-':
            if self.children[0].Evaluate(st)[1] == 'INTEIRO':
                return  (-self.children[0].Evaluate(st)[0], 'INTEIRO')
            else:
                raise Exception('UnOP - nao pode ser feita com esse tipo')

        elif self.value == '+':
            if self.children[0].Evaluate(st)[1] == 'INTEIRO':
                return (self.children[0].Evaluate(st)[0], 'INTEIRO')
            else:
                raise Exception('UnOP + nao pode ser feita com esse tipo')


        elif self.value == 'NAO':
            if self.children[0].Evaluate(st)[1] == 'BOOLEANO':
                return (not (self.children[0].Evaluate(st))[0], 'BOOLEANO') 
            else:
                raise Exception('UnOP NOT nao pode ser feita com esse tipo')

class IntVal(Node):
    def __init__(self, value, children):
        self.value = value
        self.children = children

    def Evaluate(self, st):
        return (self.value, 'INTEIRO')

class BoolVal(Node):
    def __init__(self, value, children):
        self.value = value
        self.children = children

    def Evaluate(self, st):
        return (self.value, 'BOOLEANO')

class TypeNode(Node):
    def __init__(self, value, children):
        self.value = value
        self.children = children

    def Evaluate(self, st):
        return self.value

class VarDec(Node):
    def __init__(self, value, children):
        self.value = value
        self.children = children

    def Evaluate(self, st):
        st.declareVariable(self.children[0].value, self.children[1].Evaluate(st))

class IdentifierNode(Node):
    def __init__(self, value, children):
        self.value = value
        self.children = children

    def Evaluate(self, st):
        return st.getVariable(self.value)

class AssignmentNode(Node):
    def __init__(self, value, children):
        self.value = value
        self.children = children

    def Evaluate(self, st):
        st.setVariable(self.children[0], self.children[1].Evaluate(st))

class StatementsNode(Node):
    def __init__(self, value, children):
        self.value = value
        self.children = children

    def Evaluate(self, st):
        for child in self.children:
            child.Evaluate(st)

class PrintNode(Node):
    def __init__(self, value, children):
        self.value = value
        self.children = children

    def Evaluate(self, st):
        print(self.children[0].Evaluate(st)[0])

class WhileNode(Node):
    def __init__(self, value, children):
        self.value = value
        self.children = children

    def Evaluate(self, st):
        while self.children[0].Evaluate(st)[0]:
            for c in self.children[1]:
                c.Evaluate(st)
 
class IfNode(Node):
    def __init__(self, value, children):
        self.value = value
        self.children = children

    def Evaluate(self, st):
        if self.children[0].Evaluate(st)[1] == 'BOOLEANO':
            if self.children[0].Evaluate(st)[0]:
                for c in self.children[1]:
                    c.Evaluate(st)
            elif len(self.children) == 3:
                for c in self.children[2]:
                    c.Evaluate(st)
        else:
            print('tipo errado no if')

class InputNode(Node):
    def __init__(self, value, children):
        self.value = value
        self.children = children

    def Evaluate(self, st):
        return (int(input()), 'INTEIRO')

class FuncDec(Node):
    def __init__(self, value, children):
        self.value = value
        self.children = children

    def Evaluate(self, st):
        st.declareVariable(self.value, 'FUNCAO')
        st.setVariable(self.value, [self, 'FUNCAO'])

class SubDec(Node):
    def __init__(self, value, children):
        self.value = value
        self.children = children

    def Evaluate(self, st):
        st.declareVariable(self.value, 'SUBROTINA')
        st.setVariable(self.value, [self, 'SUBROTINA'])


class FuncCall(Node):
    def __init__(self, value, children):
        self.value = value
        self.children = children

    def Evaluate(self, st):
        node = st.getVariable(self.value) ## get especial que busca na raiz

        ste = SymbolTable(st)

        # evaluate dos filho 0
        if node[1] == 'FUNCAO':
            ste.declareVariable(self.value, node[0].children[0].Evaluate(st))

        
        for i in range(1, len(node[0].children)-1):
            node[0].children[i].Evaluate(ste)
            ste.setVariable(node[0].children[i].children[0].value, self.children[i-1].Evaluate(st))
        node[0].children[len(node[0].children)-1].Evaluate(ste)

        if st.getVariable(self.value)[1] == 'FUNCAO':
            return ste.getVariable(self.value)

class NoOp(Node):
    def __init__(self, value, children):
        self.value = value
        self.children = children

    def Evaluate(self, st):
        pass

class Token:
    def __init__(self, type_t, value):
        self.type_t = type_t
        self.value = value

class Tokenizer:
    def __init__(self, origin):
        self.origin = origin
        self.position = 0
        self.actual = self.selectNext()

    def selectNext(self):
        num = ''
        ps = ''
        while self.position < len(self.origin) and (self.origin[self.position]==' '):
            self.position += 1
        if self.position == len(self.origin):
            self.actual = Token('EOF', 'e')
        elif self.origin[self.position].isdigit():
            while self.position < len(self.origin) and self.origin[self.position].isdigit():
                num = num + self.origin[self.position]
                self.position += 1
            self.actual = Token('INTEIRO', num)
        elif self.position < len(self.origin) and self.origin[self.position] == '-':
            self.actual = Token('MINUS', '-')
            self.position += 1
        elif self.position < len(self.origin) and self.origin[self.position] == '+':
            self.actual = Token('PLUS', '+')
            self.position += 1
        elif self.position < len(self.origin) and self.origin[self.position] == '*':
            self.actual = Token('MULT', '*')
            self.position += 1
        elif self.position < len(self.origin) and self.origin[self.position] == '/':
            self.actual = Token('DIV', '/')
            self.position += 1
        elif self.position < len(self.origin) and self.origin[self.position] == '(':
            self.actual = Token('OP', '(')
            self.position += 1
        elif self.position < len(self.origin) and self.origin[self.position] == ')':
            self.actual = Token('CP', ')')
            self.position += 1
        elif self.position < len(self.origin) and self.origin[self.position] == '=':
            self.actual = Token('ASSIGNMENT', '=')
            self.position += 1
        elif self.position < len(self.origin) and self.origin[self.position] == '<':
            self.actual = Token('LESS', '<')
            self.position += 1
        elif self.position < len(self.origin) and self.origin[self.position] == '>':
            self.actual = Token('GREATER', '>')
            self.position += 1
        elif self.position < len(self.origin) and self.origin[self.position] == ',':
            self.actual = Token('COMMA', ',')
            self.position += 1
        elif self.origin[self.position] == '\n':
            self.actual = Token('LB', '\n')
            self.position += 1
        elif self.position < len(self.origin) and self.origin[self.position].isalpha():
            ps += self.origin[self.position]
            self.position += 1
            while self.position < len(self.origin) and (self.origin[self.position].isalpha() or self.origin[self.position].isdigit() or self.origin[self.position] == '_'):
                ps += self.origin[self.position]
                self.position += 1
            ps = ps.upper()
            if ps in reserved:
                if ps == 'INTEIRO' or ps =='BOOLEANO':
                    self.actual = Token('TYPE', ps)
                elif ps == 'VERDADEIRO':
                    self.actual = Token('BOOLEANO', True)
                elif ps == 'FALSO':
                    self.actual = Token('BOOLEANO', False)
                else:
                    self.actual = Token(ps, ps)
            else:
                self.actual = Token('IDENTIFIER', ps)
        else:
            raise Exception('caracter invalido')
        return self.actual

class PrePro:
    def filter(code):
        filtered_code = re.sub("'.*\n", "\n", code)
        # replace tab 4 espacos
        filtered_code_no_tab = re.sub("\t", "    ", filtered_code)
        return filtered_code_no_tab

class Parser:
    
    def parseFactor():
        if Parser.tokens.actual.type_t == 'INTEIRO':
            node = IntVal(int(Parser.tokens.actual.value), [])
            Parser.tokens.selectNext()

        elif Parser.tokens.actual.type_t == 'BOOLEANO':
            node = BoolVal(Parser.tokens.actual.value, [])
            Parser.tokens.selectNext()

        elif Parser.tokens.actual.type_t == 'IDENTIFIER':
            function_name = Parser.tokens.actual.value
            Parser.tokens.selectNext()
            if Parser.tokens.actual.type_t == 'OP':
                Parser.tokens.selectNext()
                listaargs = []
                if Parser.tokens.actual.type_t != 'CP':
                    listaargs.append(Parser.parseRelExpression())

                    while Parser.tokens.actual.type_t == 'COMMA':
                        Parser.tokens.selectNext()
                        listaargs.append(Parser.parseRelExpression())

                if Parser.tokens.actual.type_t == 'CP':
                    Parser.tokens.selectNext()
                    node = FuncCall(function_name, listaargs)
                else:
                    raise Exception('Nao fechou parenteses')
            else:
                node = IdentifierNode(function_name, [])

        elif Parser.tokens.actual.type_t == 'OP':
            Parser.tokens.selectNext()
            node = Parser.parseRelExpression()
            if Parser.tokens.actual.type_t == 'CP':
                Parser.tokens.selectNext()
            else:
                raise Exception('Nao fechou parenteses')
        
        elif Parser.tokens.actual.type_t == 'PLUS':
            Parser.tokens.selectNext()
            node = UnOp('+',[Parser.parseFactor()])

        elif Parser.tokens.actual.type_t == 'MINUS':
            Parser.tokens.selectNext()
            node = UnOp('-',[Parser.parseFactor()])

        elif Parser.tokens.actual.type_t == 'NAO':
            Parser.tokens.selectNext()
            node = UnOp('NAO',[Parser.parseFactor()])

        elif Parser.tokens.actual.type_t == 'ENTRADA':
            Parser.tokens.selectNext()
            node = InputNode('',[])

        else:
            raise Exception('token invalido')

        return node
    
    def parseRelExpression():
        node = Parser.parseExpression()
        if Parser.tokens.actual.type_t == 'LESS':
            Parser.tokens.selectNext()
            node = BinOp('<', [node, Parser.parseExpression()])

        elif Parser.tokens.actual.type_t == 'GREATER':
            Parser.tokens.selectNext()
            node = BinOp('>', [node, Parser.parseExpression()])
        
        elif Parser.tokens.actual.type_t == 'ASSIGNMENT':
            Parser.tokens.selectNext()
            node = BinOp('=', [node, Parser.parseExpression()])

        return node

    def parseTerm():
        node = Parser.parseFactor()
        while Parser.tokens.actual.type_t == 'DIV' or Parser.tokens.actual.type_t == 'MULT' or Parser.tokens.actual.type_t == 'E':
            if Parser.tokens.actual.type_t == 'MULT':
                Parser.tokens.selectNext()
                node = BinOp('*', [node, Parser.parseFactor()])

            elif Parser.tokens.actual.type_t == 'DIV':
                Parser.tokens.selectNext()
                node = BinOp('/', [node, Parser.parseFactor()])

            elif Parser.tokens.actual.type_t == 'E':
                Parser.tokens.selectNext()
                node = BinOp('E', [node, Parser.parseFactor()])

        return node

    def parseExpression():
        node = Parser.parseTerm()
        while Parser.tokens.actual.type_t == 'MINUS' or Parser.tokens.actual.type_t == 'PLUS' or Parser.tokens.actual.type_t == 'OU':
            if Parser.tokens.actual.type_t == 'PLUS':
                Parser.tokens.selectNext()
                node = BinOp('+', [node, Parser.parseTerm()])

            elif Parser.tokens.actual.type_t == 'MINUS':
                Parser.tokens.selectNext()
                node = BinOp('-', [node, Parser.parseTerm()])
            
            elif Parser.tokens.actual.type_t == 'OU':
                Parser.tokens.selectNext()
                node = BinOp('OU', [node, Parser.parseTerm()])

        return node

    def parseType():
        if Parser.tokens.actual.value == 'INTEIRO':
            node = TypeNode('INTEIRO', [])

        elif Parser.tokens.actual.value == 'BOOLEANO':
            node = TypeNode('BOOLEANO', [])
        else:
            raise Exception('tipo inexistente')

        return node

    def parseStatement():
        node = NoOp(None, [])
        if Parser.tokens.actual.type_t == 'IDENTIFIER':
            variable_name = Parser.tokens.actual.value
            Parser.tokens.selectNext()
            if Parser.tokens.actual.type_t == 'ASSIGNMENT':
                Parser.tokens.selectNext()
                variable_value = Parser.parseRelExpression()
                node = AssignmentNode('=',[variable_name, variable_value])

        elif Parser.tokens.actual.type_t == 'IMPRIMA':
            Parser.tokens.selectNext()
            node = PrintNode('IMPRIMA', [Parser.parseRelExpression()])

        elif Parser.tokens.actual.type_t == 'INICIALIZE':
            Parser.tokens.selectNext()
            if Parser.tokens.actual.type_t == 'IDENTIFIER':
                variable_name = IdentifierNode(Parser.tokens.actual.value,[])
                Parser.tokens.selectNext()
                if Parser.tokens.actual.type_t == 'COMO':
                    Parser.tokens.selectNext()
                    if Parser.tokens.actual.value == 'INTEIRO' or Parser.tokens.actual.value == 'BOOLEANO':
                        node = VarDec('vardec', [variable_name, Parser.parseType()])
                        Parser.tokens.selectNext()
                    else:
                        raise Exception('Tipo não suportado')
                else:
                    raise Exception('falta AS depois do nome da variavel')
            else:
                raise Exception('falta nome da variavel depois do DIM')


        elif Parser.tokens.actual.type_t == 'ENQUANTO':
            Parser.tokens.selectNext()
            node = WhileNode('ENQUANTO', [Parser.parseRelExpression(), []])

            if Parser.tokens.actual.type_t == 'LB':
                Parser.tokens.selectNext()
                
                while Parser.tokens.actual.type_t != 'ENQUANTOFIM':
                    node.children[1].append(Parser.parseStatement())
                    Parser.tokens.selectNext()

                    if Parser.tokens.actual.type_t == 'LB':
                        Parser.tokens.selectNext()

                if Parser.tokens.actual.type_t == 'ENQUANTOFIM':
                    Parser.tokens.selectNext()
                else:
                    raise Exception('nao existe wend')
            else:
                raise Exception('sem LB depois do WHILE')  


        elif Parser.tokens.actual.type_t == 'SE':
            Parser.tokens.selectNext()
            node = IfNode('SE', [Parser.parseRelExpression(), []])
            if Parser.tokens.actual.type_t == 'ENTAO':
                Parser.tokens.selectNext()
                if Parser.tokens.actual.type_t == 'LB':
                    Parser.tokens.selectNext()
                    node.children[1].append(Parser.parseStatement())


                    while Parser.tokens.actual.type_t != 'FIM':
                        if Parser.tokens.actual.type_t == 'SENAO':
                            node.children.append([])
                            Parser.tokens.selectNext()
                            while Parser.tokens.actual.type_t != 'FIM':
                                if Parser.tokens.actual.type_t == 'LB':
                                    Parser.tokens.selectNext()
                                else:
                                    raise Exception('sem LB dentro do ELSE')
                        
                                node.children[2].append(Parser.parseStatement())
                                Parser.tokens.selectNext()

                        else:
                            node.children[1].append(Parser.parseStatement())
                            Parser.tokens.selectNext()

                    if Parser.tokens.actual.type_t == 'FIM':
                        Parser.tokens.selectNext()
                        
                        if Parser.tokens.actual.type_t == 'SE':
                            Parser.tokens.selectNext()
                        else:
                            raise Exception('falta IF em END IF')

                    else:
                        raise Exception('nao existe END')

                else:
                    raise Exception('sem LB depois do THEN')
            else:
                raise Exception('falta THEN')

        elif Parser.tokens.actual.type_t == 'CHAME':
            Parser.tokens.selectNext()
            if Parser.tokens.actual.type_t == 'IDENTIFIER':
                function_name = Parser.tokens.actual.value
                Parser.tokens.selectNext()
                if Parser.tokens.actual.type_t == 'OP':
                    Parser.tokens.selectNext()
                    listacall = []
                    while Parser.tokens.actual.type_t != 'CP':
                        listacall.append(Parser.parseRelExpression())
                        if Parser.tokens.actual.type_t == 'COMMA':
                            Parser.tokens.selectNext()
                    if Parser.tokens.actual.type_t == 'CP':
                        node = FuncCall(function_name, listacall)
                else:
                    raise Exception('nao abriu parenteses')
            else:
                raise Exception('sem identifier depois do CALL')
        else:
            node = NoOp(None, [])

        return node

    def parseFuncDec():
        node = NoOp(None, [])
        if Parser.tokens.actual.type_t == 'FUNCAO':
            Parser.tokens.selectNext()
            if Parser.tokens.actual.type_t == 'IDENTIFIER':
                function_name = Parser.tokens.actual.value
                Parser.tokens.selectNext()
                if Parser.tokens.actual.type_t == 'OP':
                    listavar = []
                    Parser.tokens.selectNext() 
                    while Parser.tokens.actual.type_t != 'CP':
                        if Parser.tokens.actual.type_t == 'IDENTIFIER':
                            variable_name = Parser.tokens.actual.value
                            Parser.tokens.selectNext()
                            if Parser.tokens.actual.type_t == 'COMO':
                                Parser.tokens.selectNext()
                                if Parser.tokens.actual.value == 'INTEIRO' or Parser.tokens.actual.value == 'BOOLEANO':
                                    listavar.append(VarDec('vardec', [IdentifierNode(variable_name, []), Parser.parseType()]))
                                    Parser.tokens.selectNext()
                                    if Parser.tokens.actual.type_t == 'COMMA':
                                        Parser.tokens.selectNext()

                                else:
                                    raise Exception('tipo nao suportado')
                            else:
                                raise Exception('falta AS depois do nome da variavel')
                        else:
                            raise Exception('falta nome da variavel')
                                            
                    if Parser.tokens.actual.type_t == 'CP':
                        Parser.tokens.selectNext()
                        if Parser.tokens.actual.type_t == 'COMO':
                            Parser.tokens.selectNext()
                            if Parser.tokens.actual.value == 'INTEIRO' or Parser.tokens.actual.value == 'BOOLEANO':
                                listavar.insert(0,Parser.parseType())
                                Parser.tokens.selectNext()
                                if Parser.tokens.actual.type_t == 'LB':
                                    Parser.tokens.selectNext()
                                    filhosfuncdec = []
                                    while Parser.tokens.actual.type_t != 'FIM':
                                        filhosfuncdec.append(Parser.parseStatement())
                                        Parser.tokens.selectNext()
                                        if Parser.tokens.actual.type_t == 'LB':
                                            Parser.tokens.selectNext()

                                    if Parser.tokens.actual.type_t == 'FIM':
                                        Parser.tokens.selectNext() 
                                        listavar.append(StatementsNode('', filhosfuncdec))
                                        if Parser.tokens.actual.type_t == 'FUNCAO':
                                            Parser.tokens.selectNext() 
                                            node = FuncDec(function_name, listavar)
                                        else:
                                            raise Exception('sem FUNCTION')
                                    else:
                                        raise Exception('sem end')
                                else:
                                    raise Exception('sem LB depois de ()')
                            else:
                                raise Exception('tipo nao suportado')
                        else:
                            raise Exception('sem AS depois do function')
                    else:
                        raise Exception('nao fechou parenteses depois de OP ')
                else:
                    raise Exception('nao abriu parenteses depois da declaracao')
            else:
                raise Exception('nome ruim')
        else:
            raise Exception('sem FUNCTION')

        return node

    def parseSubDec():
        node = NoOp(None, [])
        if Parser.tokens.actual.type_t == 'SUBROTINA':
            Parser.tokens.selectNext()
            if Parser.tokens.actual.type_t == 'IDENTIFIER':
                function_name = Parser.tokens.actual.value
                Parser.tokens.selectNext()
                if Parser.tokens.actual.type_t == 'OP':
                    listavar = [NoOp('', [])]
                    Parser.tokens.selectNext() 
                    while Parser.tokens.actual.type_t != 'CP':
                        if Parser.tokens.actual.type_t == 'IDENTIFIER':
                            variable_name = Parser.tokens.actual.value
                            Parser.tokens.selectNext()
                            if Parser.tokens.actual.type_t == 'COMO':
                                Parser.tokens.selectNext()
                                if Parser.tokens.actual.value == 'INTEIRO' or Parser.tokens.actual.value == 'BOOLEANO':
                                    listavar.append(VarDec('vardec', [IdentifierNode(variable_name, []), Parser.parseType()]))
                                    Parser.tokens.selectNext()
                                    if Parser.tokens.actual.type_t == 'COMMA':
                                        Parser.tokens.selectNext()
                                else:
                                    raise Exception('tipo nao suportado')
                            else:
                                raise Exception('falta AS depois do nome da variavel')
                        else:
                            raise Exception('falta nome da variavel')
                                            
                    if Parser.tokens.actual.type_t == 'CP':
                        Parser.tokens.selectNext()  
                        if Parser.tokens.actual.type_t == 'LB':
                            Parser.tokens.selectNext()
                            filhossubdec = []
                            while Parser.tokens.actual.type_t != 'FIM':
                                filhossubdec.append(Parser.parseStatement())
                                Parser.tokens.selectNext()
                                if Parser.tokens.actual.type_t == 'LB':
                                    Parser.tokens.selectNext()
                            if Parser.tokens.actual.type_t == 'FIM':
                                Parser.tokens.selectNext()
                                listavar.append(StatementsNode('', filhossubdec))
                                if Parser.tokens.actual.type_t == 'SUBROTINA':
                                    Parser.tokens.selectNext() 
                                    node = SubDec(function_name, listavar)
                                else:
                                    raise Exception('sem sub')
                            else:
                                raise Exception('sem end')
                                
                        else:
                            raise Exception('sem LB depois de ()')
                    else:
                        raise Exception('nao fechou parenteses depois de OP ')
                else:
                    raise Exception('nao abriu parenteses depois da declaracao')
            else:
                raise Exception('nome ruim')
        else:
            raise Exception('sem SUB')
        
        return node

    def parseProgram():
        filhosstatements = []
        while Parser.tokens.actual.type_t != 'EOF':
            if Parser.tokens.actual.type_t == 'SUBROTINA':
                filhosstatements.append(Parser.parseSubDec())
            elif Parser.tokens.actual.type_t == 'FUNCAO':
                filhosstatements.append(Parser.parseFuncDec())
            else:
                while Parser.tokens.actual.type_t == 'LB':
                    Parser.tokens.selectNext()
        
        filhosstatements.append(FuncCall('MAIN', []))
        return StatementsNode('', filhosstatements)


    def run(code):
        filtered_code = PrePro.filter(code)
        Parser.tokens = Tokenizer(filtered_code)
        res = Parser.parseProgram()

        return res



# $ python3 main.py test.vbs

# with open('teste.elisa', 'r') as f:
#     exp = f.read() + '\n'

with open(sys.argv[1], 'r') as f:
    exp = f.read() + '\n'

# print(exp)
st = SymbolTable(None)
Parser.run(exp).Evaluate(st)