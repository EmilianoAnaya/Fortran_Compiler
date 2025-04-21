use fpm_error, only : error_t
use fpm_strings
integer :: alpha
real :: beta, respuesta
logical :: flag
character :: msg
msg = "Hello World"
flag = True
alpha = 49
beta = 15.34 * alpha
respuesta = alpha - 98 + beta * 7
print*, "alpha:", alpha
print*, "beta:", beta
print*, "Respuesta:", respuesta
print*, "Flag:", flag
print*, "Msg:", msg
if (beta < 50) then
print*, "Hello Mario"
else if (alpha <= 10 * 5) then
print*, "Bye bye Mario"
else if (respuesta < 80) then
print*, "Mario and Luigi"
else
print*, "Zzzzzz"
end if
print*, "Se termino el if"
if (msg == "Hello World") then
print*, "La bandera es verdadera"
else
print*, "La bandera es falsa"
end if
print*, "Se acabo el segundo if"