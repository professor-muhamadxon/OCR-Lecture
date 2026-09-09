import re, sys
from constants import *

def text_correctize(text: str):
    text = text.lower()
    text = text.replace('-\n', '')
    text = re.sub(r"[\n]+", r"\n", text)
    text = re.sub(r"['`ʻʼ]", r"ʼ", text)
    text = re.sub(r"(?P<og>[og])ʼ", r"\g<og>ʻ", text)
    return text

def text_standartize(text: str) -> str:
    # 0. Barcha xarflarni kichik harflarga o'tkazish
    text = text.lower()
    
    # 1. Chiziq va yangi qatordan tozalash
    text = text.replace('-\n', '')
    text = text.replace('\n', ' ')

    # 2. Apostroflarni birlashtirish va o‘g‘ normalizatsiyasi
    text = re.sub(r"['`ʻʼ]", r"ʼ", text)
    text = re.sub(r"(?P<og>[og])ʼ", r"\g<og>ʻ", text)

    # 3. Qisqartmalar va raqamlar uchun nuqtani vaqtincha almashtirish
    text = re.sub(r"\b(?P<sh>[a-zа-яўқғҳ‘ʼ]{1,2})\.\b", r"\g<sh>#", text)
    text = re.sub(r"\b(?P<dg>\d+)\.\b", r"\g<dg>#", text)

    # 4. Qavs, tirnoq va h.k. belgilarni olib tashlash
    text = re.sub(r'[\"“”«»()\[\]{}]', '', text)

    # 5. Haqiqiy gap chegaralarini aniqlab, bo‘lish
    text = re.sub(r'(?P<pt>[\.\?\!:;])\s+', r'\g<pt>\n', text)
    text = re.sub(r'[\n]?(?P<tr>[—])', r'\n\g<tr>', text)

    # 6. Nuqtalarni qaytarish
    text = text.replace(r'#', r'.')
    
    return text
       
def word_standartize(word: str, reverse=False) -> str:
    letters = {
        'gʻ': 'ĝ', 'oʻ': 'ô', 'sh': 'ŝ', 'ch': 'ĉ', 'ng': 'ñ', 'нг': 'ӈ'
    }
    word = word.lower()
    word = re.sub(r"['`ʻʼ]", r"ʼ", word)
    word = re.sub(r"(?P<og>[og])ʼ", r"\g<og>ʻ", word)
    if reverse:
        letters = {v: k for k, v in letters.items()}
    for k, v in letters.items():
        word = word.replace(k, v)

    return word

def word_pattern(word:str)->list:
    pattern = []
    for char in word:
        if char in VOWEL_LETTERS:
            pattern.append("V")
        elif char in CONSONANT_LETTERS:
            pattern.append("C")
        else:
            pattern.append("P")
    return "".join(pattern)

def pattern_combinations(pattern:str)->list:
    results = []
    rules = ["CVCC", "CVC", "VC", "CV", "V"]
    attempts = 0
    max_attempts = len(pattern) * 500
    def helper(remaining, path):
        nonlocal attempts
        attempts += 1
        if attempts > max_attempts:
            return
        if not remaining:
            results.append(path)
            return
        for rule in rules:
            if remaining.startswith(rule):
                helper(remaining[len(rule):], path + [rule])
    helper(pattern, [])
    return results

def score_combination(combinations:list)->list:
    scores = []
    rules = {
        "CVCC" : 1,
        "CVC" : 2,
        "VC" : 1,
        "CV": 2,
        "V": 0,
    }
    for combination in combinations:
        score = 0
        for rule in combination:
            if rule in rules:
                score += rules[rule]
            else:
                score -= 1
        scores.append(score)
    return scores

def syllable_part(word:str, pattern:str)->str:
    cmb = pattern_combinations(pattern)
    if len(cmb) == 0:
        return word
    scr = score_combination(cmb)
    maxi = scr.index(max(scr))
    parts = []
    start = 0
    for rule in cmb[maxi]:
        end = start + len(rule)
        parts.append(word[start:end])
        start = end
    return "-".join(parts)

def word_syllable(word:str)->str:
    word = word_standartize(word)
    ptr = word_pattern(word)
    if "P" not in ptr:
        result = syllable_part(word, ptr)
    else:
        result = []
        splitted = ptr.split("P")
        end = -1
        start = 0
        for part in splitted:
            end = ptr.find("P", end + 1)
            end = len(word) if end == -1 else end
            result.append(syllable_part(word[start:end], part))
            if end < len(word):
                result.append(word[end])
            start = end + 1
            
    return word_standartize("".join(result), reverse=True)


