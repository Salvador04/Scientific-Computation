'''
Universidad Nacional Autonoma de Mexico.
Licenciatura en ciencias genomicas - Computo Cientifico 2020.
Salvador Gonzalez Juarez.

Proyecto final.
Programa 3: RegulaF.py
Calcula la raiz de una ecuacion, utilizando el metodo de Regula-falsi.
'''

# Importa las librerias que ayudan a realizar el algebra del programa.
import sympy as sp
from sympy import sympify, N

def formula(ecuacion, inicio_intervalo, final_intervalo):
  '''
  Funcion encargada de aplicar la formula general del metodo Regula-falsi, con la finalidad de hallar una aproximacion a la riaz de la ecuacion '.
  param ecuacion: ecuacion de la funcion que esta siendo empleada.
  param inicio_intervalo: float, valor que representa el inico del intervalo.
  param final_intervalo: float, valor que representa el final del intervalo.
  return float, valor inicial de 'x'.
  '''
  x = sp.Symbol('x')
  resultado = float(((inicio_intervalo * N(ecuacion.subs(x, final_intervalo))) - (final_intervalo * N(ecuacion.subs(x, inicio_intervalo)))) / (N(ecuacion.subs(x, final_intervalo)) - N(ecuacion.subs(x, inicio_intervalo))))
  return resultado

def pivote(ecuacion, k, x0):
  '''
  Funcion encargada de realizar la formula general que verifica si es necesario un cambio de pivote.
  param ecu: ecuacion de la funcion que esta siendo empleada.
  param k: float, toma el valor de 'f(x)' de algun extremo del intervalo.
  param x0: float, valor que representa la aproximacion mas reciente.
  return float, un valor cuyo signo describe la posicion del pivote respecto a la aproximacion mas reciente.
  '''
  x = sp.Symbol('x')
  flag = N(ecuacion.subs(x, k)) * N(ecuacion.subs(x, x0))
  return flag

# Inicio del programa.
print("Bienvenido a RegulaF. Este programa calcula la raiz de una ecuacion, utilizando el metodo de Regula-falsi.")

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

  # Busca un valor inicial para aplicar el metodo.
  x0 = formula(ecuacion, inicio_intervalo, final_intervalo)
  try:

    # Inicializa las variables para controlar las iteraciones del programa.
    convergio = False
    iteraciones = 0

    # Itera el siguiente codigo hasta que los valores de 'x0' y 'x1' convergan en la precision deseada.
    while convergio == False:

      # Realiza la iteracion usando como pivote el inicio del intervalo, si fuese lo mas eficiente.
      if pivote(ecuacion, inicio_intervalo, x0) < 0:
        x1 = formula(ecuacion, x0, inicio_intervalo)
        final_intervalo = x0 

      # Realiza la iteracion usando como pivote el final del intervalo, si fuese lo mas eficiente.
      elif pivote(ecuacion, final_intervalo, x0) < 0:
        x1 = formula(ecuacion, x0, final_intervalo)
        inicio_intervalo = x0

      # Si no existe un cambio de signo entre los pivotes, indica un error y termina las iteraciones.
      else:
        raise ValueError("\nNo existe cambio de signo entre los intervalos.")
        break

      # Calcula el error relativo entre 'x0' y 'x1'. Si es menor al criterio de paro, termina las iteraciones.
      iteraciones = iteraciones + 1
      if abs((x1 - x0) / x1) < (1 * 10 ** (0 - decimales)):
        convergio = True

      # En caso de que no haya convergencia, asigna el valor de 'x0' a 'x1' e itera de nuevo.
      else:
        x0 = x1

  # Si sucede un error durante las iteraciones, termina el programa.
  except ValueError as error:
    print(error)

  # Si las iteraciones concluyeron exitosamente, Transforma el valor de 'x1' a una cadena solo con los decimales deseados.
  else:
    x1_lista = [digito for digito in str(x1)]
    x1_cadena = ''    
    for i in x1_lista[:x1_lista.index('.') + 1 + decimales]:
      x1_cadena = x1_cadena + str(i)

    # Imprime los resultados.
    print("\nEl resultado es:", x1_cadena)
    print("\nLas iteraciones realizadas fueron:", (iteraciones))

'''
DICCIONARIO DE VARIABLES:

convergio: bool, bandera que indica si el metodo convergio entre la iteracion anterior y la iteracion actual.

decimales: int, valor que representa el numero de decimales de exactitud del resultado.

digito: str, variable temporal que almacena el caracter de cada digito del resultado, para convertir el numero en una lista que contiene como elementos dichos digitos.

ecuacion: sympify, ecuacion igualada a cero del problema.

final_intervalo: float, valor que representa el final del intervalo en la tabulacion deseada.

flag: float, variable que representa el resultado de la formula de evaluacion del cambio de pivote, correspondiente al metodo de Regula-falsi. Es el valor retornable de la funcion pivote( ).

i: int, contador utilizado para recorrer listas.

inicio_intervalo: float, valor que representa el inicio del intervalo en la tabulacion deseada.

iteraciones: int, contador que representa el numero de iteracion actual.

k: float, variable temporal que almacena el valor de alguno de los pivotes en la funcion pivote( ), y es utilizada para evaluar si es necesario un cambio de pivote.

resultado: float, variable que representa el valor de la aproximacion mas reciente a la raiz de la ecuacion. Su valor es calculado como indica el metodo de Regula-falsi. Es el valor retornable de la funcion formula( ).

x: sympify, literal 'x' dentro de la ecuacion.

x0: float, variable que representa el valor inicial de 'x' para comenzar a buscar la raiz de la ecuacion, y posteriormente es usada para almacenar el valor de la aproximacion anterior durante las iteraciones. 

x1: float, variable que representa el valor de la aproximacion mas reciente.

x1_cadena: str, variable que almacena los caracteres de los digitos solo de la parte que se va a imprimir del resultado. 

x1_lista: list, lista cuyos elementos representan todos los digitos del resultado. 
'''