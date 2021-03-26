/*
Universidad Nacional Autonoma de Mexico.
Licenciatura en ciencias genomicas - Computo Cientifico 2020.
Salvador Gonzalez Juarez.

Proyecto final.
Programa 4: MinCuad.c
Calcula una aproximacion funcional a la curva que siguen ciertos puntos proporcionados por el usuario, utilizando el metodo de Minimos cuadrados.
*/

/*Importa las librerias que requiere el codigo.*/
#include <stdio.h>
#include <stdlib.h>
#include <math.h>

/*Define un tipo de dato que almacena los valores 'x' y 'y' de cada uno de los puntos.*/
typedef struct _valores {
	float x;
	float y;
	struct _valores *next;
} valores;

/*Define las funciones que utiliza el programa.*/
valores *insertar_puntos(valores *lista, valores *punto);
valores *eliminar_puntos(valores *lista);
void print_lista(valores *lista);
void ErrorMemoria(valores *lista_puntos);
void cleanup_matrix(float **matriz, int grado_polinomio);
void cleanup_vector(float *vector);

/*Comienza el programa principal definiendo las variables utilizadas.*/
int main (int argc, char *argv[]) {
	valores *lista_puntos, *punto, *p;
	int i, j, k, cantidad_puntos, grado_polinomio;
	float sumatoria, temp;
	float *vector, **matriz;

	/*Inicializa el puntero que apunta a la lista enlazada de puntos.*/
	lista_puntos = NULL;
	puts("\nBienvenido a MinCuad. Este programa encuentra una aproximacion funcional a la curva que siguen ciertos puntos proporcionados por el usuario, utilizando el metodo de Minimos cuadrados.");

	/* Obtiene el grado del polinomio modelo, y por lo tanto, el numero de ecuaciones que seran generadas.*/
	do{
		puts("\nCual es el grado del polinomio modelo? ");
		scanf("%d", & grado_polinomio);
		fflush(stdin);
	} while(grado_polinomio < 1);

	/*Obtiene el numero de puntos.*/
	do{
		puts("Cuantos puntos se usaran para construir el modelo? ");
		scanf("%d", & cantidad_puntos);
		fflush(stdin);
	} while(cantidad_puntos < 1);

	/*Asigna un espacio de memoria para almacenar los valores de un punto.
	Si no hay espacio disponible, termina de forma adecuada el programa.*/
 	for(i = 0; i < cantidad_puntos; i++) {
		if(!(punto = (valores*)malloc(sizeof(valores)))) {
			free(punto);
			punto = NULL;
			ErrorMemoria(lista_puntos);
		};

		/*Obtiene el valor en 'x' del punto.*/
		printf("\nIngresa el valor en X del punto %d: ", i + 1);
		scanf("%f", & (punto -> x));
		fflush(stdin);

		/*Obtiene el valor en 'y' del punto.*/
		printf("Ingresa el valor en Y del punto %d: ", i + 1);
		scanf("%f", & (punto -> y));
		fflush(stdin);

		/*Inserta el punto generado en la lista enlazada de puntos.*/
		punto->next = NULL;
		lista_puntos = insertar_puntos(lista_puntos, punto);
	};

	/*Imprime la lista de puntos con sus valores.*/
	puts("\nA continuacion, se muestra la lista de puntos:");
	print_lista(lista_puntos);

	/*Asigna un espacio de memoria de dos dimensiones para almacenar el valor de las sumatorias de 'x' del sistema de ecuaciones.
	Si no hay espacio disponible, termina de forma adecuada el programa.*/
	if(!(matriz = (float**)malloc((grado_polinomio + 1)*sizeof(float*)))) {
		cleanup_matrix(matriz, grado_polinomio);
		ErrorMemoria(lista_puntos);
	};
	for (i = 0; i <= grado_polinomio; i++) {
		if(!(*(matriz + i) = (float *)malloc((grado_polinomio + 1)*sizeof(float)))) {
			cleanup_matrix(matriz, grado_polinomio);
			ErrorMemoria(lista_puntos);
		};
	};

	/*Obtiene el valor de las sumatorias de 'x' en el sistema de ecuaciones y los acomoda en la matriz conforme indica el metodo de Minimos cuadrados.*/
	for (i = 0; i <= grado_polinomio; i++) {
		for (j = 0; j <= grado_polinomio; j++) {
			sumatoria = 0;
			for (p = lista_puntos; p; p = p->next) {
				sumatoria += pow((p -> x), (i + j));
			};
			*(*(matriz + i) + j) = sumatoria;
		}; 
	};

	/*Asigna un espacio de memoria para almacenar el valor de las soluciones de cada ecuacion.
	Si no hay espacio disponible, termina de forma adecuada el programa.*/
	if(!(vector = (float *)malloc((grado_polinomio + 1)*sizeof(float)))) {
		cleanup_vector(vector);
		cleanup_matrix(matriz, grado_polinomio);
		ErrorMemoria(lista_puntos);
	};

	/*Obtiene el valor de la solucion de cada ecuacion y los inserta en el vector de soluciones.*/
	for (i = 0; i <= grado_polinomio; i++) {
		sumatoria = 0;
		for (p = lista_puntos; p; p = p->next) {
			sumatoria += pow((p -> x), i) * (p -> y);
		};
		*(vector + i) = sumatoria; 
	};

	/*Se realiza el algoritmo de la eliminacion de Gauss-Jordan, utilizando la matriz y el vector previemente generados.
	Divide cada una de las filas entre el valor ubicado en la diagonal de la respectiva fila.*/
	for (i = 0; i <= grado_polinomio; i++) {
		temp = matriz[i][i];
		for (j = 0; j <= grado_polinomio; j++) {
			matriz[i][j] = matriz[i][j] / temp;
		};
		vector[i] = vector[i] / temp;

		/*Calcula el valor del coeficiente para realizar la resta entre filas.*/
		for (j = i + 1; j <= grado_polinomio; j++) {
			temp = matriz [j][i];

			/*Resta el valor multiplicado por el coeficiente al valor ubicado en la misma columna, pero en filas inferiores.*/
			/*El resultado sera una matriz triangonal superior con valores de '1' en la diagonal.*/
			for (k = 0; k <= grado_polinomio; k++) {
				matriz[j][k] = matriz[j][k] - (temp * matriz[i][k]);
			};
			vector[j] = vector[j] - (temp * vector[i]);
		};
	};

	/*Se calcula de nuevo un coeficiente para realizar la resta entre filas.*/
	for (i = grado_polinomio; i > 0; i--) {
		for (j = i - 1; j >= 0; j--) {
			temp = matriz [j][i];

			/*Resta el valor multiplicado por el coeficiente al valor ubicado en la misma columna, pero en filas superiores.*/
			/*El resultado sera una matriz diagonal, especificamente la matriz identidad.*/
			for (k = 0; k <= grado_polinomio; k++) {
				matriz[j][k] = matriz[j][k] - (temp * matriz[i][k]);
			};
			vector[j] = vector[j] - (temp * vector[i]);
		};
	};

	/*Imprime los valores de los coeficientes del polinomio modelo.*/
	puts("\nEl modelo es construido por los siguientes coeficientes:");
	for (i = 0; i <= grado_polinomio; i++) {
		printf("\nEl coeficiente de x**%d es: %f", i, vector[i]);
	};

	/*Termina el programa liberando todos los espacios de memoria aparados.*/
	cleanup_vector(vector);
	cleanup_matrix(matriz, grado_polinomio);
	lista_puntos = eliminar_puntos(lista_puntos);
	print_lista(lista_puntos);
	return 0;
};

