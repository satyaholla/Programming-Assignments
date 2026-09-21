/**
 * Copyright (c) 2020 MIT License by 6.172 Staff
 *
 * Permission is hereby granted, free of charge, to any person obtaining a copy
 * of this software and associated documentation files (the "Software"), to
 * deal in the Software without restriction, including without limitation the
 * rights to use, copy, modify, merge, publish, distribute, sublicense, and/or
 * sell copies of the Software, and to permit persons to whom the Software is
 * furnished to do so, subject to the following conditions:
 *
 * The above copyright notice and this permission notice shall be included in
 * all copies or substantial portions of the Software.
 *
 * THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
 * IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
 * FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
 * AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
 * LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
 * FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS
 * IN THE SOFTWARE.
 **/

#include "../utils/utils.h"


// GLOBALS
#define BLOCK_SIZE 64 // this block size is fixed - changing this value does not lead to working code. It is defined only to prevent errors in typoing `64`
#define BITS_PER_BYTE 8
#define LOOP_UNROLL 8
#define BLOCK_SIZE_IN_BYTES (BLOCK_SIZE / BITS_PER_BYTE)

// masks used in rotation algorithm for 64x64 bit matrix
#define stay_mask_32 0xFFFFFFFE00000001
#define stay_mask_16 0xFFFE0001FFFE0001
#define stay_mask_08 0xFE01FE01FE01FE01
#define stay_mask_04 0xE1E1E1E1E1E1E1E1
#define stay_mask_02 0x9999999999999999
#define stay_mask_01 0x5555555555555555

// external storage used in rotating 64x64 bit matrix
static uint64_t rotation_matrix_1[BLOCK_SIZE];
static uint64_t rotation_matrix_2[BLOCK_SIZE];


// FUNCTION SIGNATURES
              void rotate_bit_matrix(uint8_t *img, const bits_t N);
static        void rotate_bit_matrix_64(uint64_t * matrix, uint64_t * scratch, const uint32_t row_size);
static        void rotate_rows_left(uint64_t * restrict matrix, const uint8_t additional_shift);
static        void rotate_columns_down(uint64_t * restrict matrix, uint64_t * restrict scratch);
static inline void copy_from_external_matrix(uint64_t * restrict img_pointer, uint64_t * restrict external_matrix, uint32_t N_blocks_of_64);
static inline void copy_from_external_matrix(uint64_t * restrict img_pointer, uint64_t * restrict external_matrix, uint32_t N_blocks_of_64);
static inline void little_endian_convert_64_bit_matrix(uint64_t matrix[BLOCK_SIZE]);


// FUNCTIONS

/**
 * @param img pointer to square image matrix to be rotated, represented as a contiguous block of `N * N` bits
 * @param N size of the side length of the image, in number of bits
 * Requires: N is a multiple of 64
 * Effects: Mutates `matrix` by rotating the corresponding image 90 degrees clockwise
*/
void rotate_bit_matrix(uint8_t *img, const bits_t N) {
  img = __builtin_assume_aligned(img, 8);
  const uint32_t row_size = bits_to_bytes(N);
  const uint32_t N_blocks_of_64 = N / BLOCK_SIZE;

  if (N_blocks_of_64 & 1) { // if the number of blocks in a row is odd, we need to rotate the central block
    uint64_t * middle_block_location = get_start_of_64_by_64_block(img, row_size, N_blocks_of_64 / 2, N_blocks_of_64 / 2);
    copy_to_external_matrix(middle_block_location, rotation_matrix_1, N_blocks_of_64);
    rotate_bit_matrix_64(rotation_matrix_1, rotation_matrix_2, N_blocks_of_64);
    copy_from_external_matrix(middle_block_location, rotation_matrix_1, N_blocks_of_64);
  }

  for (uint32_t h = 0; h < (N_blocks_of_64 + 1) / 2; h++) { // if N blocks is odd, we need to iterate through blocks within the central cross,
                                                            // which is why we iterate until `(N_blocks_of_64 + 1) / 2`.
    for (uint32_t w = 0; w < N_blocks_of_64 / 2; w++) {
      uint64_t * current_location = get_start_of_64_by_64_block(img, row_size, w, h);
      uint64_t * next_location;
      copy_to_external_matrix(current_location, rotation_matrix_1, N_blocks_of_64);
      
      uint32_t temp_index;
      uint64_t * matrix, * scratch;

      uint32_t i = w, j = h;
      #pragma clang loop unroll(enable)
      for (uint32_t quadrant = 0; quadrant < 4; quadrant++) {
        // alternate which rotation_matrix is the `matrix` and which is the `scratch` extra storage, depending on the quadrant we are in
        matrix = (quadrant & 1)? rotation_matrix_2: rotation_matrix_1;
        scratch = (quadrant & 1)? rotation_matrix_1: rotation_matrix_2;
        rotate_bit_matrix_64(matrix, scratch, N_blocks_of_64);

        // rotate (i,j) clockwise
        temp_index = i;
        i = N_blocks_of_64 - j - 1;
        j = temp_index;
        next_location = get_start_of_64_by_64_block(img, row_size, i, j);
        
        if (quadrant != 3)
          copy_to_external_matrix(next_location, scratch, N_blocks_of_64); // we copy to `scratch`, as that will become `matrix` for the next quadrant
        copy_from_external_matrix(next_location, matrix, N_blocks_of_64);

        current_location = next_location;
      } 
    }
  }
  return;
}

