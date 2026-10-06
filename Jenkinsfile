pipeline {

    agent any

    environment {
        IMAGE_NAME = 'jenkins-docker-cicd'
        CONTAINER_NAME = 'jenkins-docker-cicd-app'
        HOST_PORT = '5000'
        CONTAINER_PORT = '5000'
    }

    stages {

        stage('Checkout') {
            steps {
                echo 'Checking out source code from GitHub...'
                checkout scm
            }
        }

        stage('Install Dependencies') {
            steps {
                echo 'Installing Python dependencies...'

                sh '''
                    python3 -m pip install --user --upgrade pip
                    python3 -m pip install --user -r requirements.txt
                '''
            }
        }

        stage('Test') {
            steps {
                echo 'Running application tests...'

                sh '''
                    python3 -m pytest -v
                '''
            }
        }

        stage('Docker Build') {
            steps {
                echo 'Building Docker image...'

                sh '''
                    docker build -t ${IMAGE_NAME}:${BUILD_NUMBER} .
                    docker tag ${IMAGE_NAME}:${BUILD_NUMBER} ${IMAGE_NAME}:latest
                '''
            }
        }

        stage('Trivy Scan') {
            steps {
                echo 'Scanning Docker image for vulnerabilities...'

                sh '''
                    trivy image --exit-code 0 --severity HIGH,CRITICAL ${IMAGE_NAME}:${BUILD_NUMBER}
                '''
            }
        }

        stage('Deploy') {
            steps {
                echo 'Deploying application using Docker Compose...'

                sh '''
                    docker compose down || true
                    docker compose up -d --build
                '''
            }
        }

        stage('Health Check') {
            steps {
                echo 'Checking application health...'

                sh '''
                    sleep 10
                    curl -f http://localhost:5000/health
                '''
            }
        }
    }

    post {

        success {
            echo '========================================'
            echo 'CI/CD Pipeline completed successfully!'
            echo '========================================'
        }

        failure {
            echo '========================================'
            echo 'CI/CD Pipeline failed. Check the stage logs.'
            echo '========================================'
        }

        always {
            echo 'Pipeline execution completed.'
        }
    }
}