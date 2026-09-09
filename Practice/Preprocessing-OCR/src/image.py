from PIL import Image, ImageDraw
import os

percenter = lambda value, percent: int(value * (percent / 100))
colorizer = lambda rgb, fr, fg, fb: (rgb[0] * fr, rgb[1] * fg, rgb[2] * fb)
gray_colorizer = lambda gray, factor: int(gray * factor)
luminancer = lambda rgb, fr, fg, fb: int(rgb[0] * fr + rgb[1] * fg + rgb[2] * fb)
binarizer = lambda gray, threshold: 255 if gray > threshold else 0

# Show a bar diagram of segment widths and heights using matplotlib
def show_segments_bar_diagram(segments):
    """
    Display a bar diagram of segment widths and heights using matplotlib.
    Args:
        segments: list of tuples (bbox, pixels), where bbox = (min_x, min_y, max_x, max_y)
    """
    import matplotlib.pyplot as plt
    import numpy as np
    widths = [0 for _ in range(11)]
    heights = [0 for _ in range(11)]
    wmul, hmul = 60, 10
    for bbox, _ in segments:
        x, y, xx, yy = bbox
        w = xx - x
        h = yy - y
        i, j = w // wmul, h // hmul
        widths[i if i < 10 else 10] += 1
        heights[j if j < 10 else 10] += 1
    # widths.sort()
    # heights.sort()
    avgw, avgh = wmul, hmul #sum(widths) // len(widths), sum(heights) // len(heights)
    x = np.arange(len(widths)) + 1
    # One figure, two subplots (widths and heights)
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 8), sharex=True)
    ax1.bar(x, widths, alpha=0.7, color='tab:blue')
    ax1.set_ylabel('Width (pixels)')
    ax1.set_title(f'Segment Widths, AVG: {avgw}')
    x = np.arange(len(heights)) + 1
    ax2.bar(x, heights, alpha=0.7, color='tab:orange')
    ax2.set_xlabel('Segment Index')
    ax2.set_ylabel('Height (pixels)')
    ax2.set_title(f'Segment Heights, AVG: {avgh}')

    plt.tight_layout()
    plt.show()

def mask_image(image:Image, segments) -> Image:
    img = Image.new("L", image.size, "black")
    px = img.load()
    for _, pixels in segments:
        for x, y in pixels:
            px[x, y] = 255
    new_img = Image.composite(image, Image.new(image.mode, image.size, "white") ,img)
    return new_img


def clip_image(image_path:str, box:tuple[int, int, int, int], mirror:bool=False):
    image = Image.open(image_path)
    if mirror == True:
        image = image.transpose(Image.FLIP_LEFT_RIGHT)
    new_image = image.crop(box)
    if mirror == True:
        new_image = new_image.transpose(Image.FLIP_LEFT_RIGHT)
    image.close()
    new_image.save(image_path)

def standart_optimization(image_path:str,
                          color_factor = (1.1, 1.1, 1.1),
                          luminance_factor = (0.33, 0.33, 0.34),
                          threshold = (percenter(255, 80),),
                          extrude_factor = (1, 1),
                          minmax_height = (20, 80),
                          max_width = 600,
                          segmentize = False):
    image = Image.open(image_path)
    if image.mode != "RGB":
        return
    
    
    optimizations_sequence = (colorizer, luminancer, binarizer)
    optimizations_args = (color_factor, luminance_factor, threshold)
    optimized_image = sequence_optimizer(image, image.mode, "L", optimizations_sequence, optimizations_args)
    result_image = extrude_image(optimized_image, extrude_factor) 
    if segmentize:
        segments = segmentize_image(result_image)
        filtred_segments = filter_segments(segments, minmax_height, max_width)
        diff = len(filtred_segments) / len(segments) * 100
        # print(f"Image {image_path} has ({diff}) {len(segments)} segments before filtering, {len(filtred_segments)} after filtering.")
        min_diff_percent = 90
        if diff <= min_diff_percent:
            os.remove(image_path)
            return
        result_image = mask_image(optimized_image, filtred_segments)
        segments = segmentize_image(result_image)
    image.close()
    result_image.save(image_path)