def to_cyrillic(text):
    """Transliterate latin text to cyrillic  using the following rules:
    1. ye = е in the beginning of a word or after a vowel
    2. e = э in the beginning of a word or after a vowel
    3. ц exception words
    4. э exception words
    """
    # These compounds must be converted before other letters
    compounds_first = {
        'ch': 'ч', 'Ch': 'Ч', 'CH': 'Ч',
        # this line must come before 's' because it has an 'h'
        'sh': 'ш', 'Sh': 'Ш', 'SH': 'Ш',
        # This line must come before 'yo' because of it's apostrophe
        'yo‘': 'йў', 'Yo‘': 'Йў', 'YO‘': 'ЙЎ',
    }
    compounds_second = {
        'yo': 'ё', 'Yo': 'Ё', 'YO': 'Ё',
        # 'ts': 'ц', 'Ts': 'Ц', 'TS': 'Ц',  # No need for this, see TS_WORDS
        'yu': 'ю', 'Yu': 'Ю', 'YU': 'Ю',
        'ya': 'я', 'Ya': 'Я', 'YA': 'Я',
        'ye': 'е', 'Ye': 'Е', 'YE': 'Е',
        # different kinds of apostrophes
        'o‘': 'ў', 'O‘': 'Ў', 'oʻ': 'ў', 'Oʻ': 'Ў',
        'g‘': 'ғ', 'G‘': 'Ғ', 'gʻ': 'ғ', 'Gʻ': 'Ғ',
    }
    beginning_rules = {
        'ye': 'е', 'Ye': 'Е', 'YE': 'Е',
        'e': 'э', 'E': 'Э',
    }
    after_vowel_rules = {
        'ye': 'е', 'Ye': 'Е', 'YE': 'Е',
        'e': 'э', 'E': 'Э',
    }
    exception_words_rules = {
        's': 'ц', 'S': 'Ц',
        'ts': 'ц', 'Ts': 'Ц', 'TS': 'Ц',  # but not tS
        'e': 'э', 'E': 'э',
        'sh': 'сҳ', 'Sh': 'Сҳ', 'SH': 'СҲ',
        'yo': 'йо', 'Yo': 'Йо', 'YO': 'ЙО',
        'yu': 'йу', 'Yu': 'Йу', 'YU': 'ЙУ',
        'ya': 'йа', 'Ya': 'Йа', 'YA': 'ЙА',
    }

    # standardize some characters
    # the first one is the windows string, the second one is the mac string
    text = text.replace('ʻ', '‘')

    def replace_soft_sign_words(m):
        word = m.group(1)
        if word.isupper():
            result = SOFT_SIGN_WORDS[word.lower()].upper()
        elif word[0].isupper():
            result = SOFT_SIGN_WORDS[word.lower()]
            result = result[0].upper() + result[1:]
        else:
            result = SOFT_SIGN_WORDS[word.lower()]
        return result

    for word in SOFT_SIGN_WORDS:
        text = re.sub(
            r'\b(%s)' % word,
            replace_soft_sign_words,
            text,
            flags=re.U
        )

    def replace_exception_words(m):
        """Replace ц (or э) only leaving other characters unchanged"""
        return '%s%s%s' % (
            m.group(1)[:m.start(2)],
            exception_words_rules[m.group(2)],
            m.group(1)[m.end(2):]
        )
    # loop because of python's limit of 100 named groups
    for word in list(TS_WORDS.keys()) + list(E_WORDS.keys()):
        text = re.sub(
            r'\b(%s)' % word,
            replace_exception_words,
            text,
            flags=re.U
        )

    # compounds
    text = re.sub(
        r'(%s)' % '|'.join(compounds_first.keys()),
        lambda x: compounds_first[x.group(1)],
        text,
        flags=re.U
    )

    text = re.sub(
        r'(%s)' % '|'.join(compounds_second.keys()),
        lambda x: compounds_second[x.group(1)],
        text,
        flags=re.U
    )

    text = re.sub(
        r'\b(%s)' % '|'.join(beginning_rules.keys()),
        lambda x: beginning_rules[x.group(1)],
        text,
        flags=re.U
    )

    text = re.sub(
        r'(%s)(%s)' % ('|'.join(LATIN_VOWELS),
                       '|'.join(after_vowel_rules.keys())),
        lambda x: '%s%s' % (x.group(1), after_vowel_rules[x.group(2)]),
        text,
        flags=re.U
    )

    text = re.sub(
        r'(%s)' % '|'.join(LATIN_TO_CYRILLIC.keys()),
        lambda x: LATIN_TO_CYRILLIC[x.group(1)],
        text,
        flags=re.U
    )

    return text


def to_latin(text):
    """Transliterate cyrillic text to latin using the following rules:
    1. ц = s at the beginning of a word.
    ц = ts in the middle of a word after a vowel.
    ц = s in the middle of a word after consonant (DEFAULT in CYRILLIC_TO_LATIN)
        цирк = sirk
        цех = sex
        федерация = federatsiya
        функция = funksiya
    2. е = ye at the beginning of a word or after a vowel.
    е = e in the middle of a word after a consonant (DEFAULT).
    3. Сентябр = Sentabr, Октябр = Oktabr
    """
    beginning_rules = {
        'ц': 's', 'Ц': 'S',
        'е': 'ye', 'Е': 'Ye'
    }
    after_vowel_rules = {
        'ц': 'ts', 'Ц': 'Ts',
        'е': 'ye', 'Е': 'Ye'
    }

    text = re.sub(
        r'(сент|окт)([яЯ])(бр)',
        lambda x: '%s%s%s' % (x.group(1),
                              'a' if x.group(2) == 'я' else 'A', x.group(3)),
        text,
        flags=re.IGNORECASE | re.U
    )

    text = re.sub(
        r'\b(%s)' % '|'.join(beginning_rules.keys()),
        lambda x: beginning_rules[x.group(1)],
        text,
        flags=re.U
    )

    text = re.sub(
        r'(%s)(%s)' % ('|'.join(CYRILLIC_VOWELS),
                       '|'.join(after_vowel_rules.keys())),
        lambda x: '%s%s' % (x.group(1), after_vowel_rules[x.group(2)]),
        text,
        flags=re.U
    )

    text = re.sub(
        r'(%s)' % '|'.join(CYRILLIC_TO_LATIN.keys()),
        lambda x: CYRILLIC_TO_LATIN[x.group(1)],
        text,
        flags=re.U
    )

    return text
