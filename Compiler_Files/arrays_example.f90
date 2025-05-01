integer :: array1(10), j, i
real :: array2(5)
character :: hola

j = 14 * 2

array1 = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
do i = 0, 9
    print*, "Valor de 'i':", i
    array1(i) = i * 2
end do
print*,