import boto3
import json
import os
from pathlib import Path

from typing import List, Optional, Text

from evidently.metrics import ColumnDriftMetric
from evidently.metrics import DatasetSummaryMetric
from evidently.metrics import DatasetMissingValuesMetric
from evidently.metrics import RegressionQualityMetric
from evidently.ui.dashboards import CounterAgg
from evidently.ui.dashboards import DashboardPanelCounter
from evidently.ui.dashboards import DashboardPanelPlot
from evidently.ui.dashboards import PanelValue
from evidently.ui.dashboards import PlotType
from evidently.ui.workspace import Project
from evidently.ui.dashboards import ReportFilter
from evidently.ui.workspace import Workspace
from evidently.ui.workspace import WorkspaceBase
from evidently.report import Report

def get_evidently_project(
    workspace: WorkspaceBase,
    project_name: Text,
    project_description: Optional[Text] = None
) -> Project:
    """Get Evidently project object (load existing or create new).

    Args:
        workspace (WorkspaceBase): Evidently workspace object.
        project_name (Text): name of a project
        project_description (Optional[Text], optional): Project description. Defaults to None.

    Returns:
        Project: Evidently project object.
    """

    # Search project by name in the workspace
    search_proj_list: List[Project] = workspace.search_project(project_name)

    # Check if project with specified name already exists
    if search_proj_list:
        project: Project = search_proj_list[0]
    # If it does not exit create it
    else:
        project = workspace.create_project(project_name)
        project.description = project_description

    return project


def add_regression_dashboard(project: Project) -> Project:
    """Add (build) model performance (regression) dashboard to specified project.

    Args:
        project (Project): Evidently project object.

    Returns:
        Project: Evidently project object (updated).
    """

    # Regression performance
    project.dashboard.add_panel(
        DashboardPanelCounter(
            filter=ReportFilter(metadata_values={}, tag_values=[]),
            agg=CounterAgg.NONE,
            title="Regression Performance",
        )
    )

    # RegressionQualityMetric ME value panel
    project.dashboard.add_panel(
        DashboardPanelCounter(
            title="ME",
            filter=ReportFilter(metadata_values={}, tag_values=[]),
            value=PanelValue(
                metric_id="RegressionQualityMetric",
                field_path=RegressionQualityMetric.fields.current.mean_error,
                legend="value",
            ),
            text="value",
            agg=CounterAgg.LAST,
            size=1
        )
    )

    # RegressionQualityMetric MAE value panel
    project.dashboard.add_panel(
        DashboardPanelCounter(
            title="MAE",
            filter=ReportFilter(metadata_values={}, tag_values=[]),
            value=PanelValue(
                metric_id="RegressionQualityMetric",
                field_path=RegressionQualityMetric.fields.current.mean_abs_error,
                legend="value",
            ),
            text="value",
            agg=CounterAgg.LAST,
            size=1
        )
    )

    # RegressionQualityMetric aggregated metric (ME, MAE, MAPE) plots
    project.dashboard.add_panel(
        DashboardPanelPlot(
            title="Aggregated metrics in time: ME and MAE",
            filter=ReportFilter(metadata_values={}, tag_values=[]),
            values=[
                PanelValue(
                    metric_id="RegressionQualityMetric",
                    field_path=RegressionQualityMetric.fields.current.mean_error,
                    legend="ME"
                ),
                PanelValue(
                    metric_id="RegressionQualityMetric",
                    field_path=RegressionQualityMetric.fields.current.mean_abs_error,
                    legend="MAE",
                ),
            ],
            plot_type=PlotType.LINE,
        )
    )

    # RegressionQualityMetric MAPE value panel
    project.dashboard.add_panel(
        DashboardPanelCounter(
            title="MAPE",
            filter=ReportFilter(metadata_values={}, tag_values=[]),
            value=PanelValue(
                metric_id="RegressionQualityMetric",
                field_path=RegressionQualityMetric.fields.current.mean_abs_perc_error,
                legend="value",
            ),
            text="value",
            agg=CounterAgg.LAST,
            size=2
        )
    )

    project.dashboard.add_panel(
        DashboardPanelPlot(
            title="Aggregated metrics in time: MAPE",
            filter=ReportFilter(metadata_values={}, tag_values=[]),
            values=[
                PanelValue(
                    metric_id="RegressionQualityMetric",
                    field_path=RegressionQualityMetric.fields.current.mean_abs_perc_error,
                    legend="MAPE",
                ),
            ],
            plot_type=PlotType.LINE,
        )
    )

    return project


