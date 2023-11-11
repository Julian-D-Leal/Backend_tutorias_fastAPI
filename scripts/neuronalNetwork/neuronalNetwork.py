import os
import numpy as np
import pandas as pd
import spacy
from keras.models import Sequential
from keras.layers import Dense
from tensorflow import keras
from sklearn.preprocessing import MinMaxScaler, OneHotEncoder, MultiLabelBinarizer, LabelEncoder, StandardScaler
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score, mean_absolute_error
from spacy.lang.es.stop_words import STOP_WORDS

def neuronal_network_tutors():
    df = pd.read_json('scripts/neuronalNetwork/tutorScores.json', encoding='utf-8')
    df.drop(['student_email'], axis=1, inplace=True)

    # Se verifica si se le dio click al tutor
    tutors_clicks = [tutors for tutors in df['clicks']]
    clicks = []
    for i in range (len(tutors_clicks)):
        clicks.append(1 if df['tutor_email'][i] in tutors_clicks[i] else 0)
    df['clicks'] = clicks

    # Se elimina el email del tutor
    df.drop(['tutor_email'], axis=1, inplace=True)

    # Se crean las columnas de los horarios
    availability_matrix = []
    for availability in df['student_availability']:
        student_availability_matrix = [[0] * 13 for _ in range(6)]
        for slot in availability:
            day,hour = slot
            student_availability_matrix[day][hour] = 1
        availability_matrix.append(student_availability_matrix)
    availability_df = pd.DataFrame(availability_matrix)
    availability_df = availability_df.apply(lambda x: pd.Series(x[0]), axis=1)
    df = pd.concat([df, availability_df], axis=1)
    df = df.drop('student_availability', axis=1)

    availability_matrix = []
    for availability in df['tutor_availability']:
        tutor_availability_matrix = [[0] * 13 for _ in range(6)]
        for slot in availability:
            day,hour = slot
            tutor_availability_matrix[day][hour] = 1
        availability_matrix.append(tutor_availability_matrix)
    availability_df = availability_df.apply(lambda x: pd.Series(x[0]), axis=1)
    df = pd.concat([df, availability_df], axis=1)
    df = df.drop('tutor_availability', axis=1)

    # Se hacen los dummies del formato
    mlb = MultiLabelBinarizer()
    format_flatten = [", ".join(format) for format in df['format']]
    df['format'] = format_flatten
    format_matrix = mlb.fit_transform(df['format'].str.split(', '))
    format_columns = mlb.classes_
    format_df = pd.DataFrame(format_matrix, columns=format_columns)
    df = pd.concat([df, format_df], axis=1)
    df.drop(['format'], axis=1, inplace=True)

    format_flatten = [", ".join(format) for format in df['tutor_format']]
    df['tutor_format'] = format_flatten
    format_matrix = mlb.fit_transform(df['tutor_format'].str.split(', '))
    format_columns = ['tutor_' + column for column in mlb.classes_]
    format_df = pd.DataFrame(format_matrix, columns=format_columns)
    df = pd.concat([df, format_df], axis=1)
    df.drop(['tutor_format'], axis=1, inplace=True)

    # Se hacen los dummies de los metodos
    format_flatten = [", ".join(method) for method in df['method']]
    df['method'] = format_flatten
    format_matrix = mlb.fit_transform(df['method'].str.split(', '))
    format_columns = mlb.classes_
    format_df = pd.DataFrame(format_matrix, columns=format_columns)
    df = pd.concat([df, format_df], axis=1)
    df.drop(['method'], axis=1, inplace=True)

    format_flatten = [", ".join(method) for method in df['tutor_method']]
    df['tutor_method'] = format_flatten
    format_matrix = mlb.fit_transform(df['tutor_method'].str.split(', '))
    format_columns = ['tutor_' + column for column in mlb.classes_]
    format_df = pd.DataFrame(format_matrix, columns=format_columns)
    df = pd.concat([df, format_df], axis=1)
    df.drop(['tutor_method'], axis=1, inplace=True)

    # Se hacen los dummies de los tipos de grupo
    format_flatten = [", ".join(type_group) for type_group in df['type_group']]
    df['type_group'] = format_flatten
    format_matrix = mlb.fit_transform(df['type_group'].str.split(', '))
    format_columns = mlb.classes_
    format_df = pd.DataFrame(format_matrix, columns=format_columns)
    df = pd.concat([df, format_df], axis=1)
    df.drop(['type_group'], axis=1, inplace=True)

    format_flatten = [", ".join(type_group) for type_group in df['tutor_type_group']]
    df['tutor_type_group'] = format_flatten
    format_matrix = mlb.fit_transform(df['tutor_type_group'].str.split(', '))
    format_columns = ['tutor_' + column for column in mlb.classes_]
    format_df = pd.DataFrame(format_matrix, columns=format_columns)
    df = pd.concat([df, format_df], axis=1)
    df.drop(['tutor_type_group'], axis=1, inplace=True)

    # Se escala el presupuesto, el precio del tutor y la opinion del tutor
    scaler = MinMaxScaler()
    df['budget'] = scaler.fit_transform(df['budget'].values.reshape(-1, 1))
    df['tutor_cost'] = scaler.fit_transform(df['tutor_cost'].values.reshape(-1, 1))
    df['tutor_opinion'] = scaler.fit_transform(df['tutor_opinion'].values.reshape(-1, 1))

    # Se escala el score
    scaler = StandardScaler()
    df['score'] = scaler.fit_transform(df['score'].values.reshape(-1, 1))

    # Se se separa los inputs y el output
    x = df.drop(['score'], axis=1)
    y = df['score']

    # Se separan los datos en train y test
    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=42)

    # Se crea el modelo
    n_features = x_train.shape[1]
    model = Sequential()
    model.add(Dense(400, activation='relu', kernel_initializer='he_normal', input_shape=(n_features,)))
    model.add(Dense(200, activation='relu', kernel_initializer='he_normal'))
    model.add(Dense(100, activation='relu', kernel_initializer='he_normal'))
    model.add(Dense(1))
    model.compile(optimizer='adam', loss='mse')
    model.fit(x_train, y_train, epochs=200, batch_size=32, verbose=2)

    # Se obtienen las predicciones
    y_pred = model.predict(x_test)

    print('MSE: ', mean_squared_error(y_test, y_pred))
    print('MAE: ', mean_absolute_error(y_test, y_pred))
    print('R2: ', r2_score(y_test, y_pred))

    # Se guarda el modelo
    model.save('model_tutor.h5')

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

    model.save('model_subject.h5') # Se guarda el modelo

