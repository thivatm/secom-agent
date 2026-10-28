"""Helper available inside the sandbox: `from secom import df`. Ticket: SEC-5.

Loads the read-only data mounted at /data into a DataFrame named `df`.
TODO(SEC-5): reuse the same loader logic as agent/data.py so host and sandbox agree.
"""
