import re

def search_regulyar(text):
    '''Функция сканирования текста на наличие регулярных выражений(XXXX XXXXXX, XXX-XXX-XXX XX)'''
    if (re.compile(r'\b({0})\b'.format('(\d{4})\s*[-\s*]\s*(\d{6})'), flags=re.IGNORECASE).search)(text):
        return True
    elif (re.compile(r'\b({0})\b'.format('(\d{3})\s*[-\s*]\s*(\d{3})\s*[-\s*]\s*(\d{3})\s*[-\s*]\s*(\d{2})'),
                     flags=re.IGNORECASE).search)(text):
        return True


def seach_word(text,list_bad_word):
    '''Функция сканирования текста на наличие запрещенных слов'''
    for word in list_bad_word:
        if (re.compile(r'\b({0})\b'.format(word), flags=re.IGNORECASE).search)(text):
            return True