def predict_subject_score(user):
    user = pd.DataFrame([user] * 92)
    df = pd.read_json('scripts/neuronalNetwork/subjects.json', encoding='utf-8')
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
    # vectorizer = TfidfVectorizer(lowercase=True)
    # tfidf_key_words = vectorizer.fit_transform(df['keywords'].apply(lambda x: ' '.join(x))) # Se convierten las palabras clave en tfidf
    # df['keywords'] = np.array(tfidf_key_words.toarray()) # Se agrega la columna de tfidf al dataframe principal
    nlp = spacy.load("es_core_news_lg")
    vectores = [nlp(' '.join(keywords)).vector_norm for keywords in df['keywords']]
    vectores = np.array(vectores)
    scaler = StandardScaler()
    vectores = scaler.fit_transform(vectores.reshape(-1, 1))
    df['keywords'] = vectores

    label_encoder = LabelEncoder()
    label_subject = label_encoder.fit_transform(df['subject']) # Se convierte la materia en un label
    df = df.drop(['subject'], axis=1) # Se elimina la columna de la materia
    df['subject'] = label_subject # Se agrega la columna de label al dataframe principal

    model = keras.models.load_model('scripts/neuronalNetwork/model_subject.h5') # Se carga el modelo
    prediction = model.predict(df) # Se obtiene la prediccion

    json_output = pd.read_json('scripts/neuronalNetwork/subjects.json', encoding='utf-8')
    json_output['score'] = prediction
    json_output.drop(['subject_career'], axis=1, inplace=True)
    json_output.drop(['subject_semester'], axis=1, inplace=True)

    output_array = sorted([(subject,score) for subject,score in zip(json_output['subject'], json_output['score'])], key=lambda x: x[1], reverse=True)

    return output_array

