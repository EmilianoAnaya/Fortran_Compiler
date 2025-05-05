program arrays_example
integer :: array1(10), j, i, x, array2(10)
character :: hola

x = 15
array1 = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

print*, "Arreglo 'array1' inicial:", array1
do i = 9, 0, -1
    array1(i) = array1(i) * 2
    if (array1(i) == 10) then
        print*,
        print*, "HELLO WORLD", i
        print*,
        print*, "Entramos a un nuevo do!"
        do j = 0, 9
            print*, "Posición", j, "Se añade:", j
            array2(j) = j
        end do
        print*, "Salimos del do anidado"
        print*,
    end if
    print*, "Posición", i, "Cambia a:", array1(i)
end do
print*,
print*, "Arreglo 'array1' final:", array1
print*, "Arreglo 'array2':", array2

end program arrays_example