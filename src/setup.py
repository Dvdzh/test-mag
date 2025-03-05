import pandas as pd
import sqlite3
from datetime import datetime
import os
import sqlite3
import pandas as pd

import os
# def create_database():
#     """Crée la base de données SQLite et les tables nécessaires"""
#     conn = sqlite3.connect('../data/database.db')
#     cursor = conn.cursor()

#     # Création des tables
#     cursor.execute('''
#     CREATE TABLE IF NOT EXISTS congestion (
#         Date DATE,
#         Node1 TEXT,
#         Node2 TEXT,
#         Congestion FLOAT,
#         PRIMARY KEY (Date, Node1, Node2)
#     )
#     ''')

#     conn.commit()
#     return conn, cursor

# def load_data(file_path):
#     """Charge les données depuis le fichier CSV"""
#     print(f"Chargement des données depuis {file_path}...")
#     df = pd.read_csv(file_path)
#     return df

# def process_data(df):
#     """Traite les données selon les besoins"""
#     print("Traitement des données...")
    
#     # Conversion de la colonne Date
#     df['Date'] = pd.to_datetime(df['Date'])
    
#     # Renommage des colonnes si nécessaire
#     if 'Source' in df.columns:
#         df = df.rename(columns={'Source': 'Node1', 'Sink': 'Node2'})
    
#     return df

# def insert_data(conn, cursor, df):
#     """Insère les données dans la base SQLite"""
#     print("Insertion des données dans la base...")
    
#     # Préparation des données pour l'insertion
#     data_to_insert = df.to_dict('records')
    
#     # Insertion avec gestion des doublons
#     for record in data_to_insert:
#         cursor.execute('''
#         INSERT OR REPLACE INTO congestion (Date, Node1, Node2, Congestion)
#         VALUES (?, ?, ?, ?)
#         ''', (record['Date'], record['Node1'], record['Node2'], record['Congestion']))
    
#     conn.commit()
#     print("Données insérées avec succès")

def main():
    """Fonction principale d'initialisation"""
    print("Démarrage de l'initialisation des données...")
    
    print("Running src/setup.py")
    # check if there is a csv file in the data folder
    if all([not file.endswith('.csv') for file in os.listdir('data')]):
        print('Unzipping Archive.zip')
        os.system('unzip data/Archive.zip -d data/')
    else:
        print('Archive.zip already unzipped')

    # Create the database if it doesn't exist
    conn = sqlite3.connect('data/database.db')
    cursor = conn.cursor()

    date_name_dict = dict(
        NODES_CONGESTION_HOURLY='Date',
        BINDING_CONSTRAINTS_HOURLY='Interval',
    )
        
    # Read all csv files in the data folder
    for file in os.listdir('data'):
        if file.endswith('HOURLY.csv'):
            df = pd.read_csv(f'data/{file}')

            # convert date to datetime
            date_name = date_name_dict[file.split('.')[0]]
            df[date_name] = pd.to_datetime(df[date_name])

            df.to_sql(
                name=file.split('.')[0],
                con=conn,
                if_exists='replace',
                index=False
            )
            print(f'{file} has been added to the database')


if __name__ == "__main__":
    main() 