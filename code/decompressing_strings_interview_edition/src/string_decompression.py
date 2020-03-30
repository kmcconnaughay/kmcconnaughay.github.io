from typing import List, Tuple

import parsec


def decompress(text: str) -> str:
    """
    Decompresses strings that adhere to the grammar given below.

    The following grammar is given in Backus-Naur Form augmented with regular 
    expressions:

        <compression> ::= <letter><compression> | <block><compression> | ""
        <letter> ::= [A-Za-z]
        <block> ::= <number>"("<compression>")"
        <number> ::= <digit><number> | <digit>
        <digit> ::= [0-9]

    Examples:
        >>> decompress("")
        ''

        >>> decompress("abc")
        'abc'
        
        >>> decompress("10(x)")
        'xxxxxxxxxx'
        
        >>> decompress("abc2(x3(y))zzz")
        'abcxyyyxyyyzzz'

        Every block requires a number:
        >>> decompress("abc(xyz)") 
        Traceback (most recent call last):
            ...
        parsec.ParseError: expected ends with EOF at 0:3

        Every block requires a closing parenthesis:
        >>> decompress("2(x")
        Traceback (most recent call last):
            ...
        parsec.ParseError: expected ends with EOF at 0:0

        Every block requires an opening parenthesis:
        >>> decompress("2x)")
        Traceback (most recent call last):
            ...
        parsec.ParseError: expected ends with EOF at 0:0

    Args:
        text: A string that adheres to the given grammar.

    Returns:
        The decompressed string.

    Raises:
        parsec.ParseError: If the given string does not conform to the given grammar.
    """
    return _compression().parse_strict(text)


def _compression() -> parsec.Parser:
    return parsec.many(parsec.letter() ^ _block()).parsecmap(_evaluate_compression)


def _evaluate_compression(parsed_compression: List[str]) -> str:
    return "".join(parsed_compression)


def _block() -> parsec.Parser:
    @parsec.Parser
    def parse(text, index):
        p = (
            _number() + (parsec.string("(") >> _compression() << parsec.string(")"))
        ).parsecmap(_evaluate_block)
        return p(text, index)

    return parse


def _evaluate_block(parsed_block: Tuple[int, List[str]]) -> str:
    num_repetitions, letters = parsed_block
    return "".join(num_repetitions * letters)


def _number() -> parsec.Parser:
    return parsec.many1(parsec.digit()).parsecmap(_evaluate_number)


def _evaluate_number(parsed_number: List[str]) -> int:
    return int("".join(parsed_number))


if __name__ == "__main__":
    import doctest

    doctest.testmod()
