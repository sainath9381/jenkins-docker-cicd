pipeline {
    agent any

    stages {

        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Test') {
            steps {
                bat 'python -m pytest test_app.py'
            }
        }

        stage('Docker Build') {
            steps {
                bat 'docker build -t employee-app:jenkins .'
            }
        }

        stage('Trivy Scan') {
            steps {
                bat 'docker run --rm -v "%cd%:/work" aquasec/trivy:latest image --format table employee-app:jenkins > trivy-jenkins-report.txt'
            }
        }

        stage('Deploy') {
            steps {
                bat 'docker compose up -d'
            }
        }

        stage('Health Check') {
            steps {
                bat 'docker compose ps'
            }
        }
    }

    post {
        success {
            echo 'CI/CD Pipeline completed successfully!'
        }

        failure {
            echo 'CI/CD Pipeline failed. Check the stage logs.'
        }
    }
}