def add_target_drift_dashboard(project: Project) -> Project:
    """Add (build) target drift dashboard to specified project.

    Args:
        project (Project): Evidently project object.

    Returns:
        Project: Evidently project object (updated).
    """

    # Title: Target drift
    project.dashboard.add_panel(
        DashboardPanelCounter(
            filter=ReportFilter(metadata_values={}, tag_values=[]),
            agg=CounterAgg.NONE,
            title="Target Drift",
        )
    )

    # Stattest threshold
    project.dashboard.add_panel(
        DashboardPanelCounter(
            title="Stattest Threshold",
            filter=ReportFilter(metadata_values={}, tag_values=[]),
            value=PanelValue(
                metric_id="ColumnDriftMetric",
                field_path=ColumnDriftMetric.fields.stattest_threshold,
                metric_args={"column_name.name": "duration_min"},
                legend="stattest threshold"
            ),
            text="",
            agg=CounterAgg.LAST,
            size=1
        )
    )

    # Row counts
    project.dashboard.add_panel(
        DashboardPanelCounter(
            title="Row counts",
            filter=ReportFilter(metadata_values={}, tag_values=[]),
            value=PanelValue(
                metric_id="DatasetSummaryMetric",
                field_path=DatasetSummaryMetric.fields.current.number_of_rows,
                legend="row counts"
            ),
            text="",
            agg=CounterAgg.LAST,
            size=1
        )
    )

    # Target drift bar and histogram plots
    project.dashboard.add_panel(
        DashboardPanelPlot(
            title="Target: Wasserstein drift distance",
            filter=ReportFilter(metadata_values={}, tag_values=[]),
            values=[
                PanelValue(
                    metric_id="ColumnDriftMetric",
                    metric_args={"column_name.name": "duration_min"},
                    field_path=ColumnDriftMetric.fields.drift_detected,
                    legend="drift detected",
                ),
            ],
            plot_type=PlotType.BAR,
            size=2
        )
    )

    # Target drift score plot
    project.dashboard.add_panel(
        DashboardPanelPlot(
            title="Drift Score",
            filter=ReportFilter(metadata_values={}, tag_values=[]),
            values=[
                PanelValue(
                    metric_id="ColumnDriftMetric",
                    metric_args={"column_name.name": "duration_min"},
                    field_path=ColumnDriftMetric.fields.drift_score,
                    legend="drift score",
                ),
            ],
            plot_type=PlotType.LINE,
            size=2
        )
    )

    return project


