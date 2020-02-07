"""
Tools to help with representation and translation of Japanese.
"""
import pykakasi

def __romaji_conv__():
    """
    Generate romaji converter. Private hidden function.
    :returns: romaji converter
    :rtype: pykakasi.Converter
    """
    kakasi = pykakasi.kakasi()
    kakasi.setMode("J", "a")
    kakasi.setMode("H", "a")
    kakasi.setMode("K", "a")
    kakasi.setMode("s", True)
    return kakasi.getConverter().do
_ROMAJI_CONV = __romaji_conv__()

def __furigana_conv__():
    """
    Generate furigana converter. Private hidden function.
    :returns: romaji converter
    :rtype: pykakasi.Converter
    """
    kakasi = pykakasi.kakasi()
    kakasi.setMode("J", "aF")
    kakasi.setMode("H", "aF")
    kakasi.setMode("K", "aF")
    kakasi.setMode("s", True)
    return kakasi.getConverter().do
_FURIGANA_CONV = __furigana_conv__()

def __hiragana_conv__():
    """
    Generate hiragana converter. Private hidden function.
    :returns: romaji converter
    :rtype: pykakasi.Converter
    """
    kakasi = pykakasi.kakasi()
    kakasi.setMode("J", "H")
    kakasi.setMode("H", "H")
    kakasi.setMode("K", "H")
    kakasi.setMode("s", True)
    return kakasi.getConverter().do
_HIRAGANA_CONV = __hiragana_conv__()

class JPStr:
    """
    Essentially a subclass of str to add functionality explicit to Japanese.

    Use the class methods to_romaji, to_hiragana or to_furigana as JPStr factories.
    JPStr(stirng) and to_romaji(string) will return the same thing.

    :param str string: string to improve
    :param str default: do not touch
    """
    def __init__(self, string, default="romaji"):
        self.original = string
        self.hiragana = _HIRAGANA_CONV(string)
        self.romaji = _ROMAJI_CONV(string)
        self.furigana = _FURIGANA_CONV(string)
        self.default = getattr(self, default, self.romaji)

    def __str__(self):
        """
        Default simple string representation.
        Uses whatever the default representation of this JPStr instance is.

        :returns: string representation
        :rtype: str
        """
        return self.default

    def __repr__(self):
        """
        Display all the versions of the text stored within this JPStr.

        :returns: string representation
        :rtype: str
        """
        return f"Original: {self.original}\n"\
        f"Romaji: {self.romaji}\n"\
        f"Hiragana: {self.hiragana}\n"\
        f"Furigana: {self.furigana}\n"

    def __len__(self):
        """
        Length of this string is considered the length of the default representation.

        :returns: length of the default representation
        :rtype: int
        """
        return len(self.default)


def to_hiragana(string):
    """
    Factory function to create a JPStr from a string.
    Sets default output type to Hiragana.

    :param str string: string to enrich

    :returns: enriched string
    :rtype: JPStr
    """
    return JPStr(string, default="hiragana")


def to_romaji(string):
    """
    Factory function to create a JPStr from a string.
    Sets default output type to Romaji.

    Behaves the same as JPStr(string)

    :param str string: string to enrich

    :returns: enriched string
    :rtype: JPStr
    """
    return JPStr(string)


def to_furigana(string):
    """
    Factory function to create a JPStr from a string.
    Sets default output type to Furigana.

    :param str string: string to enrich

    :returns: enriched string
    :rtype: JPStr
    """
    return JPStr(string, default="furigana")
