#ifndef _DRIVER_H
#define _DRIVER_H
#include <string>
#include <map>
#include "parser.h"

// Give Flex the prototype of yylex we want ...
#define YY_DECL \
    yy::parser::symbol_type yylex (sql::Parser& drv)
// ... and declare it for the parser's sake.
YY_DECL;

namespace sql {

// Conducting the whole scanning and parsing of Calc++.
class Parser
{
public:
    Parser ();

    std::map<std::string, int> variables;

    int result;

    // Run the parser on file F.  Return 0 on success.
    int parse (const std::string& f);
    // The name of the file being parsed.
    std::string file;
    // Whether to generate parser debug traces.
    bool trace_parsing;

    // Handling the scanner.
    void scan_begin ();
    void scan_end ();
    // Whether to generate scanner debug traces.
    bool trace_scanning;
    // The token's location used by the scanner.
    yy::location location;
};

}

#endif // _DRIVER_H
