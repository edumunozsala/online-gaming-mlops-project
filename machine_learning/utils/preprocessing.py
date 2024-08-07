"""
Module with helper functions to preprocess the datasets
"""

from io import StringIO, BytesIO
import pandas as pd
import boto3
from sklearn.model_selection import train_test_split

def column_featured(df):
    """
    Prepare the columns ion the dataset for training
    """
    # Preprocessing
    df['InGamePurchases'] = df['InGamePurchases'].map({0:'No',1:'Yes'})
    df['EngagementLevel'] = df['EngagementLevel'].map({'Low':0,'Medium':1,'High':2})

    df = df.astype({'InGamePurchases':'category','GameDifficulty':'category'})

    return df

def column_featured_inference(df):
    """
    Prepare the columns ion the dataset for inference
    """

    # Preprocessing
    df['InGamePurchases'] = df['InGamePurchases'].map({0:'No',1:'Yes'})
    cols_to_drop=[]
    if 'EngagementLevel' in df.columns:
        cols_to_drop.append('EngagementLevel')
    if 'PlayerID' in df.columns:
        cols_to_drop.append('PlayerID')

    if len(cols_to_drop)>0:
        df = df.drop(columns=cols_to_drop)

    df = df.astype({'InGamePurchases':'category','GameDifficulty':'category'})

    return df

def get_numeric_columns(df: pd.DataFrame):
    """
    Return the numeric columns in the Dataframe
    """
    
    # Define the types of columns
    numeric_col = df.select_dtypes(exclude=['category','object']).columns.tolist()

    return numeric_col

def get_categorical_columns(df: pd.DataFrame):
    """
    Return the categorical columns in the Dataframe
    """

    # Define the types of columns
    #categorical_col= ['Gender', 'Location', 'GameGenre', 'InGamePurchases', 'GameDifficulty']
    categorical_col = df.select_dtypes(include=['category','object']).columns.tolist()

    return categorical_col

def split_dataset(df: pd.DataFrame, test_size: float, cols_to_drop: str, label: str):
    """
    split the dataframe into a train and test set based on the args
    """
    
    # Data Splitting

    X = df.drop(columns=cols_to_drop)
    y = df[label]

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=test_size,stratify=y,
                                                        shuffle=True,random_state=42)

    return X_train, y_train, X_test, y_test

def save_csv_to_s3(df: pd.DataFrame, bucket_name: str, prefix: str, s3_file_name: str):
    """
    Save the dataframe as a CSV file in a folder in S3 bucket
    """

    # Save DataFrame to a CSV file in-memory
    csv_buffer = StringIO()
    df.to_csv(csv_buffer, index=False)

    # Upload CSV to S3
    s3_client = boto3.client('s3')
    print("Bucket Name: ",bucket_name)
    print("Folder/File: ",prefix+'/'+s3_file_name)

    # Make sure your bucket and file name are correct
    s3_client.put_object(Bucket=bucket_name, Key=prefix+'/'+s3_file_name, 
                         Body=csv_buffer.getvalue())

    print(f"DataFrame saved to S3 bucket '{bucket_name}' as '{s3_file_name}'")    

def save_json_to_s3(json_filename: str, bucket_name: str, prefix: str, s3_file_name: str):
    """
    Save the json file to a folder in S3 bucket
    """
    
    # Initialize a session using Amazon S3
    s3 = boto3.client('s3')

    # Define the full S3 path
    if prefix.endswith('/'):
        s3_path = prefix + s3_file_name
    else:
        s3_path = prefix + '/' + s3_file_name

    # Upload the JSON string to S3
    s3.upload_file(json_filename, bucket_name, s3_path)

    print(f'File {s3_file_name} uploaded to {bucket_name}/{prefix}')
    
def load_csv_to_s3(bucket_name: str, prefix: str):
    """
    Load a csv file to a S3 bucket
    """
    
    # Initialize a session using Amazon S3
    s3 = boto3.client('s3')


    # List all the .csv files in the specified folder
    response = s3.list_objects_v2(Bucket=bucket_name, Prefix=prefix)
    csv_files = [content['Key'] for content in response.get('Contents', []) 
                 if content['Key'].endswith('.csv')]

    # Initialize an empty list to hold DataFrames
    dataframes = []

    # Download and read each .csv file into a DataFrame
    for csv_file in csv_files:
        # Get the object from S3
        obj = s3.get_object(Bucket=bucket_name, Key=csv_file)
        # Read the file content to a pandas DataFrame
        df = pd.read_csv(BytesIO(obj['Body'].read()))
        # Append the DataFrame to the list
        dataframes.append(df)

    # Concatenate all DataFrames into a single DataFrame
    combined_df = pd.concat(dataframes, ignore_index=True)

    # Display the combined DataFrame
    print(f"DataFrame created from CSV files in S3 bucket '{bucket_name}'")        
    
    return combined_df
