"""
Definitely NOT break Google's terms of service and use the Google Translate service via automation.
"""
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException

from translator.langs import LANGUAGES

GTRAN_URL = "https://translate.google.com/#view=home&op=translate&sl={sl}&tl={tl}"
DEFAULT_TL = "en"
DEFAULT_SL = "auto"
HEADLESS = Options()
HEADLESS.add_argument("--headless")
BROWSERS = {
    "chrome": webdriver.Chrome,
    "firefox": webdriver.Firefox,
    "safari": webdriver.Safari,
    "edge": webdriver.Edge
}

class Translator():
    """
    Translator service container class.
    Used to control the stack location of the driver object.

    Note that the driver is configured as headless, and implicitely waits up to 2 seconds to find elements.

    :param str browser: select which browser to run, though all are headless. Defaults to Chrome.
    """
    def __init__(self, browser="chrome"):
        self.driver = BROWSERS.get(browser, "chrome")(options=HEADLESS)
        self.driver.implicitly_wait(2)
        self.driver.get(GTRAN_URL.format(sl=DEFAULT_SL, tl=DEFAULT_TL))

    def translate(self, to_translate, target_lang=DEFAULT_TL, source_lang=DEFAULT_SL):
        """
        Translate the text "to translate" into the specified langage from the specified language using the
        Selenium framework. This implementation assumes the Selenium driver is already pointing to the google
        translate page, and simply selects the requested language via URL HTML tag and sends keystrokes.

        :param str to_translate: text to be translated
        :param str target_lang: language to translate to, defaults to english.
        :param str source_lang: language to translate from. Defaults to 'auto'. Results may vary.

        :returns: translated text
        :rtype: str
        """
        if target_lang != DEFAULT_TL or source_lang != DEFAULT_SL:
            target_lang = _get_lang(target_lang)
            source_lang = _get_lang(source_lang)
        self.driver.get(GTRAN_URL.format(sl=source_lang, tl=target_lang))
        sElem = self.driver.find_element_by_id("source")
        sElem.send_keys(to_translate)
        text = None
        try:
            text = self.driver.find_element_by_class_name("translation").text
        except NoSuchElementException:
            text = "Translation taking too long, aborted..."
        return text

    def cleanup(self):
        """
        Cleanup the translation service by closing the Selenium webdriver.
        """
        self.driver.close()


def _get_lang(language):
    """
    Get the Google Translate language code from the list, or use the input if it's already codified.

    :param str language: requested language

    :returns: Google Translate language code or None if requested language is invalid
    :rtype: str|None

    :raises BadLanguageError: if the requested language is not valid
    """
    langcode = LANGUAGES.get(
        language.lower(), language.lower() if language.lower() in LANGUAGES.values() else None
    )
    if not langcode:
        raise BadLanguageError("Language \"%s\" not valid" % language)
    return langcode


class BadLanguageError(Exception):
    """
    Exception raised when invalid language/codes are passed to the translator.
    """

if __name__ == "__main__":
    T = Translator()
    print("Translating")
    print(T.translate("こんにちは世界"))
    T.cleanup()
