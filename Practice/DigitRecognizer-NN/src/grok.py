from PIL import Image, ImageDraw

def find_corners(image: Image, black_threshold=60) -> list:
    # Rasmni grayscale qilish
    if image.mode != "L":
        image = image.convert("L")
    width, height = image.size
    pixels = image.load()

    # Eng chekka qora nuqtalarni topish uchun dastlabki qiymatlar
    min_x = width
    max_x = 0
    min_y = height
    max_y = 0
    area = 400
    botpad = 300

    # Qora piksellarni topish
    black_points = []
    for y in range(50, area):
        for x in range(50, area):
            wx = width - x
            hy = height - y - botpad
            if pixels[x, y] < black_threshold:
                black_points.append((x, y))
            if pixels[wx, y] < black_threshold:
                black_points.append((wx, y))
            if pixels[x, hy] < black_threshold:
                black_points.append((x, hy))
            if pixels[wx, hy] < black_threshold:
                black_points.append((wx, hy))
            # Eng chekka nuqtalarni yangilash
            min_x = min(min_x, x)
            max_x = max(max_x, wx)
            min_y = min(min_y, y)
            max_y = max(max_y, hy)

    if not black_points:
        print("Qora piksellar topilmadi! black_threshold ni sozlang.")
        return [(0, 0), (0, 0), (0, 0), (0, 0)]

    # Burchaklarni aniqlash
    top_left = min(black_points, key=lambda p: p[0] + p[1])  # x + y eng kichik
    top_right = min(black_points, key=lambda p: -p[0] + p[1])  # -x + y eng kichik
    bottom_right = min(black_points, key=lambda p: -p[0] - p[1])  # -x - y eng kichik
    bottom_left = min(black_points, key=lambda p: p[0] - p[1])  # x - y eng kichik

    nwidth = max(top_right[0] - top_left[0],  bottom_right[0]-bottom_left[0])
    nheight = max(bottom_left[1]-top_left[1], bottom_right[1]-top_right[1])

    corners = [top_left, bottom_left, bottom_right, top_right]
    print("Jadvalning 4 burchagi:", corners)
    print(f"Topilgan qora piksellar soni: {len(black_points)}")

    # Burchaklarni belgilash
    img_rgb = image.convert("RGB")
    draw = ImageDraw.Draw(img_rgb)
    step = 24
    draw.rectangle(((0, 0), (area, area)), outline=(0, 0, 255))
    draw.rectangle(((width - area, 0), (width, area)), outline=(0, 0, 255))
    draw.rectangle(((width-area, height-area-botpad), (width, height-botpad)), outline=(0, 0, 255))
    draw.rectangle(((0, height-area-botpad), (area, height-botpad)), outline=(0, 0, 255))

    draw.rectangle((top_left, (top_left[0] + nwidth, top_left[1] + nheight)), outline=(255, 0, 255))
    # Grid chizish
    for x in range(0, width, step):
        for y in range(0, height, step):
            draw.ellipse([x-4, y-4, x+4, y+4], fill=(0, 255, 0))

    # Burchaklarni belgilash
    for i, corner in enumerate(corners):
        draw.ellipse([corner[0]-12, corner[1]-12, corner[0]+12, corner[1]+12], fill=(255, 0, 0))
        draw.text(corner, str(i) + " - " + str(corner), fill=(0, 0, 255))

    #img_rgb.save("burchaklari_belgilangan.jpg")
    img_rgb.show()
    return corners, (nwidth, nheight)

def straighten_image(image: Image, corners: list, output_size=(300, 300)) -> Image:
    # Asl rasmni RGB rejimida ochish (transformatsiya uchun)
    if image.mode != "RGB":
        image = image.convert("RGB")

    # Topilgan burchaklar (qiyshaygan jadvalning 4 nuqtasi)
    src_points = corners  # [top_left, top_right, bottom_right, bottom_left]

    # To'g'ri to'rtburchakning burchaklari
    dst_points = [
        (0, 0),              # Yuqori chap
        (output_size[0]-1, 0),  # Yuqori o'ng
        (output_size[0]-1, output_size[1]-1),  # Pastki o'ng
        (0, output_size[1]-1)   # Pastki chap
    ]

    # Perspektiva transformatsiyasi
    straightened_image = image.transform(
        output_size,          # Yangi o'lcham (masalan, 300x300)
        Image.QUAD,           # To'rtburchak transformatsiya turi
        tuple(coord for point in src_points for coord in point),  # Burchaklar ro'yxati
        Image.BILINEAR        # Interpolatsiya usuli
    )

    straightened_image.show()
    return straightened_image

# Sinov
if __name__ == "__main__":
    image = Image.open(f"raw-images/{18}.jpg").convert("L")  # Rasm faylingizni kiriting
    corners, sz = find_corners(image, black_threshold=60)
    straighten_image(image, corners, sz)