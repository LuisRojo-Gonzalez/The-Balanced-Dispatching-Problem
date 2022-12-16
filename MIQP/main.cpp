#include <stdio.h>
#include "header.h"
#include "ilcplex/ilocplex.h"
namespace CentroOriente{

servicios_t servicios;
disponibilidad_t disponibilidad;
int** vehiculos;
int* bases;
int* tipos;
double** B_antes;
int** E_antes;

};

int main(int argc, char** argv){
	/*if(argc < 2){
		printf("NO HA ESPECIFICADO FICHEROS\n");
		return(1);
	}*/
	CentroOriente::read_sercivio(argv[1]);
	CentroOriente::read_disponibilidades(argv[2]);
	CentroOriente::read_vehiculos(argv[3]);
	CentroOriente::read_bases(argv[4]);
	CentroOriente::read_tipos(argv[5]);
	CentroOriente::read_anterior(argv[6]);
	CentroOriente::optimization();
}

namespace CentroOriente{

void optimization(){
	clock_t t_ini;
	double t;
	IloEnv env;
	IloModel model(env);
	//printf("servicios = %d\n",servicios.id[0]);
	//printf("disponibilidades = %d\n",disponibilidad.id[0]);
	IloNumVarArray B(env,vehiculos[0][0]+1,0,5000000,ILOFLOAT);//B[0] = Promedio;
	IloNumVarArray X(env,(servicios.id[0]*disponibilidad.id[0]),0,1,ILOBOOL);
	IloNumVarArray Z(env,(servicios.id[0]*servicios.id[0]),0,1,ILOBOOL);
	IloNumVarArray Y(env,servicios.id[0]+1,0,50000000,ILOFLOAT);
	int aux1;
	//add equation (1)
	IloExpr objetivo(env);
	for(int i=1;i<=vehiculos[0][0];i++)
	{
		//for(int j=1;j<=disponibilidad.id[0];j++)
		//{
		//	if(E_antes[i][1]>0||disponibilidad.m[j]==vehiculos[i][0])
		//	{
				objetivo+=(B[i]-B[0])*(B[i]-B[0]);
		//		break;
		//	}
		//}

	}
	model.add(IloMinimize(env,objetivo));
	objetivo.end();
	//add equations (2)
	for(int m=1;m<=vehiculos[0][0];m++)
	{
		//printf("\n(%d) ",vehiculos[m][0]);
		IloExpr eq2(env);
		aux1=0;
		for(int j=1;j<=disponibilidad.id[0];j++)
		{
			if(disponibilidad.m[j]==vehiculos[m][0])
			{
				aux1+=disponibilidad.e[j];
			}
			for(int i=1;i<=servicios.id[0]&&disponibilidad.m[j]==vehiculos[m][0];i++)
			{
				if(disponibilidad.d[j]>servicios.a[i]) continue; //si la disponibilidad inicia despues de la hora del servicio
				if(servicios.a[i]>disponibilidad.d[j]+disponibilidad.e[j]) continue; //si el servicio inicia tras terminar la disponibilidad
				if(disponibilidad.k[j]<servicios.k[i]) continue; //si el vehiculo de la disponibilidad es mas peque�o que el requerido por el servicio
				//printf("%d,%d ",servicios.id[i],disponibilidad.id[j]);
				eq2+=X[(i-1)*disponibilidad.id[0]+j-1]*servicios.v[i];
			}
		}
		if(aux1==0){
			model.add(B_antes[m][1]==B[m]);
			eq2.end();
		}else{
			model.add(eq2+(B_antes[m][1]*E_antes[m][1])==(aux1+E_antes[m][1])*B[m]);
			eq2.end();
		}
	}
	//add equations (3)
	IloExpr eq3(env);
	for(int m=1;m<=vehiculos[0][0];m++)
	{
		//for(int j=1;j<=disponibilidad.id[0];j++)
		//{
		//	if(E_antes[m][1]>0||disponibilidad.m[j]==vehiculos[m][0])
		//	{
				eq3+=B[m];
		//		break;
		//	}
		//}
	}
	model.add(eq3==vehiculos[0][0]*B[0]);
	eq3.end();
	//add equations (4)
	for(int i=1;i<=servicios.id[0];i++)
	{
		IloExpr eq4(env);
		for(int j=1;j<=disponibilidad.id[0];j++)
		{
			if(disponibilidad.d[j]>servicios.a[i]) continue;
			if(servicios.a[i]>disponibilidad.d[j]+disponibilidad.e[j]) continue;
			if(disponibilidad.k[j]<servicios.k[i]) continue;
			//printf("(%d %d) (%d %d) (%d %d)\n",disponibilidad.d[j],servicios.a[i]-servicios.beta[i],servicios.a[i]+servicios.b[i]+servicios.c[i],disponibilidad.d[j]+disponibilidad.e[j],disponibilidad.k[j],servicios.k[i]);
			eq4+=X[(i-1)*disponibilidad.id[0]+j-1];
		}
		model.add(eq4==1);
		eq4.end();
	}
	//add equations (5)
	for(int i=1;i<=servicios.id[0];i++){
		model.add(servicios.a[i]+servicios.b[i]+servicios.c[i]-servicios.beta[i]<=Y[i]);
		model.add(Y[i]<=servicios.a[i]+servicios.b[i]+servicios.c[i]+servicios.alfa[i]);
	}
	//add equations (6) y (7)
	//printf("disp = %d | serv =%d | x_total = %d | z_total =%d\n",disponibilidad.id[0],servicios.id[0],servicios.id[0]*disponibilidad.id[0],servicios.id[0]*servicios.id[0]);
	for(int j=1;j<=disponibilidad.id[0];j++)
	{
		for(int i=1;i<=servicios.id[0];i++)
		{
			if(disponibilidad.d[j]>servicios.a[i]) continue;
			if(servicios.a[i]>disponibilidad.d[j]+disponibilidad.e[j]) continue;
			if(disponibilidad.k[j]<servicios.k[i]) continue;				{
			for(int ii=1;ii<=servicios.id[0];ii++)
			{
				//if((i-1)*disponibilidad.id[0]+j-1>20474) printf("%d ",(i-1)*disponibilidad.id[0]+j-1);
				//if((i-1)*servicios.id[0]+ii-1>105624) printf("%d ",(i-1)*servicios.id[0]+ii-1>105624);
				if(i==ii) continue;
				if(disponibilidad.d[j]>servicios.a[ii]) continue;
				if(servicios.a[ii]>disponibilidad.d[j]+disponibilidad.e[j]) continue;
				if(disponibilidad.k[j]<servicios.k[ii]) continue;
				model.add(Y[i]-Y[ii]+servicios.b[ii]+servicios.c[ii]<=N_GRANDE*(1-Z[(i-1)*servicios.id[0]+ii-1]));
				model.add(X[(i-1)*disponibilidad.id[0]+j-1]+X[(ii-1)*disponibilidad.id[0]+j-1]<=1+Z[(i-1)*servicios.id[0]+ii-1]+Z[(ii-1)*disponibilidad.id[0]+i-1]);
				}
			}
		}
	}
	//add eq (8)
	/*for(int j=1;j<=disponibilidad.id[0];j++)
	{
		IloExpr eq8(env);
		for(int i=1;i<=servicios.id[0];i++)
		{
			if(disponibilidad.d[j]>servicios.a[i]) continue;
			if(servicios.a[i]>disponibilidad.d[j]+disponibilidad.e[j]) continue; //+servicios.b[i]+servicios.c[i]
			if(disponibilidad.k[j]<servicios.k[i]) continue;
			eq8+=X[(j-1)*servicios.id[0]+i-1];
		}
		model.add(eq8>=1);
		eq8.end();
	}*/

	//Restricciones de numero de asignaciones igual a ventanas disponibles (intento)
	//add equations (9)
	/*for(int m=1;m<=vehiculos[0][0];m++)
	{
		//printf("\n(%d) ",vehiculos[m][0]);
		IloExpr eq5(env);
		aux1=0;
		for(int j=1;j<=disponibilidad.id[0];j++)
		{
			if(disponibilidad.m[j]==vehiculos[m][0])
			{
				aux1+=1;
			}
			for(int i=1;i<=servicios.id[0]&&disponibilidad.m[j]==vehiculos[m][0];i++)
			{
				if(disponibilidad.d[j]>servicios.a[i]) continue; //si la disponibilidad inicia despues de la hora del servicio
				if(servicios.a[i]>disponibilidad.d[j]+disponibilidad.e[j]) continue; //si el servicio inicia tras terminar la disponibilidad
				if(disponibilidad.k[j]<servicios.k[i]) continue; //si el vehiculo de la disponibilidad es mas peque�o que el requerido por el servicio
				//printf("%d,%d ",servicios.id[i],disponibilidad.id[j]);
				eq5+=X[(i-1)*disponibilidad.id[0]+j-1];
			}
		}
			model.add(eq5>=aux1);
			eq5.end();
	}*/

	IloCplex solver(model);
	t_ini = clock();
	solver.setParam(IloCplex::TiLim,7200);
	solver.setParam(IloCplex::EpGap,0.01);
	solver.solve();
	printf("SOLUCION = %f\n",solver.getObjValue());
	printf("MEJOR SOLUCION = %f\n",solver.getBestObjValue());
	t= (clock() - t_ini) / (double) CLOCKS_PER_SEC;
	printf("TIME = %f\n",t);
	/*for(int i=1;i<=servicios.id[0];i++){
		printf("Y[%d]=%f\n",i,solver.getValue(Y[i]));
	}*/
	for(int i=1;i<=servicios.id[0];i++)
	{
		for(int j=1;j<=disponibilidad.id[0];j++)
		{
			if(disponibilidad.d[j]>servicios.a[i]) continue; //si la disponibilidad inicia despues de la hora del servicio
			if(servicios.a[i]>disponibilidad.d[j]+disponibilidad.e[j]) continue; //si el servicio finaliza despues del fin de la disponibilidad
			if(disponibilidad.k[j]<servicios.k[i]) continue; //si el vehiculo de la disponibilidad es mas peque�o que el requerido por el servicio
			if(solver.getValue(X[(i-1)*disponibilidad.id[0]+j-1])==1.0)	printf("Servicio %d asignado a disponibilidad %d\n",servicios.id[i],disponibilidad.id[j]);
		}
	}

	printf("B PROMEDIO = %f\n",solver.getValue(B[0]));
	for(int m=1;m<=vehiculos[0][0];m++)
	{
		printf("B[%d] = %f\n",vehiculos[m][0],solver.getValue(B[m]));
	}
}
}
