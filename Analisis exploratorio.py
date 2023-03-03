import numpy as np 
import pandas as pd
import plotly.express as px

#Apertura de los datos Daniel
data_cardiaca = pd.read_csv("Analitica computacional/Proyecto1 Enfermedades cardiacas/cleveland_data.csv")

#Apertura datos Christer
#data_cardiaca = pd.read_csv("cleveland_data.csv")

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

#se crea una varaible categorica de 1 si esta diagnosticado con enfermedad cardiaca y 0 no
data_cardiaca["cardiac"]=np.where(data_cardiaca["num"]>0,True,False)

#Distribucion de las edades categorizando por sexo y si esta diagnosticado con enfermedad cardiaca
fig = px.histogram(data_cardiaca,x = "age", color = "sex", pattern_shape = "cardiac",
                   labels = {"age":"Age",
                             "sex":"Sex",
                             "cardiac":"Diagnostico"})
fig.show()

#Distribucion de los casos que reportan dolor en el pecho
fig = px.pie(data_cardiaca, names = "cp")
#fig.show()

#Distribucion de la presion sanguinea en reposos sistolica
fig = px.histogram(data_cardiaca,x = "trestbps", color = "sex", pattern_shape = "cardiac",
                   labels = {"trestbps":"Presión sanguinea en reposo",
                             "sex":"Sexo",
                             "cardiac":"Diagnostico"})
fig.add_annotation(x=120,
            text="Valor normal",
            showarrow=True,
            arrowhead=1)
fig.add_annotation(x=130,
            text="Valor elevado",
            showarrow=True,
            arrowhead=1)
fig.add_annotation(x=140,
            text="Hipertension fase 1",
            showarrow=True,
            arrowhead=1)
fig.add_annotation(x=180,
            text="Hipertension fase 2",
            showarrow=True,
            arrowhead=1)
fig.add_annotation(x=190,
            text="Crisis de hipertension",
            showarrow=True,
            arrowhead=1)
fig.show()

#Distribucion de niveles de colesterol
#Dada la grafiac se encontro que hay un dato atipico pues se tiene un colesterol mayor a 560 que esto ya estaria la persona muerta
fig = px.histogram(data_cardiaca,x = "chol", color = "sex", pattern_shape = "cardiac",
                   labels = {"chol":"nivel de colesterol",
                             "sex":"Sexo",
                             "cardiac":"Diagnostico"})
fig.add_annotation(x=200,
            text="Valor normal",
            showarrow=True,
            arrowhead=1)
fig.add_annotation(x=240,
            text="Nivel máximo",
            showarrow=True,
            arrowhead=1)
fig.add_annotation(x=250,
            text="Nivel alto",
            showarrow=True,
            arrowhead=1)
fig.show()

a = 1