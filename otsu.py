from PIL import Image
import glob
import os
import sys
import time


def IntensitySum(hist):
    s = 0
    for i in range(len(hist)):
        s += i * hist[i]
    return s


def main():
    path = sys.argv[1]
    times = []
    for infile in glob.glob(os.path.join(path, '*.jpg')):
        file, ext = os.path.splitext(infile)
        name = os.path.split(file)[-1]

        start_time = time.time()
        image = Image.open(infile).convert('L')  # to black and white (ITU-R 601-2)
        hist = image.histogram()

        all_intensity_sum = IntensitySum(hist)
        all_pixel_count = image.size[0] * image.size[1]
        first_class_pixel_count = 0
        first_class_intensity_sum = 0
        best_sigma = 0
        for i in range(len(hist)):
            if hist[i] == 0: continue
            first_class_pixel_count += hist[i]
            if first_class_pixel_count == all_pixel_count: break
            first_class_intensity_sum += i * hist[i]

            first_class_prob = first_class_pixel_count / all_pixel_count
            second_class_prob = 1.0 - first_class_prob

            first_class_mean = first_class_intensity_sum / first_class_pixel_count
            second_class_mean = (all_intensity_sum - first_class_intensity_sum) \
                                / (all_pixel_count - first_class_pixel_count)
            mean_delta = first_class_mean - second_class_mean

            sigma = first_class_prob * second_class_prob * mean_delta * mean_delta
            if sigma > best_sigma:
                best_sigma = sigma
                best_threshold = i

        image.point(lambda x: 255 if x > best_threshold else 0).save(os.path.join('output', name + '.png'))
        times.append(1e6 * (time.time() - start_time) / all_pixel_count)
    mean = sum(times) / len(times)
    print("average operating time (s / MP):", mean)

if __name__ == "__main__":
    main()
