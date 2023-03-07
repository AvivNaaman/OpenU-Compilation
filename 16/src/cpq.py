"""
Main entry point for the CPL to Quad compiler.
"""

import logging
from pathlib import Path

import sly
from cpl_parser import CplParser
from cpl_lexer import CplLexer
from cpl_ast import Program
from argparse import ArgumentParser

STUDENT_NAME = "Aviv Naaman"

if __name__ == '__main__':
    logger = logging.getLogger()
    
    arg_parser = ArgumentParser()
    arg_parser.add_argument('file', metavar='f', help='Path to CPL source file to compile.')
    args = arg_parser.parse_args()
    file_path = Path(args.file)
    try:
        with open(file_path, 'r') as f:
            source = f.read()
    except IOError:
        logger.error("Failed to open source file %s" % str(file_path))
        exit(-1)
    except Exception:
        raise
    
    # Tokenize + Parse
    lexer = CplLexer()
    parser = CplParser()
    try:
        tokens = lexer.tokenize(source)
        prog: Program = parser.parse(tokens)
    except sly.lex.LexError as e:
        logger.error("Lexical error: %s" % e)
        exit(1)
    
    if prog is None:
        logger.error("Parsing failed. View output above for more information.")
        exit(1)

    # To generate code for the program, visit the AST's nodes.
    success = prog.visit()
    
    # Check if the program was successfully compiled.
    if not success or prog.code is None:
        logger.error("Compilation failed due to semantic error. View output above for more information.")
        exit(1)

    # Write final output file
    try:
        prog.code.write(file_path.parent / (file_path.stem + '.quad'), STUDENT_NAME)
    except IOError:
        logger.error("Compilation succeeded, but failed to write output file %s." % str(file_path))
        exit(1)

    # Write student's name to stderr
    logger.error(STUDENT_NAME)
