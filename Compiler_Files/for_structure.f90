program for_structure
integer :: i, j, z, x, alpha, beta

alpha = 30
beta = 20 + alpha

print*, "Inicio primer do"
do i = 10, 0, -1
    if (i == 5) then
        print*, "El valor de 'i' es 5"
        select case (beta)
        case (10)
            print*, "El valor de 'beta' es 10"
        case (20)
            print*, "El valor de 'beta' es 20"
        case (50)
            print*, "El valor de 'beta' es 50"
	    	if (alpha < beta) then
			print*, "'alpha' es menor que 'beta'"
			print*, "Inicia do anidado"
			do x = 0, 5
				print*, "Valor de 'x':" x
				select case (x)
				case (0)
					print*, "Apenas inicio el do"
				case (3)
					print*, "El do va a la mitad"
				case (5)
					print*, "Ha terminado el do"
				end select	
			end do
			print*, "Termina do anidado"
		end if
        case default
            print*, "No sé que valor es 'beta'"
        end select
    end if
    print*, "valor de 'i':" i
end do
print*, "Final primer do"
print*,
print*, "Inicio segundo do"
do j = 15, 1, -5
    print*, "valor de 'j':" j
    do z = 1, 3
        print*, "valor de 'z':" z
        select case (beta)
        case (10)
            print*, "El valor de 'beta' es 10"
        case (20)
            print*, "El valor de 'beta' es 20"
        case default
            print*, "No sé que valor es 'beta'"
        end select
    end do
end do
print*, "Final segundo do"
print*,
print*, "Estado final de 'i':", i
print*, "Estado final de 'j':", j
print*, "Estado final de 'z':", z
end program for_structure