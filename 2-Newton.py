'''
Universidad Nacional Autonoma de Mexico.
Licenciatura en ciencias genomicas - Computo Cientifico 2020.
Salvador Gonzalez Juarez.

Proyecto final.
Programa 2: Newton.py
Calcula la raiz de una ecuacion, utilizando el metodo de Newton-Raphson.
'''

# Importa las librerias que ayudan a realizar el algebra y calculo del programa.
import sympy as sp
from sympy import sympify, Derivative, simplify, N

def encontrar_x0 (ecuacion, inicio_intervalo, final_intervalo, incremento):
  '''
  Funcion encargada de buscar un valor inicial de x dado el cambio de signo en una tabulacion de cierto intervalo.
  param ecuacion: ecuacion de la funcion con la cual se calcularan los resultados de la tabulacion.
  param inicio_intervalo: float, valor que representa el inico del intervalo al cual se le realizara la tabulacion.
  param final_intervalo: float, valor que representa el final del intervalo al cual se le realizara la tabulacion.
  param incremento: float, valor que representa el incremento entre cada valor de 'x'.
  return float, valor inicial de 'x'.
  '''
  # Se generan los valores de 'x' en el intervalo, tomando como referencia el valor del incremento.
  try:
    tabulacion_x = []
    subintervalos = (final_intervalo - inicio_intervalo) / incremento
    temp = inicio_intervalo
    for i in range(0, int(subintervalos + 1)):
      tabulacion_x.append(temp)
      temp = temp + incremento

    # Tabula los valores de 'x' para encontrar los valores de 'fx' y los resultados son guardados en una lista.
    tabulacion_fx = []
    x = sp.Symbol('x')
    for i in tabulacion_x:
      temp = N(ecuacion.subs(x, i))
      tabulacion_fx.append(temp)

    # Busca un cambio de signo entre cada dos valores continuos.
    for i in range(len(tabulacion_fx)):
      if (tabulacion_fx[i]) * (tabulacion_fx[i + 1]) < 0:
        resultado = float(tabulacion_x[i] + tabulacion_x[i + 1]) / 2
        break

  # Si no es encontrado un cambio de signo, se indica en el valor retornable.
  except IndexError:
    resultado = None

  # Regresa el valor inicial obtenido.
  finally:
    return resultado

# Inicio del programa.
print("Bienvenido a Newton. Este programa calcula la raiz de una ecuacion, utilizando el metodo de Newton-Raphson.")

# Se obtiene la ecuacion que sera utilizada. Se verifica que no este mal escrita.
try:
  ecuacion = input("\nEscribe la ecuacion de la funcion: ")
  ecuacion = sympify(ecuacion, evaluate = False)

# Si la ecuacion esta mal escrita, indica el error y termina el programa. Si esta bien, continua con el programa.
except AttributeError:
  print("\nError: la ecuacion no esta bien escrita. Intentalo de nuevo.")
else:

  # Se obtienen los parametros numericos del programa.
  inicio_intervalo = float(input("\nEscribe el inicio del intervalo: "))
  final_intervalo = float(input("Escribe el final del intervalo: "))
  decimales = int(input("\nEscribe el numero de aproximacion de decimales: "))
  incremento = float(input("Escribe el valor del incremento de 'x' para realizar la tabulacion de 'f(x)': "))

  # Busca un valor inicial para aplicar el metodo.
  x0 = encontrar_x0(ecuacion, inicio_intervalo, final_intervalo, incremento)

  # Realiza el siguiente codigo si se encuentra el valor inicial 'x0'. Imprime el valor de 'x0' utilizado.
  if(x0):
    print("\nEl valor de x0 utilizado es:", str(x0))

    # Calcula la derivada de la ecuacion.
    x = sp.Symbol('x')
    derivada = Derivative(ecuacion, x).doit()
    simplify(derivada)

    # Inicializa las variables para controlar las iteraciones del programa.
    convergio = False
    iteraciones = 0

    # Itera el siguiente codigo hasta que los valores de 'x0' y 'x1' convergan en la precision deseada.
    while convergio == False:

      # Calcula el valor de 'x1' usando como valor aproximado a 'x0'.
      x1 = x0 - (N(ecuacion.subs(x, x0)) / N(derivada.subs(x, x0)))
      iteraciones = iteraciones + 1

      # Calcula el error relativo entre 'x0' y 'x1'. Si es menor al criterio de paro, termina las iteraciones.
      if abs((x1 - x0) / x1) < (1 * 10 ** (0 - decimales)):
        convergio = True

      # En caso de que no haya convergencia, asigna el valor de 'x0' a 'x1' e itera de nuevo.
      else:
        x0 = x1

    # Transforma el valor de 'x1' a una cadena solo con los decimales deseados.
    x1_lista = [digito for digito in str(x1)]
    x1_cadena = ''
    for i in x1_lista[:x1_lista.index('.') + 1 + decimales]:
      x1_cadena = x1_cadena + str(i)

    # Imprime los resultados.
    print("\nEl resultado es:", x1_cadena)
    print("\nLas iteraciones realizadas fueron:", (iteraciones))

  # Si no se encontro un valor para 'x0', termina el programa.
  else:
    print("\nNo hubo cambio de signo en el intervalo")

'''
DICCIONARIO DE VARIABLES:

convergio: bool, bandera que indica si el metodo convergio entre la iteracion anterior y la iteracion actual.

decimales: int, valor que representa el numero de decimales de exactitud del resultado.

derivada: sympify, derivada de la ecuacion del problema, utlizada para aproximarse a la raiz como indica el metodo de Newton-Raphson.

digito: str, variable temporal que almacena el caracter de cada digito del resultado, para convertir el numero en una lista que contiene como elementos dichos digitos.

ecuacion: sympify, ecuacion igualada a cero del problema.

final_intervalo: float, valor que representa el final del intervalo en la tabulacion deseada.

i: int, contador utilizado para recorrer listas.

incremento: float, valor del incremento entre las 'x' de la tabulacion. Su valor depende totalmente de la profundidad que el usario desea para la busqueda del cambio de signo.

inicio_intervalo: float, valor que representa el inicio del intervalo en la tabulacion deseada.

iteraciones: int, contador que representa el numero de iteracion actual.

resultado: float, variable que representa el valor intermedio entre una pareja de valores de 'x' que generaron un cambio de signo en la tabulacion. Es el valor retornable de la funcion encontrar_x0( ). Su valor es utilizado como el valor de x0.

subintervalos: float, almacena el numero de subintervalos, calculado como la diferencia entre el final del intervalo y el inicio del intervalo, dividido entre el valor del incremento. Es utilizada en la funcion encontrar_x0( ).

tabulacion_fx: list, lista que contiene los resultados de la tabulacion en la funcion encontrar_x0( ).

tabulacion_x: list, lista que contiene todos los valores de 'x' dentro del intervalo en la funcion encontrar_x0( ).

temp: float, variable temporal utilizada para llenar las listas tabulacion_x y tabulacion_fx dentro de la funcion encontrar_x0( ).

x: sympify, literal 'x' dentro de la ecuacion.

x0: float, variable que representa el valor inicial de 'x' para comenzar a buscar la raiz de la ecuacion, y posteriormente es usada para almacenar el valor de la aproximacion anterior durante las iteraciones. 

x1: float, variable que representa el valor de la aproximacion mas reciente.

x1_cadena: str, variable que almacena los caracteres de los digitos solo de la parte que se va a imprimir del resultado. 

x1_lista: list, lista cuyos elementos representan todos los digitos del resultado. 
'''