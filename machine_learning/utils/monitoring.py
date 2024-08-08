"""
Helper function to execute the performance reports and Test Suites, using Evidently AI library
"""
import os
from typing import List
from datetime import datetime
import pandas as pd

from evidently import ColumnMapping
from evidently.report import Report
from evidently.metric_preset import DataDriftPreset, DataQualityPreset, TargetDriftPreset

from evidently.test_suite import TestSuite
from evidently.test_preset import DataDriftTestPreset, NoTargetPerformanceTestPreset

def prepare_current_data(df: pd.DataFrame, cols_to_drop: List):
    """
    Prepare and remove columns from the dataset to be used for reporting
    """
    # Check the columns to included in the df
    actual_cols_to_drop= [col for col in cols_to_drop if col in df.columns]
    # Drop the columns
    df= df.drop(columns=actual_cols_to_drop)
    
    return df

def create_summary_report(report_date: datetime, reference: pd.DataFrame, data_sample: pd.DataFrame, 
                  col_mapping: ColumnMapping, tmp_folder: str = '/tmp/reports'):
    """
    Create a Data Quality report and save it to disk
    """
    summary_report = Report(
        metrics=[
                DataQualityPreset()        
                ],
        timestamp= report_date,
    )

    summary_report.run(reference_data=reference, current_data=data_sample, column_mapping=col_mapping)
    report_filename=os.path.join(tmp_folder,f"summary_report_{report_date.strftime('%Y%m%d%H%M%S')}.json")
    
    summary_report.save(report_filename)
    
    return report_filename

def create_data_drift_report(report_date: datetime, reference: pd.DataFrame, data_sample: pd.DataFrame, 
                  col_mapping: ColumnMapping, tmp_folder: str = '/tmp/reports'):
    """
    Create a Data Drift report and save it to disk
    """
    
    data_drift_report = Report(
        metrics=[
                DataDriftPreset()        
                ],
        timestamp= report_date,
    )

    data_drift_report.run(reference_data=reference, current_data=data_sample, column_mapping=col_mapping)
    report_filename=os.path.join(tmp_folder,f"data_drift_report_{report_date.strftime('%Y%m%d%H%M%S')}.json")
    data_drift_report.save(report_filename)
    
    return report_filename

def create_prediction_drift_report(report_date: datetime, reference: pd.DataFrame, data_sample: pd.DataFrame, 
                  col_mapping: ColumnMapping, tmp_folder: str = '/tmp/reports'):
    """
    Create a Prediction Drift report and save it to disk
    """

    pred_drift_report = Report(
        metrics=[
                TargetDriftPreset()
                ],
        timestamp= report_date,
    )

    pred_drift_report.run(reference_data=reference, current_data=data_sample, column_mapping=col_mapping)
    report_filename=os.path.join(tmp_folder,f"pred_drift_report_{report_date.strftime('%Y%m%d%H%M%S')}.json")
    pred_drift_report.save(report_filename)
    
    return report_filename

def create_test_suite(report_date: datetime, reference: pd.DataFrame, data_sample: pd.DataFrame, 
                  col_mapping: ColumnMapping):
    """
    Create and run the Test Suite and return it
    """
    
    test_suite = TestSuite(
        tests=[DataDriftTestPreset(),
               NoTargetPerformanceTestPreset(),
               ],
        timestamp=report_date,
    )

    test_suite.run(reference_data=reference, current_data=data_sample, column_mapping=col_mapping)
    
    return test_suite

def check_test_failures(test_json: dict):
    """
    Check which tests have failed and return true if any of the most impactful are included
    """
    failure= False
    for test in test_json['tests']:
        if test['status']!= 'SUCCESS':
            # if more than 30% drifted columns
            if test['name']=='Share of Drifted Columns':
                failure=True
            # if prediction is a drifted column
            elif (test['name']=='Drift per Column') and (test['parameters']['column_name']=='prediction'):
                failure=True
            # AvgSessionDurationMinutes and SessionsPerWeek have a strong correlation/influence
            # if AvgSessionDurationMinutes is a drifted column                
            elif (test['name']=='Drift per Column') and (test['parameters']['column_name']=='AvgSessionDurationMinutes'):
                failure=True
            # if SessionsPerWeek is a drifted column                                
            elif (test['name']=='Drift per Column') and (test['parameters']['column_name']=='SessionsPerWeek'):
                failure=True
    
    return failure

def get_num_features(df: pd.DataFrame):
    """
    Return the list of numerical columns
    """
    num_features = df.select_dtypes(exclude=['category','object']).columns.tolist()
    
    return num_features

def get_cat_features(df: pd.DataFrame):
    """
    Return the list of categorical columns
    """
    cat_features = df.select_dtypes(include=['category','object']).columns.tolist()
    
    return cat_features

def get_column_mapping(data: pd.DataFrame, prediction_col: str, label_col: str = None):
    """
    Create and return the Column Mapping object for the reports and tests
    """
    # Define Column Mapping
    num_features = get_num_features(data)
    cat_features = get_cat_features(data)
    
    column_mapping = ColumnMapping(
        prediction=prediction_col,
        numerical_features=num_features,
        categorical_features=cat_features,
        target=label_col
    )    
    
    return column_mapping

def create_reports(report_date, ref_data, curr_data, prediction_col, label_col= None):
    """
    Run all the reports and save them to temporary disk
    """
    # Create the directory
    temp_folder='/tmp/reports'
    os.makedirs(temp_folder, exist_ok=True)
    
    column_mapping= get_column_mapping(curr_data, prediction_col, label_col)
    # Create the Summary or Data Quality report
    print("Creating Summary report")
    summary_report= create_summary_report(report_date, ref_data, curr_data, 
                  column_mapping)
    # Create the Summary or Data Quality report
    print("Creating Data Drift report")
    data_drift_report= create_data_drift_report(report_date, ref_data, curr_data, 
                  column_mapping)

    # Create the Summary or Data Quality report
    print("Creating Prediction Drift report")
    pred_drift_report= create_prediction_drift_report(report_date, ref_data, curr_data, 
                  column_mapping)

    return summary_report, data_drift_report, pred_drift_report