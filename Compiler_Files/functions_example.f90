program functions_example

integer :: i, j, result
integer :: array1(5)
character :: mi_variable

i = 15
j = 20

mi_variable = "hola"

array1 = [1, 2, 3, 4, 5]

if (mi_variable == "hola") then
    print*, "Se validó el char 'mi_variable'"
else
    print*, "chin :c"
end if

result = sumar(array1(4), i) + sumar(12, j)
print*, "Resultado de la suma de 'i' más 'j':", result

result = restar(j, 10)
print*, "Resultado de la resta de 'j' menos '10':", result

result = sumar(12, 40) - restar(j, i)
print*, "Resultado de resta de 'sumar(12 40)' menos 'restar(j i)':", result

end program functions_example

integer function sumar(a, b)
    integer intent(in) :: b, a
    integer :: resultado, i
    resultado = a + b

    print*,
    print*, "Comienza un if dentro de la funcion 'sumar'"
    if (resultado > 50) then
        print*, "La suma de 'a' más 'b' fue mayor que 50! :O"
    else
        print*, "La suma de 'a' más 'b' fue menor que 50! :c"
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

        if (result * i > 50) then
            print*, "'result':", result, "Es mayor que 50 al ser multiplicado por:", i
        end if
    end do
    print*, "Termina iteracion do en 'restar'"
    print*,
    restar = a - b
end function restar
