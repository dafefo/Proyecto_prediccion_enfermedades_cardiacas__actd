import numpy as np 
import pandas as pd
import plotly.express as px
from plotly.subplots import make_subplots
import plotly.graph_objects as go

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
#Discretizar las variables
#se crea una varaible categorica de 1 si esta diagnosticado con enfermedad cardiaca y 0 no
data_cardiaca["cardiac"]=np.where(data_cardiaca["num"]>0,True,False)

#Cambiar los nombres de sexo
data_cardiaca["sex"]=np.where(data_cardiaca["sex"]>0,"Male","Female")

#Cambiar los nombres de fbs
data_cardiaca["fbs"]=np.where(data_cardiaca["fbs"]>0,">120","<120")

#Cambiar los nombres de exang
data_cardiaca["exang"]=np.where(data_cardiaca["exang"]>0,"Si","No")

#Cambiar los nombres de slope
data_cardiaca["slope"]= pd.cut(data_cardiaca["slope"], bins=[0,1,2,3],labels=["positiva","plana","negativa"])

#Cambiar los nombres de thal
data_cardiaca["thal"]= pd.cut(data_cardiaca["thal"], bins=[0,3,6,7],labels=["normal","fijo","reversible"])

#Cambiar los nombres de cp
data_cardiaca["cp"]= pd.cut(data_cardiaca["cp"], bins=[0,1,2,3,4],labels=["Angina normal","Angina atipica","No angina","Asintomatico"])

#Cambiar los nombres de restecg
data_cardiaca["restecg"]= pd.cut(data_cardiaca["restecg"], bins=[-1,0,1,2],labels=["Normal","ST anormal","Hipertrofia ventricular"])

#Se crea una avraible categorica de la edad. 
edad_discrt = pd.cut(data_cardiaca["age"],bins = [0,50,100], labels = ["Joven","Mayor"])
data_cardiaca.insert(1,"age_group", edad_discrt)

#Se crea una variable categorica para el colesterol
chol_discrt = pd.cut(data_cardiaca["chol"],bins=[0,200,240,600], labels = ["normal","alto","muy alto"])
data_cardiaca.insert(6,"chol_group",chol_discrt)

#Se crea una varibale categorica para la presion sanguinea en reposo
trestbps_discrt = pd.cut(data_cardiaca["trestbps"],bins=[0,119,129,139,179,210], labels=["normal","elevada","presion arterial nivel 1","presion arterial nivel 2","crisis"])
data_cardiaca.insert(5,"trestbps_group", trestbps_discrt)
print(data_cardiaca.columns)
#Histogramas de todas las variables
fig = make_subplots(rows=3, cols=4,
    subplot_titles=("Edad", "Sexo", "Colesterol", "Azucar en Sangre", "Angina por ejercicio",
                    "Pendiente ST","Thal","Numero de vasos","Dolor de pecho","Presion sanguinea",
                    "Electrogardiograma")
    )

fig.add_histogram2d(x = data_cardiaca["age_group"],bingroup=data_cardiaca["cardiac"],row=1,col=1)
fig.add_histogram(x = data_cardiaca["sex"],row=1,col=2)
fig.add_histogram(x = data_cardiaca["chol_group"],row=1,col=3)
fig.add_histogram(x = data_cardiaca["fbs"],row=1,col=4)
fig.add_histogram(x = data_cardiaca["exang"],row=2,col=1)
fig.add_histogram(x = data_cardiaca["slope"],row=2,col=2)
fig.add_histogram(x = data_cardiaca["thal"],row=2,col=3)
fig.add_histogram(x = data_cardiaca["ca"],row=2,col=4)
fig.add_histogram(x = data_cardiaca["cp"],row=3,col=1)
fig.add_histogram(x = data_cardiaca["trestbps_group"],row=3,col=2)
fig.add_histogram(x = data_cardiaca["restecg"],row=3,col=3)



fig.show()
#Edad
print(data_cardiaca.head())
fig = px.histogram(data_cardiaca, x = "age_group", color = "cardiac", text_auto=True, barnorm= "percent",
                   category_orders={"age_group":["Joven","Mayor"],
                                    "cardiac":[True,False]})
fig.show()
#

#Presion sanguinea
fig = px.histogram(data_cardiaca, x = "trestbps_group", color = "cardiac", text_auto=True, barnorm= "percent",
                   category_orders={"trestbps_group":["normal","elevada","presion arterial nivel 1","presion arterial nivel 2","crisis"],
                                    "cardiac":[True,False]})
fig.show()

#Distribucion de las edades categorizando por sexo y si esta diagnosticado con enfermedad cardiaca
fig = px.histogram(data_cardiaca,x = "age", color = "sex", pattern_shape = "cardiac",
                   labels = {"age":"Age",
                             "sex":"Sex",
                             "cardiac":"Diagnostico"})
#fig.show()

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
#fig.show()

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
#fig.show()


a = 1