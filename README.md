# Gestion_Horas_Django

Gestor de horas trabajadas para una empresa.
Todo usuario necesita estar dentro de un tenant que sera la empresa.
Los usuarios tienen que tener roles diferenciados entre Usuario, manager y recursos humanos.
Los usuarios con rol recursos humanos son los unicos que pueden añadir usuarios al sitema de la empresa.
Los usuarios con el rol usuario pueden introducir horas trabajadas en los diferentes proyectos. Cuando tengan las horas menusales, 
pueden confirmarlas para que le manager les de el visto bueno.
Los usuarios con rol manager pueden añadir proyectos al tenant asi como visualizar todos los graficos sobre las horas de los empleados de su equipo. 
El manager aceptara las horas de los miembros del equipo al final de mes.
Se ha añadido un calendario para que el usuario pueda interactuar con el para añadir o ver las horas introducidas.
**En un futuro se plantea hacer un sistema para el pago automatizado de las horas, en cuanto el manager acepte las horas de los miembros del equipo.

Se han utilizado las tecnologias:
- Django
- PostgresQL
- javaScript
- HTML
- CSS
- Docker
