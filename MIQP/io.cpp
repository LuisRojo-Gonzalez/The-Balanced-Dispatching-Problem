#include "header.h"
#include <stdio.h>
#include <stdlib.h>

namespace CentroOriente{

void read_sercivio(char* fichero){
	FILE* f;
	int id,a,v,k,alfa,beta,l,c;
	float b;
	//memory allocation
	servicios.id = new int[MAX_SERVICIOS];
	servicios.a = new int[MAX_SERVICIOS];
	servicios.b = new int[MAX_SERVICIOS];
	servicios.c = new int[MAX_SERVICIOS];
	servicios.v = new int[MAX_SERVICIOS];
	servicios.l = new int[MAX_SERVICIOS];
	servicios.k = new int[MAX_SERVICIOS];
	servicios.alfa = new int[MAX_SERVICIOS];
	servicios.beta = new int[MAX_SERVICIOS];

	//printf("SERVICIOS\n");
	servicios.id[0]=0;
	f=fopen(fichero,"rt");
	while(!feof(f))
	{
		servicios.id[0]++;
		fscanf(f,"%d %d %f %d %d %d %d %d %d\n",&id,&a,&b,&v,&k,&alfa,&beta,&l,&c);
		servicios.id[servicios.id[0]]=id;
		servicios.a[servicios.id[0]]=a;
		servicios.b[servicios.id[0]]=(int)b;
		servicios.v[servicios.id[0]]=v;
		servicios.k[servicios.id[0]]=k;
		servicios.alfa[servicios.id[0]]=alfa;
		servicios.beta[servicios.id[0]]=beta;
		servicios.l[servicios.id[0]]=l;
		servicios.c[servicios.id[0]]=c;
		//printf("%6d %6d %6d %6d %6d %6d %6d %6d %6d\n",servicios.id[servicios.id[0]],servicios.a[servicios.id[0]],servicios.b[servicios.id[0]],servicios.v[servicios.id[0]],servicios.k[servicios.id[0]],servicios.alfa[servicios.id[0]],servicios.beta[servicios.id[0]],servicios.l[servicios.id[0]],servicios.c[servicios.id[0]]);
	}
	//printf("\nServicios Totales = %d\n",servicios.id[0]);
	fclose(f);
}

void read_disponibilidades(char* fichero){
	FILE* f;
	int id,m,d,e,l,k;
	//memory allocation
	disponibilidad.id = new int[MAX_DISPONIBILIDAD];
	disponibilidad.m = new int[MAX_DISPONIBILIDAD];
	disponibilidad.d = new int[MAX_DISPONIBILIDAD];
	disponibilidad.e = new int[MAX_DISPONIBILIDAD];
	disponibilidad.l = new int[MAX_DISPONIBILIDAD];
	disponibilidad.k = new int[MAX_DISPONIBILIDAD];

	//printf("DISPONIBILIDADES\n");
	//read data
	disponibilidad.id[0]=0;
	f=fopen(fichero,"rt");
	while(!feof(f))
	{
		disponibilidad.id[0]++;
		fscanf(f,"%d %d %d %d %d %d\n",&id,&m,&d,&e,&l,&k);
		disponibilidad.id[disponibilidad.id[0]]=id;
		disponibilidad.m[disponibilidad.id[0]]=m; 
		disponibilidad.d[disponibilidad.id[0]]=d; 
		disponibilidad.e[disponibilidad.id[0]]=e; 
		disponibilidad.l[disponibilidad.id[0]]=l;
		disponibilidad.k[disponibilidad.id[0]]=k;
		//printf("%6d %6d %6d %6d %6d %6d\n",disponibilidad.id[disponibilidad.id[0]],disponibilidad.m[disponibilidad.id[0]],disponibilidad.d[disponibilidad.id[0]],disponibilidad.e[disponibilidad.id[0]],disponibilidad.l[disponibilidad.id[0]],disponibilidad.k[disponibilidad.id[0]]);
	}
	//printf("\nDisponibilidades Totales = %d\n",disponibilidad.id[0]);
	fclose(f);
}

void read_vehiculos(char* fichero){
	FILE* f;
	int id, tipo;
	//memory allocation
	vehiculos = new int*[MAX_VEHICULOS];
	for(int i=0;i<MAX_VEHICULOS;i++) vehiculos[i] = new int[2];
	//printf("VEHICULOS\n");
	//read data
	vehiculos[0][0] = 0;
	f=fopen(fichero,"rt");
	while(!feof(f))
	{
		vehiculos[0][0]++;
		//printf("%d ",vehiculos[0][0]);
		fscanf(f,"%d %d\n",&id,&tipo);
		vehiculos[vehiculos[0][0]][0]=id;
		vehiculos[vehiculos[0][0]][1]=tipo;
		//printf("%6d %6d\n",vehiculos[vehiculos[0][0]][0],vehiculos[vehiculos[0][0]][1]);
	}
	//printf("\nVehiculos Totales = %d\n",vehiculos[0][0]);
	fclose(f);
}

void read_bases(char* fichero){
	FILE* f;
	int id;
	//memory allocation
	bases = new int[MAX_BASES];

	//read data
	bases[0] = 0;
	f=fopen(fichero,"rt");
	while(!feof(f))
	{
		fscanf(f,"%d\n",&id);
		bases[++bases[0]]=id;
		//printf("%6d\n",id);
	}
	//printf("\nBases Totales = %d\n",bases[0]);
	fclose(f);
}

void read_tipos(char* fichero){
	FILE* f;
	int id;
	//memory allocation
	tipos = new int[MAX_TIPOS];

	//read data
	tipos[0] = 0;
	f=fopen(fichero,"rt");
	while(!feof(f))
	{
		fscanf(f,"%d\n",&id);
		tipos[++tipos[0]]=id;
		//printf("%6d\n",id);
	}
	//printf("\nTipos Totales = %d\n",tipos[0]);
	fclose(f);
}

void read_anterior(char* fichero){
	FILE* f;
	int id;
	float aux1;
	int aux2,aux3;
	//memory allocation
	E_antes = new int*[MAX_VEHICULOS];
	B_antes = new double*[MAX_VEHICULOS];
	for(int i=0;i<MAX_VEHICULOS;i++)
	{
		E_antes[i]= new int[2];
		B_antes[i]= new double[2];
	}
	//read data
	aux3=0;
	f=fopen(fichero,"rt");
	while(!feof(f))
	{
		fscanf(f,"%d %f %d\n",&id,&aux1,&aux2);
		aux3++;
		B_antes[aux3][0]=(double)id;
		E_antes[aux3][0]=id;
		B_antes[aux3][1]=(double)aux1;
		E_antes[aux3][1]=aux2;
		//printf("%6d %f %d\n",(int)B_antes[aux3][0],B_antes[aux3][1],E_antes[aux3][1]);
	}
	fclose(f);

}

};