program functions_example

integer :: i, j
real :: result
integer :: array1(5)

i = 15
j = 20

array1 = [1, 2, 3, 4, 5]

result = sumar(array1(0), array1(4)) + sumar(array1(1), j)
print*, "Resultado de la suma de dos funciones de 'sumar' es:", result

result = restar(j, 10) * 2 + 2
print*, "Resultado de la function 'restar' por 2 es:", result

result = sumar(12, 40) - restar(j, i)
print*, "Resultado de resta de 'sumar(12 40)' menos 'restar(j i)':", result

end program functions_example

real function sumar(a, b)
    integer intent(in) :: b
    real intent(in) :: a
    integer :: i
    real :: resultado
    resultado = a + b

    print*,
    print*, "Comienza un if dentro de la funcion 'sumar'"
    if (resultado > 50) then
        print*, "La suma de", a, "más", b, "fue mayor que 50! :O"
    else
        print*, "La suma de", a, "más", b, "fue menor que 50 :c"
    end if
    print*, "Termina el if dentro de la funcion 'sumar'"
    print*,
    
    sumar = resultado
end function sumar

real function restar(a, b)
    real intent(in) :: a, b
    integer :: i
    real :: result
    result = a - b
    print*,
    print*, "Empieza iteracion do en 'restar'"
    do i = 0, 10
        select case (i)
        case (5)
            print*, "La iteracion do va justo en la mitad"
        case (10)
            print*, "La iteración do esta en el final"
        end select

        if ((result * i) > 50) then
            print*, "'result':", result, "Es mayor que 50 al ser multiplicado por:", i
        end if
    end do
    print*, "Termina iteracion do en 'restar'"
    print*,
    restar = result
end function restar
