import os
import psycopg

def get_connection():
	return psycopg.connect(
		host = os.getenv("DB_HOST", "127.0.0.1"),
		port = 5432,
		dbname = os.getenv("DB_NAME", "predictions"),
		user = os.getenv("DB_USER", "mlops"),
		password = os.environ["DB_PASSWORD"],
	)

def save_prediction(input_value: int, prediction: int):
	with get_connection() as conn:
		with conn.cursor() as cur:
			cur.execute(
				"""
				INSERT INTO prediction_logs (input_value, prediction)
				VALUES (%s, %s)
				""",
				(input_value, prediction),
			)