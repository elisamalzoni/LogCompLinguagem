%{
    extern int yylex();
    void yyerror(const char *s) { printf("ERROR: %sn", s); }
%}

%token <string> TIDENTIFICADOR TINTEIRO TBOOLEANO
%token <token> IGUAL MENOR MAIOR 
%token <token> APAR FPAR VIRGULA
%token <token> MAIS MENOS MUL DIV 
%token <token> INTEIRO BOOLEANO IMPRIMA FIM 
%token <token> NAO E OU 
%token <token> ENQUANTO ENQUANTOFIM ENTAO SE SENAO ENTRADA INICIALIZE COMO SUBROTINA VERDADEIRO FALSO FUNCAO CHAME


%start program

%%

program : subdec | funcdec | program
        ;
b :
  | TIDENTIFICADOR COMO type a
  ;

a : 
  | a
  | VIRGULA TIDENTIFICADOR COMO type
  ;

subdec : SUBROTINA TIDENTIFICADOR APAR b a FPAR statement FIM SUBROTINA
       ;

funcdec : FUNCAO TIDENTIFICADOR APAR b a FPAR COMO type statement FIM FUNCAO;

c :
  | SENAO  statement
  ;

d :
  |VIRGULA relexp d
  ;

ea :
  | relexp d
  ;

statement :
          | statement
          | TIDENTIFICADOR IGUAL relexp
          | IMPRIMA relexp
          | INICIALIZE TIDENTIFICADOR COMO type
          | ENQUANTO relexp statement ENQUANTOFIM
          | SE relexp ENTAO statement c FIM SE
          | CHAME TIDENTIFICADOR APAR ea FPAR
          ;


type : INTEIRO | BOOLEANO
     ;
comp : IGUAL | MAIOR | MENOR;

relexp : expression
       | comp expression
       ;

mate : MAIS | MENOS | OU;

expression : term
           | term mate term
           ;

matema : MUL | DIV | E;

term : factor 
     | factor matema factor
     ;

bool : VERDADEIRO | FALSO;

g : 
  | APAR ea FPAR
  ;

j : MAIS | MENOS | NAO;

h : APAR  relexp  FPAR;

factor : INTEIRO 
      | bool
      | TIDENTIFICADOR g
      | j factor
      | h
      | ENTRADA
      ;

%%