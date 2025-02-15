from Os_Lab_Project.Modules.Filters import *
from Os_Lab_Project.Modules.Threading import *
from Os_Lab_Project.Modules.File_handeling import *
import threading


def rgb_to_gray(image):
    rows = len(image)
    cols = len(image[0])

    res_mat = [[0 for _ in range(cols)] for _ in range(rows)]

    for i in range(rows):
        for j in range(cols):
            res_mat[i][j] = min(max(int(0.2989 * image[i][j][2] + 0.5870 * image[i][j][1] + 0.1140 * image[i][j][0]), 0), 255)

    return res_mat


def find_mean(matrix):
    all_sum = 0
    n = 0

    if isinstance(matrix[0][0], list):
        for row in matrix:
            for pixel in row:
                all_sum += sum(pixel)
                n += 3
    else:
        for row in matrix:
            for val in row:
                all_sum += val
                n += 1

    mean = all_sum / n if n > 0 else 0

    print(f"Calculated mean value: {mean}")
    return mean


def do_threshold(matrix, mean_value):
    rows = len(matrix)
    cols = len(matrix[0])

    for i in range(rows):
        for j in range(cols):
            if matrix[i][j] > mean_value:
                matrix[i][j] = 0
            else:
                matrix[i][j] = 255


def apply_filter(image_path, filter_name='s'):
    image = cv2.imread(image_path)
    grayed = rgb_to_gray(image)

    n_threads = find_n_threads(grayed)
    all_matrix = divide_image(grayed, n_threads)

    height = len(grayed)
    width = len(grayed[0])

    if filter_name == 'bw':
        final_matrix = [[[0, 0, 0] for _ in range(width)] for _ in range(height)]
    else:
        final_matrix = [[0 for _ in range(width)] for _ in range(height)]

    threads = []
    lock = threading.Lock()

    if filter_name == 's':
        filter_function = sobel_filter
    elif filter_name == 'mb':
        filter_function = mb_filter
    elif filter_name == 'bw':
        filter_function = bw_filter
    elif filter_name == 'sh':
        filter_function = sharp_filter

    sub_n = 0
    mat_len = len(all_matrix)

    for start_row, sub_matrix in all_matrix:

        if filter_name == 's' or filter_name == 'sh':
            if sub_n != mat_len - 1:
                sub_matrix.append(all_matrix[sub_n + 1][1][0])
                sub_matrix.append(all_matrix[sub_n + 1][1][1])
                sub_matrix.append(all_matrix[sub_n + 1][1][2])
            else:
                sub_matrix.append([0 for _ in range(width)])

        # if sub_n != 0:
        #     sub_matrix.insert(0, all_matrix[sub_n-1][-1][0])
        # else:
        #     sub_matrix.insert(0, [0 for _ in range(width)])

        sub_n += 1

        thread = threading.Thread(target=filter_function, args=(sub_matrix, final_matrix, start_row, lock))

        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    mean = find_mean(final_matrix)

    if filter_name == 's':
        do_threshold(final_matrix, mean)

    return final_matrix
