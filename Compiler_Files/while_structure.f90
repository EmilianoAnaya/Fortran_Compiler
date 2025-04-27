integer :: i, j, m, x, b, c

i = 0
x = 10
b = 30
c = 30

print*, "Inicia ciclo while"
do while (i <= 15)
    print*, "Valor de 'i':", i
    if (i == 5) then
        print*, "El ciclo va a la mitad"
	print*,
	print*, "Inicia do normal anidado"
	do j = 0, 10
		print*, "Valor de j:", j
		select case (x)
		case (10)
			print*, "El valor de 'x' es 10!"
			print*,
			print*, "Se ejecuta un nuevo do!"
			do m = 10, 1, -1
				print*, "El valor de 'm' es:", m
			end do 
			print*, "Termina el do"
			print*,
		case (20)
			print*, "El valor de 'x' es 20!"
			print*,
			print*, "Entramos a un nuevo select"
			select case (c)
			case (20)
				print*, "El valor de 'c' es 20 :D"
			case (30)
				print*, "El valor de 'c' es 30 c:"
			case default
				print*, "No sé que es 'c' D:"
			end select
			print*, "Termina el select"
			print*,
		case (30)
			print*, "El valor de 'x' es 30!"
			print*,
			print*, "Entramos a un if"
			if (b == 20) then
				print*, "El valor de 'b' es 20"
			else if (b == 30) then 
				print*, "El valor de 'b' es 30"
			else
				print*, "No sé que es 'b'"
			end if
			print*, "Salimos del if"
			print*,
		case default
			print*, "No sé que hacer jeje :D"
		end select
	end do
	print*, "Termina do normal anidado"
	print*,
    end if
    i = i + 1
end do
print*, "Fin ciclo while"