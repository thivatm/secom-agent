"""Load the SECOM dataset into one DataFrame. Ticket: SEC-2.

Spec: Data section. Measure, don't assume.
"""
from pathlib import Path

import pandas as pd

from agent.config import DATA_DIR


def load_secom(data_dir: Path = DATA_DIR) -> pd.DataFrame:
    """Return one row per run: sensor_000 ... sensor_NNN, label ("pass"/"fail"), timestamp.

    TODO(SEC-2):
      - read secom.data (space-separated, NaN for missing) and name the sensor columns
      - read secom_labels.data: label (-1 = pass, 1 = fail) and timestamp
      - check both files have the same number of rows; parse timestamp as datetime
    """
    raise NotImplementedError