def predict_tutor_score(user,tutors):
    # with open('scripts/createUsers/users.json','r',encoding='utf-8') as f:
    #     users = json.load(f)
    # tutors = [user for user in users if user['is_tutor'] == True]
    df = pd.DataFrame(tutors)
    user = pd.DataFrame([user] * len(df))

    emails = df['email']
    subjects = df['subjects_tutor']

    df.drop(['name'], axis=1, inplace=True)
    df.drop(['password'], axis=1, inplace=True)
    df.drop(['is_tutor'], axis=1, inplace=True)
    df.drop(['is_student'], axis=1, inplace=True)
    df.drop(['type_tutor'], axis=1, inplace=True)
    df.drop(['subjects_tutor'], axis=1, inplace=True)

    opinions = [sum(x['calification_tutor'] for x in tutor['tutor_opinions']) / len(tutor['tutor_opinions']) if tutor['tutor_opinions'] is not None else 0 for tutor in tutors]
    # opinions = [sum(x['calification_tutor'] for x in tutor['tutor_opinions']) / len(tutor['tutor_opinions']) for tutor in tutors]
    df.drop(['tutor_opinions'], axis=1, inplace=True)
    df['tutor_opinions'] = [1 - abs(opinion-5)/5 for opinion in opinions]

    df['student_availability'] = user['student_availability']
    df['format'] = user['format']
    df['budget'] = user['budget']
    df['method'] = user['method']
    df['type_group'] = user['type_group']
    df['clicks'] = user['clicks']
    new_order = ['email', 'student_availability', 'format', 'budget', 'method', 'type_group', 'clicks', 'availability', 'format_tutor', 'cost_tutor', 'method_tutor', 'type_group_tutor', 'tutor_opinions']
    df = df[new_order]
    
    tutors_clicks = [tutors for tutors in df['clicks']]
    clicks = []
    for i in range (len(tutors_clicks)):
        clicks.append(1 if df['email'][i] in tutors_clicks[i] else 0)
    df['clicks'] = clicks

    df.drop(['email'], axis=1, inplace=True)

    columumns = []
    for i in range(6):
        for j in range(13):
            columumns.append(str(i)+'-'+str(j))

    df['student_availability'] = df['student_availability'].apply(lambda x: [[x['day'], x['hour']] for x in x])
    availability_matrix = []
    for availability in df['student_availability']:
        student_availability_matrix = [0] * 78
        for slot in availability:
            day,hour = slot
            student_availability_matrix[day*13+hour] = 1
        availability_matrix.append(student_availability_matrix)
    availability_df = pd.DataFrame(availability_matrix, columns=columumns)

    # Concatenate the original DataFrame with the availability DataFrame
    df = pd.concat([df, availability_df], axis=1)
    df.drop(['student_availability'], axis=1, inplace=True)

    columumns = []
    for i in range(6):
        for j in range(13):
            columumns.append("tutor_"+str(i)+'-'+str(j))

    df['availability'] = df['availability'].apply(lambda x: [[x['day'], x['hour']] for x in x])

    availability_matrix = []
    for availability in df['availability']:
        tutor_availability_matrix = [0] * 78
        for slot in availability:
            day,hour = slot
            tutor_availability_matrix[day*13+hour] = 1
        availability_matrix.append(tutor_availability_matrix)
    availability_df = pd.DataFrame(availability_matrix, columns=columumns)
    # Concatenate the original DataFrame with the availability DataFrame
    df = pd.concat([df, availability_df], axis=1)
    df.drop(['availability'], axis=1, inplace=True)
    
    mlb = MultiLabelBinarizer()
    # format_flatten = [", ".join(format) for format in df['format']]
    # df['format'] = format_flatten
    # format_matrix = mlb.fit_transform(df['format'].str.split(', '))
    # format_columns = mlb.classes_
    # format_df = pd.DataFrame(format_matrix, columns=format_columns)
    # df = pd.concat([df, format_df], axis=1)
    # df.drop(['format'], axis=1, inplace=True)
    format_student = df['format'][0]
    df.drop(['format'], axis=1, inplace=True)
    df['Presencial'] = 1 if 'Presencial' in format_student else 0
    df['Virtual'] = 1 if 'Virtual' in format_student else 0

    format_flatten = [", ".join(format) for format in df['format_tutor']]
    df['format_tutor'] = format_flatten
    format_matrix = mlb.fit_transform(df['format_tutor'].str.split(', '))
    format_columns = ['tutor_' + column for column in mlb.classes_]
    format_df = pd.DataFrame(format_matrix, columns=format_columns)
    df = pd.concat([df, format_df], axis=1)
    df.drop(['format_tutor'], axis=1, inplace=True)

    scaler = MinMaxScaler()
    df['budget'] = scaler.fit_transform(df['budget'].values.reshape(-1, 1))

    df['cost_tutor'] = scaler.fit_transform(df['cost_tutor'].values.reshape(-1, 1))

    # format_flatten = [", ".join(method) for method in df['method']]
    # df['method'] = format_flatten
    # format_matrix = mlb.fit_transform(df['method'].str.split(', '))
    # format_columns = mlb.classes_
    # format_df = pd.DataFrame(format_matrix, columns=format_columns)
    # df = pd.concat([df, format_df], axis=1)
    # df.drop(['method'], axis=1, inplace=True)
    format_student = df['method'][0]
    df.drop(['method'], axis=1, inplace=True)
    df['Aprendizaje Activo'] = 1 if 'Aprendizaje activo' in format_student else 0
    df['Aprendizaje Auditivo'] = 1 if 'Aprendizaje auditivo' in format_student else 0
    df['Aprendizaje Kinestésico'] = 1 if 'Aprendizaje kinestésico' in format_student else 0
    df['Aprendizaje Pragmático'] = 1 if 'Aprendizaje pragmático' in format_student else 0
    df['Aprendizaje Reflexivo'] = 1 if 'Aprendizaje reflexivo' in format_student else 0
    df['Aprendizaje Teórico'] = 1 if 'Aprendizaje teórico' in format_student else 0
    df['Aprendizaje Visual'] = 1 if 'Aprendizaje visual' in format_student else 0
    

    format_flatten = [", ".join(method) for method in df['method_tutor']]
    df['method_tutor'] = format_flatten
    format_matrix = mlb.fit_transform(df['method_tutor'].str.split(', '))
    format_columns = ['tutor_' + column for column in mlb.classes_]
    format_df = pd.DataFrame(format_matrix, columns=format_columns)
    df = pd.concat([df, format_df], axis=1)
    df.drop(['method_tutor'], axis=1, inplace=True)

    # format_flatten = [", ".join(type_group) for type_group in df['type_group']]
    # df['type_group'] = format_flatten
    # format_matrix = mlb.fit_transform(df['type_group'].str.split(', '))
    # format_columns = mlb.classes_
    # format_df = pd.DataFrame(format_matrix, columns=format_columns)
    # df = pd.concat([df, format_df], axis=1)
    # df.drop(['type_group'], axis=1, inplace=True)
    format_student = df['type_group'][0]
    df.drop(['type_group'], axis=1, inplace=True)
    df['Grupal'] = 1 if 'Grupal' in format_student else 0
    df['Individual'] = 1 if 'Individual' in format_student else 0

    format_flatten = [", ".join(type_group) for type_group in df['type_group_tutor']]
    df['type_group_tutor'] = format_flatten
    format_matrix = mlb.fit_transform(df['type_group_tutor'].str.split(', '))
    format_columns = ['tutor_' + column for column in mlb.classes_]
    format_df = pd.DataFrame(format_matrix, columns=format_columns)
    df = pd.concat([df, format_df], axis=1)
    df.drop(['type_group_tutor'], axis=1, inplace=True)

    df['tutor_opinions'] = scaler.fit_transform(df['tutor_opinions'].values.reshape(-1, 1))

    model = keras.models.load_model('scripts/neuronalNetwork/model_tutor.h5')
    prediction = model.predict(df)

    output = zip(emails, prediction, subjects)
    output_sorted = sorted(output, key=lambda x: x[1], reverse=True)

    return output_sorted

