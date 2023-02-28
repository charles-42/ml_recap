import os
import sys
import inspect
import numpy as np

# je recherche dans un premier temps le chemin de mon répertoire courant
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
# A partir de celui-ci je déduis le chemin de mon répertoire parent
parentdir = os.path.dirname(currentdir)

# J'ajoute le chemin de mon répertoire parent au "python path" 
sys.path.insert(0, parentdir) 

import pandas as pd
df_features = pd.read_csv("data/features_2022_01_01_2022_01_31.csv")
df_tracks = pd.read_csv("data/tracks_2022_01_01_2022_01_31.csv")

df_final = df_features.merge(df_tracks,on="id")
print(df_final.columns)
df_propre = df_final[['danceability', 'energy', 'key', 'loudness', 'mode', 'speechiness',
       'acousticness', 'instrumentalness', 'liveness', 'valence', 'tempo',
       'type', 'duration_ms','time_signature', 'popularity'
       ]]

from sklearn.model_selection import train_test_split
X = df_propre.drop('popularity', axis=1)
y = df_propre['popularity']
X_train, X_test, y_train, y_test = train_test_split(X, y, train_size=0.8, shuffle=False,test_size=0.2, random_state=42)

############### IV.a Numeric features ##############

from sklearn.pipeline import Pipeline
from sklearn.preprocessing import MinMaxScaler, PolynomialFeatures

from sklearn.compose import make_column_selector
numeric_features = make_column_selector(dtype_include=np.number)

## reste du pipe

numeric_transformer = Pipeline([
        ('poly', PolynomialFeatures(2)),
        ('minmax', MinMaxScaler()) 
        ])


############### IV.c Categorial features ##############
from sklearn.compose import make_column_selector
categorial_features = make_column_selector(dtype_include=object)

from sklearn.preprocessing import OneHotEncoder
categorical_transformer = OneHotEncoder()



############### IV.d Combinaison ##############
from sklearn.compose import ColumnTransformer

preprocessor = ColumnTransformer(
    transformers=[
        ('num', numeric_transformer, numeric_features),
        ('cat', categorical_transformer, categorial_features)
    ],
    remainder="passthrough" 
)



############### IV.d Estimator ##############
from sklearn.linear_model import LinearRegression
reg = LinearRegression()


############### IV.d Final_pipe ##############

from sklearn.pipeline import Pipeline
pipe = Pipeline([
     ('preprocessor', preprocessor),

     ('clf', reg)
])


##########################################################
################ V MLFlow ####################
##########################################################

import mlflow
try:
    experiment_id = mlflow.get_experiment_by_name("pdg_model").experiment_id
except AttributeError:
    experiment_id = mlflow.create_experiment("pdg_model")

import mlflow
from mlflow.models.signature import infer_signature
run_name = "linear_model"


with mlflow.start_run(experiment_id=experiment_id, run_name=run_name) as run:
    # Log the baseline model to MLflow
    pipe.fit(X_train, y_train)
    
    # for param,value in model_fit.best_estimator_[-1].get_params().items():
    #     mlflow.log_param(param, value)
    

    
    signature = infer_signature(X_train, pipe.predict(X_train))

    
    mlflow.sklearn.log_model(pipe, "linear_model", signature=signature)

    
    model_uri = mlflow.get_artifact_uri("linear_model")
    
    
    eval_data = X_test
    eval_data["label"] = y_test

    # Evaluate the logged model
    result = mlflow.evaluate(
        model_uri,
        eval_data,
        targets="label",
        model_type="regressor",
        evaluators=["default"],
    )