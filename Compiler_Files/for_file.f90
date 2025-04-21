integer :: i, j, x
x = 30

do i = 10, 0, -1
	if (i == 5) then
		print*, "El valor de 'i' es 5"
		select case (x)
		case (15)
			print*, "'x' es 15"
		case (30) 
			print*, "'x' es 30"
		case default
			print*, "No se que eres"
		end select
	end if
	do j = 0, 5
		print*, "Valor de 'j':", j
	end do
	print*, "Valor del for primario 'i':", i
end do
print*,
print*, "Se acabó el do con un valor de 'i' de:", i
print*, "Y el valor de 'j' es:", j