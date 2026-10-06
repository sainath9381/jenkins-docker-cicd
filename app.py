from flask import Flask, jsonify
import os
import mysql.connector

app = Flask(__name__)


@app.route("/")
def home():
    return "CI/CD Application is running successfully!"


@app.route("/health")
def health():
    return jsonify({
        "application": "jenkins-docker-cicd",
        "status": "healthy"
    })


@app.route("/db-health")
def db_health():
    try:
        connection = mysql.connector.connect(
            host=os.getenv("DB_HOST", "mysql"),
            user=os.getenv("DB_USER", "appuser"),
            password=os.getenv("DB_PASSWORD", "apppassword"),
            database=os.getenv("DB_NAME", "employee_db")
        )

        connection.close()

        return jsonify({
            "database": "connected",
            "status": "healthy"
        })

    except Exception as e:
        return jsonify({
            "database": "disconnected",
            "status": "unhealthy",
            "error": str(e)
        }), 500


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=5000
    )