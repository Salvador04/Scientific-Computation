'''
Universidad Nacional Autonoma de Mexico.
Licenciatura en ciencias genomicas - Computo Cientifico 2020.
Salvador Gonzalez Juarez.

Proyecto final.
Programa 6: GaussSei.py
Resuelve un sistema de ecuaciones utilizando el metodo de Gauss-Seidel.
'''

def convergencia(soluciones_temp, soluciones, indice, cantidad_ecu, decimales):
	'''
	Funcion encargada de comprobar la convergencia simutaneamente para todas las incognitas del sistema de ecuaciones. La convergencia global se calcula de forma recursiva.
	param soluciones_temp: list, vector que contiene los valores obtenidos de cada incognita en la ultima iteracion.
	param soluciones: list, vector que contiene los valores obtenidos de cada incognita en la iteracion anterior a la ultima.
	param indice: int, valor que indica cual es la incognita que se esta evaluando, y representa un indice dentro de los vectores de solucion.
	param cantidad_ecu: int, valor que indica cuantas incognitas hay en el sistema de ecuaciones.
	param decimales: int, valor que se utiliza para calcular el criterio de convergencia.
	return flag, variable booleana que indica si hubo convergencia en todas las incognitas o no.
	'''
	# Se calcula si la incognita actual cumple con la convergencia.
	flag = (abs((soluciones_temp[indice] - soluciones[indice])) / soluciones_temp[indice]) < (1 * 10 ** (0 - decimales))

	# Si la incognita actual es la ultima en el sistema de ecuaciones, solo retorna el resultado booleano.
	if indice == (cantidad_ecu - 1):
		return flag

	# Si hay mas incognitas en el sistema de ecuaciones, calcula su convergencia y decide si ambas convergen o no.
	else:
		flag_temp = convergencia(soluciones_temp, soluciones, indice + 1, cantidad_ecu, decimales)
		flag = flag_temp and flag
		return flag

def revisar_matriz(matriz):
	'''
	Funcion encargada de revisar si la matriz del sistema de ecuaciones es diagonalmente dominante.
	param matriz: list, es el arreglo de dos dimensiones que contiene los valores ceficientes del sistema de ecuaciones.
	return bool, indica si la matriz del sistema de ecuaciones es dominante.
	'''
	flag = True
	for i in range(len(matriz)):
		for j in range(len(matriz)):
			if i != j:
				if abs(matriz[i][i]) < abs(matriz[i][j]):
					flag = False
	return flag

# Inicio del programa.
print("Bienvenido a GaussSei. Este programa resuelve un sistema de ecuaciones utilizando el metodo de Gauss-Seidel.")

# Se obtiene un numero correcto de ecuaciones.
cantidad_ecu = 0
while cantidad_ecu < 1:
	cantidad_ecu = int(input("\nEscribe el numero de ecuaciones (debe ser igual al numero de incognitas): "))
	if cantidad_ecu < 1:
		print("El valor debe ser mayor a 0. Intentalo de nuevo.")

# Inicializa dos vectores vacios. El primero contendra la matriz de coeficientes del sistema de ecuaciones, mientra que el segundo contendra las igualdades de cada ecuacion.
matriz = []
vector = []

# Se obtiene toda la informacion del sistema de ecuaciones y la almacena de forma correcta en ambos vectores.
for i in range(cantidad_ecu):
	print("\nEn la ecuacion " + str(i + 1) + ": ")
	fila = []
	for j in range(cantidad_ecu):
		fila.append(float(input("\tEscribe el coeficiente de la incognita " + str(j + 1) + ": ")))
	matriz.append(fila)
	vector.append(float(input("\tEscribe la igualdad de la ecuacion: ")))

# Se revisa si la matriz del sistema de ecuaciones es diagonalmente dominante.
try:
	if revisar_matriz(matriz) == False:

		# Si la matriz no es diagonalmente independiente, se intercambian las filas para intentar obtener una matriz diagonalmente dominante.
		for i in range(len(matriz)):
			for j in range(i, len(matriz)):

				# El intercambio se hace buscando el valor mas alto para cada variable en cada fila de la matriz
				if abs(matriz[i][i]) < abs(matriz[j][i]):
					fila = matriz[i][:]
					matriz[i] = matriz[j][:]
					matriz[j] = fila[:]

					# Ademas de hacer el intercambio de filas en la matriz, se intercambian los valores en el vector de soluciones.
					temp = vector[i]
					vector[i] = vector[j]
					vector[j] = temp

		# Si despues del arreglo de la matriz, esta continua siendo no diagonalmente dominante, entonces termina el programa.
		# El motivo es debido a que en esta instancia no se puede asegurar la convergencia del sistema.
		if revisar_matriz(matriz) == False:
			raise ValueError
except ValueError:
	print("\nError: El sistema no es diagonalmente dominante. El programa ha terminado porque no se puede asegurar convergencia del metodo en esta instancia.")