/**
 * @param matrix pointer to matrix to be rotated, represented as an array of 64 uint64_t values
 * @param scratch pointer to matrix which can be used as extra storage during the algorithm, represented as an array of 64 uint64_t values
 * Effects: Mutates `matrix` by rotating its corresponding sub-image 90 degrees clockwise
 *          Mutates `scratch` arbitrarily
 * 
 * See 6.106 recitation notes for explanation of the row-column-row algorithm used
*/
static void rotate_bit_matrix_64(uint64_t * matrix, uint64_t * scratch, const uint32_t N_blocks_of_64) {
  // convert out of little endian so that bit operations on 64 bit values work
  little_endian_convert_64_bit_matrix(matrix);

  // rotate all rows r left by r + 1
  rotate_rows_left(matrix, 1);

  // rotate each column c down by c + 1
  rotate_columns_down(matrix, scratch);

  // // rotate all rows r left by r
  rotate_rows_left(matrix, 0);

  // convert back into little endian
  little_endian_convert_64_bit_matrix(matrix);
}

/**
 * @param matrix pointer to 64x64 bit matrix whose rows are to be rotated, represented as an array of 64 uint64_t values
 * @param additional_shift
 * Effects: Mutates `matrix` by left-rotating each row `r` of the matrix by `r + additional_shift`, where row numbers are zero-indexed from the top of the matrix
*/
static void rotate_rows_left(uint64_t * restrict matrix, const uint8_t additional_shift) {
  for (int r = 0; r < BLOCK_SIZE; r++) {
    //  (matrix[r] << ((r + additional_shift) % BLOCK_SIZE)) | (matrix[r] >> ((2 * BLOCK_SIZE - r - additional_shift) % BLOCK_SIZE));
    matrix[r] = __builtin_rotateleft64(matrix[r], r + additional_shift); 
  }
}

