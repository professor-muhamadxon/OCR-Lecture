from config import *
import utility as u
import convertion as c
import image as i
import pickle
from tqdm import tqdm
import uzbek_language as uz
import os

import multiprocessing as mp


def pdf_to_image(pdf_folder, output_folder):
    pdf_files = u.discover_files(pdf_folder, "pdf")
    method = "fitz"  # or "poppler"
    tasks = u.create_tasks(c.pdf_to_images, pdf_files, output_folder, method, False, None, None)
    wrapper = u.default_wrapper
    u.process_task(wrapper, tasks)
    print(f"Converted {len(pdf_files)} PDFs to images in {output_folder} using method '{method}'.")

def binarize_images(folder, threshold_percent):
    files = u.discover_files(folder, ".png")
    tasks = u.create_tasks(i.binarize_image, files, threshold_percent)
    wrapper = u.default_wrapper

    u.process_task(wrapper, tasks)
    print(f"Binarized {len(files)} images in {folder} with threshold {threshold_percent}%.")

def clip_optimization(folder, box:tuple[int, int, int, int], mirror:bool=False):
    files = u.discover_files(folder, "png")
    tasks = u.create_tasks(i.clip_image, files, box, mirror)
    if mirror != None:
        for task in tasks:
            task[3] = mirror
            mirror = not mirror
    wrapper = u.default_wrapper
    u.process_task(wrapper, tasks)
    print(f"Cropped {len(files)} images in {folder} with box {box} and mirror={mirror}.")

def standart_optimization(folder):
    files = u.discover_files(folder, "png")
    tasks = u.create_tasks(i.standart_optimization, files)
    wrapper = u.default_wrapper
    u.process_task(wrapper, tasks)
    print(f"Optimized {len(files)} images in {folder}.")

def image_to_text(image_folder, text_folder):
    files = u.discover_files(image_folder, "png")
    tasks = u.create_tasks(c.image_to_text, files, text_folder, False)
    wrapper = u.default_wrapper
    u.process_task(wrapper, tasks)
    print(f"Converted {len(files)} images to texts in {text_folder}.")


def load_text_unique(filepath):
    with open(filepath, "r", encoding="utf-8") as f:
        lines = set(f.readlines())
    with open(filepath[:-4] + "_unique,txt", "w", encoding="utf-8") as f:
        for word in lines:
            f.write(word + "\n")
    
def extract_places():
    import os
    import re

    # Asosiy katalog
    base_dir = r"testing/texts/"   # <-- o'zingizning yo'lni yozing

    # Natijalarni yozish uchun fayl
    output_file = "dataset/suzlik/checked/uzbek_capital_words.txt"

    all_words = set()  # takroriy so'zlarni oldini olish uchun

    for root, dirs, files in tqdm(os.walk(base_dir)):
        for file in files:
            if file.endswith(".txt"):
                file_path = os.path.join(root, file)
                with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                    text = f.read()
                    
                    # faqat katta lotin harflardan iborat so'zlarni olish
                    # (apostrof va defis ham ruxsat etilgan)
                    words = re.findall(r"[A-Zʼʻ’'\-/ ]{6,}", text)
                    
                    # faqat lotin harflarini tekshirish (kirillni chiqarib tashlash)
                    #  words = [w for w in words if re.fullmatch(r"[IVXʼʻ’\-/ ]+", w)]
                    
                    clear_words = []
                    for w in words:
                        if re.fullmatch(r"[IVXʼʻ’\-/ ]+", w):
                            continue
                        if len(w) <= 3:
                            continue
                        clear_words.append(w)
                    
                    all_words.update(clear_words)

    # Natijalarni faylga yozish
    with open(output_file, "w", encoding="utf-8") as f:
        for word in sorted(all_words):
            f.write(word + "\n")

    print(f"✅ {len(all_words)} ta katta harfli lotincha o'zbek so'z topildi va {output_file} faylga yozildi.")


