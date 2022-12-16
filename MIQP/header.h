
namespace CentroOriente{

#define MAX_SERVICIOS 10000
#define MAX_DISPONIBILIDAD 2000
#define MAX_VEHICULOS 100
#define MAX_BASES 16
#define MAX_TIPOS 16
#define N_GRANDE 100000
#define yes 1
#define no 0
//#define IloArray<IloNumVarArray>IloNumVarArray2;

typedef struct{
	int* id;
	int* a;//tiempo inicio servicio
	int* b;//tiempo traslado
	int* c;//tiempo a la base
	int* v;//valor estimado
	int* l;//base mas cercana
	int* k;//tipo de servicio
	int* alfa;//tolerancia atraso
	int* beta;//tolerancia adelanto
}servicios_t;

typedef struct{
	int* id;//llave*
	int* m;//vehiculo
	int* d;//tiempo de inicio
	int* e;//duracion
	int* l;//base donde inicia
	int* k;//tipo
}disponibilidad_t;

extern servicios_t servicios;
extern disponibilidad_t disponibilidad;
extern int** vehiculos;
extern int* bases;
extern int* tipos;
extern double** B_antes;
extern int** E_antes;

//funciones en io
void read_sercivio(char* fichero);
void read_disponibilidades(char* fichero);
void read_vehiculos(char* fichero);
void read_bases(char* fichero);
void read_tipos(char* fichero);
void read_anterior(char* fichero);
void optimization();
};
