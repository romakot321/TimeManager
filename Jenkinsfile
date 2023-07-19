#!groovy

pipeline {
    agent any
    stages {
        stage("Run images") {
            steps {
                sh 'docker-compose up -d --build --remove-orphans'
                sh 'sleep 8'
                sh 'docker-compose exec -d api init_models'
            }
        }
    }
}