/**
 * @param matrix pointer to 64x64 bit matrix whose columns are to be rotated, represented as an array of 64 uint64_t values
 * @param scratch pointer to 64x64 bit matrix which can be used as extra storage during the algorithm, represented as an array of 64 uint64_t values
 * Effects: Mutates `matrix` by down-rotating each column `c` of the matrix by `c + 1`, where column numbers are zero-indexed from the left of the matrix
*/
static void rotate_columns_down(uint64_t * restrict matrix, uint64_t * restrict scratch) {
  // rotate down by 32
  #pragma clang loop unroll(enable)
  for (int r = 0; r < BLOCK_SIZE; r++)
    scratch[r] = (matrix[r] & stay_mask_32) | (matrix[(r + BLOCK_SIZE - 32) % BLOCK_SIZE] & ~stay_mask_32);
  
  // rotate down by 16
  #pragma clang loop unroll(enable)
  for (int r = 0; r < BLOCK_SIZE; r++)
    matrix[r] = (scratch[r] & stay_mask_16) | (scratch[(r + BLOCK_SIZE - 16) % BLOCK_SIZE] & ~stay_mask_16);

  // rotate down by 8
  #pragma clang loop unroll(enable)
  for (int r = 0; r < BLOCK_SIZE; r++)
    scratch[r] = (matrix[r] & stay_mask_08) | (matrix[(r + BLOCK_SIZE - 8) % BLOCK_SIZE] & ~stay_mask_08);

  // rotate down by 4
  #pragma clang loop unroll(enable)
  for (int r = 0; r < BLOCK_SIZE; r++)
    matrix[r] = (scratch[r] & stay_mask_04) | (scratch[(r + BLOCK_SIZE - 4) % BLOCK_SIZE] & ~stay_mask_04);

  // rotate down by 2
  #pragma clang loop unroll(enable)
  for (int r = 0; r < BLOCK_SIZE; r++)
    scratch[r] = (matrix[r] & stay_mask_02) | (matrix[(r + BLOCK_SIZE - 2) % BLOCK_SIZE] & ~stay_mask_02);
  
  // rotate down by 1
  #pragma clang loop unroll(enable)
  for (int r = 0; r < BLOCK_SIZE; r++)
    matrix[r] = (scratch[r] & stay_mask_01) | (scratch[(r + BLOCK_SIZE - 1) % BLOCK_SIZE] & ~stay_mask_01);
}


// HELPER FUNCTIONS

/**
 * @param matrix_start a pointer to the beginning of the input matrix
 * @param row_size the size, in bytes, of a row of the matrix
 * @param w the index of the column of some 64-bit x 64-bit block B in the matrix
 * @param h the index of the row of B
 * @returns a pointer to the first row (as a 64-bit integer) of B
*/
static inline uint64_t * get_start_of_64_by_64_block(uint8_t * matrix_start, uint32_t row_size, uint32_t w, uint32_t h) {
  return (uint64_t *) (matrix_start + BLOCK_SIZE * row_size * h + (BLOCK_SIZE / BITS_PER_BYTE) * w);
}

/**
 * @param img_pointer pointer to start of 64x64 bit block within larger matrix `M`
 * @param external_matrix pointer to external matrix to which data is being copied, represented as an array of 64 uint64_t values
 * @param N_blocks_of_64 number of blocks of 64 bits within a row of matrix `M`
 * Effects: Mutates `external_matrix`, by copying the data in the block represented by `img_pointer` to it
*/
static inline void copy_to_external_matrix(uint64_t * restrict img_pointer, uint64_t * restrict external_matrix, uint32_t N_blocks_of_64) {
  img_pointer = __builtin_assume_aligned(img_pointer, 8);
  
  #pragma clang loop vectorize(enable) interleave(enable)
  for (uint32_t r = 0; r < BLOCK_SIZE; r++) {
    external_matrix[r] = *(img_pointer + N_blocks_of_64 * r);
  }
}

/**
 * @param img_pointer pointer to start of 64x64 bit block within larger matrix `M`
 * @param external_matrix pointer to external matrix from which data is being copied, represented as an array of 64 uint64_t values
 * @param N_blocks_of_64 number of blocks of 64 bits within a row of matrix `M`
 * Effects: Mutates `M`, by copying the data in `external_matrix` to it
*/
static inline void copy_from_external_matrix(uint64_t * restrict img_pointer, uint64_t * restrict external_matrix, uint32_t N_blocks_of_64) {
  img_pointer = __builtin_assume_aligned(img_pointer, 8);

  #pragma clang loop vectorize(enable) interleave(enable)
  for (uint32_t r = 0; r < BLOCK_SIZE; r++) {
    *(img_pointer + N_blocks_of_64 * r) = external_matrix[r];
  }
}

/**
 * @param matrix 64x64 bit matrix of values, represented as an array of 64 uint64_t values
 * Effects: mutates `matrix`, by toggling the little endian representation of each row
 *          This operation is an involution, so we don't need separate functions for converting to vs. from little endian
*/
static inline void little_endian_convert_64_bit_matrix(uint64_t matrix[BLOCK_SIZE]) {
  #pragma clang loop unroll(enable)
  for (int r = 0; r < BLOCK_SIZE; r++) {
    *(matrix + r) = __builtin_bswap64(*(matrix + r));
  }
}