def load_image(image_path: str) -> Image:
    """
    Loads an image from the specified path.
    
    :param image_path: Path to the image file.
    :return: PIL Image object.
    """
    try:
        return Image.open(image_path)
    except Exception as e:
        print(f"Error loading image {image_path}: {e}")
        raise

def sequence_optimizer(image:Image, input_mode, output_mode, sequence:list, args:list) -> Image:
    """
    Applies a sequence of image processing functions to an image.
    
    :param image: PIL Image object to be processed.
    :param input_mode: The input color mode of the image (e.g., "RGB", "L").
    :param output_mode: The desired output color mode of the image (e.g., "RGB", "L").
    :param sequence: List of functions to apply in sequence.
    :param args: List of arguments for each function in the sequence.
    :return: Processed PIL Image object.
    """
    if image.mode != input_mode:
        raise ValueError(f"Image must be in {input_mode} mode, but is in {image.mode} mode.")
    
    if output_mode not in ["RGB", "L", "1"]:
        raise ValueError(f"Output mode must be one of ['RGB', 'L', '1'], but is {output_mode}.")
    
    pixels = image.load()
    optimized_image = Image.new(output_mode, image.size)
    optimized_pixels = optimized_image.load()

    for x in range(image.width):
        for y in range(image.height):
            pixel = pixels[x, y]
            for func, arg in zip(sequence, args):
                # print(f"Applying {func.__name__} with args {arg} to {pixel} pixel ({x}, {y})")
                pixel = func(pixel, *arg)

            optimized_pixels[x, y] = pixel

    return optimized_image

def color_optimizer(image:Image, factor_rgb:tuple[float, float, float]) -> Image:
    """
    Adjusts the color saturation of an image by a given factor.
    
    :param image: PIL Image object to be processed.
    :param factor_rgb: Tuple of three floats representing the RGB factors (0-2).
    :return: Processed PIL Image object with adjusted color saturation.
    """

    for color_factor in factor_rgb:
        if not (0 <= color_factor <= 2):
            raise ValueError("Color factors must be between 0 and 2.")
    
    colored = Image.new("RGB", image.size)
    colored.paste(image)
    pixels = colored.load()
    for x in range(colored.width):
        for y in range(colored.height):
            rgb = pixels[x, y]
            r, g, b = colorizer(rgb, *factor_rgb)
            pixels[x, y] = (min(r, 255), min(g, 255), min(b, 255))
    return colored

def grayscale_optimizer(image:Image) -> Image:
    """
    Converts an image to grayscale.
    
    :param image: PIL Image object to be processed.
    :return: Processed PIL Image object in grayscale.
    """
    gray_image = Image.new("L", image.size)
    pixels = image.load()
    gray_pixels = gray_image.load()
    
    for x in range(image.width):
        for y in range(image.height):
            rgb = pixels[x, y]
            gray_color = luminancer(rgb, 0.33, 0.33, 0.34)
            gray_pixels[x, y] = gray_color

    return gray_image

def binarize_optimizer(image:Image, threshold_percent:int) -> Image:
    """    Converts an image to black and white based on a threshold percentage.
    :param image: PIL Image object to be processed.
    :param threshold_percent: Percentage threshold for binarization (0-100).
    :return: Processed PIL Image object in black and white.
    """
    
    if not (0 <= threshold_percent <= 100):
        raise ValueError("Threshold percent must be between 0 and 100.")
    
    threshold = int(255 * (threshold_percent / 100))
    bw_image = Image.new("1", image.size)
    pixels = image.load()
    bw_pixels = bw_image.load()
    
    for x in range(image.width):
        for y in range(image.height):
            gray = pixels[x, y]
            bw_pixels[x, y] = binarizer(gray, threshold)

    return bw_image

def extrude_image(image:Image, factor:int) -> Image:
    """    Enlarges an image by a specified pixel factor.
    :param image: PIL Image object to be processed.
    :param factor: Factor by which to enlarge the image.
    :return: Processed PIL Image object enlarged by the specified pixel factor.
    """

    if image.mode != "L" and image.mode != "1":
        raise ValueError("Image must be in grayscale mode (L, 1).")

    extruded_image = Image.new(image.mode, image.size)
    width, height = image.size
    pixels = image.load()
    extruded_pixels = extruded_image.load()
    fx, fy = factor
    
    for x in range(width):
        for y in range(height):
            pixel = pixels[x, y]
            if pixel == 0: # Assuming 0 is black in grayscale
                extruded_pixels[x, y] = pixel
                for dx in range(-fx, fx + 1):
                    for dy in range(-fy, fy + 1):
                        if 0 <= x + dx < width and 0 <= y + dy < height and dx != dy != 0:
                            extruded_pixels[x + dx, y + dy] = pixel
                continue
            if pixel != 0:
                extruded_pixels[x, y] = pixel

    return extruded_image

