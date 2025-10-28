pipeline {
    agent any

    environment {
        IMAGE_NAME = 'flask-devsecops-app'
    }

    stages {

        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Install Dependencies') {
            steps {
                bat '''
                    python -m venv venv
                    call venv\\Scripts\\activate
                    pip install --upgrade pip
                    pip install -r requirements.txt pytest bandit safety
                '''
            }
        }

        stage('Run Tests') {
            steps {
                bat '''
                    call venv\\Scripts\\activate
                    pytest -q
                '''
            }
        }

        stage('Static Code Analysis - Bandit') {
            steps {
                bat '''
                    call venv\\Scripts\\activate
                    bandit -r . -f txt -o bandit_report.txt || exit 0
                '''
                archiveArtifacts artifacts: 'bandit_report.txt', allowEmptyArchive: true
            }
        }

        stage('Dependency Check - Safety') {
            steps {
                bat '''
                    call venv\\Scripts\\activate
                    safety check -r requirements.txt --full-report > safety_report.txt || exit 0
                '''
                archiveArtifacts artifacts: 'safety_report.txt', allowEmptyArchive: true
            }
        }

        stage('Build & Scan Docker Image') {
            steps {
                bat '''
                    docker-compose build
                    trivy image %IMAGE_NAME%:latest > trivy_report.txt || exit 0
                '''
                archiveArtifacts artifacts: 'trivy_report.txt', allowEmptyArchive: true
            }
        }

        stage('Deploy Application') {
            steps {
                bat 'docker-compose up -d'
            }
        }
    }

    post {
        always {
            cleanWs()
        }
    }
}
