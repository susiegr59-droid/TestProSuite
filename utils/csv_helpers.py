import os
import pandas as pd


def ensure_data_folder():
    os.makedirs("data", exist_ok=True)


def load_csv(file_path, columns):
    ensure_data_folder()

    if os.path.exists(file_path):
        df = pd.read_csv(file_path)

        for col in columns:
            if col not in df.columns:
                df[col] = ""

        return df[columns]

    return pd.DataFrame(columns=columns)


def initialize_csv(file_path, columns):
    ensure_data_folder()

    if not os.path.exists(file_path):
        pd.DataFrame(columns=columns).to_csv(file_path, index=False)


def save_csv(df, file_path):
    ensure_data_folder()
    df.to_csv(file_path, index=False)
    