def binarize_image(image_path, threshold_percent):
    """    Converts an image to black and white based on a threshold percentage.
    :param image_path: Path to the image file.
    :param threshold_percent: Percentage threshold for binarization (0-100).
    :return: None, saves the binarized image back to the same path.
    """
    image = Image.open(image_path).convert("L")  # Convert to grayscale
    threshold = percenter(255, threshold_percent)
    bw = image.point(lambda x: 255 if x > threshold else 0, mode='1')
    image.close()
    bw.save(image_path)

def segmentize_image(image:Image) -> list[tuple[tuple[int, int, int, int], list[tuple[int, int]]]]:
    """
    Segments an image into regions based on size constraints.
    
    :param image: PIL Image object to be processed.
    :return: List of tuples, each containing a bounding box and a list of pixel coordinates for the region.
    """
    if image.mode != 'L':
        raise ValueError("Image must be in binary mode ('L').")
    
    pixels = image.load()
    width, height = image.size

    regions = []
    visited = set()

    for x in range(width):
        for y in range(height):
            if (x, y) in visited or pixels[x, y] == 255:  # Skip already visited or white pixels
               continue
            segments = [(x, y)]
            walk_stack = [(x, y)]
            while walk_stack:
                cx, cy = walk_stack.pop()
                if (cx, cy) in visited or not (0 <= cx < width and 0 <= cy < height):
                    continue
                if pixels[cx, cy] == 0:  # Black pixel
                    visited.add((cx, cy))
                    segments.append((cx, cy))
                    # 4-connectivity
                    walk_stack.extend([(cx-1, cy), (cx+1, cy), (cx, cy-1), (cx, cy+1), (cx-1, cy-1), (cx+1, cy+1), (cx-1, cy+1), (cx+1, cy-1)])
            if segments:
                min_x = min(seg[0] for seg in segments)
                max_x = max(seg[0] for seg in segments)
                min_y = min(seg[1] for seg in segments)
                max_y = max(seg[1] for seg in segments)
                bbox = (min_x, min_y, max_x, max_y)
                regions.append((bbox, segments))
    return regions

def filter_segments(segments, minmax_height=(6, 80), max_width = 300):
    filtred = []
    for segment in segments:
        x, y, xx, yy = segment[0]
        h = yy - y
        w = xx - x
        mn, mx = minmax_height
        if (h < mn or h > mx) or w > max_width:
            continue
        filtred.append(segment)
    return filtred
    


def draw_segments(size:tuple[int, int], segments:list[tuple[tuple[int, int, int, int], list[tuple[int, int]]]], draw_box=True, draw_pixels=True) -> Image:
    """
    Draws bounding boxes around segmented regions on the image.
    
    :param segments: List of tuples, each containing a bounding box and a list of pixel coordinates for the region.
    :return: Processed PIL Image object with drawn segments.
    """

    image = Image.new('RGB', size, "white")  # Create a white image in RGB mode
    draw = ImageDraw.Draw(image)
    if draw_box and draw_pixels:
        for i, (bbox, pixels) in enumerate(segments):
            draw.rectangle(bbox, outline="red")  # Draw red rectangle for the segment
            x, y, xx, yy = bbox
            w, h = xx - x, yy - y
            tw, th = str(w), str(h)
            py = y - 16 if i & 1 == 1 else yy + 8

            draw.text((x + w // 2 - len(tw + th) * 5, py), f"{tw}x{th}", fill="red")
            color = (w * h % 255 + 50, w * 5 % 255 + 50, h * 10 % 255 + 50)
            for px in pixels:
                draw.point(px, fill=color)  # Draw colored pixel for the segment

    return image

# copilot section start


# copilot section end