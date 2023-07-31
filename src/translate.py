from deep_translator import GoogleTranslator, LibreTranslator, ChatGptTranslator
import pysubs2

from src.utils import get_logger, init_logger
_logger = get_logger()


def translate_subs(in_path, out_path, source='auto', target='en'):

    translator = GoogleTranslator(source=source, target=target)
    _logger.info("%s translator loaded.", 'google')
  
    subs = pysubs2.load(in_path, encoding="utf-8")

    for sub in subs:
        translate = translator.translate(text=sub.text) 
        if translate:
            sub.text = translate
        else:            
            _logger.debug("Fail to translate: %s", sub.text)
            sub.text = ''

    subs.save(out_path)
    _logger.info("File %s saved", out_path)
