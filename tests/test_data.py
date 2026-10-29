import pandas as pd
import pytest

from agent.data import load_secom

N_RUNS = 1567
N_FAILS = 104


@pytest.fixture(scope="module")
def df():
    return load_secom()


def sensor_cols(df):
    return [c for c in df.columns if c.startswith("sensor_")]


def test_row_count(df):
    assert len(df) == N_RUNS


def test_sensor_columns_named_in_order(df):
    cols = sensor_cols(df)
    assert cols == [f"sensor_{i:03d}" for i in range(len(cols))]
    assert list(df.columns) == cols + ["label", "timestamp"]


def test_sensor_columns_are_numeric(df):
    assert all(pd.api.types.is_float_dtype(df[c]) for c in sensor_cols(df))


def test_labels(df):
    assert set(df["label"]) == {"pass", "fail"}
    assert (df["label"] == "fail").sum() == N_FAILS


def test_timestamp(df):
    assert pd.api.types.is_datetime64_any_dtype(df["timestamp"])
    assert df["timestamp"].notna().all()


def write_fake_data(tmp_path, sensor_rows, label_rows):
    (tmp_path / "secom.data").write_text("\n".join(sensor_rows) + "\n")
    (tmp_path / "secom_labels.data").write_text("\n".join(label_rows) + "\n")


def test_row_count_mismatch_raises(tmp_path):
    write_fake_data(
        tmp_path,
        ["1.0 2.0", "3.0 NaN"],
        ['-1 "19/07/2008 11:55:00"'],
    )
    with pytest.raises(ValueError, match="rows"):
        load_secom(tmp_path)


def test_unknown_label_raises(tmp_path):
    write_fake_data(
        tmp_path,
        ["1.0 2.0"],
        ['0 "19/07/2008 11:55:00"'],
    )
    with pytest.raises(ValueError, match="label"):
        load_secom(tmp_path)


def test_small_file_parses(tmp_path):
    write_fake_data(
        tmp_path,
        ["1.0 NaN", "3.0 4.0"],
        ['-1 "19/07/2008 11:55:00"', '1 "01/08/2008 09:00:00"'],
    )
    df = load_secom(tmp_path)
    assert list(df.columns) == ["sensor_000", "sensor_001", "label", "timestamp"]
    assert df["sensor_001"].isna().sum() == 1
    assert list(df["label"]) == ["pass", "fail"]
    assert df["timestamp"].iloc[1] == pd.Timestamp(2008, 8, 1, 9, 0)