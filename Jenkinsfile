pipeline {
    agent any

    parameters {
        string(name: 'KEY_NAME', defaultValue: 'foodexpress-key', description: 'Existing AWS EC2 key pair name')
        string(name: 'AWS_REGION', defaultValue: 'ap-southeast-1', description: 'AWS region to deploy into')
        string(name: 'INSTANCE_TYPE', defaultValue: 't2.micro', description: 'EC2 instance type')
    }

    environment {
        // Jenkins credential IDs you must create beforehand (see notes below)
        DOCKERHUB_CREDS       = credentials('dockerhub-creds')   // type: Username with password
        AWS_CREDS             = credentials('aws-creds')         // type: Username with password (Access Key / Secret Key)
        AWS_ACCESS_KEY_ID     = "${AWS_CREDS_USR}"
        AWS_SECRET_ACCESS_KEY = "${AWS_CREDS_PSW}"

        IMAGE_NAME = "saratpiya17/foodexpress"   // <-- change to your actual Docker Hub repo
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
                    sh "docker build -t ${IMAGE_NAME}:${IMAGE_TAG} -t ${IMAGE_NAME}:latest ."
                }
            }
        }

        stage('Push Docker Image') {
            steps {
                sh "echo ${DOCKERHUB_CREDS_PSW} | docker login -u ${DOCKERHUB_CREDS_USR} --password-stdin"
                sh "docker push ${IMAGE_NAME}:${IMAGE_TAG}"
                sh "docker push ${IMAGE_NAME}:latest"
            }
        }

        stage('Terraform Init') {
            steps {
                dir("${TF_DIR}") {
                    sh 'terraform init -input=false'
                }
            }
        }

        stage('Terraform Plan') {
            steps {
                dir("${TF_DIR}") {
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

        stage('Terraform Apply (provision new instance)') {
            steps {
                dir("${TF_DIR}") {
                    sh 'terraform apply -input=false -auto-approve tfplan'
                }
            }
        }

        stage('Show Output') {
            steps {
                dir("${TF_DIR}") {
                    sh 'terraform output public_ip'
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
            sh 'docker logout || true'
        }
    }
}