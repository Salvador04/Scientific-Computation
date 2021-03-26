'''
Universidad Nacional Autonoma de Mexico.
Licenciatura en ciencias genomicas - Computo Cientifico 2020.
Salvador Gonzalez Juarez.

Proyecto final.
Programa 5: Lagrange.py
Calcula la interpolacion de un valor dado un conjunto de puntos u obtiene el polinomio de la funcion que siguen estos mismos, utilizando el metodo de Interpolacion de Lagrange.
'''

# Importa las librerias que ayudan a realizar el algebra del programa
import sympy as sp
from sympy import sympify, poly

def interpolacion(valores_x, valores_y, flag, valor = 1):
	'''
  	Funcion encargada de aplicar la formula general del metodo de interpolacion de Lagrange.
  	param valores_x: list, lista que contiene todos los valores de 'x'.
  	param valores_y: list, lista que contiene todos los valores de 'y.
  	param flag: bool, bandera que indica la modalidad del programa (si se busca interpolar un valor u obtener el polinomio).
  	param valor: float, valor que se busca interpolar. Por default es '1' y no es requerido si se quiere obtener el polinomio.
  	return el valor interpolado o el polinomio, dependiendo de la modalidad.
  	'''
	if flag:
		x = valor
	else:
		x = sp.Symbol('x')

	# Inicializa las variable que utilizan las iteraciones.
	nominador = 1
	denominador = 1
	polinomio = 0
	indice = 0

	# Realiza las iteraciones correspondientes al metodo de interpolacion de Lagrange.
	for xi in valores_x:
		for xj in valores_x:

			# Continua solo si se cumple la condicion impuesta por el metodo de Lagrange para los valores de 'xj' y 'xi'.
			if xj != xi:
				if flag:
					nominador = nominador * (x - xj)
					denominador = denominador * (xi - xj)
				else:
					nominador = sympify(nominador * (x - xj))
					denominador = sympify(denominador * (xi - xj))

		# Calcula el valor de cada uno de los terminos.
		if flag:
			termino = (nominador / denominador) * valores_y[indice]
			polinomio = polinomio + termino
		else:
			termino = sympify((nominador / denominador) * valores_y[indice])
			polinomio = sympify(polinomio + termino)

		# Inicializa los valores de las variables utilizadas para la siguiente iteracion.
		indice = indice + 1
		nominador = 1
		denominador = 1

	return polinomio

# Inicio del programa.
print("Bienvenido a Lagrange. Este programa calcula la interpolacion de un valor dado un conjunto de puntos u obtiene el polinomio de la funcion que siguen estos mismos, utilizando el metodo de Interpolacion de Lagrange.")

# Pide al usuario un numero correcto de puntos.
cantidad_puntos = 0
while cantidad_puntos <= 1:
	cantidad_puntos = int(input("\nEscribe el numero de puntos: "))
	if cantidad_puntos <= 1:
		print("El valor debe ser mayor a 1. Intentalo de nuevo.")

# Genera un par de listas donde se guardaran los valores en 'x' y en 'y' de los puntos, respectivamente.
valores_x = []
valores_y = []

# Pide al usuario los valores en 'x' y en 'y' de todos los puntos, y los guarda en la lista correspondiente.
for i in range(cantidad_puntos):
	valores_x.append(float(input("\nIngresa el valor en 'x' del punto " + str(i + 1) + ": ")))
	valores_y.append(float(input("Ingresa el valor en 'y' del punto " + str(i + 1) + ": ")))

# Pregunta al usuario que modalidad del programa quiere usar.
flag = None
while (flag != 'i') and (flag != 'p'): 
	flag = input("\nSi quieres interpolar un valor, escribe 'i'. Si quieres obtener el polinomio, escribe 'p': ")
	if (flag != 'i') and (flag != 'p'):
		print("Intentalo de nuevo.")

# Si el usuario eligio la modalidad de interpolacion de un valor, continua con el siguiente codigo.
if flag == 'i':

	# Obtiene el valor a interpolar, lo interpola e imprime el resultado.
	lista_valores = (input("\nIngresa los valores que quieres interpolar (separa los valores con un espacio): "))
	lista_valores = lista_valores.split(" ")
	for valor in lista_valores:
		resultado = interpolacion(valores_x, valores_y, True, float(valor))
		print("\nEl valor interpolado de " + valor + " es: " + str(resultado))

# Si el usuario eligio la modalidad de obtencion del polinomio, continua con el siguiente codigo.
else:

	# Obtiene el polinomio de la funcion.
	resultado = interpolacion(valores_x, valores_y, False)

	# Prepara el polinomio para una correcta impresion.
	resultado = str(poly(resultado))
	resultado = resultado.lstrip("Poly(").rstrip(")")
	resultado = resultado.split(",")

	# Imprime solo el polinomio como resultado.
	print("\nEl polinomio es de la funcion es: " + str(resultado[0]))

'''
DICCIONARIO DE VARIABLES:

cantidad_puntos: int, variable que representa la cantidad de puntos que seran usados para hacer la interpolacion. 

denominador: float o sympify, multiplicador usado para calcular el denominador de cada uno de los terminos en la funcion interpolacion( ).

flag: bool, bandera que indica la modalidad del programa (si se busca interpolar un valor u obtener el polinomio).

i: int, contador utilizado para recorrer listas.

indice: int, variable de tipo acumulador utilizada para poder accesar de manera correcta a los valores que contiene la lista valores_y, dentro de  la funcion interpolacion( ).

lista_valores: list, lista que contiene todos los valores que el usuario desea interpolar.

nominador: float o sympify, variable de tipo multiplicador usado para calcular el nominador de cada uno de los terminos en la funcion interpolacion( ).

polinomio: float o sympify, variable que contiene el valor del resultado de la interpolacion, ya sea en forma de polinomio o como polinomio resuelto. Se calcula como indica el metodo de Lagrange. Es el valor retornable de la funcion interpolacion( ).

resultado: float o sympify, variable que representa el resultado de la interpolacion de cada valor, o el polinomio que describe la curva formada por los puntos.

termino: float o sympify, variable temporal que almacena el valor de un termino del polinomio, para luego sumarlo con el resto del polinomio. Es usada dentro de la funcion interpolacion( ).

valor: float, variable que representa uno de los valores que el usuario quiere interpolar.

valores_x: list, lista que contiene el valor en 'x' de cada uno de los puntos proporcionados por el usuario.

valores_y: list, lista que contiene el valor en 'y' de cada uno de los puntos proporcionados por el usuario.

x (en modo interpolacion): float, variable que almacena el valor del parametro valor en la funcion interpolacion( ).

x (en modo polinomio): sympify, literal 'x' dentro de la ecuacion.

xi: float, variable que representa uno de los valores de la lista valores_x, y es utilizada para crear el denominador de cada uno de los terminos en la funcion interpolacion( ).

xj: float, variable que representa uno de los valores de la lista valores_x, y es utilizada para crear el nominador y denominador de cada uno de los terminos en la funcion interpolacion( ).
'''