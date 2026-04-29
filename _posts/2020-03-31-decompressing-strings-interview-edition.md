---
layout: post
title: Decompressing Strings, Interview Edition
---

My worst interview experience happened at $CURRENT_EMPLOYER in early 2016. It was not the fault of
my interviewer. She had been hastily summoned to my room after my original interviewer canceled and,
not ten minutes after she arrived, another rather persistent woman claimed the room for a Very
Important™ meeting with Key Clients™.

Thus began a long trek through the building as we desperately sought an unoccupied room with a
whiteboard. This being $CURRENT_EMPLOYER on a weekday in the middle of the afternoon, such spots
were a coveted and rare commodity. My interviewer made the occassional foray into small talk as we
quested, but I intuited that she felt as panicked as me and our abortive attempts at conversation
eventually ceased.

And lo, twenty minutes later and a mere ten minutes before the end of the interview we found a
suitable space. I rushed to the whiteboard to recreate my first ten minutes of work while also
trying to remember what exactly my interviewer had asked me to solve and wondering whether the lost
time would negatively affect my hiring decision and for _science's_ sake what did she ask me to
do...

I did not write anything close to a working solution in that interview, but the _uniqueness_ of the
experience left the problem indelibly imprinted in my psyche. Now, as I self-isolate in the midst of
a global pandemic, I am bored and looking for things to do, so I finally solved it. Take that,
imposter syndrome.

The problem is to decompress strings. Given the string "a2(xy)b", write a `decompress` function that
returns "axyxyb", i.e. duplicate the parts inside parentheses a number of times indicated by the
leading number.

Some necessary clarifications:

- Multiple parenthetical blocks are allowed, e.g. "2(x)3(y)" should expand to "xxyyy".
- Nested parenthetical blocks are allowed, e.g. "2(x3(y))" should expand to "xyyyxyyy".
- If the input is malformed, e.g. a closing parenthesis is missing, the function should throw an
  exception.

