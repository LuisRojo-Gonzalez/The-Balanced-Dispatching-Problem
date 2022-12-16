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

#Selecciona aquellas columnas a utilizar
veh = veh.iloc[:,0:2]
veh['B_m'] = 0
veh['B_m_e'] = 0
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
    
    #Analiza cuando no hay ningun vehiculo disponible para esa hora
    if len(veh_disp) == 0:
        contador = contador + 1 #cuenta cuantos servicios no podria satisfacer
        vehiculo_aux.append(0) # indica que vehiculo hizo tal servicio
        continue
        #proceso de cambio hora de inicio
#        inicio_aux = pd.DataFrame(disp_payperiod[disp_payperiod['k_j'].ge(tipo_veh)])
#        inicio_serv = inicio_aux['d_j'].min()
#        veh_disp = pd.DataFrame(disp_payperiod[disp_payperiod['k_j'].ge(tipo_veh) & disp_payperiod['d_j'].le(inicio_serv)])# & disp_payperiod['t_j'].ge(termino_serv)]) #Factibilidad por tipo y turno
#        
#        if len(veh_disp) == 1:
#            vehiculo = veh_disp.iloc[0,1] #vehiculo asignado
#            ventana = veh_disp.iloc[0,0] #ventana disponible
#            trabajo = disp_payperiod.loc[disp_payperiod['m_j'] == vehiculo,'e_j'].sum()
#            #trabajo = disp_payperiod.loc[disp_payperiod['m_j'].eq(vehiculo) & disp_payperiod['j'].ge(ventana),'e_j'].sum()
#            actual = valor/trabajo
#            veh.loc[veh['id_m'] == vehiculo, 'B_m'] = (veh.loc[veh['id_m'] == vehiculo, 'B_m'].values+actual)[0] #entrega ratio de ingreso-tiempo
#            disp_payperiod.loc[disp_payperiod['j'] == ventana, 'd_j'] = disp_payperiod.loc[disp_payperiod['j'] == ventana, 'd_j']+duracion_serv #hora de disponibilidad vehiculo asignado
#        
#        else:
#            #seleccion de vehiculo segun formula
#            #veh_disp['B_m'] = veh.loc[veh.loc['id_m'] == veh_disp.loc['m_j'], 'B_m']
#            ratio = pd.DataFrame()
#            for j in range(len(veh_disp)):
#                auto = veh_disp.iloc[j,1]
#                window = veh_disp.iloc[j,0]
#                tiempo = disp_payperiod.loc[disp_payperiod['m_j'] == auto,'e_j'].sum()
#                #tiempo = disp_payperiod.loc[disp_payperiod['m_j'].eq(auto) & disp_payperiod['j'].ge(window),'e_j'].sum()
#                #coef = pd.DataFrame(veh.loc[veh['id_m'] == auto, 'B_m']/tiempo)
#                coef = pd.DataFrame(veh.loc[veh['id_m'] == auto, 'B_m'])
#                ratio = ratio.append(coef, ignore_index=True)
#            #Obtiene el ratio cercano
#            suma = ratio.sum()
#            ratio_aux = pd.DataFrame()
#            for k in range(len(veh_disp)):
#                auto = veh_disp.iloc[k,1]
#                window = veh_disp.iloc[k,0]
#                tiempo_aux = disp_payperiod.loc[disp_payperiod['m_j'] == auto,'e_j'].sum()
#                #tiempo_aux = disp_payperiod.loc[disp_payperiod['m_j'].eq(auto) & disp_payperiod['j'].ge(window),'e_j'].sum()
#                #coef_aux = pd.DataFrame((1/(2*len(veh_disp)))*(suma-(valor/tiempo_aux)*(len(veh_disp)-1)))
#                coef_aux = pd.DataFrame((1/(len(veh_disp)))*(suma-(valor/tiempo_aux)*(len(veh_disp)-1)))
#                ratio_aux = ratio_aux.append(coef_aux, ignore_index=True)
#            #elige el ratio mas cercano
#            asig = pd.DataFrame(abs(ratio.values-ratio_aux.values)).idxmin()[0]
#        
#            vehiculo = veh_disp.iloc[asig,1] #vehiculo asignado
#            ventana = veh_disp.iloc[asig,0]
#            trabajo = disp_payperiod.loc[disp_payperiod['m_j'] == vehiculo,'e_j'].sum()
#            #trabajo = disp_payperiod.loc[disp_payperiod['m_j'].eq(vehiculo) & disp_payperiod['j'].ge(ventana),'e_j'].sum()
#            actual = valor/trabajo
#            veh.loc[veh['id_m'] == vehiculo, 'B_m'] = (veh.loc[veh['id_m'] == vehiculo, 'B_m'].values+actual) #entrega ratio de ingreso-tiempo
#            disp_payperiod.loc[disp_payperiod['j'] == ventana, 'd_j'] = disp_payperiod.loc[disp_payperiod['j'] == ventana, 'd_j']+duracion_serv #hora de disponibilidad vehiculo asignado
    
    else:
        if len(veh_disp) == 1:
            vehiculo = veh_disp.iloc[0,1] #vehiculo asignado
            ventana = veh_disp.iloc[0,0] #ventana disponible
            # trabajo = disp_payperiod.loc[disp_payperiod['m_j'] == vehiculo,'e_j'].sum()
            trabajo = disp_payperiod.loc[disp_payperiod['m_j'].eq(vehiculo) & disp_payperiod['j'].ge(ventana),'e_j'].sum()
            actual = valor/trabajo
            actual_e = valor/trabajo
            veh.loc[veh['id_m'] == vehiculo, 'B_m'] = (veh.loc[veh['id_m'] == vehiculo, 'B_m'].values+actual)[0] #entrega ratio de ingreso-tiempo
            veh.loc[veh['id_m'] == vehiculo, 'B_m_e'] = (veh.loc[veh['id_m'] == vehiculo, 'B_m_e'].values+actual_e)[0] #entrega ratio de ingreso-tiempo
            disp_payperiod.loc[disp_payperiod['j'] == ventana, 'd_j'] = disp_payperiod.loc[disp_payperiod['j'] == ventana, 'd_j']+duracion_serv #hora de disponibilidad vehiculo asignado

            vehiculo_aux.append(vehiculo) # indica que vehiculo hizo tal servicio
            
            plata = plata + valor # indicador de dinero recaudado
            
        else:
            #seleccion de vehiculo segun ingreso menor ratio A_m/e
