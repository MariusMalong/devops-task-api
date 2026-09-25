pipeline {
    agent any
    
    environment {
        IMAGE_NAME = 'devops_task_api'
        STAGING_PORT = '8000'
        PROD_PORT = '8080'
    }
    
    stages {
        stage('1. Build') {
            steps {
                echo 'Building the Docker artefact...'
                // Generates a versioned working artefact
                sh 'docker build -t ${IMAGE_NAME}:${BUILD_NUMBER} .'
                sh 'docker tag ${IMAGE_NAME}:${BUILD_NUMBER} ${IMAGE_NAME}:latest'
            }
        }
        
        stage('2. Test') {
            steps {
                echo 'Running automated test suite with pytest...'
                // Executes the test suite directly inside the built container
                sh 'docker run --rm ${IMAGE_NAME}:latest python -m pytest -v'
            }
        }
        
        stage('3. Code Quality') {
            steps {
                echo 'Running Flake8 for code maintainability...'
                // Scans the codebase for structural issues and code smells
                sh 'docker run --rm ${IMAGE_NAME}:latest flake8 .'
            }
        }
        
        stage('4. Security') {
            steps {
                echo 'Scanning for security vulnerabilities using Bandit...'
                // Performs automated AST security analysis on the Python code[cite: 2]
                sh 'docker run --rm ${IMAGE_NAME}:latest bandit -r app/ -ll -ii'
            }
        }
        
        stage('5. Deploy (Staging)') {
            steps {
                echo 'Deploying to staging environment via Docker Compose...'
                // Automated deployment to a reliable test infrastructure[cite: 2]
                sh 'docker compose down' 
                sh 'docker compose up -d'
                sleep time: 5, unit: 'SECONDS'
            }
        }
        
        stage('6. Release (Production)') {
            steps {
                echo 'Promoting build to Production environment...'
                // Simulates a repeatable production release on a separate port[cite: 2]
                sh 'docker run -d --name ${IMAGE_NAME}_prod -p ${PROD_PORT}:8000 ${IMAGE_NAME}:${BUILD_NUMBER}'
                sleep time: 5, unit: 'SECONDS'
            }
        }
        
        stage('7. Monitoring & Alerting') {
            steps {
                echo 'Verifying telemetry and health endpoints for monitoring tools...'
                // Proves the application exposes live metrics for Datadog/New Relic[cite: 2]
                sh 'curl -s -f http://localhost:${PROD_PORT}/health || exit 1'
                sh 'curl -s -f http://localhost:${PROD_PORT}/metrics | grep "http_requests_total" || exit 1'
            }
        }
    }
    
    post {
        always {
            echo 'Cleaning up production release container...'
            sh 'docker rm -f ${IMAGE_NAME}_prod || true'
        }
        success {
            echo 'Pipeline completed successfully. All 7 Top HD stages passed.'
        }
        failure {
            echo 'Pipeline failed. Check the logs for the failing stage.'
        }
    }
}