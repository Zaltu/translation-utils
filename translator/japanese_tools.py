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

def wrapper():
    class JPStr:
        """
        Essentially a subclass of str to add functionality explicit to Japanese.

        Use the class methods to_romaji, to_hiragana or to_furigana as JPStr factories.
        JPStr(stirng) and to_romaji(string) will return the same thing.

        :param str string: string to improve
        :param str default: do not touch
        """
        _hiragana_conv = __hiragana_conv__()
        _romaji_conv = __romaji_conv__()
        _furigana_conv = __furigana_conv__()
        def __init__(self, string, default="romaji"):
            self.original = string
            self.hiragana = JPStr._hiragana_conv(string)
            self.romaji = JPStr._romaji_conv(string)
            self.furigana = JPStr._furigana_conv(string)
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

        @classmethod
        def to_hiragana(cls, string):
            """
            Factory function to create a JPStr from a string.
            Sets default output type to Hiragana.

            :param str string: string to enrich

            :returns: enriched string
            :rtype: JPStr
            """
            return JPStr(string, default="hiragana")

        @classmethod
        def to_romaji(cls, string):
            """
            Factory function to create a JPStr from a string.
            Sets default output type to Romaji.

            Behaves the same as JPStr(string)

            :param str string: string to enrich

            :returns: enriched string
            :rtype: JPStr
            """
            return JPStr(string)

        @classmethod
        def to_furigana(cls, string):
            """
            Factory function to create a JPStr from a string.
            Sets default output type to Furigana.

            :param str string: string to enrich

            :returns: enriched string
            :rtype: JPStr
            """
            return JPStr(string, default="furigana")
    return JPStr
