pipeline {
    agent any

    options{
        // Max number of build logs to keep and days to keep
        buildDiscarder(logRotator(numToKeepStr: '5', daysToKeepStr: '5'))
        // Enable timestamp at each job in the pipeline
        timestamps()
    }

    environment{
        registry = 'quochungtran/classify_disaster_text'
        registryCredential = 'dockerhub'      
    }

    stages {
        stage('Test') {
            agent {
                docker {
                    image 'python:3.9' 
                }
            }
            steps {
                echo 'Testing model correctness..'
                sh 'pip install -r requirements.txt && pytest'
            }
        }
        stage('Build') {
            steps {
                script {
                    def dockerfile = 'Dockerfile'
                    echo 'Building image for deployment..'
                    dockerImage = docker.build(registry + ":$BUILD_NUMBER", 
                                             "-f ./deployment/model_predictor/Dockerfile .") 
                    echo 'Pushing image to dockerhub..'
                    docker.withRegistry( '', registryCredential ) {
                        dockerImage.push()
                        dockerImage.push('latest')
                    }
                }
            }
        }
        stage('Deploy application to Google Kubernestes Engine') {
            agent{
                kubernetes{
                    containerTemplate{
                        name 'helm' // name of the container to be used for hel, upgrade
                        image 'quochungtran/jenkins:lts' // the image containing helm
                        alwaysPullImage true // Always pull image in case of using the same tag
                     }
                }
            }
            steps{
                script{
                    container('helm'){
                        sh("helm upgrade --install disaster-text-classifier \
                        ./helm/disaster_chart --namespace model-serving")
                    }
                }
            }
        }
    }
}