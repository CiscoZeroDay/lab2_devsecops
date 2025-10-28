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
                sh 'python3 -m venv venv'
                sh './venv/bin/pip install --upgrade pip'
                sh './venv/bin/pip install -r requirements.txt pytest bandit safety'
            }
        }

        stage('Run Tests') {
            steps {
                sh './venv/bin/pytest -q'
            }
        }

        stage('Static Code Analysis - Bandit') {
            steps {
                sh './venv/bin/bandit -r . -f txt -o bandit_report.txt || true'
                archiveArtifacts artifacts: 'bandit_report.txt', allowEmptyArchive: true
            }
        }

        stage('Dependency Check - Safety') {
            steps {
                sh './venv/bin/safety check -r requirements.txt --full-report > safety_report.txt || true'
                archiveArtifacts artifacts: 'safety_report.txt', allowEmptyArchive: true
            }
        }

        stage('Build & Scan Docker Image') {
            steps {
                sh 'docker-compose build'
                sh 'trivy image ${IMAGE_NAME}:latest > trivy_report.txt || true'
                archiveArtifacts artifacts: 'trivy_report.txt', allowEmptyArchive: true
            }
        }

        stage('Deploy Application') {
            steps {
                sh 'docker-compose up -d'
            }
        }
    }

    post {
        always {
            cleanWs()
        }
    }
}
