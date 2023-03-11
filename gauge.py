# -*- coding: utf-8 -*-
"""
Created on Sat Mar 11 09:58:57 2023

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


#def calcularProbabilidad(psexo, pgrupoEdad, pgrupoColesterol, pfbs, pexang, pcp, ptrestbpsgroup, prestcg, pslope,pca, pthal):
    
 #   probabilidadEstimada=infer.query(["cardiac"], evidence={"sex": psexo, "age_group":pgrupoEdad, "chol_group": pgrupoColesterol, "fbs": pfbs, "exang": pexang , "cp":pcp , "trestbps_group":ptrestbpsgroup , "restecg":prestcg , "slope":pslope , "ca":pca , "thal":pthal})
  #  return probabilidadEstimada
    

#print(calcularProbabilidad(1,"Mayor","normal",1,1,4,"elevada",2,3,2,6))
###############################
def calcularProbabilidad(selected_values_list):
    probabilidadEstimada=infer.query(["cardiac"], evidence={"sex": selected_values_list[1], "age_group":selected_values_list[0], "chol_group": selected_values_list[4], "fbs": selected_values_list[5], "exang": selected_values_list[7], "cp":selected_values_list[2] , "trestbps_group":selected_values_list[3] , "restecg":selected_values_list[6], "slope":selected_values_list[8] , "ca":selected_values_list[9] , "thal":selected_values_list[10]})
    return probabilidadEstimada



import plotly.graph_objects as go
probabilidadCardiaca=0
'''
fig = go.Figure()
fig.add_trace(go.Indicator(
    name = "my_trace",
    domain={'x': [0, 1], 'y': [0, 1]},
    value=450,
    mode="gauge+number+delta",
    title={'text': "Speed"},
    delta={'reference': 380},
    gauge={'axis': {'range': [None, 500]},
           'steps': [
               {'range': [0, 250], 'color': "lightgray"},
               {'range': [250, 400], 'color': "gray"}],
           'threshold': {'line': {'color': "red", 'width': 4}, 'thickness': 0.75, 'value': 490}}))
'''

import numpy as np 
import pandas as pd
import plotly.express as px
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State

# Load the Cleveland Heart Disease dataset
#df = pd.read_csv('https://archive.ics.uci.edu/ml/machine-learning-databases/heart-disease/processed.cleveland.data', header=None)
df= data_cardiaca

# Rename the columns with descriptive names
df.columns = [
    'age', 'edad', 'sexo', 'cp', 'rtrestbps','trestbps', 'rchol','colesterol', 'fbs', 'restecg', 'thalach',
    'exang', 'oldpeak', 'pendiente', 'ca', 'thal','num', 'cardiac'
]

# Define the variables to include in the dropdown menus
dropdown_vars = [col for col in df.columns if col not in ['index','age','rtrestbps','rchol','thalach', 'oldpeak','num','cardiac', 'target']]



# Define the app layout
app = dash.Dash(__name__)
app.layout = html.Div([
    
    html.Div([
        html.Label(f'Seleccione un valor para {var}'),
        dcc.Dropdown(
            id=f'{var}-dropdown',
            options=[
                {'label': 'Mayor', 'value': 'Mayor'},
                {'label': 'Joven', 'value': 'Joven'}
            ] if var == 'edad' else (
                [
                    {'label': 'normal', 'value': 'normal'},
                    {'label': 'elevada', 'value': 'elevada'},
                    {'label': 'presion arterial nivel 1', 'value': 'nivel 1'},
                    {'label': 'presion arterial nivel 2', 'value': 'nivel 2'},
                    {'label': 'crisis', 'value': 'crisis'}
                ] if var == 'trestbps' else (
                    [
                        {'label': 'normal', 'value': 'normal'},
                        {'label': 'alto', 'value': 'alto'},
                        {'label': 'muy alto', 'value': 'muy alto'}
                    ] if var == 'colesterol' else
                        [
                            {'label': '0', 'value': 0},
                            {'label': '3', 'value': 3},
                            {'label': '2', 'value': 2},
                            {'label': '1', 'value': 1}
                        ] if var == 'ca' else
                            [
                                {'label': '6', 'value': 6},
                                {'label': '3', 'value': 3},
                                {'label': '7', 'value': 7}
                            ] if var == 'thal' else
                            [{'label': val, 'value': val} for val in df[var].unique()]
                )
            ),
            value=df[var].unique()[0],  # Default value
        )
    ]) for var in dropdown_vars
] + [
    html.Button('Submit', id='submit-button', n_clicks=0),
    html.Div(id='output-container', children=''),html.Div([dcc.Graph(id="my_gauge")])
    
    
])

# Define the app callback
@app.callback(
    Output('my_gauge', 'figure'),
    Output('output-container', 'children'),
    
    [Input('submit-button', 'n_clicks')],
    [State(f'{var}-dropdown', 'value') for var in dropdown_vars]
)
def update_output(n_clicks, *selected_values):
    #lista= ["Mayor",1,1,"normal","normal",1,2,0,3,0,6]
    if n_clicks > 0:
        selected_values_list = [val if val != "?" else None for val in selected_values]
        print(selected_values_list)
        print(calcularProbabilidad(selected_values_list))
        probs=calcularProbabilidad(selected_values_list)
        probabilidadCardiaca=probs.values[1]
        
        fig = go.Figure()
        fig.add_trace(go.Indicator(
            name = "my_trace",
            domain={'x': [0, 1], 'y': [0, 1]},
            value=15,
            mode="gauge+number+delta",
            title={'text': "Speed"},
            delta={'reference': 380},
            gauge={'axis': {'range': [None, 500]},
                   'steps': [
                       {'range': [0, 250], 'color': "lightgray"},
                       {'range': [250, 400], 'color': "gray"}],
                   'threshold': {'line': {'color': "red", 'width': 4}, 'thickness': 0.75, 'value': 490}}))
     
        return fig
    
'''@app.callback(
    Output('my_gauge', 'figure'),
    [Input('submit-button', 'n_clicks')],
    [State(f'{var}-dropdown', 'value') for var in dropdown_vars]
    )
def update_gauge(n_clicks, *selected_values):
    if n_clicks > 0:
        selected_values_list = [val if val != "?" else None for val in selected_values]
        probs=calcularProbabilidad(selected_values_list)
        probabilidadCardiaca=probs.values[1]
        
        fig = go.Figure(go.Indicator(
            domain = {'x': [0, 1], 'y': [0, 1]},
            value = 0.5,
            mode = "gauge+number+delta",
            title = {'text': "perro"},
            delta = {'reference': 0.7},
            gauge = {'axis': {'range': [None, 1]},
                     'steps' : [
                         {'range': [0, 0.5], 'color': "lightgray"},
                         {'range': [0.5, 0.9], 'color': "gray"}],
                     'threshold' : {'line': {'color': "red", 'width': 4}, 'thickness': 0.75, 'value': 490}}))
    
        return fig
        
'''
# Run the app
if __name__ == '__main__':
    app.run_server(debug=False)