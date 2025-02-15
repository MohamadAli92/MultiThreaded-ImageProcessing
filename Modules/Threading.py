def divide_image(image, n_threads):
    height = len(image)
    all_matrix = []
    rows_for_thread = (height + n_threads - 1) // n_threads

    for first_row in range(0, height, rows_for_thread):
        end_row = min(first_row + rows_for_thread, height)
        sub_matrix = image[first_row:end_row]
        all_matrix.append((first_row, sub_matrix))

    return all_matrix


def find_n_threads(image):
    n_thread = max(9, len(image) // 30)
    print(f"Using {n_thread} threads.")
    return n_thread
