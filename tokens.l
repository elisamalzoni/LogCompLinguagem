// https://gnuu.org/2009/09/18/writing-your-own-toy-compiler/
%{
#include <string>
#include "node.h"
#include "parser.hpp"
#define SAVE_TOKEN yylval.string = new std::string(yytext, yyleng)
#define TOKEN(t) (yylval.token = t)
extern "C" int yywrap() { }
%}

%%

[ \t\n]                 ;
[a-zA-Z_][a-zA-Z0-9_]*  SAVE_TOKEN; return TIDENTIFIER;
[0-9]+.[0-9]*           SAVE_TOKEN; return TDOUBLE;
[0-9]+                  SAVE_TOKEN; return TINTEGER;
"="                     return TOKEN(EQUAL);
"=="                    return TOKEN(CEQUAL);
"!="                    return TOKEN(NEQUAL);
"<"                     return TOKEN(LT);
"<="                    return TOKEN(LET);
">"                     return TOKEN(GT);
">="                    return TOKEN(GET);
"("                     return TOKEN(OPARENT);
")"                     return TOKEN(CPARENT);
"{"                     return TOKEN(OBRACE);
"}"                     return TOKEN(CBRACE);
"."                     return TOKEN(DOT);
","                     return TOKEN(COMMA);
"+"                     return TOKEN(PLUS);
"-"                     return TOKEN(MINUS);
"*"                     return TOKEN(MUL);
"/"                     return TOKEN(DIV);
"void"                  return TOKEN(VOID);
"int"                   return TOKEN(INT);
"float"                 return TOKEN(FLOAT);
"++"                    return TOKEN(INC);
"--"                    return TOKEN(DEC);
"*="                    return TOKEN(MULEQUAL);
"/="                    return TOKEN(DIVEQUAL);
"+="                    return TOKEN(PLUSEQUAL);
"-="                    return TOKEN(MINUSEQUAL);
""



%%