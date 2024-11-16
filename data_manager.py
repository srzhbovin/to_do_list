import pandas as pd
from datetime import datetime

DATA_FILE_PATH = 'targets.csv'


def load_data() -> pd.DataFrame:
    try:
        targets_df = pd.read_csv(DATA_FILE_PATH, parse_dates=['created_at'])
    except FileNotFoundError:
        targets_df = pd.DataFrame(columns=['id', 'title', 'description', 'completed', 'created_at'])
    return targets_df


def save_data(df):
    df.to_csv(DATA_FILE_PATH, index=False)