#            #veh_disp['B_m'] = veh.loc[veh.loc['id_m'] == veh_disp.loc['m_j'], 'B_m']
#            ratio = pd.DataFrame()
#            for j in range(len(veh_disp)):
#                auto = veh_disp.iloc[j,1]
#                window = veh_disp.iloc[j,0]
#                tiempo = disp_payperiod.loc[disp_payperiod['m_j'] == auto,'e_j'].sum()
#                #tiempo = disp_payperiod.loc[disp_payperiod['m_j'].eq(auto) & disp_payperiod['j'].ge(window),'e_j'].sum()
#                #coef = pd.DataFrame(veh.loc[veh['id_m'] == auto, 'B_m']/tiempo)
#                coef = pd.DataFrame(veh.loc[veh['id_m'] == auto, 'B_m'])
#                ratio = ratio.append(coef, ignore_index=True)
#            #Obtiene el ratio cercano
#            suma = ratio.sum()
#            #suma = pd.DataFrame([veh.loc[:,'B_m'].sum()])
#            ratio_aux = pd.DataFrame()
#            for k in range(len(veh_disp)):
#                auto = veh_disp.iloc[k,1]
#                window = veh_disp.iloc[k,0]
#                tiempo_aux = disp_payperiod.loc[disp_payperiod['m_j'] == auto,'e_j'].sum()
#                #tiempo_aux = disp_payperiod.loc[disp_payperiod['m_j'].eq(auto) & disp_payperiod['j'].ge(window),'e_j'].sum()
#                #coef_aux = pd.DataFrame((1/(2*len(veh_disp)))*(suma-(valor/tiempo_aux)*(len(veh_disp)-1)))
#                coef_aux = pd.DataFrame((1/(2*len(veh_disp)))*(suma-(valor/tiempo_aux)*(len(veh_disp)-1)))
#                ratio_aux = ratio_aux.append(coef_aux, ignore_index=True)
#            #elige el ratio mas cercano
#            asig = pd.DataFrame(abs(ratio.values-ratio_aux.values)).idxmin()[0]
#            #asig1 = pd.DataFrame(ratio.values-ratio_aux.values)
#            #asig = asig1[asig1>=0].idxmin()[0]
            
            asig1 = veh.loc[veh['id_m'].isin(veh_disp['m_j'])].sort_values(by=['B_m'])
            
            vehiculo = asig1.iloc[0,0]
            
            vehiculo_aux.append(vehiculo) # indica que vehiculo hizo tal servicio
            
            plata = plata + valor # indicador de dinero recaudado        
            
            #vehiculo = veh_disp.iloc[veh_disp['m_j'] == asig,1] #vehiculo asignado
            ventana = veh_disp.loc[veh_disp['m_j'] == vehiculo,'j']
            ventana = pd.DataFrame(ventana).iloc[0,0]
            trabajo = disp_payperiod.loc[disp_payperiod['m_j'] == vehiculo,'e_j'].sum()
            trabajo = disp_payperiod.loc[disp_payperiod['m_j'].eq(vehiculo) & disp_payperiod['j'].ge(ventana),'e_j'].sum()
            actual = valor/trabajo
            actual_e = valor/trabajo            
            veh.loc[veh['id_m'] == vehiculo, 'B_m'] = (veh.loc[veh['id_m'] == vehiculo, 'B_m'].values+actual) #entrega ratio de ingreso-tiempo
            veh.loc[veh['id_m'] == vehiculo, 'B_m_e'] = (veh.loc[veh['id_m'] == vehiculo, 'B_m_e'].values+actual_e)[0] #entrega ratio de ingreso-tiempo
            disp_payperiod.loc[disp_payperiod['j'] == ventana, 'd_j'] = disp_payperiod.loc[disp_payperiod['j'] == ventana, 'd_j']+duracion_serv #hora de disponibilidad vehiculo asignado
    
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
#asignados = veh.loc[veh['B_m'] != 0, 'B_m']
#tamaño = len(asignados)
#var = asignados.var(ddof=0)*tamaño
ingresos = veh.loc[:,'B_m_e']
var = ingresos.var(ddof=0)*len(ingresos)