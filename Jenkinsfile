#!/usr/bin/env groovy

import java.text.*

node {
    def app
    def yaml_path
    def version_tag

    def app_name = 'ai-lab-flask-react-starter'
    def namespace = 'default'
    def cluster = 'preprod.local'

    def date = new Date()
    def datestring = new SimpleDateFormat("yyyy-MM-dd").format(date);

    try {
        stage('Clean workspace') {
            cleanWs()
        }

        stage('Checkout code') {
            checkout(
                scm: [$class: 'GitSCM',
                    branches: [[name: '*/master']],
                    userRemoteConfigs: [[url: "git@github.com:navikt/ai-lab-flask-react-starter.git", credentialsId: 'ci-flask-react-starter']]]
            )
            def git_commit_hash = sh(script: "git rev-parse --short HEAD", returnStdout: true).trim()
            version_tag = "${datestring}-${git_commit_hash}"
        }

        stage('Copy certificate bundle') {
            sh "cp /etc/ssl/certs/ca-bundle.crt ca-bundle.crt"
        }

        stage('Build react app') {
            sh "chmod +x scripts/buildReactApp.sh"
            sh "./scripts/buildReactApp.sh"
        }

        stage('Build docker image') {
            app = docker.build("${app_name}")
        }

        stage('Upload nais.yaml to nexus server') {
            yaml_path = "https://repo.adeo.no/repository/raw/nais/${app_name}/${version_tag}/nais.yaml"
            sh "curl -s -S --upload-file nais.yaml ${yaml_path}"
        }

        stage('Push docker image') {
            docker.withRegistry('https://repo.adeo.no:5443', 'nexus-credentials') {
                app.push("${version_tag}")
            }
        }

        stage('Deploy app to nais') {
            sh "curl --fail -k -d '{\"application\": \"${app_name}\", \"version\": \"${version_tag}\", \"skipFasit\": true, \"namespace\": \"${namespace}\", \"manifesturl\": \"${yaml_path}\"}' https://daemon.nais.${cluster}/deploy"
        }
    } catch(e) {
        echo "Build failed"
        throw e
    } finally {
        sh "docker rmi -f \$(docker images | grep 'repo.adeo.no:5443/${app_name}' | awk '{print \$3}') | true"
    }
}