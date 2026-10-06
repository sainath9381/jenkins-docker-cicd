pipeline {

    agent any

    environment {
        VENV = '/var/lib/jenkins/venv'
        IMAGE_NAME = 'jenkins-docker-cicd-app'
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
                    if [ ! -d "$VENV" ]; then
                        python3 -m venv "$VENV"
                    fi

                    "$VENV/bin/python" -m pip install --upgrade pip
                    "$VENV/bin/pip" install -r requirements.txt
                '''
            }
        }

        stage('Test') {
            steps {
                echo 'Running application tests...'

                sh '''
                    "$VENV/bin/pytest" -v test_app.py
                '''
            }
        }

        stage('Docker Build') {
            steps {
                echo 'Building Docker image...'

                sh '''
                    docker build -t "$IMAGE_NAME:latest" .
                '''
            }
        }

        stage('Trivy Scan') {
            steps {
                echo 'Scanning Docker image with Trivy...'

                sh '''
                    if command -v trivy >/dev/null 2>&1; then
                        trivy image \
                          --format table \
                          --output trivy-report.txt \
                          "$IMAGE_NAME:latest" || true
                    else
                        echo "Trivy is not installed. Skipping scan."
                    fi
                '''

                archiveArtifacts artifacts: 'trivy-report.txt',
                                 allowEmptyArchive: true
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

                    echo "Running containers:"
                    docker compose ps

                    echo "Testing application..."

                    if curl -f http://localhost/health; then
                        echo "Health check successful on port 80"
                    elif curl -f http://localhost:5000/health; then
                        echo "Health check successful on port 5000"
                    else
                        echo "Health check failed"
                        docker compose logs --tail=100
                        exit 1
                    fi
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