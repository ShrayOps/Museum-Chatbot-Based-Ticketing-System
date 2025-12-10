from googletrans import Translator

# Initialize the translator
translator = Translator()

def translate_text(text, source_lang, target_lang):
    """
    Translate text from source language to target language
    
    Parameters:
    text (str): The text to translate
    source_lang (str): Source language code (e.g., 'en', 'hi', 'mr')
    target_lang (str): Target language code
    
    Returns:
    str: Translated text
    """
    try:
        translation = translator.translate(text, src=source_lang, dest=target_lang)
        return translation.text
    except Exception as e:
        print(f"Translation error: {e}")
        return text  # Return original text if translation fails

# Language dictionary for UI display
LANGUAGES = {
    'en': 'English',
    'hi': 'Hindi',
    'mr': 'Marathi',
    'gu': 'Gujarati',
    'ta': 'Tamil'
}
