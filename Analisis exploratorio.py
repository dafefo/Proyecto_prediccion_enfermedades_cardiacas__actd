import numpy as np 
import pandas as pd
import plotly.express as px
from plotly.subplots import make_subplots
import plotly.graph_objects as go

#Apertura de los datos Daniel
#data_cardiaca = pd.read_csv("Analitica computacional/Proyecto1 Enfermedades cardiacas/cleveland_data.csv")

#Apertura datos Christer
#data_cardiaca = pd.read_csv("cleveland_data.csv")
data_cardiaca = pd.read_csv('https://archive.ics.uci.edu/ml/machine-learning-databases/heart-disease/processed.cleveland.data', header=None)
data_cardiaca.columns = [
    'age', 'sex', 'cp', 'trestbps', 'chol','fbs', 'restecg','thalac', 'exang', 'oldpeak', 'slope',
    'ca', 'thal', 'num'
]
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
data_cardiaca["sex"]=np.where(data_cardiaca["sex"]>0,"Hombre","Mujer")

#Cambiar los nombres de fbs
data_cardiaca["fbs"]=np.where(data_cardiaca["fbs"]>0,">120","<120")

#Cambiar los nombres de exang
data_cardiaca["exang"]=np.where(data_cardiaca["exang"]>0,"Si","No")

#Cambiar los nombres de slope
data_cardiaca["slope"]= pd.cut(data_cardiaca["slope"], bins=[0,1,2,3],labels=["positiva","plana","negativa"])

#Cambiar los nombres de thal
data_cardiaca["thal"]= pd.cut(data_cardiaca["thal"], bins=[0,3,6,7],labels=["Normal","Fijo","Reversible"])

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

#Subplot de los histogramas de las variables que generan la enfermedad
fig = make_subplots(rows=3, cols=2, subplot_titles=["Edad","Sexo","Nivel de colesterol","Glicemia en Ayunas"])

trace0 = go.Histogram(x=data_cardiaca["age"], name="Edad", showlegend=False, marker=dict(color="#F58518"))
trace1 = go.Histogram(x=data_cardiaca["sex"], name = "Sexo", showlegend=False, marker=dict(color="#BAB0AC"))
trace2 = go.Histogram(x=data_cardiaca["chol"], name = "Nivel de colesterol", showlegend=False, marker=dict(color="#F58518"))
trace3 = go.Histogram(x=data_cardiaca["fbs"], name = "Glicemia en Ayunas", showlegend=False, marker=dict(color="#BAB0AC"))

fig.append_trace(trace0, 1, 1)
fig.append_trace(trace1, 1, 2)
fig.append_trace(trace2, 2, 1)
fig.append_trace(trace3, 2, 2)


fig.show()
#Edad
print(data_cardiaca.head())
fig = px.histogram(data_cardiaca, x = "age_group", color = "cardiac", text_auto=True, barnorm= "percent",
                   category_orders={"age_group":["Joven","Mayor"],
                                    "cardiac":[True,False]},
                    color_discrete_map={True:"#F58518", False:"#BAB0AC"},
                    title="Relacion edad y enfermedad cardiaca")
fig.update_layout(legend_title = "Sufre de enfermedad cardiaca",
                  xaxis_title = "Edad",
                  yaxis_title = "Conteo(Porcentaje)")
fig.show()
#Sexo
fig = px.histogram(data_cardiaca, x = "sex", color = "cardiac", text_auto=True, barnorm= "percent",
                   category_orders={"sex":["Hombre","Mujer"],
                                    "cardiac":[True,False]},
                    color_discrete_map={True:"#F58518", False:"#BAB0AC"},
                    title="Relación sexo y enfermedad cardiaca")
fig.update_layout(legend_title = "Sufre de enfermedad cardiaca",
                  xaxis_title = "Sexo",
                  yaxis_title = "Conteo(Porcentaje)")
fig.show()

#Cp
fig = px.histogram(data_cardiaca, x = "cp", color = "cardiac", text_auto=True, barnorm= "percent",
                   category_orders={"cp":["Angina normal","Angina atipica","No angina","Asintomatico"],
                                    "cardiac":[True,False]},
                    color_discrete_map={True:"#F58518", False:"#BAB0AC"},
                    title="Relación dolor de pecho y enfermedad cardiaca")
fig.update_layout(legend_title = "Sufre de enfermedad cardiaca",
                  xaxis_title = "Dolor de Pecho",
                  yaxis_title = "Conteo(Porcentaje)")
fig.show()

#trestbps
fig = px.histogram(data_cardiaca, x = "trestbps_group", color = "cardiac", text_auto=True, barnorm= "percent",
                   category_orders={"trestbps_group":["normal","elevada","presion arterial nivel 1","presion arterial nivel 2","crisis"],
                                    "cardiac":[True,False]},
                                    color_discrete_map={True:"#F58518", False:"#BAB0AC"},
                                    title="Relación presión arterial en reposo y enfermedad cardiaca")
