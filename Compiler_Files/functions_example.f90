program functions_example

integer :: i, j, result
integer :: array1(5)

i = 15
j = 20

array1 = [1, 2, 3, 4, 5]

result = sumar(array1(4), i) + sumar(12, j)
print*, "Resultado de la suma de 'i' más 'j':", result

result = restar(j, 10)
print*, "Resultado de la resta de 'j' menos '10':", result

result = sumar(12, 40) - restar(j, i)
print*, "Resultado de resta de 'sumar(12, 40)' menos 'restar(j,i)':", result

end program functions_example

integer function sumar(a, b)
    integer intent(in) :: b, a
    integer :: resultado
    resultado = a + b
    print*, "Resultado:", resultado
    sumar = resultado
end function sumar

real function restar(a, b)
    real intent(in) :: a, b
    restar = a - b
end function restar