This is a parsing problem! And as such the first step is to define the relevant
[grammar](https://w.wiki/6jCG), which will guide us as we implement our parser.

A `<letter>` is a terminal symbol:

```bnf
<letter> ::= [A-Za-z]
```

The above is given in [Backus-Naur Form](https://w.wiki/5ZUC) augmented with
[regular expressions](https://w.wiki/3jKQ). It means that the `<letter>` symbol can be exactly one
of "A", "B", "C", ..., "X", "Y", "Z", "a", "b", "c", ..., "x", "y", or "z".

A `<digit>` is also a terminal symbol.

```bnf
<digit> ::= [0-9]
```

This means that a `<digit>` can be exactly one of 0, 1, 2, 3, 4, 5, 6, 7, 8, or 9.

To represent numbers that have more than one digit, we need to introduce our first recursive (as
opposed to terminal) symbol, `<number>`:

```bnf
<number> :: = <digit><number> | <digit>
```

We can use this to understand numbers with more than one digit. Here's how we might use the
definition to parse "735":

1. Use the left definition, `<digit><number>`. 7 matches the definition of `<digit>` and we try to
   parse 35 according to the definition of `<number>`.
1. Use the left definition again. 3 matches the definition of `<digit>` and we try to parse 5
   according to the definition of `<number>`.
1. Now we only have 5. The left definition no longer applies because there are no digits that follow
   5, so we apply the right definition. 5 matches the definition of `<digit>` and we are finished
   parsing. 735 is three digits.

The next two rules are more complicated, but they are mutually recursive and so must be introduced
together.

```bnf
<compression> ::= <letter><compression> | <block><compression> | ""
<block> ::= <number>"("<compression>")"
```

Though more complicated than the definition of `<number>`, these follow the same basic principles. A
`<compression>` can be a `<letter>` followed by another compressed string, a `<block>` followed by
another compressed string, or the empty string. A `<block>` is a `<number>` followed by an open
parenthesis, then a compressed string (which we just defined), and finally a close parenthesis.

Here is the full grammar:

```bnf
<compression> ::= <letter><compression> | <block><compression> | ""
<letter> ::= [A-Za-z]
<block> ::= <number>"("<compression>")"
<number> ::= <digit><number> | <digit> <digit> ::= [0-9]
```

Try parsing the following strings from the definition of `<compression>`!

1. "a"
1. "a"
1. "ab"
1. "13(x)"
1. "2(x)3(y)"
1. "2(m3(n))"
1. "ab4(x5(y)z)2(mn)"

Let's walk through the last example in detail. Each line is the result of applying one definition to
the string and we already know that we start with a `<compression>`

1. "ab4(x5(y)z)2(mn)" is a `<compression>`
1. "a" is a `<letter>` and "b4(x5(y)z)2(mn)" is a `<compression>`
1. "b" is a `<letter>` and "4(x5(y)z)2(mn)" is a `<compression>`
1. "4(x5(y)z)" is a `<block>` and "2(mn)" is a `<compression>`
1. "2(mn)" is a `<block>`

We can continue to break down the string "4(x5(y)z)" that we found:

1. "4(x5(y)z)" is a `<block>`
1. "4" is a `<number>`, "(" is an open parenthesis, "x5(y)z" is a `<compression>`, and ")" is a
   close parenthesis

And we could continue to break down the string "x5(y)z" we found in the last step, but I'll leave
that as an exercise to the (inhumanly) diligent reader.

Of course, just understanding the structure of a given string isn't enough. We also need to evaluate
it to get the final decompressed string. In the examples above, this is what we'd like the output of
our `decompress` function to be:

1. "a"
1. "ab"
1. "xxxxxxxxxxxxx"
1. "xxyyy"
1. "mnnnmnnn"
1. "abxyyyyyzxyyyyyzxyyyyyzxyyyyyzmnmn"

We are finally at the point where we can start writing code. For the sake of my personal erudition I
decided to use a neat little Python library called [Parsec](https://pythonhosted.org/parsec/). It
provides a selection of [parser combinators](https://w.wiki/MPD6) that ease the development of
bespoke parsers.

Let's again start simply. How do we parse a letter?

```python
import parsec

parsec.letter().parse("a") # returns "a"
parsec.letter().parse("1") # throws an exception
```

Neat. And a digit?

```python
parsec.digit().parse("1") # returns "1"
parsec.digit().parse(")") # throws an exception
```

Okay, those are easy. What about parsing a number, which can have many digits?

```python
parsec.many1(parsec.digit()).parse("123") # returns ["1", "2", "3"]
parsec.many1(parsec.digit()).parse("3a4") # throws an exception
```

The `parsec.many1` function accepts a parser as an argument and returns another parser that uses the
argument one to many times. However, the output isn't quite what we want. We don't want a list of
strings of digits, we want a real integer. We can write an `_evaluate_number` function to do this:

```python
from typing import *

def _evaluate_number(parsed_number: List[str]) -> int:
    return int("".join(parsed_number))
```

Given a list of strings, the `_evaluate_number` function concatenates them and casts the result to
an integer. Let's combine our parser and evaluator:

```python
def _number() -> parsec.Parser():
    return parsec.many1(parsec.digit()).parsecmap(_evaluate_number)

_number().parse("543") # returns 543
```

To simplify things, let's assume that we have a function that provides a `<block>` parser:

```python
def _block() -> parsec.Parser:
    # We'll implement this soon
    pass
```

Let's use it to write a `<compression>` parser:

```python
def _compression() -> parsec.Parser:
    return parsec.many(parsec.letter() ^ _block())
```

The `^` operator takes two parsers and returns a new parser that, when given input, tries the parser
on the left and, if that fails, tries the parser on the right. The `parsec.many` function is almost
identical to the `parsec.many1` function, except that `parsec.many1` must use its parser at least
once while `parsec.many` can use its parser zero times. So, in literate English, the `_compression`
function returns a parser that matches either a letter or a block zero or more times.

Now we can return to the definition of the block parser. Let's try the obvious definition:

```python
def _block() -> parsec.Parser:
    return _number() + (
        parsec.string("(") >> _compression() << parsec.string(")")
    )
```

There's a lot going on here, so let's examine each part. The `+` operator combines two parsers.
First it runs the parser on the left side of the operator, then it runs the parser on the right side
of the operator, and last it returns the results of both parsers. The `>>` operator takes two
parsers and discards the result of the parser on the left side of the operator. Similarly, the `<<`
operator takes two parsers and discards the result of the parser on the right side of the operator.
So `parsec.string("(") >> _compression() << parsec.string(")")` is a parser that matches an open
parenthesis, a `<compression>`, and a close parenthesis but only retains the output of the
`_compression` parser, discarding the parentheses. Thus the entire `_block` function returns a
parser that parses a `<number>` and a `<compression>`.

Unfortunately, the naive definition doesn't work because it recurses forever. Python is an
[eagerly evaluated](https://w.wiki/MPDU) language, so when we invoke the `_compression` function, it
calls the `_block` function which calls the `_compression` function which calls the `_block`
function which calls the `_compression` function...

We can get around this by manually making Python lazy:

```python
def _block() -> parsec.Parser:
    @parsec.Parser
    def parse(text, index) -> Tuple[int, List[str]]:
        p = (
            _number() + (
                parsec.string("(") >> _compression() << parsec.string(")")
            )
        )
        return p(text, index)

    return parse
```

Now the `_block` function returns another function (which the `@parsec.Parser` annotation turns into
a fully-fledged parser) that parses a `<block>` but, crucially, does _not_ invoke that function,
meaning that `_compression` won't be called until it's needed.

Now all that remains is to write accompanying evaluate functions:

```python
def _evaluate_block(parsed_block: Tuple[int, List[str]]) -> str:
    num_repetitions, letters = parsed_block
    return "".join(num_repetitions * letters)

def _evaluate_compression(parsed_compression: List[str]) -> str:
    return "".join(parsed_compression)
```

The `_evaluate_block` function takes a tuple whose first element is the output of the `_number`
parser and whose second element is the output of the `_compression` parser. It then repeats the
output of the `_compression` parser as many times as indicated by the `_number` parser.

The `_evaluate_compression` function takes a list of strings that are the outputs of many
invocations of the `parsec.letter` parser and our `_block` parser, concatenates the strings, and
returns the result.

We can plug the evaluate functions into our parsers with `parsecmap`:

```python
def _block() -> parsec.Parser:
    @parsec.Parser
    def parse(text, index) -> str:
        p = (
            _number() + (
                parsec.string("(") >> _compression() << parsec.string(")")
            )
        ).parsecmap(_evaluate_block)
        return p(text, index)

    return parse

def _compression() -> parsec.Parser:
    return parsec.many(
        parsec.letter() ^ _block()
    ).parsecmap(_evaluate_compression)
```

Et voilà, we have a fully fledged parser! We can write a `decompress` function which satisfies the
definition given in the original problem:

```
def decompress(text: str) -> str:
    return _compression().parse_strict(text)

decompress("abc") # returns "abc"
decompress("2(xy)") # returns "xyxy"
decompress("a2(x3(y)z)b") # returns "axyyyzxyyyzb"
```

Here is the full code:

```python
def decompress(text: str) -> str:
    return _compression().parse_strict(text)

def _compression() -> parsec.Parser:
    return parsec.many(
        parsec.letter() ^ _block()
    ).parsecmap(_evaluate_compression)

def _evaluate_compression(parsed_compression: List[str]) -> str:
    return "".join(parsed_compression)

def _block() -> parsec.Parser:
    @parsec.Parser
    def parse(text, index) -> str:
        p = (
            _number() + (
                parsec.string("(") >> _compression() << parsec.string(")")
            )
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
```

Note that you should <i>definitely</i> not use this code in any kind of production system; there are
better ways to compress data and this code is vulnerable to things like the
<a href="https://en.wikipedia.org/wiki/Billion_laughs_attack">billion laughs attack</a>. But it was
fun to learn more about parsers and to slay some of my closeted dragons.

Until next time, adieu.
