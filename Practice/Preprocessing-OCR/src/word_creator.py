import csv
import re
from collections import defaultdict
from tqdm import tqdm

UZ_LETTERS_ORDER = [
    "a","b","d","e","f","g","h","i","j","k","l","m",
    "n","o","p","q","r","s","t","u","v","x","y","z",
    "oʻ","gʻ", "sh","ch","ng"
]

# -------------------
# Normalizatsiya
# -------------------
def normalize(word: str) -> str:
    word = word.strip().lower()
    word = re.sub(r"[ʻ'ʼ`]", "ʼ", word)
    word = word.replace("oʼ", "oʻ").replace("gʼ", "gʻ")
    return word

# -------------------
# Fayllarni yuklash
# -------------------
def load_names(path):
    names = set()
    with open(path, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            if "uzname" in row and row["uzname"]:
                names.add(normalize(row["uzname"]))
    return names

def load_capitals(path):
    with open(path, "r", encoding="utf-8") as f:
        return {normalize(line).lower() for line in f if line.strip()}

def load_uil(path):
    with open(path, "r", encoding="utf-8") as f:
        return {normalize(line) for line in f if line.strip()}

def load_all_words(path):
    words = {}
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            parts = line.strip(" \n").split("\t")
            if len(parts) == 2:
                word, count = parts
                words[normalize(word)] = int(count)
            elif len(parts) == 1:
                words[normalize(parts[0])] = 0
    return words

# -------------------
# O‘zaklarni tayyorlash (alfavit + uzunlik teskari)
# -------------------
def prepare_lemmas(lemmas):
    grouped = defaultdict(list)
    for lemma in lemmas:
        if not lemma:
            continue
        grouped[lemma[0]].append(lemma)
    for k in grouped:
        grouped[k] = sorted(grouped[k], key=lambda x: (-len(x), x))
    return grouped

# -------------------
# Eng uzun mos o‘zakni topish
# -------------------
def find_lemma(word, grouped):
    first = word[0]
    if first not in grouped:
        return None
    for lemma in grouped[first]:
        parts = word.split("-")  # defisli so‘zlar uchun
        for part in parts:
            if part.startswith(lemma):
                if len(lemma) == 1 and part != lemma and word != "u":
                    return None
                return lemma
    return None

def uzsort(words):
    sorted_dict = {}
    sorted_list = []
    for word, count in words:
        word = normalize(word)
        letter = word[:2]
        if letter in UZ_LETTERS_ORDER:
            if letter not in sorted_dict:
                sorted_dict[letter] = []
            sorted_dict[letter].append((word, count))
        else:
            letter = word[0]
            if letter in UZ_LETTERS_ORDER:
                if letter not in sorted_dict:
                    sorted_dict[letter] = []
                sorted_dict[letter].append((word, count))
    for letter in UZ_LETTERS_ORDER:
        if letter in sorted_dict:
            sorted_list.extend(sorted_dict[letter])
    return sorted_list

# -------------------
# Asosiy jarayon
# -------------------
def extract_top_words(all_words_path, uil_path, capital_path, names_path, output_path, limit=500_000, min_count_outside=100):
    print("⏳ Fayllar yuklanmoqda...")
    names = load_names(names_path)
    capitals = load_capitals(capital_path)
    uil = load_uil(uil_path)
    all_words = load_all_words(all_words_path)
    # path = "dataset/suzlik/fitz/all_words_by_count.tsv"
    # all_words = load_all_words(path)
    # all_clear_words = load_all_words(all_words_path)
    
    # filtred_words = {}
    # for word, count in tqdm(all_words.items(), desc="filtring"):
    #     if word in all_clear_words or count >= 5:
    #         filtred_words[word] = count
    
    # with open("dataset/suzlik/checking/all_clear_words_count_sorted.tsv", "w", encoding="utf-8") as file:
    #     filtred_list = sorted(list(filtred_words.items()), key=lambda x: x[0])
    #     filter_dict = dict()
    #     for word, count in tqdm(filtred_list):
    #         word = normalize(word)
    #         letter = word[:2]
    #         if letter in UZ_LETTERS_ORDER:
    #             if letter not in filter_dict:
    #                 filter_dict[letter] = []
    #             filter_dict[letter].append((word, count))
    #         else:
    #             letter = word[0]
    #             if letter in UZ_LETTERS_ORDER:
    #                 if letter not in filter_dict:
    #                     filter_dict[letter] = []
    #                 filter_dict[letter].append((word, count))
    #     for letter in UZ_LETTERS_ORDER:
    #         if letter in filter_dict:
    #             for word, count in filter_dict[letter]:
    #                 file.write(f"{word}\t{count}\n")
    # all_words = filtred_words
    # all_clear_words = None

    print("📑 O‘zaklarni tayyorlash...")
    grouped_lemmas = prepare_lemmas(uil)

    print("🔎 So‘zlarni moslashtirish...")
    collected = {}
    all_words = sorted(list(all_words.items()), key=lambda x: x[0])

    for word, count in tqdm(all_words, desc="so'zlar aniqlanmoqda"):
        lemma = find_lemma(word, grouped_lemmas)
        if re.match(r"[а-я]+", word) == None:
            continue
        if lemma:  # bazaviy korpusga tegadi
            collected[word] = collected.get(word, 0) + count
        elif word in names or word in capitals:  # ismlar va joy nomlari
            collected[word] = collected.get(word, 0) + count
        elif count >= min_count_outside:  # korpusda yo‘q, lekin ko‘p ishlatilgan
            collected[word] = collected.get(word, 0) + count

    print(f"✅ Umumiy yig‘ilgan so‘zlar: {len(collected)}")

    # Chastota bo‘yicha saralash
    sorted_words = uzsort(collected.items())

    # Limit
    if limit != None:
        top_words = sorted_words[:limit]
    else:
        top_words = sorted_words

    # Natijani yozish
    with open(output_path, "w", encoding="utf-8") as f:
        for word, count in top_words:
            if count >= min_count_outside:
                f.write(f"{word}\t{count}\n")
    
    

    print(f"📂 {output_path} fayliga {len(top_words)} ta so‘z yozildi.")


def find_symmetric_va(filepath):
    results = []
    with open(filepath, "r", encoding="utf-8") as f:
        for line in f:
            text = normalize(line.strip())
            if "va" in text:
                parts = text.split("va")
                if len(parts) == 2:
                    left, right = parts
                    left_len, right_len = len(left), len(right)
                    # "deyarli bir xil" sharti: uzunlik farqi <= 2
                    if abs(left_len - right_len) <= 2:
                        results.append((text, left, right))

    with open("symmetric_va.txt", "w", encoding="utf-8") as f:
        for full, left, right in results:
            f.write(f"{full}\t({left}) <va> ({right})\n")

    print(f"✅ {len(results)} ta simmetrik 'va' topildi. Natija symmetric_va.txt faylida.")


# -------------------
# Ishga tushirish
# -------------------
if __name__ == "__main__":
    # filepath = "dataset/suzlik/checked/90K_UIL.txt"
    # found = find_symmetric_va(filepath)
    extract_top_words(
        all_words_path="dataset/suzlik/checking/all_clear_words_count_sorted.tsv",
        uil_path="dataset/suzlik/checked/90K_UIL.txt",
        capital_path="dataset/suzlik/checked/capital_words.txt",
        names_path="dataset/suzlik/checked/ismlar.csv",
        output_path="dataset/suzlik/checked/filtred_words.tsv",
        limit=None,
        min_count_outside=5
    )
