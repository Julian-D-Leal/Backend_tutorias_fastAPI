from keras.models import Sequential
from keras.layers import Dense
from tensorflow import keras
import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler, OneHotEncoder, MultiLabelBinarizer, LabelEncoder, StandardScaler
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score, mean_absolute_error
from spacy.lang.es.stop_words import STOP_WORDS

def neuronal_network_subjects():
    pf = pd.read_json('subjectScores.json', encoding='utf-8')
    pf.drop(['email'], axis=1, inplace=True)

    scal = StandardScaler()
    score = scal.fit_transform(pf[['subject_score']].values) # Se normalizan la calificación de las materias
    pf['subject_score'] = score

    scaler = MinMaxScaler()
    pf[['semester', 'subject_semester']] = scaler.fit_transform(pf[['semester', 'subject_semester']]) # Se normalizan los datos

    enc = OneHotEncoder(sparse=False)
    career_one_hot = enc.fit_transform(pf['career'].values.reshape(-1, 1)) # Se convierte la carrera en one hot
    career_columns = enc.get_feature_names_out(['career'])
    career_df = pd.DataFrame(career_one_hot, columns=career_columns) # Se crea un dataframe con las columnas de la carrera
    pf = pd.concat([pf, career_df], axis=1) # Se agrega el dataframe de la carrera al dataframe principal
    pf = pf.drop(['career'], axis=1) # Se elimina la columna de la carrera

    mlb = MultiLabelBinarizer()
    subject_career_one_hot = mlb.fit_transform(pf['subject_career'].str.split(', ')) # Se convierte la materia en one hot
    subject_career_columns = mlb.classes_
    subject_career_df = pd.DataFrame(subject_career_one_hot, columns=subject_career_columns) # Se crea un dataframe con las columnas de la materia
    pf = pd.concat([pf, subject_career_df], axis=1) # Se agrega el dataframe de la materia al dataframe principal
    pf = pf.drop(['subject_career'], axis=1) # Se elimina la columna de la materia

    pf ['keywords'] = [list (filter(lambda x: isinstance(x,str) and x not in STOP_WORDS , y)) for y in pf['keywords']] # Se eliminan las palabras vacias
    vectorizer = TfidfVectorizer(lowercase=True)
    tfidf_key_words = vectorizer.fit_transform(pf['keywords'].apply(lambda x: ' '.join(x))) # Se convierten las palabras clave en tfidf
    pf['keywords'] = np.array(tfidf_key_words.toarray()) # Se agrega la columna de tfidf al dataframe principal

    label_encoder = LabelEncoder()
    label_subject = label_encoder.fit_transform(pf['subject']) # Se convierte la materia en un label
    pf = pf.drop(['subject'], axis=1) # Se elimina la columna de la materia
    pf['subject'] = label_subject # Se agrega la columna de label al dataframe principal

    x = pf.drop(['subject_score'], axis=1) # Se separa la columna de la materia
    y = pf['subject_score'] # Se separa la columna de la nota
    X_train, X_test, y_train, y_test = train_test_split(x, y, random_state=42, test_size=0.2) # Se separan los datos en train y test

    n_features = X_train.shape[1] # Se obtiene la cantidad de features
    model = Sequential() # Se crea el modelo
    model.add(Dense(100, activation='relu', kernel_initializer='he_normal', input_shape=(n_features,))) # Se agrega la capa de entrada
    model.add(Dense(50, activation='relu', kernel_initializer='he_normal')) # Se agrega la capa oculta
    model.add(Dense(1)) # Se agrega la capa de salida
    model.compile(optimizer='adam', loss='mse') # Se compila el modelo
    model.fit(X_train, y_train, epochs=150, batch_size=32, verbose=2) # Se entrena el modelo

    y_pred = model.predict(X_test) # Se obtienen las predicciones

    print('MSE: ', mean_squared_error(y_test, y_pred))
    print('MAE: ', mean_absolute_error(y_test, y_pred))
    print('R2: ', r2_score(y_test, y_pred))

    model.save('subjectScores.h5') # Se guarda el modelo

def predict_subject_score(user):
    user = pd.DataFrame([user] * 92)
    df = pd.read_json('scripts/neuronalNetwork/data_scores.json', encoding='utf-8')
    df.drop(['email'], axis=1, inplace=True)
    df['semester'] = user['semester']
    df['career'] = user['career']
    df['keywords'] = user['keywords']

    scaler = MinMaxScaler()
    df[['semester', 'subject_semester']] = scaler.fit_transform(df[['semester', 'subject_semester']]) # Se normalizan los datos


    career = df['career'][0]
    df = df.drop(['career'], axis=1) # Se elimina la columna de la carrera
    df['career_Administración de Empresas'] = 1 if career == 'Administración de Empresas' else 0
    df['career_Construcción'] = 1 if career == 'Construcción' else 0
    df['career_Contaduría'] = 1 if career == 'Contaduría' else 0
    df['career_Ingeniería de Alimentos'] = 1 if career == 'Ingeniería de Alimentos' else 0
    df['career_Ingeniería de Sistemas'] = 1 if career == 'Ingeniería de Sistemas' else 0
    df['career_Nutrición y Dietética'] = 1 if career == 'Nutrición y Dietética' else 0
    df['career_Tecnología en Desarrollo de Software'] = 1 if career == 'Tecnología en Desarrollo de Software' else 0
    df['career_Tecnología en Electrónica'] = 1 if career == 'Tecnología en Electrónica' else 0
    df['career_Trabajo social'] = 1 if career == 'Trabajo social' else 0

    mlb = MultiLabelBinarizer()
    subject_career_one_hot = mlb.fit_transform(df['subject_career'].str.split(', ')) # Se convierte la materia en one hot
    subject_career_columns = mlb.classes_
    subject_career_df = pd.DataFrame(subject_career_one_hot, columns=subject_career_columns) # Se crea un dataframe con las columnas de la materia
    df = pd.concat([df, subject_career_df], axis=1) # Se agrega el dataframe de la materia al dataframe principal
    df = df.drop(['subject_career'], axis=1) # Se elimina la columna de la materia

    df['keywords'] = [list (filter(lambda x: isinstance(x,str) and x not in STOP_WORDS , y)) for y in df['keywords']] # Se eliminan las palabras vacias
    vectorizer = TfidfVectorizer(lowercase=True)
    tfidf_key_words = vectorizer.fit_transform(df['keywords'].apply(lambda x: ' '.join(x))) # Se convierten las palabras clave en tfidf
    df['keywords'] = np.array(tfidf_key_words.toarray()) # Se agrega la columna de tfidf al dataframe principal

    label_encoder = LabelEncoder()
    label_subject = label_encoder.fit_transform(df['subject']) # Se convierte la materia en un label
    df = df.drop(['subject'], axis=1) # Se elimina la columna de la materia
    df['subject'] = label_subject # Se agrega la columna de label al dataframe principal

    model = keras.models.load_model('scripts/neuronalNetwork/subjectScores.h5') # Se carga el modelo
    prediction = model.predict(df) # Se obtiene la prediccion

    return prediction

user_pred_subject = {
    "career": "Ingeniería de Sistemas",
    "semester": 7,
    "keywords": [
        "python",
        "java",
        "Programación"
        "Objetos",
        "Análisis"
    ]
  }

