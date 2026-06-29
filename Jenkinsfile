pipeline {
    agent any

    parameters {
        string(name: 'KEY_NAME', defaultValue: 'foodexpress-key', description: 'Existing AWS EC2 key pair name')
        string(name: 'AWS_REGION', defaultValue: 'us-east-1', description: 'AWS region to deploy into')
        string(name: 'INSTANCE_TYPE', defaultValue: 't2.micro', description: 'EC2 instance type')
    }

    environment {
        IMAGE_NAME = "saratpiya17/foodexpress"
        IMAGE_TAG  = "${BUILD_NUMBER}"
        APP_DIR    = "app"
        TF_DIR     = "terraform"
    }

    stages {

        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Build Docker Image') {
            steps {
                dir("${APP_DIR}") {
                    sh """
                        docker build \
                          -t ${IMAGE_NAME}:${IMAGE_TAG} \
                          -t ${IMAGE_NAME}:latest .
                    """
                }
            }
        }

        stage('Push Docker Image') {
            steps {
                withCredentials([
                    usernamePassword(
                        credentialsId: 'dockerhub-creds',
                        usernameVariable: 'DOCKERHUB_USERNAME',
                        passwordVariable: 'DOCKERHUB_PASSWORD'
                    )
                ]) {
                    sh """
                        echo "\$DOCKERHUB_PASSWORD" | docker login -u "\$DOCKERHUB_USERNAME" --password-stdin
                        docker push ${IMAGE_NAME}:${IMAGE_TAG}
                        docker push ${IMAGE_NAME}:latest
                    """
                }
            }
        }

        stage('Terraform Init') {
            steps {
                dir("${TF_DIR}") {
                    withCredentials([
                        usernamePassword(
                            credentialsId: 'aws-creds',
                            usernameVariable: 'AWS_ACCESS_KEY_ID',
                            passwordVariable: 'AWS_SECRET_ACCESS_KEY'
                        )
                    ]) {
                        sh 'terraform init -input=false'
                    }
                }
            }
        }

        stage('Terraform Plan') {
            steps {
                dir("${TF_DIR}") {
                    withCredentials([
                        usernamePassword(
                            credentialsId: 'aws-creds',
                            usernameVariable: 'AWS_ACCESS_KEY_ID',
                            passwordVariable: 'AWS_SECRET_ACCESS_KEY'
                        )
                    ]) {
                        sh """
                            terraform plan -input=false \
                              -var="aws_region=${params.AWS_REGION}" \
                              -var="instance_type=${params.INSTANCE_TYPE}" \
                              -var="key_name=${params.KEY_NAME}" \
                              -var="docker_image=${IMAGE_NAME}:${IMAGE_TAG}" \
                              -out=tfplan
                        """
                    }
                }
            }
        }

        stage('Terraform Apply') {
            steps {
                dir("${TF_DIR}") {
                    withCredentials([
                        usernamePassword(
                            credentialsId: 'aws-creds',
                            usernameVariable: 'AWS_ACCESS_KEY_ID',
                            passwordVariable: 'AWS_SECRET_ACCESS_KEY'
                        )
                    ]) {
                        sh 'terraform apply -input=false -auto-approve tfplan'
                    }
                }
            }
        }

        stage('Show Output') {
            steps {
                dir("${TF_DIR}") {
                    withCredentials([
                        usernamePassword(
                            credentialsId: 'aws-creds',
                            usernameVariable: 'AWS_ACCESS_KEY_ID',
                            passwordVariable: 'AWS_SECRET_ACCESS_KEY'
                        )
                    ]) {
                        sh 'terraform output public_ip'
                    }
                }
            }
        }
    }

    post {
        success {
            echo "Deployment complete - new FoodExpress EC2 instance is running ${IMAGE_NAME}:${IMAGE_TAG}."
        }

        failure {
            echo "Pipeline failed - check the stage logs above."
        }

        always {
            script {
                node {
                    sh 'docker logout || true'
                }
            }
        }
    }
}