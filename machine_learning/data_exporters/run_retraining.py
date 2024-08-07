from utils import monitoring

from mage_ai.orchestration.triggers.api import trigger_pipeline
if 'data_exporter' not in globals():
    from mage_ai.data_preparation.decorators import data_exporter


@data_exporter
def trigger(*args, **kwargs):
    """
    Trigger another pipeline to run.

    Documentation: https://docs.mage.ai/orchestration/triggers/trigger-pipeline
    """
    #failure = monitoring.check_test_failures(args[0])
    
    test_json=args[0]

    failure= False
    for test in test_json['tests']:
        if test['status']!='SUCCESS':
            print("Failure: ", test['name'])
            print("Failure description: ", test['description'])
            failure=True
            #break

    print(failure)
    
    """
    trigger_pipeline(
        'training_workflow',        # Required: enter the UUID of the pipeline to trigger
        #variables={},           # Optional: runtime variables for the pipeline
        check_status=True,     # Optional: poll and check the status of the triggered pipeline
        error_on_failure=True, # Optional: if triggered pipeline fails, raise an exception
        poll_interval=60,       # Optional: check the status of triggered pipeline every N seconds
        poll_timeout=None,      # Optional: raise an exception after N seconds
        verbose=True,           # Optional: print status of triggered pipeline run
    )
    """