valores *insertar_puntos(valores *lista, valores *punto) {
	/*Esta funcion inserta la esctrucutra que representa un punto, a la lista enlazada que contendra todos los puntos.
	param *lista: valores, es la lista enlazada que contendra los puntos y sus respectivos valores dentro de cada estructura.
	param *punto: valores, es una estructura que contiene los valores de un solo punto.*/
	valores *p;

	/*Si la lista esta vacia, agrega el punto como primer elemento de la lista.*/
	if(!lista){
		punto->next = NULL;
		lista = punto;
		return(lista);
	};

	/*Acomoda los puntos en orden creciente con respecto al valor de 'x'.*/
	if(punto->x < lista->x){
		punto->next = lista;
		lista = punto;
		return(lista);
	};
	for(p = lista; p->next; p = p->next) {
		if(punto->x < p->next->x)
			break;
	};
	punto->next = p->next;
	p->next = punto;
	return(lista);
};

valores *eliminar_puntos(valores *lista) {
	/*Esta funcion elimina las estrucutras enlazadas de la lista, liberando el espacio que ocupan.
	param *lista: valores, es la lista enlazada que contiene los puntos y sus respectivos valores dentro de cada estructura.*/
	valores *p;
	do {
		if(!lista)
			return(NULL);
		p = lista;
		lista = lista->next;
		free(p);
		p = NULL;
	} while(lista);
	return(lista);
};