fig.update_layout(legend_title = "Sufre de enfermedad cardiaca",
                  xaxis_title = "Presión Arterial",
                  yaxis_title = "Conteo(Porcentaje)")
fig.show()

#Colesterol
fig = px.histogram(data_cardiaca, x = "chol_group", color = "cardiac", text_auto=True, barnorm= "percent",
                   category_orders={"chol_group":["normal","alto","muy alto"],
                                    "cardiac":[True,False]},
                    color_discrete_map={True:"#F58518", False:"#BAB0AC"},
                    title="Relación nivel de colesterol y enfermedad cardiaca")
fig.update_layout(legend_title = "Sufre de enfermedad cardiaca",
                  xaxis_title = "Nivel de Colesterol",
                  yaxis_title = "Conteo(Porcentaje)")
fig.show()

#fbs
fig = px.histogram(data_cardiaca, x = "fbs", color = "cardiac", text_auto=True, barnorm= "percent",
                   category_orders={"fbs":[">120","<120"],
                                    "cardiac":[True,False]},
                    color_discrete_map={True:"#F58518", False:"#BAB0AC"},
                    title="Relación glicemia en ayunas y enfermedad cardiaca")
fig.update_layout(legend_title = "Sufre de enfermedad cardiaca",
                  xaxis_title = "Azucar en sangre (mg/dl)",
                  yaxis_title = "Conteo(Porcentaje)")
fig.show()

#restecg
fig = px.histogram(data_cardiaca, x = "restecg", color = "cardiac", text_auto=True, barnorm= "percent",
                   category_orders={"restecg":["Normal","ST anormal","Hipertrofia ventricular"],
                                    "cardiac":[True,False]},
                    color_discrete_map={True:"#F58518", False:"#BAB0AC"},
                    title="Relación electrocardiograma y enfermedad cardiaca")
fig.update_layout(legend_title = "Sufre de enfermedad cardiaca",
                  xaxis_title = "Resultado electrocardiograma",
                  yaxis_title = "Conteo(Porcentaje)")
fig.show()

#exang
fig = px.histogram(data_cardiaca, x = "exang", color = "cardiac", text_auto=True, barnorm= "percent",
                   category_orders={"exang":["Si","No"],
                                    "cardiac":[True,False]},
                    color_discrete_map={True:"#F58518", False:"#BAB0AC"},
                    title="Relación angina inducida por ejercicio y enfermedad cardiaca")
fig.update_layout(legend_title = "Sufre de enfermedad cardiaca",
                  xaxis_title = "Presencia de angina durante ejercicio ",
                  yaxis_title = "Conteo(Porcentaje)")
fig.show()

#slope
fig = px.histogram(data_cardiaca, x = "slope", color = "cardiac", text_auto=True, barnorm= "percent",
                   category_orders={"slope":["positiva","plana","negativa"],
                                    "cardiac":[True,False]},
                    color_discrete_map={True:"#F58518", False:"#BAB0AC"},
                    title="Relación pendiente de la curva ST y enfermedad cardiaca")
fig.update_layout(legend_title = "Sufre de enfermedad cardiaca",
                  xaxis_title = "Pendiente curva ST",
                  yaxis_title = "Conteo(Porcentaje)")
fig.show()

#ca
fig = px.histogram(data_cardiaca, x = "ca", color = "cardiac", text_auto=True, barnorm= "percent",
                   category_orders={"cardiac":[True,False]},
                    color_discrete_map={True:"#F58518", False:"#BAB0AC"},
                    title="Relación número de vasos sanguineos mayores coloreados con fluroscopia y enfermedad cardiaca")
fig.update_layout(legend_title = "Sufre de enfermedad cardiaca",
                  xaxis_title = "Número de vasos marcados",
                  yaxis_title = "Conteo(Porcentaje)")
fig.show()

#thal
fig = px.histogram(data_cardiaca, x = "thal", color = "cardiac", text_auto=True, barnorm= "percent",
                   category_orders={"thal":["Normal","Fijo","Reversible"],"cardiac":[True,False]},
                    color_discrete_map={True:"#F58518", False:"#BAB0AC"},
                    title="Relación Thallium Stress test y enfermedad cardiaca")
fig.update_layout(legend_title = "Sufre de enfermedad cardiaca",
                  xaxis_title = "Thallium Stress Test",
                  yaxis_title = "Conteo(Porcentaje)")
fig.show()

###################################################################################################################
"""#Distribucion de las edades categorizando por sexo y si esta diagnosticado con enfermedad cardiaca
fig = px.histogram(data_cardiaca,x = "age", color = "sex", pattern_shape = "cardiac",
                   labels = {"age":"Age",
                             "sex":"Sex",
                             "cardiac":"Diagnostico"})
fig.show()

#Distribucion de los casos que reportan dolor en el pecho
fig = px.pie(data_cardiaca, names = "cp")
fig.show()

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
#fig.show()
"""

a = 1