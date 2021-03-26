'''
Universidad Nacional Autonoma de Mexico.
Licenciatura en ciencias genomicas - Computo Cientifico 2020.
Salvador Gonzalez Juarez.

Proyecto final.
Programa 7: Simpson.py
Calcula una solucion aproximada de una integral, utilizando el metodo de Regla de Simpson de 1/3.
'''

# Importa las librerias que ayudan a realizar el algebra del programa.
import sympy as sp
from sympy import sympify, N

def tabular_x (inicio_intervalo, incremento, subintervalos):
	'''
	Funcion encargada de generar todos los valores de 'x' para la tabulacion del intervalo.
	param inicio_intervalo: float, valor que representa el inico del intervalo al cual se le realizara la tabulacion.
	param incremento: float, valor que representa el incremento entre cada valor de 'x' en la tabulacion.
	param subintervalos: int, valor que representa el numero de subintervalos, y por lo tanto, el numero de variables a tabular.
	return list, lista que contiene todos los valores de x dentro del intervalo.
	'''
	tabulacion_x = []
	valor_x = inicio_intervalo
	for i in range(0,subintervalos + 1):
		tabulacion_x.append(valor_x)
		valor_x = valor_x + incremento
	return tabulacion_x

def tabular_fx (ecuacion, tabulacion_x):
	'''
	Funcion encargada de generar la tabulacion de los valores de 'x' en el intervalo.
	param ecuacion: ecuacion de la funcion con la cual se calcularan los resultados de la tabulacion.
	param tabulacion_x: list, lista que contiene todos los valores de 'x' dentro del intervalo.
	return list, lista que contiene los resultados de la tabulacion.
	'''
	tabulacion_fx = []
	x = sp.Symbol('x')
	for i in tabulacion_x:
		valor_fx = N(ecuacion.subs(x, i))
		tabulacion_fx.append(valor_fx)
	return tabulacion_fx

# Inicio del programa.
print("Bienvenido a Simpson. Este programa calcula una solucion aproximada de una integral utilizando el metodo de Regla de Simpson de 1/3.")

# Se obtiene la ecuacion que sera utilizada. Se verifica que no este mal escrita.
try:
	ecuacion = input("\nEscribe la ecuacion de la funcion: ")
	ecuacion = sympify(ecuacion, evaluate = False)

# Si la ecuacion esta mal escrita, indica el error y termina el programa. Si esta bien, continua con el programa.
except AttributeError:
	print("\nError: la ecuacion no esta bien escrita. Intentalo de nuevo.")
else:

	# Se obtiene la longitud del intervalo.
	inicio_intervalo = float(input("\nEscribe el inicio del intervalo: "))
	final_intervalo = float(input("Escribe el final del intervalo: "))
	intervalo = final_intervalo - inicio_intervalo

	# Si no existe un intervalo, indica el error y termina el programa. De otro modo, continua con el programa.
	if intervalo == 0:
		print("\nError: no hay intervalo entre los parametros. Intentalo de nuevo.")
	else:

		# Se obtiene el numero de subintervalos y se verifica que sea par.
		flag = False
		while flag == False:
			subintervalos = int(input("\nEscribe el numero de subintervalos (debe ser un entero par mayor a 0): "))
			if ((subintervalos % 2) == 0) and (subintervalos > 0):
				flag = True

		# Se calcula el valor del incremento.
		incremento = intervalo / subintervalos

		# Se tabulan los valores de 'x' y los valores de 'fx'.
		valores_x = tabular_x(inicio_intervalo, incremento, subintervalos)
		valores_fx = tabular_fx(ecuacion, valores_x)

		# Modifica los valores de 'fx' respecto a la formula de la regla de Simpson.
		factor = 4
		for i in range(len(valores_fx)):
			if i == 0:
				continue
			if i == (len(valores_fx) - 1):
				continue
			valores_fx[i] = valores_fx[i] * factor
			if factor == 4:
				factor = 2
			else:
				factor = 4

		# Suma todos los terminos correspondientes a los valores de 'fx'.
		suma = 0
		for i in valores_fx:
			suma = suma + i

		# Termina de calcular el resultado y lo imprime.
		suma = str((incremento / 3) * (suma))
		print("\nEl resultado es: " + suma)
        
'''
DICCIONARIO DE VARIABLES:

ecuacion: sympify, funcion de la integral del problema.

factor: int, valor que representa el coeficiente de los terminos que resuelven el problema por el metodo de Simpson. El metodo indica que este factor no tiene efecto en el primer y ultimo termino, y que alterna su valor entre 4 y 2 en los terminos intermedios.

final_intervalo: float, valor que representa el final del intervalo en la integral.

flag: bool, bandera que indica si el numero de subintervalos es par o no.

i: int, contador utilizado para recorrer listas.

incremento: float, es la longitud de cada subintervalo. Se calcula dividiendo la longitud del intervalo entre el numero de subintervalos.

inicio_intervalo: float, valor que representa el inicio del intervalo en la integral.

intervalo: float, longitud entre el inicio del intervalo y el final del intervalo.

subintervalos: int, numero de subintervalos o bandas utilizadas para resolver el problema con el metodo de Simpson.

suma: float, valor que representa la solucion de la suma de terminos, y despues de multiplicarlo por un coeficiente, el resultado del metodo.

tabulacion_fx: list, lista que contiene los resultados de la tabulacion en la funcion tabular_fx( ).

tabulacion_x: list, lista que contiene todos los valores de 'x' dentro del intervalo en la funcion tabular_x( ).

valor_fx: float, variable temporal que almacena el calculo de la tabulacion para un valor de la lista tabulacion_x, en la funcion tabular_fx( ).

valor_x: float, variable temporal que almacena el valor del limite entre subintervalos en la funcion tabular_x( ).

valores_fx: list, es el conjunto de valores que representa la aplicacion de la ecuacion, sustituyendo los valores de 'x'.

valores_x: list, es el conjunto de valores que son frontera entre los subintervalos. Este conjunto representa los valores de 'x'.

x: sympify, literal 'x' dentro de la ecuacion.
'''