def add_data_quality_dashboard(project: Project) -> Project:
    """Add (build) data quality dashboard to specified project.

    Args:
        project (Project): Evidently project object.

    Returns:
        Project: Evidently project object (updated).
    """

    # Title: Data Quality
    project.dashboard.add_panel(
        DashboardPanelCounter(
            filter=ReportFilter(metadata_values={}, tag_values=[]),
            agg=CounterAgg.NONE,
            title="Data Quality",
        )
    )

    # Counter: Share of Drifted Features
    project.dashboard.add_panel(
        DashboardPanelCounter(
            title="Share of Drifted Features",
            filter=ReportFilter(metadata_values={}, tag_values=[]),
            value=PanelValue(
                metric_id="DatasetDriftMetric",
                field_path="share_of_drifted_columns",
                legend="share",
            ),
            text="share",
            agg=CounterAgg.LAST,
            size=1,
        )
    )

    # Counter: Number of Columns
    project.dashboard.add_panel(
        DashboardPanelCounter(
            title="Inference Count",
            filter=ReportFilter(metadata_values={}, tag_values=[]),
            value=PanelValue(
                metric_id="DatasetSummaryMetric",
                field_path="current.number_of_rows",
                legend="Count",
            ),
            text="Inferences",
            agg=CounterAgg.LAST,
            size=1,
        )
    )

    # Plot: Predictions drift score - BAR
    project.dashboard.add_panel(
        DashboardPanelPlot(
            title="Sessions per Week",
            filter=ReportFilter(metadata_values={}, tag_values=[]),
            values=[
                PanelValue(
                    metric_id="ColumnSummaryMetric",
                    field_path="current_characteristics.p25",
                    metric_args={"column_name.name": "SessionsPerWeek"},
                    legend="p25",
                ),
                PanelValue(
                    metric_id="ColumnSummaryMetric",
                    field_path="current_characteristics.p50",
                    metric_args={"column_name.name": "SessionsPerWeek"},
                    legend="p50",
                ),
                PanelValue(
                    metric_id="ColumnSummaryMetric",
                    field_path="current_characteristics.p75",
                    metric_args={"column_name.name": "SessionsPerWeek"},
                    legend="p75",
                ),                
            ],
            plot_type=PlotType.LINE,
            size=1,
        )
    )

    # Plot: Predictions drift score - BAR
    project.dashboard.add_panel(
        DashboardPanelPlot(
            title="Avg Session Duration (min)",
            filter=ReportFilter(metadata_values={}, tag_values=[]),
            values=[
                PanelValue(
                    metric_id="ColumnSummaryMetric",
                    field_path="current_characteristics.p25",
                    metric_args={"column_name.name": "AvgSessionDurationMinutes"},
                    legend="p25",
                ),
                PanelValue(
                    metric_id="ColumnSummaryMetric",
                    field_path="current_characteristics.p50",
                    metric_args={"column_name.name": "AvgSessionDurationMinutes"},
                    legend="p50",
                ),
                PanelValue(
                    metric_id="ColumnSummaryMetric",
                    field_path="current_characteristics.p75",
                    metric_args={"column_name.name": "AvgSessionDurationMinutes"},
                    legend="p75",
                ),                
            ],
            plot_type=PlotType.LINE,
            size=1,
        )
    )

    # Plot: Dataset Quality
    project.dashboard.add_panel(
        DashboardPanelPlot(
            filter=ReportFilter(metadata_values={}, tag_values=[]),
            title="Number of Missing Values and Duplicate Rows",
            values=[
                PanelValue(
                    metric_id="DatasetSummaryMetric",
                    field_path="current.number_of_missing_values",
                    legend="Missing Values"
                ),
                PanelValue(
                    metric_id="DatasetSummaryMetric",
                    field_path="current.number_of_duplicated_rows",
                    legend="Duplicate Rows"
                ),
            ],
            plot_type=PlotType.LINE,
            size=1,
        ),
    )

    return project


