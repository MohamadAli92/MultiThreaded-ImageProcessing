# MultiThreaded-ImageProcessing
Multithreaded program for processing filters on images faster.

## Project Overview
This project aims to develop a **multithreaded image processing application** capable of efficiently applying filters to large images. The approach involves dividing an image into **sub-matrices**, processing each in parallel using multiple threads, and then reassembling the final image. The use of **multithreading** significantly enhances performance in image processing tasks.

## Objectives
- Implement **image processing techniques** within an operating systems laboratory project.
- Utilize **multithreading** to enhance performance.
- Ensure **proper synchronization** between threads.

## Implementation Steps

### 1. Load the Image
- Read an image from disk into memory.
- Maintain a **single copy** of the image in the main thread.
- Store the image as a **matrix in memory**.
- Child threads treat the main thread's image matrix as a **shared resource**.

### 2. Divide the Image
- Split the image into **sub-matrices (chunks)** for parallel processing.
- Assign specific **ranges** of the main matrix to each thread.

### 3. Apply Filters
- Implement multiple **image filters** applicable to each sub-matrix.
- Each thread **stores** its results in a separate matrix before modifying the main image matrix.

### 4. Multithreading
- Process each sub-matrix **simultaneously** using multiple threads.
- The number of threads **scales dynamically** based on image size (minimum of **9 threads**).

### 5. Synchronization
- Avoid **cloning** the matrix due to memory constraints.
- Modify the main image matrix **directly** while ensuring correct results.
- Ensure **neighboring sub-matrices** do not interfere by waiting for adjacent threads to finish.

### 6. Reassemble and Save the Image
- Combine the **processed sub-matrices** back into a single image.
- Save the final image **to disk**.

## Edge Detection Filter
### **Purpose:**
Identify **edges** in the image by highlighting areas with high contrast or intensity changes. This helps in detecting **boundaries and shapes** within the image.

### **Processing Steps:**
1. **Convert RGB to Grayscale** using the formula:

$Gray = 0.2989 \times R + 0.5870 \times G + 0.1140 \times B$

3. **Apply Edge Detection Kernels:**
   - For each **3×3 window** in the image, perform a **Hadamard product** using:
     - **X-Direction Kernel** \(G_x\)
     - **Y-Direction Kernel** \(G_y\)
   - Compute the **gradient magnitude** for each pixel:

      $G = \sqrt{G_x^2 + G_y^2}$

   - Replace the pixel value in the corresponding **edge-detected image**.

4. **Thresholding for Binary Image Conversion:**
   - Compute the **mean pixel intensity** of the resulting matrix.
   - If a pixel value is **greater than the mean**, set it to **black (0)**.
   - Otherwise, set it to **white (255)**.

### **Additional:**
- Implemented **two additional filters**.

## References & Additional Resources
- **Sobel Edge Detection in Digital Image Processing** - [YouTube Video](https://www.youtube.com/watch?v=Yz7h9L4gecQ)

- **Screenshots**:

<table>
        <tr><td><img src="https://github.com/user-attachments/assets/12817a48-0a85-4368-afa6-f7012153bf98" alt="Sharpen"></td></tr>
        <tr><td><img src="https://github.com/user-attachments/assets/943bf804-e4ce-42e4-92f7-57afd6712c8f" alt="Sharpen"></td></tr>
        <tr><td><img src="https://github.com/user-attachments/assets/1fab6277-1807-46bd-bdcb-bc4b5e94ee18" alt="Sobel"></td></tr>
</table>
