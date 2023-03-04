import logging
from pathlib import Path
from cpl_parser import CplParser
from cpl_lexer import CplLexer
from cpl_ast import Program
from argparse import ArgumentParser

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
    
    lexer = CplLexer()
    tokens = lexer.tokenize(source)
    
    parser = CplParser()
    prog: Program = parser.parse(tokens)

    print(prog)
    prog.visit()
    assert prog.code is not None and prog.success
    prog.code.write(file_path.parent / (file_path.stem + '.quad'))
    