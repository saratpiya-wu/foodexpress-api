pipeline {
    agent any

    environment {
        DOCKERHUB_CREDENTIALS = credentials('dockerhub-creds')
        AWS_CREDENTIALS       = credentials('aws-creds')
        DOCKER_IMAGE          = "saratpiya17/foodexpress"
        IMAGE_TAG             = "${BUILD_NUMBER}"
        EC2_KEY_NAME          = "foodexpress-key"   // name of your AWS key pair
    }

    stages {

        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Build Docker Image') {
            steps {
                dir('app') {
                    sh "docker build -t ${DOCKER_IMAGE}:${IMAGE_TAG} -t ${DOCKER_IMAGE}:latest ."
                }
            }
        }

        stage('Push Docker Image') {
            steps {
                sh "echo ${DOCKERHUB_CREDENTIALS_PSW} | docker login -u ${DOCKERHUB_CREDENTIALS_USR} --password-stdin"
                sh "docker push ${DOCKER_IMAGE}:${IMAGE_TAG}"
                sh "docker push ${DOCKER_IMAGE}:latest"
            }
        }

        stage('Terraform Init & Apply') {
            environment {
                AWS_ACCESS_KEY_ID     = "${AWS_CREDENTIALS_USR}"
                AWS_SECRET_ACCESS_KEY = "${AWS_CREDENTIALS_PSW}"
            }
            steps {
                dir('terraform') {
                    sh 'terraform init -input=false'
                    sh """
                        terraform apply -auto-approve \
                          -var="docker_image=${DOCKER_IMAGE}:${IMAGE_TAG}" \
                          -var="key_name=${EC2_KEY_NAME}"
                    """
                }
            }
        }

        stage('Deploy / Update Container on EC2') {
            steps {
                dir('terraform') {
                    script {
                        env.EC2_PUBLIC_IP = sh(
                            script: 'terraform output -raw public_ip',
                            returnStdout: true
                        ).trim()
                    }
                }
                sshagent(['ec2-ssh-key']) {
                    sh """
                        ssh -o StrictHostKeyChecking=no ubuntu@${EC2_PUBLIC_IP} '
                            sudo docker pull ${DOCKER_IMAGE}:${IMAGE_TAG} &&
                            sudo docker stop foodexpress || true &&
                            sudo docker rm foodexpress || true &&
                            sudo docker run -d --restart unless-stopped -p 80:5000 --name foodexpress ${DOCKER_IMAGE}:${IMAGE_TAG}
                        '
                    """
                }
            }
        }

        stage('Show App URL') {
            steps {
                echo "FoodExpress API is live at: http://${EC2_PUBLIC_IP}/"
            }
        }
    }

    post {
        success {
            echo "Pipeline completed successfully."
        }
        failure {
            echo "Pipeline failed — check the stage logs above."
        }
    }
}