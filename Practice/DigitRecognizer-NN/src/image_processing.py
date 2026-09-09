import os, copy, gzip, random, pickle
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image, ImageDraw
from tqdm import tqdm

columns = 26
rows = 36
rect_size = (32 * columns, 32 * rows)

def split_numbers(image: Image) -> list[tuple[int, Image]]:
    width, height = image.size
    crop_w = width // columns
    crop_h = height // rows
    pad_x, pad_y = 2, 2
    images = []
    counter = 0
    # print(width, height, crop_w, crop_h)
    for y in range(crop_h, height, crop_h):
        for x in range(crop_w, width, crop_w):
            images.append((counter, image.crop((x + pad_x, y + pad_y, x + crop_w - pad_x, y + crop_h - pad_y))))
        counter = (counter + 1) % 10
    return images

def rename_files(srcdir = "raw-images"):
    counter = 0
    files = os.listdir(srcdir)
    for file in files:
        counter += 1
        src = f"{srcdir}/{file}"
        dst = f"{srcdir}/{counter}.jpg"
        os.rename(src, dst)

def color_convert_image(image: Image) -> Image:
    pixels = image.getdata()
    new_image = Image.new(mode="L", size=image.size)
    new_image.putdata(luminance_filter(pixels))
    return new_image

def find_corners(image: Image, black_threshold=60, drawTemplate=False) -> list:
    if image.mode != "L":
        image = image.convert("L")
    width, height = image.size
    pixels = image.load()

    min_x = width
    max_x = 0
    min_y = height
    max_y = 0
    area = 400
    botpad = 300

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

            min_x = min(min_x, x)
            max_x = max(max_x, wx)
            min_y = min(min_y, y)
            max_y = max(max_y, hy)

    if not black_points:
        print(black_threshold, "qora piksellar topilmadi! black_threshold ni sozlang.")
        return [(0, 0), (0, 0), (0, 0), (0, 0)], (0, 0)

    top_left = min(black_points, key=lambda p: p[0] + p[1])  # x + y eng kichik
    top_right = min(black_points, key=lambda p: -p[0] + p[1])  # -x + y eng kichik
    bottom_right = min(black_points, key=lambda p: -p[0] - p[1])  # -x - y eng kichik
    bottom_left = min(black_points, key=lambda p: p[0] - p[1])  # x - y eng kichik

    nwidth = max(top_right[0] - top_left[0],  bottom_right[0]-bottom_left[0])
    nheight = max(bottom_left[1]-top_left[1], bottom_right[1]-top_right[1])

    corners = [top_left, bottom_left, bottom_right, top_right]
    # print("Jadvalning 4 burchagi:", corners)
    # print(f"Topilgan qora piksellar soni: {len(black_points)}")

    if drawTemplate:
        img_rgb = image.convert("RGB")
        draw = ImageDraw.Draw(img_rgb)
        step = 16

        blue_color =  (0, 0, 255)
        black_color = (0, 0, 0)
        yellow_color = (255, 255, 0)
        red_color = (255, 0, 0)
        green_color = (0, 255, 0)
        draw.rectangle(((0, 0), (area, area)), outline=blue_color, width=6)
        draw.rectangle(((width - area, 0), (width, area)), outline=blue_color, width=6)
        draw.rectangle(((width-area, height-area-botpad), (width, height-botpad)), outline=blue_color, width=6)
        draw.rectangle(((0, height-area-botpad), (area, height-botpad)), outline=blue_color, width=6)

        draw.rectangle((top_left, (top_left[0] + nwidth, top_left[1] + nheight)), outline=yellow_color, width=12)
        for x in range(0, width, step):
            for y in range(0, height - botpad, step):
                draw.circle((x, y), 2, fill=green_color)

        for i, corner in enumerate(corners):
            draw.circle(corner, 12, fill=red_color)
            draw.text(corner, str(i), fill=black_color)
        img_rgb.save("example/1-borders.png")
        img_rgb.show()
    return corners, (nwidth, nheight)

def transform_image(image: Image, corners: list, output_size=(300, 300)) -> Image:
    src_points = corners
    dst_points = [
        (0, 0),     
        (output_size[0]-1, 0),
        (output_size[0]-1, output_size[1]-1),
        (0, output_size[1]-1)
    ]

    new_image = image.transform(
        output_size,
        Image.QUAD,
        tuple(coord for point in src_points for coord in point),
        Image.BILINEAR
    )

    new_image = new_image.resize(rect_size)

    #new_image.show()
    return new_image

def luminance_filter(pixels:list[tuple[int, int, int]]) -> list[int]:
    # luminance calculation
    color_converter = lambda r, g, b: int(0.2126*r + 0.7152*g + 0.0722*b)

    gray_pixels = []
    for r, g, b in pixels:
        gray_pixels.append(abs(color_converter(r, g, b) - 255))
    return gray_pixels

