from datetime import datetime
import pandas as pd
import os

from evidently import ColumnMapping
from evidently.report import Report
from evidently.metric_preset import DataDriftPreset, DataQualityPreset, TargetDriftPreset

from evidently.test_suite import TestSuite
from evidently.test_preset import DataDriftTestPreset, NoTargetPerformanceTestPreset

def create_summary_report(report_date: datetime, reference: pd.DataFrame, data_sample: pd.DataFrame, 
                  col_mapping: ColumnMapping, tmp_folder: str = '/tmp/reports'):
    
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
    
    test_suite = TestSuite(
        tests=[DataDriftTestPreset(),
               NoTargetPerformanceTestPreset(),
               ],
        timestamp=report_date,
    )

    test_suite.run(reference_data=reference, current_data=data_sample, column_mapping=col_mapping)
    
    return test_suite

def check_test_failures(test_json: dict):
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
    num_features = df.select_dtypes(exclude=['category','object']).columns.tolist()
    
    return num_features

def get_cat_features(df: pd.DataFrame):
    cat_features = df.select_dtypes(include=['category','object']).columns.tolist()
    
    return cat_features

def get_column_mapping(data: pd.DataFrame, prediction_col: str, label_col: str = None):
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
    
    # Create the directory
    temp_folder='/tmp/reports'
    os.makedirs(temp_folder, exist_ok=True)
    
    column_mapping= get_column_mapping(curr_data, prediction_col)
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