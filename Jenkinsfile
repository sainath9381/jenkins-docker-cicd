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
                    trivy image \
                      --format table \
                      --output trivy-report.txt \
                      "$IMAGE_NAME:latest"
                '''

                archiveArtifacts artifacts: 'trivy-report.txt',
                                  allowEmptyArchive: false
            }
        }

        stage('Deploy') {
            steps {
                echo 'Deploying application using Docker Compose...'
                sh '''
                    docker compose down || true
                    docker compose up -d
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

                    if curl -f http://localhost:5000/health; then
                        echo "Health check successful on port 5000"
                    elif curl -f http://localhost/health; then
                        echo "Health check successful on port 80"
                    else
                        echo "Health check failed"
                        docker compose logs --tail=100
                        exit 1
                    fi
                '''
            }
        }

        stage('Docker Cleanup') {
            steps {
                echo 'Cleaning unused Docker resources...'
                sh '''
                    docker container prune -f
                    docker builder prune -f
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
                echo 'Preparing previous Docker image for rollback...'

                sh '''
                    if docker image inspect "$IMAGE_NAME:latest" >/dev/null 2>&1; then
                        docker tag "$IMAGE_NAME:latest" "$IMAGE_NAME:previous"
                        echo "Previous image saved as $IMAGE_NAME:previous"
                    else
                        echo "No previous image found. This is the first deployment."
                    fi

                    echo "Building new Docker image..."
                    docker build -t "$IMAGE_NAME:latest" .
                '''
            }
        }

        stage('Trivy Scan') {
            steps {
                echo 'Scanning Docker image with Trivy...'

                sh '''
                    trivy image \
                      --format table \
                      --output trivy-report.txt \
                      "$IMAGE_NAME:latest"
                '''

                archiveArtifacts artifacts: 'trivy-report.txt',
                                  allowEmptyArchive: false
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
                        echo "Health check failed!"
                        echo "Starting automatic rollback..."

                        docker compose logs --tail=100

                        if docker image inspect "$IMAGE_NAME:previous" >/dev/null 2>&1; then

                            echo "Previous image found."
                            echo "Rolling back to previous version..."

                            docker compose down || true

                            docker tag "$IMAGE_NAME:previous" "$IMAGE_NAME:latest"

                            docker compose up -d

                            sleep 10

                            echo "Checking rolled-back application..."

                            if curl -f http://localhost:5000/health; then
                                echo "Rollback completed successfully."
                            else
                                echo "Rollback health check failed."
                                docker compose logs --tail=100
                                exit 1
                            fi

                        else
                            echo "No previous image available for rollback."
                            exit 1
                        fi
                    fi
                '''
            }
        }

        stage('Docker Cleanup') {
            steps {
                echo 'Cleaning unused Docker images...'

                sh '''
                    docker image prune -f
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