def color_map_digits(digits):
    average_digits = {i: np.absolute(np.mean(digits[i], axis=0)) for i in range(10)}

    fig, axes = plt.subplots(2, 5, figsize=(15, 8), constrained_layout=True)
    fig.suptitle("0-9 raqamlar issiqlik xaritasi", fontsize=16)

    for i, ax in enumerate(axes.flat):
        im = ax.imshow(average_digits[i].reshape(28, 28), cmap="coolwarm")
        ax.set_title(f"{i} - raqami ({len(digits[i]):6d} ta)")
        ax.axis("off")

    fig.colorbar(im, ax=axes[:, -1], shrink=0.6)
    plt.show()

def normalize_values(pixels: np.ndarray) -> np.ndarray:
    maxv = np.max(pixels)
    minv = np.min(pixels)
    diff = maxv - minv
    if diff <= 0:
        print(diff, maxv, minv)
        exit()
    return ((pixels - minv) / diff)

def mnist_heatmap():
    import mnist_loader
    data, _, _ = mnist_loader.load_data("data/mnist.pkl.gzip")
    digits = { i: [] for i in range(0, 10)}
    for i, v in enumerate(data[1]):
        digits[v].append(data[0][i].reshape((28, 28)))
    color_map_digits(digits)

def adu_mnist_heatmap():
    import mnist_loader
    data, _, _ = mnist_loader.load_data("data/adu_mnist.pkl.gzip")
    digits = { i: [] for i in range(0, 10)}
    for i, v in enumerate(data[1]):
        digits[v].append(data[0][i].reshape((28, 28)))
    color_map_digits(digits)

def main_example(num):
    digits = { i: [] for i in range(0, 10)}
    image = Image.open(f"{('raw-images/'+str(num)) if num > 0 else 'example/0-example'}.jpg")
    corners, size = find_corners(image, black_threshold=60, drawTemplate=True)
    new_image = transform_image(image, corners, size)
    new_image.save("example/2-trasformed.png")
    new_image = color_convert_image(new_image)
    new_image.save("example/3-grayscaled.png")
    images = split_numbers(new_image)
    counter = 1
    for number, crop_image in tqdm(images):
        digits[number].append(np.asarray(crop_image))
        counter += 1
    image.close()
    for i in range(10):
        Image.fromarray(digits[i][0], mode="L").save(f"example/4-{i}.png")
    
    norm_digits = { i: [] for i in range(0, 10)}
    for d, v in digits.items():
        for e in v:
            norm_digits[d].append(normalize_values(e.flatten()))
    color_map_digits(norm_digits)

def process_images(save_pickle=True, show_heatmap=False, save_cropped=False):
    digits = { i: [] for i in range(0, 10)}
    for i in range(1, 41):
        image = Image.open(f"raw-images/{i}.jpg")
        corners, size = find_corners(image, black_threshold=60, drawTemplate=True)
        new_image = transform_image(image, corners, size)
        new_image = color_convert_image(new_image)
        images = split_numbers(new_image)
        counter = 1
        for number, crop_image in tqdm(images):
            if save_cropped:
                crop_image.save(f"images/{number}-{i:02d}-{counter:03d}.png")
            digits[number].append(normalize_values(np.asarray(crop_image).flatten()))
            counter += 1
        image.close()
    if save_pickle:
        print("saving dataset")
        images = []
        labels = []

        for digit, imgs in digits.items():
            for img in imgs:
                images.append(img)
                labels.append(digit)
        shuff = list(zip(images, labels))
        random.shuffle(shuff)
        images, labels = zip(*shuff)
        images = np.asarray(images)
        labels = np.asanyarray(labels)
        training_data = (images, labels)
        size = len(labels)
        val = size // 4
        test = size // 2
        validation_data = (images[:val:], labels[0:val:])
        test_data = (images[:test:], labels[0:test:])
        f = gzip.open("data/adu_mnist.pkl.gzip", "wb")
        dataset = (training_data, validation_data, test_data)
        pickle.dump(dataset, f)
        f.close()
    if show_heatmap:
        color_map_digits(digits)
        

if __name__ == "__main__":
    #main_example(0)
    #rename_files()
    #process_images()
    #mnist_heatmap()
    adu_mnist_heatmap()

    '''image = Image.open("raw-images/10.jpg")
    corners, size = find_corners(image)
    print("Jadval", size)
    jadval = transform_image(image, corners, size)
    rasmchalar = split_numbers(jadval)
    print(rasmchalar[400][0])
    rasmchalar[400][1].show()
    print("done.")'''