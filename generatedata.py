import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import great_expectations as ge


# Set random seed
np.random.seed(42)

# Generate synthetic data
n_records = 1000

# Create customer IDs (with intentional duplicates)
customer_ids = np.random.randint(1000, 9999, size=n_records)
customer_ids[:10] = customer_ids[10:20]  # Create duplicates

# Generate dates
base_date = datetime.now()
days_ago = np.random.randint(0, 365, n_records)
dates = [base_date - timedelta(days=int(x)) for x in days_ago]

# Create dataset
data = {
    'transaction_id': range(1, n_records + 1),
    'customer_id': customer_ids,
    'transaction_date': dates,
    'transaction_amount': np.random.uniform(10, 10000, n_records),
    'account_type': np.random.choice(['checking', 'savings', 'investment', None], n_records, p=[0.4, 0.3, 0.2, 0.1]),
    'transaction_type': np.random.choice(['deposit', 'withdrawal', 'transfer', None], n_records, p=[0.35, 0.35, 0.2, 0.1]),
    'status': np.random.choice(['completed', 'pending', 'failed', None], n_records, p=[0.8, 0.1, 0.05, 0.05])
}

# Create DataFrame
df = pd.DataFrame(data)

# Introduce quality issues
df.loc[np.random.choice(df.index, 20), 'transaction_amount'] = -100  # Negative amounts
df.loc[np.random.choice(df.index, 30), 'transaction_amount'] = np.nan  # Missing amounts

# Export the DataFrame to a CSV file
df.to_csv('synthetic_data.csv', index=False)

print("Dataset Preview:")
print("\nData Quality Summary:")
print(df.describe(include='all'))
print("\nData Types:")
print(df.dtypes)        