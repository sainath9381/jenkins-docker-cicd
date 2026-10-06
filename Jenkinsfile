pipeline {
    agent any

    stages {

        stage('Checkout') {
            steps {
                echo 'Checking out source code from GitHub...'
                checkout scm
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
                echo 'Building Docker images...'
                sh '''
                    docker compose build
                '''
            }
        }

        stage('Trivy Scan') {
            steps {
                echo 'Scanning Docker images for vulnerabilities...'
                sh '''
                    rm -f trivy-report.txt

                    for image in $(docker compose config --images); do
                        echo "========================================" >> trivy-report.txt
                        echo "Scanning: $image" >> trivy-report.txt
                        echo "========================================" >> trivy-report.txt

                        trivy image --severity HIGH,CRITICAL "$image" \
                            >> trivy-report.txt || true
                    done

                    echo "Trivy scan completed."
                '''
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
                echo 'Checking running containers...'
                sh '''
                    sleep 15

                    echo "===== Docker Containers ====="
                    docker compose ps

                    echo "===== Application Health ====="
                    curl -f http://localhost:5000/health

                    echo ""
                    echo "===== Database Health ====="
                    curl -f http://localhost:5000/db-health

                    echo ""
                    echo "Health checks passed successfully."
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