def extrude_words(counter_words_path, clear_words_path):
    if not os.path.exists("sozlik.pickle"):
        clear_words = set()
        with open(clear_words_path, "r", encoding="utf-8") as reader:
            for line in reader:
                line = line.rstrip("\n")
                clear_words.add(line)
        counter_words = dict()
        letter_words = dict()
        with open(counter_words_path, "r", encoding="utf-8") as reader:
            try:
                for line in reader:
                    parts = line.rstrip("\n").strip().split("\t")
                    for i in range(0, len(parts), 2):
                        if parts[i] == ' ' or parts[i+1] == ' ':
                            continue
                        counter_words[parts[i]] = int(parts[i+1])
                        if parts[i][0] not in letter_words:
                            letter_words[parts[i][0]] = set()
                        letter_words[parts[i][0]].add(parts[i])
            except Exception as e:
                print(line, parts[i], parts[i+1], i, " - error")
                print(e)
        
        with open("sozlik.pickle", "wb") as f:
            pickle.dump((counter_words, clear_words, letter_words), f)
    else:
        with open("sozlik.pickle", "rb") as f:
            counter_words, clear_words, letter_words = pickle.load(f)
    # words = sorted(list(counter_words.items()), key=lambda x: x[0])
    # unique_clear_words = sorted(list(clear_words))
    unique_words =  dict()
    unique_not_words = dict()
    try:
        for target_word in tqdm(list(clear_words)[75000:]):
            target_word = target_word.lower()
            if len(target_word) <= 2:
                unique_words[target_word] = 0
                continue
            for word in letter_words[target_word[0]]: # tqdm(counter_words.items()):
                word = word.lower()
                fail = False
                ln = len(word)
                for i in range(ln // 2):
                    if word[i] in uz.KRILLS or word[ln - i - 1] in uz.KRILLS:
                        fail = True
                        break
                if fail:
                    continue
                counter = counter_words[word]
                if word.startswith(target_word):
                    if word not in clear_words:
                        syllabes = uz.to_syllable(word[len(target_word):])
                        fail = False
                        for syllable in syllabes.split('-'):
                            if syllable not in uz.POSTFIXES:
                                fail = True
                                break
                        if fail:
                            continue
                        unique_words[word] = counter
                else:
                    unique_not_words[word] = counter


    except Exception as e:
        print("Error during word extraction:", e)
    finally:
        with open("other_words.txt", "w", encoding="utf-8") as f:
            for word, counter in tqdm(unique_words.items()):
                print(f"{word}\t{counter}", file=f)
        with open("not_other_words.txt", "w", encoding="utf-8") as f:
            for word, counter in tqdm(unique_not_words.items()):
                print(f"{word}\t{counter}", file=f)

def load_words(filepath):
    words = list()
    with open(filepath, "r", encoding="utf-8") as f:
        for line in f:
            word, count = line.rstrip("\n").split("\t")
            words.append((word, int(count)))
    return words

def make_unique(filepath):
    words = sorted(list(set(load_words(filepath))), key=lambda x: x[0])
    with open(filepath, "w", encoding="utf-8") as f:
        for word, count in words:
            print(word, count, sep="\t", file=f)
            
def syllaby(words):
    stats = dict()
    longs = []
    for word, count in tqdm(words, desc="Syllable processing..."):
        if len(word) > 15:
            fail = False
            for letter in word:
                if letter in uz.KRILLS:
                    fail = True
                    break
            if not fail:
                longs.append((word, count))
            continue
        word = uz.to_latin(word)
        syllables = uz.to_syllable(word).split('-')
        for i, part in enumerate(syllables):
            if part not in stats:
                stats[part] = [0 for _ in range(11)]
            stats[part][i if i < 10 else 10] += 1
    stats = sorted(list(stats.items()), key=lambda x: len(x[0]), reverse=True)
    with open("syllable_statistics.tsv", "w", encoding="utf-8") as f:
        for part, counts in stats:
            # if sum(counts[3:]) < 2000 or len(part) > 6:
            #     continue
            f.write(f"{part}\t" + "\t".join(map(str, counts)) + "\n")
    with open("long_words.tsv", "w", encoding="utf-8") as f:
        for word, count in longs:
            f.write(f"{word}\t{count}\n")

def test_image_optimizing():
    print("Testing image optimization...")
    image_path = "testing/images/30 jildlik 1-jild/page-0001.png"  # Replace with your image path
    # image_path = "testing/images/30 jildlik 1-jild/page-0010.png"  # Replace with your image path
    image = i.load_image(image_path)

    # Example sequence of operations
    sequence = [i.colorizer, i.luminancer, i.binarizer]
    args = [(1.5, 1.5, 1.5), (0.33, 0.33, 0.34), (i.percenter(255, 60),)]
    
    optimized_image = i.sequence_optimizer(image, "RGB", "1", sequence, args)
    extruded_image = i.extrude_image(optimized_image, 4)
    extruded_image.save("testing/images/optimized_image.png")
    print("Image optimization completed and saved as 'optimized_image.png'.")


# copilot section start


# copilot section end

if __name__ == "__main__":
    if PROCESS_TYPE == "parallel":
        # mp.set_start_method("spawn", force=True)
        mp.freeze_support()
    
    # pdf_to_image(library_folder, image_folder)
    # image_folder = "testing/images/"
    # text_folder = "testing/texts/"
    # image_to_text(image_folder, text_folder)
    # # image_path = image_folder + "/JNL2"
    # clip_optimization(
    #     image_path,
    #     box=(160, 270, 1960, 2760),  # Example box coordinates (left, upper, right, lower)
    #     mirror=None  # Set to True if you want to mirror the image before and after cropping
    # )   
    # standart_optimization(image_path)
    # image_to_text(image_folder, text_folder)
    # extrude_words(
    #     "dataset/library/so'zlik/all_words_by_count.csv",
    #     "dataset/library/so'zlik/clear_words.txt"
    # )
    # syllaby(
    #     load_words("not_other_words.txt")
    # )
    # all_words = "all_words.txt"
    # filtred_words = "filtred_word.txt"
    # make_unique(all_words)
    # make_unique(filtred_words)
    extract_places()