void print_lista(valores *lista) {
	/*Esta funcion imprime los valores de cada uno de los puntos que estan dentro de la lista enlazada.
	param *lista: valores, es la lista enlazada que contiene los puntos y sus respectivos valores dentro de cada estructura.*/
	int i;
	valores *p;
	if(!lista)
		puts("\n\nLa lista esta vacia!");
	else {
		i = 1;
		for(p = lista; p; p = p->next) {
			printf("\nPunto %d\n", i++);
			printf("  Valor en X: %f\n", p->x);
			printf("  Valor en Y: %f\n", p->y);
		};
	};
};

void ErrorMemoria(valores *lista_puntos) {
	/*Esta funcion indica que hubo un error al reservar la memoria requerida. Libera el espacio apartado por los elementos de la lista enlazada y termina el programa.
	param *lista_puntos: valores, es la lista enlazada que contiene los puntos y sus respectivos valores dentro de cada estructura.*/
	puts("\nError: memoria insuficiente.");
	lista_puntos = eliminar_puntos(lista_puntos);
	exit(1);
};

void cleanup_matrix(float **matriz, int grado_polinomio) {
	/*Esta funcion libera el espacio apartado por los elementos que componen la matriz del sistema de ecuaciones.
	param **matriz: float, es el arreglo de dos dimensiones que contiene los valores conocidos del sistema de ecuaciones.
	param grado_polinomio: int, es el valor que indica la dimension de la matriz.*/
	int i;
	if (matriz){
		for (i = 0; i <= grado_polinomio; i++) {
			if (*(matriz + i)){
				free(*(matriz + i));
				*(matriz + i) = NULL;
			};
		};
	free(matriz);
	matriz = NULL;
	};
};

void cleanup_vector(float *vector) {
	/*Esta funcion libera el espacio apartado por el vector que contiene las soluciones al sistema de ecuaciones.
	param *vector: float, es el arreglo de una dimension que contiene las soluciones del sistema de ecuaciones.
	param grado_polinomio: int, es el valor que indica la dimension del vector.*/
	free(vector);
	vector = NULL;
};

/*
DICCIONARIO DE VARIABLES:

cantidad_puntos: int, representa el numero de puntos de los cuales queremos obtener una aproximacion funcional, y es utilizada para crear la lista enlazada que contiene la informacion de esos puntos.

grado_polinomio: int, representa el grado del polinomio modelo, y es utilizado para obtener la matriz del sistema de ecuaciones, y poder recorrer dicha matriz.

i: int, contador utilizado para recorrer listas.

j: int, contador utilizado para recorrer listas.

k: int, contador utilizado para recorrer listas.

lista_puntos: valores *, puntero que apunta a la lista enlazada que almacena la informacion de los puntos proporcionada por el usuario.

matriz: float **, puntero que apunta a un vector de dos dimensiones el cual almacena el valor de las sumatorias de 'x' del sistema de ecuaciones, y es fundamental para la resolucion del sistema por eliminacion de Gauss-Jordan.

punto: valores *, puntero que apunta a una sola esructura que almacena la informacion de un solo punto. Posteriormente esta estructura es enlazada con la lista de puntos.

p: valores *, puntero temporal que ayuda a manipular la lista enlazada sin perder el puntero a la lista de puntos o a alguna de las estructuras que lo componen.

sumatoria: float, variable temporal que almacena las sumatorias que indica el metodo de Minimos cuadrados, para luego almacenarlos en la matriz del sistema de ecuaciones como coeficientes, o en el vector de soluciones, como la solucion de cada ecuacion.

temp: float, variable temporal utilizada para almacenar el coeficiente por el cual se debe multiplicar o dividir cada uno de los valores es una fila para realizar el algoritmo de la eliminacion de Gauss-Jordan

vector: float *, puntero que apunta a un vector de una dimension el cual almacena el valor de las sumatorias que representan las soluciones de cada ecuacion. Una vez resuelta la eliminacion de Gauss-Jordan, este vector contendra los coeficientes que son la respuesta para construir el polinomio modelo.
*/