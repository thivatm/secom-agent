from pathlib import Path

import pandas as pd

from agent.config import DATA_DIR

LABEL_MAP = {-1: "pass", 1: "fail"}
TIMESTAMP_FORMAT = "%d/%m/%Y %H:%M:%S" # day-first: secom_labels.data has dates like 19/07/2008

def load_secom(data_dir: Path = DATA_DIR) -> pd.DataFrame:
    # Single spaced separated data, missing readings are NaN
    data_dir = Path(data_dir)
    sensors = pd.read_csv(data_dir / "secom.data", sep=" ", header=None, na_values=["NaN"])
    sensors.columns = [f"sensor_{i:03d}" for i in range(sensors.shape[1])]

    labels = pd.read_csv(
        data_dir / "secom_labels.data", sep=" ", header=None, names=["label", "timestamp"]
    )

    if len(sensors) != len(labels):
        raise ValueError(
            f"secom.data has {len(sensors)} rows but secom_labels.data has {len(labels)}"
        )

    unknown = set(labels["label"].unique()) - set(LABEL_MAP)
    if unknown:
        raise ValueError(f"Unexpected label vlaues: {sorted(unknown)}")

    labels["label"] = labels["label"].map(LABEL_MAP)
    labels["timestamp"] = pd.to_datetime(labels["timestamp"], format=TIMESTAMP_FORMAT)

    return pd.concat([sensors, labels], axis=1)
