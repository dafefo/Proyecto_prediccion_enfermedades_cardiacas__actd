# -*- coding: utf-8 -*-
"""
Created on Wed Mar  8 10:06:22 2023

@author: baka
"""

import numpy as np 
import pandas as pd
import plotly.express as px
from pgmpy.models import BayesianNetwork
from pgmpy.factors.discrete import TabularCPD
from pgmpy.estimators import MaximumLikelihoodEstimator
from pgmpy.inference import VariableElimination
##################CARGA Y MANIPULACION DE DATOS#####################################################
#Apertura de los datos Daniel
#data_cardiaca = pd.read_csv("Analitica computacional/Proyecto1 Enfermedades cardiacas/cleveland_data.csv")

#Apertura datos Christer
data_cardiaca = pd.read_csv("C:/Users/baka/Desktop/analitica/Proyectos/Proyecto_prediccion_enfermedades_cardiacas__actd/cleveland_data.csv")

#En las variables ca y thal hay datos faltantes que se ubican con el simbolo ?
print(data_cardiaca.loc[data_cardiaca["ca"]=="?"])
#en la variable ca estan en las posiciones 166,192,287,302
print(data_cardiaca.loc[data_cardiaca["thal"]=="?"])
#en la variable Thal estan en 87 y 266
#Es decir en total se deben eliminar 6 datos de la base de 303

#Remover los datos faltantes
faltantes = np.array([87,166,192,266,287,302])
for i in faltantes:
    data_cardiaca = data_cardiaca.drop(i)

#Pasar las columans de tipo object a numeros
data_cardiaca["ca"]=pd.to_numeric(data_cardiaca["ca"])
data_cardiaca["thal"]=pd.to_numeric(data_cardiaca["thal"])

estadisticas = data_cardiaca.describe()
#Discretizar las variables
#se crea una varaible categorica de 1 si esta diagnosticado con enfermedad cardiaca y 0 no
data_cardiaca["cardiac"]=np.where(data_cardiaca["num"]>0,True,False)

#Se crea una avraible categorica de la edad. 
edad_discrt = pd.cut(data_cardiaca["age"],bins = [0,50,100], labels = ["Joven","Mayor"])
data_cardiaca.insert(1,"age_group", edad_discrt)

#Se crea una variable categorica para el colesterol
chol_discrt = pd.cut(data_cardiaca["chol"],bins=[0,200,240,600], labels = ["normal","alto","muy alto"])
data_cardiaca.insert(6,"chol_group",chol_discrt)

#Se crea una varibale categorica para la presion sanguinea en reposo
trestbps_discrt = pd.cut(data_cardiaca["trestbps"],bins=[0,119,129,139,179,210], labels=["normal","elevada","presion arterial nivel 1","presion arterial nivel 2","crisis"])
data_cardiaca.insert(5,"trestbps_group", trestbps_discrt)
print(data_cardiaca.head())
print(data_cardiaca.columns)

#########RED BAYESIANA################################################
#Se crea el modelo Bayesiano
model = BayesianNetwork([("sex", "cardiac"), ("fbs", "cardiac"), ("age_group","cardiac"), ("chol_group","cardiac"), ("cardiac", "exang"),("cardiac","slope"),("cardiac", "thal"), ("cardiac","cp"), ("cardiac","ca"), ("cardiac","trestbps_group"), ("cardiac","restecg")])
emv = MaximumLikelihoodEstimator(model=model, data=data_cardiaca)

model.fit(data=data_cardiaca, estimator = MaximumLikelihoodEstimator) 
for i in model.nodes():
    print(model.get_cpds(i))
    
model.check_model()

infer = VariableElimination(model)
posterior_p = infer.query(["cardiac"], evidence={"sex": 1, "age_group":"Mayor", "chol_group": "normal", "fbs": 1, "exang": 1})
print(posterior_p)

######################Función###########################################


def calcularProbabilidad(psexo, pgrupoEdad, pgrupoColesterol, pfbs, pexang, pcp, ptrestbpsgroup, prestcg, pslope,pca, pthal):
    
    probabilidadEstimada=infer.query(["cardiac"], evidence={"sex": psexo, "age_group":pgrupoEdad, "chol_group": pgrupoColesterol, "fbs": pfbs, "exang": pexang , "cp":pcp , "trestbps_group":ptrestbpsgroup , "restecg":prestcg , "slope":pslope , "ca":pca , "thal":pthal})
    return probabilidadEstimada
    

print(calcularProbabilidad(1,"Mayor","normal",1,1,4,"elevada",2,3,2,6).values)

lista= ["Mayor",1,1,"normal","normal",1,2,0,3,0,6]

###############################
###############################
def calcularProbabilidadl(selected_values_list):
    
    probabilidadEstimada=infer.query(["cardiac"], evidence={"sex": selected_values_list[1], "age_group":selected_values_list[0], "chol_group": selected_values_list[4], "fbs": selected_values_list[5], "exang": selected_values_list[7], "cp":selected_values_list[2] , "trestbps_group":selected_values_list[3] , "restecg":selected_values_list[6], "slope":selected_values_list[8] , "ca":selected_values_list[9] , "thal":selected_values_list[10]})
    return probabilidadEstimada
    

print(calcularProbabilidadl(lista))
