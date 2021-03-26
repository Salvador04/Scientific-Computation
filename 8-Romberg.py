'''
Universidad Nacional Autonoma de Mexico.
Licenciatura en ciencias genomicas - Computo Cientifico 2020.
Salvador Gonzalez Juarez.

Proyecto final.
Programa 8: Romberg.py 
Calcula una solucion aproximada de una integral, utilizando el metodo de Integracion de Romberg.
'''

# Importa las librerias que ayudan a realizar el algebra del programa.
import sympy as sp
from sympy import sympify, N

def calcular_I(J, iteraciones, intervalo):
	'''
	Funcion encargada de calcular el primer valor de 'I' para cada iteracion.
	param J: float, valor actual de 'J', requerido para calcular el valor de 'I'.
	param iteraciones: int, iteracion actual. Es imporante para calcular el valor fraccionario.
	param intervalo: float, longitud del intervalo, requerido para calcular el valor de 'I'.
	return float, valor de 'I' sin refinar.
	'''
	I = (intervalo * J) / 2 ** iteraciones
	return I

def refinamiento(resultados, I):
	'''
	Funcion encargada de hacer el refinamiento del valor 'I'.
	param resultados: list, lista que contiene todos los valores obtenidos durante el refinamiento de la iteracion anterior.
	param I: float, valor actual de 'I'.
	return list, lista que contiene los valores de los nuevos refinamientos de 'I'.
	'''
	# Inicia las variables que seran utilizadas en la funcion.
	temp = 1
	resultados_temp = []

	# Almacena el valor actual de 'I' en la lista temporal.
	resultados_temp.append(I)
	
	# Realiza los refinamientos necesarios dependiendo de la iteracion actual, conforme indica el metodo de Romberg.
	# La iteracion actual se conoce por el numero de valores en el vector de resultados antes del siguiente codigo.
	# Ademas, almacena cada uno de los refinamientos obtenidos en el vector temporal.
	for i in resultados:
		coeficiente = 4 ** temp
		I = (coeficiente * I - i) / (coeficiente - 1)
		resultados_temp.append(I)
		temp = temp + 1

	# Regresa una lista con los nuevos refinamientos de 'I'.
	return resultados_temp
	
# Inicio del programa.
print("Bienvenido a Romberg. Este programa calcula una solucion aproximada de una integral, utilizando el metodo de Integracion de Romberg.")

# Se obtiene la ecuacion que sera utilizada. Se verifica que no este mal escrita.
try:
	ecuacion = input("\nEscribe la ecuacion de la funcion: ")
	ecuacion = sympify(ecuacion, evaluate = False)

# Si la ecuacion esta mal escrita, indica el error y termina el programa. Si esta bien, continua con el programa.
except AttributeError:
	print("\nError: la ecuacion no esta bien escrita. Intentalo de nuevo.")
