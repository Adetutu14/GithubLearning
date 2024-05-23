import os
from datetime import datetime
#import re
import pandas as pd
from sqlalchemy import create_engine
import ast # Abstract syntax tree used for obtaining actual python objects from string
from dotenv import dotenv_values
dotenv_values()

def get_database_conn():
    # Get database credentials from environment variable
    config = dict(dotenv_values('.env'))
    print(config)
    # db_user_name = config.get('DB_USER_NAME')
    # db_password = config.get('DB_PASSWORD')
    # db_name = config.get('DB_NAME')
    # port = config.get('PORT')
    # host = config.get('HOST')
    # # Create and return a postgresql database connection object
    # return create_engine(f'postgresql+psycopg2://{db_user_name}:{db_password}@{host}:{port}/{db_name}')

get_database_conn()

###  Data Extraction layer
def extract_data():
    log_extract_data = []
    # DeclareS the json's dictionary confirmed 12 keys for locating values
    log_keys = ["event_date", "event_timestamp", "event_name", "event_params", "event_server_timestamp_offset", "user_pseudo_id", "user_properties", "user_first_touch_timestamp", "mobile_os_hardware_model", "language", "time_zone_offset_seconds", "version"]
    with open('logs/application_logs.json', 'r') as log_file:
        for line in log_file:
            log_data = ast.literal_eval(line) # use for converting string to valid dict/lis/tuple etc
            event_date = log_data.get('event_date')
            event_date = datetime.strptime(event_date, '%Y%m%d')
            user_id = log_data.get('user_pseudo_id')
            event_name = log_data.get('event_name')
            mobile_os_hardware_model = log_data.get('mobile_os_hardware_model')
            version = log_data.get('version')
            log_extract_data.append([event_date, user_id, event_name, mobile_os_hardware_model, version])
# #     #Copy extracted data to a pandas dataframe
    log_data = pd.DataFrame(log_extract_data, columns=['date', 'user_id', 'event_name', 'mobile_os_type', 'version'])
    # Export data to a CSV file. This is your stanging area
    filename = f'log_data_{datetime.now().strftime("%Y%m%d%H%M%S")}.csv'
    path = f'raw/{filename}'
    if os.path.exists('raw') == False:
        os.mkdir('raw')
        log_data.to_csv(path, index= False) 
        print('Data extracted and written to file')
    else:
        log_data.to_csv(path, index= False)
        print('Data extracted and written to file')

#extract_data()

# # Data transformation layer 
def transform_data():
    # Define a function to convert the date column to a uniform date format
    files = os.listdir('raw')
    for file in files:
        log_data = pd.read_csv(f'raw/{file}')
        log_data['date'] = log_data['date'].apply(lambda x:datetime.strptime(x, '%Y-%m-%d').date())
        log_data.to_csv(f'transformed/{file}', index=False)
    print('Transformed data is now written to a csv file')

    

def load_data():
    db_connection = get_database_conn()
    csv_files = os.listdir('transformed')
    for file in csv_files:
        log_data = pd.read_csv(f'transformed/{file}')
        log_data.to_sql('log_data', con= db_connection, if_exists= 'append', index=False)
    print('Data loaded succesffuly load')


#extract_data()
#transform_data()
# load_data()
