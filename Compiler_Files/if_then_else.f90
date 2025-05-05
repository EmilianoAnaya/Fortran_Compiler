program if_then_else
integer :: beta, alpha, zeta, mi_numero, mi_select

beta = 40
alpha = 50
zeta = 20
mi_numero = 70
mi_select = 20

print*, "Empieza el if"

if (beta == 50) then
    print*, "Hello Mario"
    
else if (beta < 10 * 5) then
    print*, "Bye bye Mario"
    if (alpha < 49) then
        print*, "Alpha es menor"
    else
        print*, "Alpha es mayor"
        if (zeta < 30) then
            print*, "Tercer if anidado"
            print*, "Inicia select en if"
            select case (mi_numero + 20)
            case (50)
                print*, "El número es 50"
            case (70)
                print*, "El número es 70"
            case (90)
                print*,
                print*, "Evaluando 'select' anidado"
                select case (mi_select)
                case (10)
                    print*, "'mi_select' es 10"
                case (20)
                    print*, "'mi_select' es 20"
                case default
                    print*, "No sé que es 'mi_select'"
                end select
                print*, "Se acabo el select anidado"
                print*,
                
                print*, "El número es 90"
                if (90 > beta) then
                    print*, "El número es mayor que 'beta'"
                else
                    print*, "El número es menor que 'beta'"
                end if
            case default
                print*, "El número no es ni 50, 70 o 90"
            end select
            print*, "Termina select en if"
        else if (alpha > 30) then
            print*, "Tercer if anidado falso"
        else
            print*, "Rariterium"
        end if
        print*, "AJUA"
    end if
    print*, "Doble if anidado"
else if (beta < 20) then
    print*, "Mario and Luigi"
else
    print*, "Zzzzzz"
end if

print*, "Se acabo el if"
if (beta > 69) then
    print*, "Segundo If"
else
    print*, "Segundo if incorrecto"
end if
print*, "Adios"

end program if_then_else
