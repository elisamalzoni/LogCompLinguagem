```
Program = {SubDec | FuncDec}

SubDec = subrotina, identifier, '(', [identifier, como, Type,{',', identifier, como, Type}], ')', '\n', {statement, '\n'}, fim, subrotina;

FuncDec = funcao, identifier, '(', [identifier, como, Type], [',', identifier, como, Type], ')', como, Type, '\n', {statement, '\n'}, fim, funcao;

Statement = λ 
          | ( identifier, '=', Rel. Exp. ) | (imprima, Rel. Exp.) 
          | (inicialize, identifier, como, type) 
          | (enquanto, Rel. Exp, '\n', {statement, '\n'}, enquantofim) 
          | (se, Rel. Exp., entao, '\n', {statement, '\n'}, [senao, '\n', {statement, '\n'}] , fim, se) 
          | (chame, identifier, '(', [Rel. Exp. {',', Rel. Exp.}], ')');

Type = inteiro | booleano;

Rel. Exp. = Expression, [ ('=' | '>' | '<') , expression ];

Expression = Term, { ('+' | '-'| 'ou') , Term };

Term = Factor, { ('*' | '/' | 'e') , Factor };

Fator = número
      | (verdadeiro | falso) 
      | identifier ['(', [Rel. Exp. {',', Rel. Exp.}], ')']
      | ( ( '+' | '-' |'nao') , Factor ) 
      | ( '(' , Rel. exp. , ')' ) 
      | entrada;
```
