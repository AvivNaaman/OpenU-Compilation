import logging
from cpl_parser import CplParser
from lexer import CplLexer
from cpl_ast import Program
from argparse import ArgumentParser
if __name__ == '__main__':
    lexer = CplLexer()
    parser = CplParser()
    logger = logging.getLogger()
    
    arg_parser = ArgumentParser()
    arg_parser.add_argument('file', metavar='f', help='Path to CPL source file to compile.')
    args = arg_parser.parse_args()
    
    try:
        with open(args.file, 'r') as f:
            source = f.read()
        tokens = lexer.tokenize(source)
        prog: Program = parser.parse(tokens)
        print(prog)
        prog.visit()
    except IOError:
        logger.error("Failed to open source file %s" % args.file)
        exit(-1)
    except Exception:
        raise