else:

	# Se obtiene el inicio y el final del intervalo, y se calcula su longitud.
	inicio_intervalo = float(input("\nEscribe el inicio del intervalo: "))
	final_intervalo = float(input("Escribe el final del intervalo: "))
	intervalo = final_intervalo - inicio_intervalo

	# Se obtiene el numero de decimales deseado.
	decimales = int(input("\nEscribe el numero de aproximacion de decimales: "))

	# Se inicializan las variables que seran utilizadas a lo largo del programa.
	resultados = []
	x = sp.Symbol('x')

	# Se calcula el valor inicial de 'J' y el valor inicial de 'I'. Almacena este ultimo en el vector de resultados.
	J = (N(ecuacion.subs(x, inicio_intervalo)) + N(ecuacion.subs(x, final_intervalo))) / 2
	I = calcular_I(J, 0, intervalo)
	resultados.append(I)

	# Inicializa las variables para controlar las iteraciones del programa.
	convergio = False
	iteraciones = 0

	# Itera el siguiente codigo hasta que los ultimos valores obtenidos para 'I' convergan en la precision deseada.
	while convergio == False:

		# Se guarda el valor de 'I' antes de la iteracion para poder calcular la convergencia.
		I_anterior = resultados[-1]

		# Se calcula el numero de terminos para calcular 'J' en la nueva iteracion.
		num_terminos = 2 ** iteraciones

		# Se preparan las variables necesarias para calcular 'J', incluyendo el valor de las fracciones como indica el metodo de Romberg.
		iteraciones = iteraciones + 1
		suma = 0
		fraccion_original = 1 / 2 ** iteraciones
		fraccion = fraccion_original

		# Se calcula el valor de cada termino para calcular el valor de 'J'.
		for i in range(num_terminos):
			suma = (N(ecuacion.subs(x, (inicio_intervalo + intervalo * fraccion)))) + suma
			fraccion = fraccion + 2 * fraccion_original

		# Termina de calcular el valor de 'J' y con ese valor calcula el primer valor de 'I' para la iteracion correspondiente.
		J = J + suma
		I = calcular_I(J, iteraciones, intervalo)

		# Refina el valor de 'I' como indica el metodo de Romberg.
		# Reemplaza los valores dentro del vector de resultados con cada uno de los refinamientos. Finalmente obtiene el valor mas reciente de 'I'.
		resultados = refinamiento(resultados, I)
		I = resultados[-1]

		# Calcula el error relativo entre los valores mas recientes de 'I'. Si es menor al criterio de paro, termina las iteraciones.
		if abs((I - I_anterior) / I) < (1 * 10 ** (0 - decimales)):
			convergio = True

	# Transforma el valor de 'I' a una cadena solo con los decimales deseados.
	resultado_lista = [digito for digito in str(I)]
	resultado_cadena = ''    
	for i in resultado_lista[:resultado_lista.index('.') + 1 + decimales]:
		resultado_cadena = resultado_cadena + str(i)

	# Imprime los resultados.
	print("\nEl resultado es:", resultado_cadena)
	print("\nLas iteraciones realizadas fueron:", (iteraciones))

'''
DICCIONARIO DE VARIABLES:

coeficiente: int, variable que almacena el valor del coeficiente utilizado para calcular los refinamienos de 'I', en la funcion refinamiento( ).

convergio: bool, bandera que indica si el metodo convergio entre la iteracion anterior y la iteracion actual.

decimales: int, valor que representa el numero de decimales de exactitud del resultado.

digito: str, variable temporal que almacena el caracter de cada digito del resultado, para convertir el numero en una lista que contiene como elementos dichos digitos.

ecuacion: sympify, funcion de la integral del problema.

final_intervalo: float, valor que representa el final del intervalo en la integral.

fraccion: float, valor que representa un multiplo de la fraccion original y es utilizado como coeficiente para calcular un termino especifico de 'J'. como indica el metodo de Romberg.

fraccion_original: float, valor que representa el coeficiente fraccionario minimo utilizado para calcular los terminos para calcular 'J', como indica el metodo de Romberg.

i: int, contador utilizado para recorrer listas.

I: float, valor que representa la aproximacion de la iteracion actual. 

I_anterior: float, valor que representa la aproximacion de la iteracion anterior.

inicio_intervalo: float, valor que representa el inicio del intervalo en la integral.

intervalo: float, longitud entre el inicio del intervalo y el final del intervalo.

iteraciones: int, contador que representa el numero de iteracion actual.

J: float, valor necesario para calcular la aproximacion de la iteracion actual, calculado como indica el metodo de Romberg.

num_terminos: int, indica el numero de terminos necesarios para calcular 'J'.

resultado_cadena: str, variable que almacena los caracteres de los digitos solo de la parte que se va a imprimir del resultado.

resultado_lista: list, lista cuyos elementos representan todos los digitos del resultado.

resultados: list, vector que almacena el valor de la aproxiimacion de la iteracion actual y sus respectivos refinamientos.

resultados_temp: list, vector temporal utilizado para almacenar los nuevos refinamientos de I, para luego retornar ese conjunto de valores en la funcion refinamiento( ).

suma: float, valor que representa el resultado de la suma de los terminos para calcular el nuevo valor de 'J'.

temp: int, contador que ayuda a calcular los coeficientes utilizados en el refinamiento de 'I', como indica el metodo de Romberg, utilizado en la funcion refinamiento( ).

x: sympify, literal 'x' dentro de la ecuacion.
'''