def add_predictions_drift_dashboard(project: Project) -> Project:
    """Add (build) predictions drift dashboard to specified project.

    Args:
        project (Project): Evidently project object.

    Returns:
        Project: Evidently project object (updated).
    """

    # Title: Predictions drift
    project.dashboard.add_panel(
        DashboardPanelCounter(
            filter=ReportFilter(metadata_values={}, tag_values=[]),
            agg=CounterAgg.NONE,
            title="Predictions Drift",
        )
    )

    # Counter: Stattest threshold
    project.dashboard.add_panel(
        DashboardPanelCounter(
            title="Stattest Threshold",
            filter=ReportFilter(metadata_values={}, tag_values=[]),
            value=PanelValue(
                metric_id="ColumnDriftMetric",
                field_path=ColumnDriftMetric.fields.stattest_threshold,
                metric_args={"column_name.name": "prediction"},
                legend="stattest threshold"
            ),
            text="",
            agg=CounterAgg.LAST,
            size=1
        )
    )
    
    # Plot: Predictions drift score plot - LINE
    project.dashboard.add_panel(
        DashboardPanelPlot(
            title="Drift Score: Wasserstein distance",
            filter=ReportFilter(metadata_values={}, tag_values=[]),
            values=[
                PanelValue(
                    metric_id="ColumnDriftMetric",
                    metric_args={"column_name.name": "prediction"},
                    field_path=ColumnDriftMetric.fields.drift_score,
                    legend="drift score",
                ),
            ],
            plot_type=PlotType.BAR,
            size=1
        )
    )
    
    # Counter: Drift Detected
    project.dashboard.add_panel(
        DashboardPanelCounter(
            title="Predictions Drift Detected",
            filter=ReportFilter(metadata_values={}, tag_values=[]),
            value=PanelValue(
                metric_id="ColumnDriftMetric",
                field_path=ColumnDriftMetric.fields.drift_detected,
                metric_args={"column_name.name": "prediction"},
                legend="drift detected"
            ),
            text="",
            agg=CounterAgg.LAST,
            size=2
        )
    )

    return project


def build_dashboards(myworkspace: str, project_name: str):
    """
    Build dashboards for projects:
    - Data Quality
    - Predictions Drift
    - Model Performance
    - Target Drift
    """

    # [Get workspace]
    path_ws = Path(os.path.dirname(__file__)).parent / myworkspace
    ws: Workspace = Workspace.create(path_ws)

    # [Build dashboards]
    project = get_evidently_project(ws, project_name)    
    project.dashboard.panels = []
    
    # Data Quality
    #project = get_evidently_project(ws, "Data Quality")
    project = add_data_quality_dashboard(project)
    project.save()

    # Predictions Drift
    #project = get_evidently_project(ws, "Predictions Drift")
    #project.dashboard.panels = []
    project = add_predictions_drift_dashboard(project)
    project.save()

    """
    # Model Performance
    project_mp = get_evidently_project(ws, "Model Performance")
    project_mp.dashboard.panels = []
    project_mp = add_regression_dashboard(project_mp)
    project_mp.save()

    # Target Drift
    project_td = get_evidently_project(ws, "Target Drift")
    project_td.dashboard.panels = []
    project_td = add_target_drift_dashboard(project_td)
    project_td.save()
    """
    
    return ws, project.id

def download_json_from_s3(bucket_name: str, prefix: str, ws: Workspace, project_id: str):
    # Initialize a session using Amazon S3
    s3 = boto3.client('s3')


    # List all the .csv files in the specified folder
    response = s3.list_objects_v2(Bucket=bucket_name, Prefix=prefix)
    json_files = [content['Key'] for content in response.get('Contents', []) if content['Key'].endswith('.json')]

    # Initialize an empty list to hold DataFrames
    os.makedirs("reports", exist_ok=True)

    # Download and read each .csv file into a DataFrame
    for json_file in json_files:
        # Get the json report from S3
        local_path = os.path.join("reports", os.path.basename(json_file))
        s3.download_file(bucket_name, json_file, local_path)
        # Save the report to the wrokspace
        ws.add_snapshot(project_id, Report.load(local_path))

    print(f'Reports downloaded and added to workspace')
    
if __name__== "__main__":
    
    myworkspace= os.getenv('PERFORMANCE_DASHBOARD',"myworkspace")
    project= os.getenv('PERFORMANCE_PROJECT',"online_gaming")
    bucket_name= os.getenv('AWS_BUCKET_NAME',"mlops-zoomcamp-gaming")
    prefix="monitoring/reports"
    
    ws, project_id=build_dashboards(myworkspace,project)
    download_json_from_s3(bucket_name, prefix, ws, project_id)
    