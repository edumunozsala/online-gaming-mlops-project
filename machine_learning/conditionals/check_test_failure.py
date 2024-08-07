from utils import monitoring

if 'condition' not in globals():
    from mage_ai.data_preparation.decorators import condition


@condition
def evaluate_condition(*args, **kwargs) -> bool:
    status= monitoring.check_test_failures(args[0])
    return status
