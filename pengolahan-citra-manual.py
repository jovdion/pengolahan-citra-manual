# Manual Image Processing Functions without Libraries

# Load a simple PPM image file
def load_ppm(file_path):
    with open(file_path, 'r') as f:
        assert f.readline().strip() == 'P3'  # P3 indicates ASCII format
        width, height = map(int, f.readline().strip().split())
        max_val = int(f.readline().strip())  # typically 255
        pixels = []
        for _ in range(height):
            row = []
            for _ in range(width):
                r = int(f.readline().strip())
                g = int(f.readline().strip())
                b = int(f.readline().strip())
                row.append([r, g, b])
            pixels.append(row)
    return pixels, width, height, max_val

# Save image data to PPM
def save_ppm(filename, pixels, width, height, max_val=255):
    with open(filename, 'w') as f:
        f.write("P3\n")
        f.write(f"{width} {height}\n")
        f.write(f"{max_val}\n")
        for row in pixels:
            for pixel in row:
                f.write(f"{pixel[0]}\n{pixel[1]}\n{pixel[2]}\n")

# Invert colors
def invert_colors(pixels):
    return [[[255 - p for p in pixel] for pixel in row] for row in pixels]

# Grayscale conversion
def grayscale(pixels):
    return [[[int(sum(pixel) / 3)] * 3 for pixel in row] for row in pixels]

# Rotate image by 90 degrees
def rotate_image(pixels, width, height, angle=90):
    if angle == 90:
        rotated = [[pixels[height - x - 1][y] for x in range(height)] for y in range(width)]
        return rotated, height, width
    elif angle == 180:
        rotated = [[pixels[height - y - 1][width - x - 1] for x in range(width)] for y in range(height)]
        return rotated, width, height
    elif angle == 270:
        rotated = [[pixels[x][width - y - 1] for x in range(height)] for y in range(width)]
        return rotated, height, width
    return pixels, width, height

# Histogram equalization
def histogram_equalization(pixels):
    flat_pixels = [p[0] for row in pixels for p in row]  # Flatten only the red channel (assuming grayscale)
    hist = [0] * 256
    for p in flat_pixels:
        hist[p] += 1
    cumulative_hist = [sum(hist[:i + 1]) for i in range(256)]
    scale_factor = 255 / cumulative_hist[-1]
    lookup_table = [int(cumulative_hist[i] * scale_factor) for i in range(256)]
    return [[[lookup_table[p[0]]] * 3 for p in row] for row in pixels]

# Black & White Threshold
def black_white(pixels, threshold=127):
    return [[[255, 255, 255] if sum(pixel) / 3 > threshold else [0, 0, 0] for pixel in row] for row in pixels]

# Simple Box Blur (Gaussian Approximation)
def blur_image(pixels, width, height, radius=1):
    def get_average(x, y):
        acc = [0, 0, 0]
        count = 0
        for dx in range(-radius, radius + 1):
            for dy in range(-radius, radius + 1):
                nx, ny = x + dx, y + dy
                if 0 <= nx < height and 0 <= ny < width:
                    count += 1
                    for c in range(3):
                        acc[c] += pixels[nx][ny][c]
        return [int(a / count) for a in acc]
    return [[get_average(x, y) for y in range(width)] for x in range(height)]

# Main Function
if __name__ == "__main__":
    # Load image (using PPM format)
    input_file = "example.ppm"  # Replace with your PPM file
    pixels, width, height, max_val = load_ppm(input_file)

    # Invert Colors
    inverted_image = invert_colors(pixels)
    save_ppm("output_inverted.ppm", inverted_image, width, height)

    # Convert to Grayscale
    grayscale_image = grayscale(pixels)
    save_ppm("output_grayscale.ppm", grayscale_image, width, height)

    # Rotate Image
    rotated_image, rotated_width, rotated_height = rotate_image(pixels, width, height, 90)
    save_ppm("output_rotated.ppm", rotated_image, rotated_width, rotated_height)

    # Histogram Equalization
    equalized_image = histogram_equalization(pixels)
    save_ppm("output_equalized.ppm", equalized_image, width, height)

    # Black and White Threshold
    bw_image = black_white(pixels, threshold=127)
    save_ppm("output_bw.ppm", bw_image, width, height)

    # Blur Image
    blurred_image = blur_image(pixels, width, height, radius=1)
    save_ppm("output_blurred.ppm", blurred_image, width, height)

    print("Processing complete. All processed images saved as .ppm files.")