# Si la matriz del sistema de ecuaciones es diagonalmente dominante, continua con el programa.
else:

	# Se obtiene el numero de decimales deseado.
	decimales = int(input("\nEscribe el numero de aproximacion de decimales: "))

	# Inicializa dos vectores con la solucion trivial '0' para cada incognita en el sistema de ecuaciones.
	soluciones = []
	for i in range(cantidad_ecu):
		soluciones.append(0)
	soluciones_temp = []
	for i in range(cantidad_ecu):
		soluciones_temp.append(0)

	# Inicializa las variables para controlar las iteraciones del programa.
	iteraciones = 0
	convergio = False

	# Itera el siguiente codigo hasta que los valores de cada incognita convergan en la precision deseada.
	while convergio == False:

		# Se elige una incognita con la cual trabajar, y se inicializa la suma del despeje.
		for i in range(cantidad_ecu):
			suma = 0

			# El siguiente codigo realiza el despeje de la incognita actual.
			for j in range(cantidad_ecu):
				if (i != j):

					# Calcula la suma dependiendo del signo del coeficiente de la incognita actual.
					if matriz[i][i] < 0:
						suma = suma + (matriz[i][j] * soluciones_temp[j])

					else:
						suma = suma + (-1 * (matriz[i][j]) * soluciones_temp[j])

			# Termina de calcular el despeje, y toma en cuenta los signos del coeficiente de la incognita actual.
			if matriz[i][i] < 0:
				suma = (suma + (-1 * vector[i])) / (-1 * matriz[i][i])
			else:
				suma = (suma + vector[i]) / (matriz[i][i])

			# Asigna el resultado del despeje al espacio correspondiente de la incognita actual en el vector de soluciones temporal.
			soluciones_temp[i] = suma

		# Calcula el error relativo entre el valor de las incognitas en la iteracion actual y la iteracion anteriror.
		# Si es menor al criterio de paro, termina las iteraciones.
		iteraciones = iteraciones + 1
		indice = 0
		if convergencia(soluciones_temp, soluciones, indice, cantidad_ecu, decimales) == True:
			convergio = True
				
		# En caso de que no haya convergencia, asigna los valores del vector de soluciones temporal al vector de soluciones de la iteracion.
		else:
			soluciones = soluciones_temp[:]

	# Transforma el valor de cada incognita a una cadena solo con los decimales deseados e imprime los resultados.
	for i in soluciones_temp:
		incognita_lista = [digito for digito in str(i)]
		incognita_cadena = ''
		for digito in incognita_lista[:incognita_lista.index('.') + 1 + decimales]:
			incognita_cadena = incognita_cadena + str(digito)
		print("\nEl resultado para la incognita " + str(soluciones_temp.index(i) + 1) + " es:", incognita_cadena)
	print("\nLas iteraciones realizadas fueron:", (iteraciones))

'''
DICCIONARIO DE VARIABLES:

cantidad_ecu: int, variable que representa el numero de ecuaciones que posee el sistemas, asi como el numero de varibles y con ambos se puede inferir la dimension de la matriz del sistema de ecuaciones.

convergio: bool, bandera que indica si el metodo convergio entre la iteracion anterior y la iteracion actual.

decimales: int, valor que representa el numero de decimales de exactitud de los resultados.

digito: str, variable temporal que almacena el caracter de cada digito del resultado, para convertir el numero en una lista que contiene como elementos dichos digitos.

fila: list, vector temporal que es utilizado para la creacion de sublistas, que son posterioremente aniadidos a listas para crear la matriz del sistema de ecuaciones. Ademas, es utiliazado para manipular la matriz sin perder informacion.

flag: bool, bandera que indica si se cumplio con la convergencia en la funcion convergencia( ), y que indica si la matriz es diagonalmente dominante en la funcion revisar_matriz( ). 

i: int, contador utilizado para recorrer listas.

incognita_cadena: str, variable que almacena los caracteres de los digitos solo de la parte que se va a imprimir del resultado. Se inicializa para el resultado correspondiente a cada una de las incognitas.

incognita_lista: list, lista cuyos elementos representan todos los digitos del resultado. Se inicializa para el resultado correspondiente a cada una de las incognitas.

indice: int, contador que indica cual es la incognita que se esta evaluando, en la funcion recursiva convencia( ). Es utilizada como indice para poder recorrer el vector de soluciones.

iteraciones: int, contador que representa el numero de iteracion actual.

j: int, contador utilizado para recorrer listas.

matriz: list, vector de dos dimensiones que contiene los coeficientes de cada ecuacion del sistema ordenados en sus filas.

soluciones: list, lista que almacena los valores aproximados de cada una de las variables, de la iteracion anterior.

soluciones_temp: list, lista que almacena los valores mas aproximados a cada una de las variables, en la iteracion actual.

suma: float, variable temporal que almacena el despeje para calcular el valor aproximado de una variable, como indica el metodo de Gauss-Seidel.

temp: float, variable temporal que es utilizada para manipular el vector de igualdades sin perder informacion.

vector: list, vector de una dimension que almacena las igualdades de cada una de las ecuaciones que compone el sistema.
'''