user_pred_subject = {
    "career": "Ingeniería de Sistemas",
    "semester": 1,
    "keywords": []
  }

user_pred_tutor = {
    "student_availability": [
      [
        0,
        0
      ],
      [
        0,
        1
      ],
      [
        0,
        2
      ],
      [
        0,
        3
      ]
    ],
    "format": [
      "Presencial"
    ],
    "budget":20000,
    "method": [
      "Aprendizaje Teórico",
      "Aprendizaje Auditivo"
    ],
    "type_group": [
        "Individual"
    ],
    "clicks":['solmayoralpeña@gmail.com']
  }

def recommendation(subject_score, tutor_score):
    import tensorflow as tf
    os.environ['CUDA_VISIBLE_DEVICES'] = '-1'

    if tf.test.gpu_device_name():
        print('GPU found')
    else:
        print("No GPU found")

    # with tf.device('/CPU:0'):
    #     a = tf.constant([[1.0, 2.0, 3.0], [4.0, 5.0, 6.0]])
    #     b = tf.constant([[1.0, 2.0], [3.0, 4.0], [5.0, 6.0]])

    emails = [tutor[0] for tutor in tutor_score]
    scores = [tutor[1][0] for tutor in tutor_score]
    subjects = [tutor[2] for tutor in tutor_score]
    subject_score = [(subject[0], subject[1]) for subject in subject_score if subject[1] > 0.1]
    subjects_score = [0] * len(emails)

    for subject in subject_score:
        for i in range(len(emails)):
            score_aux = 0
            for j in range(len(subjects[i])):
                if subject[0] == subjects[i][j]:
                    score_aux += subject[1]
            subjects_score[i] += score_aux
    subjects_score = [score for i,score in enumerate(subjects_score)]
    total_score = [scores[i]*0.5 + subjects_score[i]*0.5 for i in range(len(emails))]
    return sorted(zip(emails, total_score), key=lambda x: x[1], reverse=True)[0:10]