# CPEA-TAE-FIELD v1.0 — reproducible computational protocol

EEG → preprocessing → microstates → PLV → entropy/complexity → transition detection → IRP → TAE.

This is a simulation/protocol scaffold, not empirical validation. “Field” denotes a multivariate neurodynamic representation derived from EEG; it does not assume consciousness is an electromagnetic field.

Install:
`pip install -r requirements.txt`

Run:
`python src/run_pipeline.py`

Test:
`pytest -q`

Primary endpoint: subject-level IRP difference between structurally meaningful exceptions and physically matched, predictively irrelevant exceptions.

Preregistered TAE candidate: surprise > 90th calibration percentile AND IRP > 95th baseline/control percentile AND predefined persistence AND improved subsequent prediction.
