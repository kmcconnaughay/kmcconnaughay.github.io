import parsec
import pytest

from src.string_decompression import decompress


def test_decompress_emptyInput_returnsInput():
    assert decompress("") == ""


def test_decompress_noNesting_returnsInput():
    assert decompress("abc") == "abc"


def test_decompress_oneLevelOfNesting_expandsNestedInput():
    assert decompress("a4(b)c") == "abbbbc"


def test_decompress_blockRepeatedZeroTimes_returnsEmptyString():
    assert decompress("0(xyz)") == ""


def test_decompress_twoLevelsOfNesting_expandsNestedInput():
    assert (
        decompress("a2(bc10(de)f)") == "abcdedededededededededefbcdedededededededededef"
    )


def test_decompress_multipleCompressedBlocks_expandsInput():
    assert decompress("2(a)xyz3(b)") == "aaxyzbbb"


def test_decompress_extraOpenParenthesis_throwsParseException():
    with pytest.raises(parsec.ParseError):
        decompress("a2(b)3(c")


def test_decompress_extraClosingParenthesis_throwsParseException():
    with pytest.raises(parsec.ParseError):
        decompress("3(c)(de")


def test_decompress_missingNumber_throwsParseException():
    with pytest.raises(parsec.ParseError):
        decompress("abc(xyz)")
