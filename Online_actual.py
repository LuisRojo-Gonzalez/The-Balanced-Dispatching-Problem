#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jun  8 13:54:05 2019

@author: luisrojo
"""

# Importing the libraries
import pandas as pd
from time import time

#Importa base de datos
veh = pd.read_excel('BD.xlsx', sheet_name='Vehiculos')
disp = pd.read_excel('BD.xlsx', sheet_name='Disponibilidad')
serv = pd.read_excel('BD.xlsx', sheet_name='Servicios')
ranking = pd.read_excel('BD.xlsx', sheet_name='Ranking')

#Selecciona aquellas columnas a utilizar
veh = veh.iloc[:,0:2]
veh['B_m'] = 0
disp = disp.iloc[:,0:7]
serv = serv.iloc[:,0:11]

#Determina periodo de pago
dias = 30 #cuantos dias quiero considerar
payperiod = 60*24*dias #determina longitud periodo de pago

#Selecciona servicios que pertenecen al periodo de pago
serv_payperiod = pd.DataFrame(serv[serv['a_i']<=payperiod])

#Selecciona ventanas que pertenecen al periodo de pago
disp_payperiod = pd.DataFrame(disp[disp['d_j']<=payperiod])

#Calcula fin turno
disp_payperiod['t_j'] = disp_payperiod['d_j']+disp_payperiod['e_j']

#Cuenta los no asignados
contador = 0
plata = 0
vehiculo_aux = []

#medidor tiempo total
tiempo_total_inicial = time()

for i in range(len(serv_payperiod)):
    tiempo_inicial = time()
    serv_payperiod_aux = pd.DataFrame(serv_payperiod.iloc[i,:]).T #Servicio que llega
    inicio_serv = serv_payperiod_aux.iloc[0,1] #tiempo inicio servicio solicitado
    duracion_serv = serv_payperiod_aux.iloc[0,2]
    termino_serv = serv_payperiod_aux.iloc[0,1] + serv_payperiod_aux.iloc[0,2] #tiempo finalizacion servicio solicitado
    tipo_veh = serv_payperiod_aux.iloc[0,4] #tipo vehiculo necesitado
    valor = serv_payperiod_aux.iloc[0,3] #valor servicio
    veh_disp = pd.DataFrame(disp_payperiod[disp_payperiod['k_j'].ge(tipo_veh) & disp_payperiod['d_j'].le(inicio_serv) & disp_payperiod['t_j'].ge(termino_serv)]).drop_duplicates(subset=['m_j', 't_j']) #Factibilidad por tipo y turno
    
    # Analiza cuando no hay ningun vehiculo disponible para esa hora
    if len(veh_disp) == 0:
        contador = contador + 1 #cuenta cuantos servicios no podria satisfacer
        vehiculo_aux.append(0) # indica que vehiculo hizo tal servicio
        continue
    
    else:
        if len(veh_disp) == 1:
            vehiculo = veh_disp.iloc[0,1] #vehiculo asignado
            ventana = veh_disp.iloc[0,0] #ventana disponible
            # trabajo = disp_payperiod.loc[disp_payperiod['m_j'] == vehiculo,'e_j'].sum()
            trabajo = disp_payperiod.loc[disp_payperiod['m_j'].eq(vehiculo) & disp_payperiod['j'].ge(ventana),'e_j'].sum()
            actual = valor/trabajo
            veh.loc[veh['id_m'] == vehiculo, 'B_m'] = (veh.loc[veh['id_m'] == vehiculo, 'B_m'].values+actual)[0] #entrega ratio de ingreso-tiempo
            disp_payperiod.loc[disp_payperiod['j'] == ventana, 'd_j'] = disp_payperiod.loc[disp_payperiod['j'] == ventana, 'd_j']+duracion_serv #hora de disponibilidad vehiculo asignado
            
            vehiculo_aux.append(vehiculo) # indica que vehiculo hizo tal servicio
            
            plata = plata + valor # indicador de dinero recaudado
        
        else:
            # entrega el ranking que se utilizara de acuerdo a la tarifa
            if (valor < 10000):
                intervalo = 1
            else:
                if ((valor >= 10000) & (valor < 20000)):
                    intervalo = 2
                else:
                    if ((valor >= 20000) & (valor < 40000)):
                        intervalo = 3
                    else:
                        intervalo = 4
                        
            # filtra el ranking sobre los vehiculos disponibles
            ranking_aux = ranking.loc[ranking['id'].isin(veh_disp['m_j'])]
            
            # selecciona el vehiculo con el menor ranking
            menor_1 = ranking_aux.iloc[:, intervalo].nsmallest(2).iloc[0]            
            auto_1 = ranking_aux.loc[ranking_aux.iloc[:, intervalo] == menor_1, 'id'].iloc[0]
            window_1 = veh_disp.loc[veh_disp['m_j'] == auto_1, 'j']
            # tiempo_1 = disp_payperiod.loc[disp_payperiod['m_j'] == auto_1,'e_j'].sum()
            tiempo_1 = disp_payperiod.loc[disp_payperiod['m_j'].eq(auto_1) & disp_payperiod['j'].ge(window_1),'e_j'].sum()
            ingreso_1 = (veh.loc[veh['id_m'] == auto_1, 'B_m'].values)[0]*tiempo_1
            asig = auto_1
            
            vehiculo_aux.append(asig) # indica que vehiculo hizo tal servicio
            
            plata = plata + valor # indicador de dinero recaudado
            
            # actualiza lo valores del vehiculo asignado
            ventana = veh_disp.loc[veh_disp['m_j'] == asig,'j'].values[0]
            # trabajo = disp_payperiod.loc[disp_payperiod['m_j'] == asig,'e_j'].sum()
            trabajo = disp_payperiod.loc[disp_payperiod['m_j'].eq(auto_1) & disp_payperiod['j'].ge(window_1),'e_j'].sum()
            actual = valor/trabajo
            veh.loc[veh['id_m'] == asig, 'B_m'] = (veh.loc[veh['id_m'] == asig, 'B_m'].values+actual) #entrega ratio de ingreso-tiempo
            disp_payperiod.loc[disp_payperiod['j'] == ventana, 'd_j'] = disp_payperiod.loc[disp_payperiod['j'] == ventana, 'd_j']+duracion_serv #hora de disponibilidad vehiculo asignado

            # actualiza el ranking
            ranking.iloc[:, intervalo].loc[(ranking.iloc[:, intervalo] > menor_1)] = ranking.iloc[:, intervalo].loc[(ranking.iloc[:, intervalo] > menor_1)] - 1

            # actualiza el asignado como el ultimo del ranking
            ranking.iloc[:, intervalo].loc[(ranking['id'] == asig)] = len(veh)
        
    tiempo_final = time()
    tiempo_ejecucion = tiempo_final - tiempo_inicial
    print ('El tiempo de ejecucion fue:',tiempo_ejecucion) #En segundos

serv_payperiod['m_j'] = vehiculo_aux

tiempo_total_final = time()

tiempo_total = tiempo_total_final-tiempo_total_inicial
print ('El tiempo total de ejecucion fue:',tiempo_total) #En segundos

tiempo_promedio = tiempo_total/len(serv_payperiod)
print ('El tiempo de ejecucion promedio fue:',tiempo_promedio) #En segundos

#Calcula la varianza de los ingresos
ingresos = veh.loc[:,'B_m']
var = ingresos.var(ddof=0)*len(ingresos)