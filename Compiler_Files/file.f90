integer :: mi_numero
character :: mi_string, my_string

mi_string = "buenas"
my_string = "adios"
mi_numero = 30

print*, "Primer Select"
select case (mi_numero + 20)
case (50)
    print*, "El número es 50"
    mi_numero = mi_numero + 20
    print*, "Inicia select anidado"
    select case (mi_string)
    case ("hola")
        print*, "Mi string es hola"
    case ("buenas")
        print*, "Mi string es buenas"
        if (mi_numero == 30) then
            print*, "Y mi numero es 30"
        else
            print*, "Y mi numero NO es 30 :("
        end if
    case default
        print*, "No sé que es mi string"
    end select
    print*, "Se acabo select anidado"
case (70)
    print*, "El número es 70"
case (90)
    print*, "El número es 90"
case default
    print*, "El número no es ni 50, 70 o 90"
end select
print*, "Se acabó el select"
print*, "My number is now:", mi_numero

print*, "Segundo Select"
select case (my_string)
case ("hola")
    print*, "El numero es 50"
case ("adios")
    print*, "El número es 70"
case ("buenas")
    print*, "El número es 90"
case default
    print*, "El número no es ni 50, 70 o 90"
end select
print*, "Se acabó el segundo select"