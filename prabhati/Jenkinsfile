pipeline{
    agent any
    stages {
        // soft build : requirement.txt, collectstatic, migrate
        
        stage('soft build'){
            steps  {
                sh "chmod +x cicd/soft_build/entrypoint.sh"
                sh "cicd/soft_build/./entrypoint.sh"
            }
        }

        //--------------------------------------------------------------------------------------------------
        // hard build : to setup the project first time

        // stage('Setup Python Virtual ENV'){
        //     steps  {
        //         sh "chmod +x cicd/hard_build/entrypoint.sh"
        //         sh "cicd/hard_build/./entrypoint.sh"
        //     }
        // }
        // stage('Setup DataBase'){
        //     steps  {
        //         sh "chmod +x cicd/hard_build/database.sh"
        //         sh "cicd/hard_build/./database.sh"
        //     }
        // }
        // stage('Setup Gunicorn Setup'){
        //     steps {
        //         sh "chmod +x cicd/hard_build/gunicorn.sh"
        //         sh "cicd/hard_build/./gunicorn.sh"

        //     }
        // }
        // stage('setup NGINX'){
        //     steps {
        //         sh "chmod +x cicd/hard_build/nginx.sh"
        //         sh "cicd/hard_build/./nginx.sh"
        //     }
        // }
        // stage('setup Celery'){
        //     steps {
        //         sh "chmod +x cicd/hard_build/celery.sh"
        //         sh "cicd/hard_build/./celery.sh"
        //     }
        // }
        // stage('last commands'){
        //     steps {
        //         sh "chmod +x cicd/hard_build/last_commands.sh"
        //         sh "cicd/hard_build/./last_commands.sh"

        //     }
        // }

        //--------------------------------------------------------------------------------------------------
    }
}
