from config import CPU_COUNT, PROCESS_TYPE
import string
from os import path, listdir

def strip_text(text:str) -> str:
    return text.strip(string.punctuation + string.whitespace)

def discover_files(folder, ext=""):
    files = []
    for target in listdir(folder):
        target_path = path.join(folder, target)
        if path.isdir(target_path):
            files += discover_files(target_path)
        if path.isfile(target_path) and target_path.endswith(ext):
            files.append(target_path)
    return files

def discover_folders(folder):
    dirs = []
    for target in listdir(folder):
        target_path = path.join(folder, target)
        if path.isdir(target_path):
            dirs += discover_folders(target_path)
            continue
        if path.isfile(target_path):
            dirs.append(folder)
            break
    return dirs

def create_tasks(function, files, *args):
    return [[function, *([file] + list(args))] for file in files]

def sequence_wrapper(task):
    sequence, args = task[0], task[1]
    for i, worker in enumerate(sequence):
        worker(*args[i])

def default_wrapper(task):
    worker, args = task[0], task[1:]
    worker(*args)

def __parallel_process(wrapper, tasks):
    from multiprocessing import Pool
    from tqdm import tqdm
    with Pool(processes=CPU_COUNT) as pool:
        return list(tqdm(pool.imap(wrapper, tasks), total=len(tasks), desc="Processing parallel mode"))


def __default_process(wrapper, tasks):
    from tqdm import tqdm
    for task in tqdm(tasks, desc="Processing default mode"):
        wrapper(task)


def process_task(wrapper, tasks, mode=PROCESS_TYPE):
    match mode:
        case "parallel":
            __parallel_process(wrapper, tasks)
        case _:
            __default_process(wrapper, tasks)
