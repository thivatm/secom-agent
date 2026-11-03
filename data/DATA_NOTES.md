# SECOM data notes (SEC-2)

Measured facts, not assumptions. Fill in every TODO with a number you computed.

| Fact | Value | How measured |
|---|---|---|
 | Rows (runs) | 1,567 | `len(df)` |
| Sensor columns | 590 (`sensor_000` to `sensor_589`) | `df.filter(like="sensor_").shape[1]` |
| Pass / fail counts | 1,463 pass / 104 fail (6.64% fail) | `df["label"].value_counts()` |
| Timestamp format | `DD/MM/YYYY HH:MM:SS`, quoted, day-first | raw file inspection; `19/07/2008`
proves day-first |
| Date range | 2008-07-19 11:55 to 2008-10-17 06:07, rows sorted by time | `min()`, `max()`,
`is_monotonic_increasing` |
| Runs per month | Jul 63, Aug 555, Sep 590, Oct 359 | `dt.to_period("M").value_counts()` |
| Overall missing share | 4.54% of sensor cells; 538 of 590 sensors have at least one NaN |
`sensors.isna().to_numpy().mean()` |
| Sensors with >50% missing | 28 | `(sensors.isna().mean() > 0.5).sum()` |
| Constant sensors | 116 (one distinct non-null value); 0 sensors are all-NaN | `sensors.nunique(dropna=True) == 1` |
