import math


def sobel_filter(sub_matrix, result_matrix, first_row, lock):
    gx_kernel = [[-1, 0, 1], [-2, 0, 2], [-1, 0, 1]]
    gy_kernel = [[-1, -2, -1], [0, 0, 0], [1, 2, 1]]

    rows = len(sub_matrix)
    cols = len(sub_matrix[0])

    # for row in sub_matrix:
    #     row.insert(0, 0)
    #     row.append(0)

    # sub_matrix.insert(0, sub_matrix[0])
    # sub_matrix.append(sub_matrix[-1])

    for i in range(1, rows - 1):
        for j in range(1, cols - 1):
            gx = 0
            gy = 0

            for k in range(3):
                for m in range(3):
                    gx += gx_kernel[k][m] * sub_matrix[i - 1 + k][j - 1 + m]
                    gy += gy_kernel[k][m] * sub_matrix[i - 1 + k][j - 1 + m]

            g_m = math.sqrt(gx ** 2 + gy ** 2)

            lock.acquire()
            result_matrix[first_row + i][j] = g_m
            lock.release()

    print(f"\nChanged sub_matrix row {first_row}")


def mb_filter(sub_matrix, result_matrix, first_row, lock):
    rows = len(sub_matrix)
    cols = len(sub_matrix[0])
    k = 7  # kernel size
    pad_size = k // 2

    # Create a padded version of sub_matrix with edge padding
    padded_matrix = [[0] * (cols + 2 * pad_size) for _ in range(rows + 2 * pad_size)]
    for i in range(rows):
        for j in range(cols):
            padded_matrix[i + pad_size][j + pad_size] = sub_matrix[i][j]

    # Fill the edges
    for i in range(pad_size):
        for j in range(cols):
            padded_matrix[i][j + pad_size] = sub_matrix[0][j]  # Top edge
            padded_matrix[rows + pad_size + i][j + pad_size] = sub_matrix[rows - 1][j]  # Bottom edge

    for i in range(rows):
        for j in range(pad_size):
            padded_matrix[i + pad_size][j] = sub_matrix[i][0]  # Left edge
            padded_matrix[i + pad_size][cols + pad_size + j] = sub_matrix[i][cols - 1]  # Right edge

    # Fill the corners
    for i in range(pad_size):
        for j in range(pad_size):
            padded_matrix[i][j] = sub_matrix[0][0]  # Top-left corner
            padded_matrix[i][cols + pad_size + j] = sub_matrix[0][cols - 1]  # Top-right corner
            padded_matrix[rows + pad_size + i][j] = sub_matrix[rows - 1][0]  # Bottom-left corner
            # Bottom-right corner
            padded_matrix[rows + pad_size + i][cols + pad_size + j] = sub_matrix[rows - 1][cols - 1]

    # Perform the median blur
    for i in range(pad_size, rows + pad_size):
        for j in range(pad_size, cols + pad_size):
            region = [padded_matrix[i + m][j + n] for m in range(-pad_size, pad_size + 1) for n in
                      range(-pad_size, pad_size + 1)]
            region.sort()
            median_value = region[len(region) // 2]

            lock.acquire()
            result_matrix[first_row + i - pad_size][j - pad_size] = median_value
            lock.release()


def bw_filter(sub_matrix, result_matrix, first_row, lock):
    rows = len(sub_matrix)
    cols = len(sub_matrix[0])

    res_mat = [[[0, 0, 0] for _ in range(cols)] for _ in range(rows)]

    for i in range(rows):
        for j in range(cols):
            blue_value = sub_matrix[i][j]
            res_mat[i][j][0] = blue_value
            res_mat[i][j][1] = blue_value
            res_mat[i][j][2] = 255

    lock.acquire()
    for i in range(rows):
        for j in range(cols):
            result_matrix[first_row + i][j] = res_mat[i][j]
    lock.release()

    print(f"\nChanged sub_matrix row {first_row}")


def sharp_filter(sub_matrix, result_matrix, first_row, lock):
    kernel = [[0, -1, 0],
              [-1, 5, -1],
              [0, -1, 0]]

    rows = len(sub_matrix)
    cols = len(sub_matrix[0])

    for i in range(1, rows - 1):
        for j in range(1, cols - 1):
            segment = [[sub_matrix[i - 1 + m][j - 1 + n] for n in range(3)] for m in range(3)]

            sharpened_value = 0
            for m in range(3):
                for n in range(3):
                    sharpened_value += segment[m][n] * kernel[m][n]

            sharpened_value = min(max(sharpened_value, 0), 255)

            lock.acquire()
            result_matrix[first_row + i][j] = sharpened_value
            lock.release()

    print(f"\nChanged sub_matrix row {first_row}")
