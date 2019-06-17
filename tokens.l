%{
#include <stdio.h>
%}


TIDENTIFICADOR [a-zA-Z_][a-zA-Z0-9_]*
INTEIRO [0-9]+

%%
"="                    TOKEN(IGUAL);
"<"                    TOKEN(MENOR);
">"                    TOKEN(MAIOR);
"("                    TOKEN(APAR);
")"                    TOKEN(FPAR);
","                    TOKEN(VIRGULA);
"+"                    TOKEN(MAIS);
"-"                    TOKEN(MENOS);
"*"                    TOKEN(MUL);
"/"                    TOKEN(DIV);
inteiro                TOKEN(INTEIRO);
booleano               TOKEN(BOOLEANO);
imprima                TOKEN(IMPRIMA);
fim                    TOKEN(FIM);
nao                    TOKEN(NAO);
e                      TOKEN(E);
ou                     TOKEN(OU);
enquanto               TOKEN(ENQUANTO);
enquantofim            TOKEN(ENQUANTOFIM);
se                     TOKEN(SE);
entao                  TOKEN(ENTAO);
senao                  TOKEN(SENAO);
entrada                TOKEN(ENTRADA);
inicialize             TOKEN(INICIALIZE);
como                   TOKEN(COMO);
subrotina              TOKEN(SUBROTINA);
verdadeiro             TOKEN(VERDADEIRO);
falso                  TOKEN(FALSO);
funcao                 TOKEN(FUNCAO);
chame                  TOKEN(CHAME);
identifier             TOKEN(TIDENTIFICADOR);

.                       printf("Unknown token!n"); yyterminate();
%%