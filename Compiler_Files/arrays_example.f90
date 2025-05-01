integer :: array1(10), j, i
real :: array2(5)
character :: hola

j = 14 * 2

array1 = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
print*, "Arreglo 'array1' inicial:", array1
do i = 0, 9
    array1(i) = i * 2
    print*, "Posición", i, "Cambia a:", array1(i)
end do
print*, "Arreglo 'array1' final:", array1