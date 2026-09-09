from config import tesseract_path, poppler_path, IMAGE_DPI, CPU_POPPLER
from utility import strip_text

from PIL import Image
import pytesseract as tr
import os


tr.pytesseract.tesseract_cmd = tesseract_path
# print(tr.get_languages())

def extract_text(image_path, lang='rus+uzb_cyrl', oem = 3, psm = 3):
    image = Image.open(image_path)
    return tr.image_to_string(image, lang=lang, config=f"--oem {oem} --psm {psm}")

def extract_folder_filename(path):
    sep = os.path.split(path)
    filename = sep[-1][:-4]
    folder = os.path.split(sep[0])[-1]
    return filename, folder

def image_to_text(image_path, output_folder, if_exists_stop=True):
    filename, folder = extract_folder_filename(image_path)
    filepath = os.path.join(output_folder, folder, filename + ".txt")
    if os.path.exists(filepath) and if_exists_stop:
        return
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    text = extract_text(image_path)
    with open(filepath, "w", encoding="utf-8") as file:
        file.write(text)

def __by_poppler(ip, op, sp, ep):
    from pdf2image import convert_from_path
    convert_from_path(
        pdf_path=ip,
        output_folder=op,
        first_page=sp,
        last_page=ep,
        dpi=IMAGE_DPI,
        thread_count=CPU_POPPLER,
        paths_only=True,
        grayscale=False,
        output_file="page-",
        poppler_path=poppler_path
    )


def __by_fitz(ip, op, sp, ep):
    import fitz
    doc = fitz.open(ip)
    for page in doc:
        page_number = page.number + 1
        if sp != None and page_number < sp:
            continue
        if ep != None and page_number > ep:
            break
        # pix = page.get_pixmap(dpi=300, colorspace="GRAY").pil_image()
        pix = page.get_pixmap(dpi=300).pil_image().resize((2048, 3010))
        filepath = os.path.join(op, f"page-{page_number:04d}.png")
        if not os.path.exists(filepath):
            pix.save(filepath)

def pdf_to_images(pdf_file:str, output_folder:str, method="fitz", if_exists_stop=True, start_page = None, end_page = None):
    try:
        target_path = strip_text( os.path.join(output_folder, os.path.basename(pdf_file[:-4])))
        if os.path.exists(target_path) and if_exists_stop:
            return
        os.makedirs(target_path, exist_ok=True)
        match method:
            case "poppler":
                __by_poppler(pdf_file, target_path, start_page, end_page)
            case "fitz":
                __by_fitz(pdf_file, target_path, start_page, end_page)
            case _:
                raise ValueError("use only these method names -> {poppler | fitz}")
    except Exception as ex:
        print("error -> convert_pdf_to_images: ", ex.with_traceback())

