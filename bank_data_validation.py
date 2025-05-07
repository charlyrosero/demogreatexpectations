import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import great_expectations as gx
from great_expectations.core import ExpectationSuite
from great_expectations.data_context import DataContext
from great_expectations.data_context.types.base import DataContextConfig, InMemoryStoreBackendDefaults

# Set random seed for reproducibility
np.random.seed(42)

# Generate sample data
n_records = 1000

# Generate dates for the last 30 days
end_date = datetime.now()
start_date = end_date - timedelta(days=30)
dates = [start_date + timedelta(days=x) for x in range(30)]

data = {
    'transaction_id': [f'TXN{i:06d}' for i in range(n_records)],
    'account_number': [f'ACC{np.random.randint(100000, 999999)}' for _ in range(n_records)],
    'transaction_date': np.random.choice(dates, n_records),
    'transaction_type': np.random.choice(['DEPOSIT', 'WITHDRAWAL', 'TRANSFER'], n_records),
    'amount': np.random.uniform(10, 10000, n_records).round(2),
    'balance': np.random.uniform(1000, 50000, n_records).round(2),
    'customer_id': [f'CUST{np.random.randint(1000, 9999)}' for _ in range(n_records)],
    'branch_id': [f'BR{np.random.randint(1, 50)}' for _ in range(n_records)]
}

# Create DataFrame
bank_df = pd.DataFrame(data)

# Save to CSV
bank_df.to_csv('bank_transactions.csv', index=False)

# Initialize Great Expectations with proper configuration
data_context_config = DataContextConfig(
    store_backend_defaults=InMemoryStoreBackendDefaults(),
    checkpoint_store_name="checkpoint_store",
    evaluation_parameter_store_name="evaluation_parameter_store",
    expectations_store_name="expectations_store",
    validations_store_name="validations_store",
    plugins_directory=None,
    validation_operators={},
    stores={
        "checkpoint_store": {
            "class_name": "CheckpointStore",
            "store_backend": {
                "class_name": "InMemoryStoreBackend",
            },
        },
        "evaluation_parameter_store": {
            "class_name": "EvaluationParameterStore",
            "store_backend": {
                "class_name": "InMemoryStoreBackend",
            },
        },
        "expectations_store": {
            "class_name": "ExpectationsStore",
            "store_backend": {
                "class_name": "InMemoryStoreBackend",
            },
        },
        "validations_store": {
            "class_name": "ValidationsStore",
            "store_backend": {
                "class_name": "InMemoryStoreBackend",
            },
        },
    },
)

context = DataContext(project_config=data_context_config)

# Create a new datasource
datasource = context.sources.add_pandas(
    name="bank_data",
    dataframe=bank_df
)

# Create a new DataAsset
data_asset = datasource.add_dataframe_asset(
    name="transactions",
    dataframe=bank_df
)

# Create a new ExpectationSuite
expectation_suite_name = "bank_transactions_suite"
context.create_expectation_suite(expectation_suite_name)

# Create a validator
validator = context.get_validator(
    batch_request=data_asset.build_batch_request(),
    expectation_suite_name=expectation_suite_name
)

# Add expectations
# 1. Expect transaction amounts to be positive
validator.expect_column_values_to_be_between(
    column="amount",
    min_value=0,
    max_value=None
)

# 2. Expect account numbers to be unique
validator.expect_column_values_to_be_unique(
    column="account_number"
)

# 3. Expect transaction types to be in a specific set
validator.expect_column_values_to_be_in_set(
    column="transaction_type",
    value_set=["DEPOSIT", "WITHDRAWAL", "TRANSFER"]
)

# 4. Expect balance to be positive
validator.expect_column_values_to_be_between(
    column="balance",
    min_value=0,
    max_value=None
)

# 5. Expect transaction dates to be within the last 30 days
validator.expect_column_values_to_be_between(
    column="transaction_date",
    min_value=start_date,
    max_value=end_date
)

# Save the expectation suite
validator.save_expectation_suite()

# Run validation
checkpoint_config = {
    "name": "bank_transactions_checkpoint",
    "config_version": 1,
    "class_name": "SimpleCheckpoint",
    "validations": [
        {
            "batch_request": data_asset.build_batch_request(),
            "expectation_suite_name": expectation_suite_name
        }
    ]
}

context.add_checkpoint(**checkpoint_config)
results = context.run_checkpoint(checkpoint_name="bank_transactions_checkpoint")

# Display results
print("\nValidation Results:")
print(results) 