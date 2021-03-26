'''
Universidad Nacional Autonoma de Mexico.
Licenciatura en ciencias genomicas - Computo Cientifico 2020.
Salvador Gonzalez Juarez.

Proyecto final.
Programa 9: Euler.py
Calcula una solucion aproximada de una ecuacion diferencial, empleando el metodo de Euler.
'''

# Importa las librerias que ayudan a realizar el algebra del programa.
import sympy as sp
from sympy import sympify, N

# Importa una funcion para poder mostrar los resultados de una forma grafica.
from tabulate import tabulate

def tabular_x (valor_x0, valor_x, incremento):
	'''
	Funcion encargada de generar los valores de 'x' en el intervalo indicado.
	param valor_x0: float, valor que representa el inico del intervalo.
	param valor_x: float, valor que representa el final del intervalo.
	param incremento: float, valor que representa el incremento entre cada valor de 'x'.
	return list, lista que contiene los valores de 'x' dentro del intervalo.
	'''
	tabulacion_x = []
	subintervalos = (valor_x - valor_x0) / incremento
	subintervalos = round(subintervalos, 0)
	temp = valor_x0
	for i in range(0, int(subintervalos)):
		tabulacion_x.append(temp)
		temp = temp + incremento
	return tabulacion_x

# Inicio del programa.
print("Bienvenido a Euler. Este programa calcula una solucion aproximada de una ecuacion diferencial, empleando el metodo de Euler.")

# Se obtiene la ecuacion que sera utilizada. Se verifica que no este mal escrita.
try:
	ecuacion = input("\nEscribe la ecuacion de la funcion: ")
	ecuacion = sympify(ecuacion, evaluate = False)

# Si la ecuacion esta mal escrita, indica el error y termina el programa. Si esta bien, continua con el programa.
except AttributeError:
	print("\nError: la ecuacion no esta bien escrita. Intentalo de nuevo.")
else:

	# Se obtienen los parametros que emplea el metodo.
	valor_x0 = float(input("\nEscribe el valor inicial de 'x': "))
	valor_y0 = float(input("Escribe el valor inicial de 'y': "))
	incremento = float(input("\nEscribe el valor del incremento: "))
	valor_x = float(input("\nEscribe el valor de final de 'x': "))

	# Si no existe un intervalo, indica el error y termina el programa. De otro modo, continua con el programa.
	if (valor_x - valor_x0) == 0:
		print("\nError: no hay intervalo entre los parametros. Intentalo de nuevo.")
	else:

		# Se generan los valores de 'x' en el intervalo. Ademas se definen variables para la sustitucion de valores en la ecuacion y
		# se genera una lista la cual ira guardando los resultados para la construccion de una tabulacion.
		valores_x = tabular_x(valor_x0, valor_x, incremento)
		x = sp.Symbol('x')
		y = sp.Symbol('y')
		resultados = []

		# Realiza las iteraciones correspondientes al metodo de Euler, mejorando la aproximacion por cada iteracion.
		# Ademas, introduce los valores actuales de las variables 'x' y 'y' en la tabla de resultados.
		for i in valores_x:
			resultados.append([i, valor_y0])
			valor_y0 = valor_y0 + incremento * N(ecuacion.subs([(x, i), (y, valor_y0)]))

		# Introduce los ultimos valores de las variables 'x' y 'y' en la tabla de resultados.
		resultados.append([i + incremento, valor_y0])

		# Se imprimen los resultados del problema.
		print("\n", tabulate(resultados, headers = ["x","y(x)"]))
		print("\nEl resultado es: " + str(valor_y0))

'''
DICCIONARIO DE VARIABLES:

ecuacion: sympify, funcion de la ecuacion diferencial del problema.

i: int, contador utilizado para recorrer listas.

incremento: float, almacena el incremento constante que debe hacerse para llegar del valor 'x' inicial a el valor 'x' final. Es utilizada para calcular el numero de subintervalos entre esos valores.

resultados: list, lista de dos dimensiones que almacena los valores de 'x' y los valores en 'y' asociados a cada una de esas 'x'.

subintervalos: float, almacena el numero de subintervalos de una longitud igual al valor del incremento, que existen dentro del intervalo entre el valor inicial y final de 'x'. Es utilizada en la funcion tabular_x( ).

tabulacion_x: list, lista que almacena los valores de frontera entre cada subintervalo entre el valor 'x' inicial y el valor 'x' final, en la funcion tabular_x( ).

temp: float, variable temporal que almacena el valor del limite entre subintervalos en la funcion tabular_x( ).

valor_x: float, almacena el valor final de 'x', requerido por el metodo de Euler.

valor_x0: float, almacena el valor inicial de 'x', requerido por el metodo de Euler.

valor_y0: float, almacena el valor en 'y' asociado a 'x' inicial.

valores_x: list, es el conjunto de valores que son frontera entre los subintervalos. Este conjunto representa los valores de 'x'.

x: sympify, literal 'x' dentro de la ecuacion.

y: sympify, literal 'y' dentro de la ecuacion.
'''