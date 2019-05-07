%{
  #include <stdio.h>
  #include <math.h>
  int yylex (void);
  void yyerror (char const *);
%}

%%
function-definition : {declaration-specifier}* declarator {declaration}* compound-statement
;

declaration-specifier : type-specifier
;
        
type-specifier : 
    VOID
    | INT
    | FLOAT

;

conditional-expression: 
    logical-or-expression
    | logical-or-expression ? expression : conditional-expression
;

logical-or-expression : logical-and-expression
                          | logical-or-expression || logical-and-expression
;

logical-and-expression : inclusive-or-expression
                           | logical-and-expression && inclusive-or-expression
;
and-expression : equality-expression
                   | and-expression & equality-expression
;
equality-expression : equality-expression CEQUAL relational-expression
                        | equality-expression NEQUAL relational-expression
;
additive-expression : multiplicative-expression
                        | additive-expression PLUS multiplicative-expression
                        | additive-expression MINUS multiplicative-expression
;
multiplicative-expression : cast-expression
                              | multiplicative-expression MUL cast-expression
                              | multiplicative-expression DIV cast-expression
;
cast-expression : unary-expression
                    | OPARENT type-name CPARENT cast-expression
;
unary-expression :   | INC unary-expression
                     | DEC unary-expression
                     | unary-operator cast-expression
;

expression : assignment-expression
               | expression , assignment-expression
;
assignment-expression : conditional-expression
                          | unary-expression assignment-operator assignment-expression
;
assignment-operator : EQUAL
                        | MULEQUAL
                        | DIVEQUAL
                        | PLUSEQUAL
                        | MINUSEQUAL
;
unary-operator :  PLUS
                    | MINUS
;
compound-statement : OBRACE {declaration}* {statement}* CBRACE
;
statement : labeled-statement
              | expression-statement
              | compound-statement
              | selection-statement
              | iteration-statement
;

expression-statement : {expression}?;
;
selection-statement : se OPARENT expression CPARENT statement
                        | se OPARENT expression CPARENT statement senao statement
;

iteration-statement : enquanto OPARENT expression CPARENT statement
                        | para OPARENT {expression}? ; {expression}? ; {expression}? CPARENT statement
;
%%