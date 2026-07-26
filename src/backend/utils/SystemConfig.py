import os


DB_HOSTNAME = os.environ.get("DB_HOSTNAME", "localhost")
#DB_HOSTNAME = os.environ.get("DB_HOSTNAME", "pax-db")
DB_PORT = int(os.environ.get("DB_PORT", "8210"))
DB_NAME = os.environ.get("DB_NAME", "PaxDB")

# Host:port of the external C2 REST API. Empty when Pax runs standalone, in
# which case seeded data is used instead (see utils/LocalC2Data.py).
C2_REST = os.environ.get("C2_REST", "")
