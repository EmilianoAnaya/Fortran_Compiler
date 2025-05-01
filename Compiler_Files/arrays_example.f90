integer :: array1(10), i, j
real :: array2(5)
character :: hola

j = 15
i = (j + 15) * 2

array1 = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
array1(0) = i + j
array1(9) = i - j
array1(1) = i * j
