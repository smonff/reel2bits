#!/usr/bin/env groovy

// http://www.asciiarmor.com/post/99010893761/jenkins-now-with-more-gopher
// https://medium.com/@reynn/automate-cross-platform-golang-builds-with-jenkins-ef7b07f1366e
// http://grugrut.hatenablog.jp/entry/2017/04/10/201607
// https://gist.github.com/wavded/5e6b0d5016c2a3c05237

node('linux && x86_64 && go') {
    // Install the desired Go version
    def root = tool name: 'Go 1.8.3', type: 'go'

    ws("${JENKINS_HOME}/jobs/${JOB_NAME}/builds/${BUILD_ID}/src/dev.sigpipe.me/dashie/reel2bits") {
        // Export environment variables pointing to the directory where Go was installed
        env.GOROOT="${root}"
        env.GOPATH="${JENKINS_HOME}/jobs/${JOB_NAME}/builds/${BUILD_ID}/"
        env.PATH="${GOPATH}/bin:$PATH"

        stage('Requirements') {
            sh 'go version'

            sh 'go get -u github.com/golang/lint/golint'
            sh 'go get -u github.com/tebeka/go2xunit'
            sh 'go get github.com/Masterminds/glide'
        }

        stage('Checkout') {
        //    git url: 'https://dev.sigpipe.me/dashie/reel2bits.git'
            checkout scm
        }

        String applicationName = "reel2bits"
        String appVersion = sh (
            script: "cat reel2bits.go | awk -F'\"' '/const APP_VER/ { print \$2 }'",
            returnStdout: true
            ).trim()
        String buildNumber = "${appVersion}-${env.BUILD_NUMBER}"

        stage('Install dependencies') {
            sh 'glide install'
        }

        stage('Test') {
            // Static check and publish warnings
            sh 'golint $(go list ./... | grep -v /vendor/) > lint.txt'
            warnings canComputeNew: false, canResolveRelativePaths: false, defaultEncoding: '', excludePattern: '', healthy: '', includePattern: '', messagesPattern: '', parserConfigurations: [[parserName: 'Go Lint', pattern: 'lint.txt']], unHealthy: ''

            // The real tests then publish the results
            try {
                // broken due to some go /vendor directory crap
                sh 'go test -v $(go list ./... | grep -v /vendor/) > tests.txt'
            } catch (err) {
                if (currentBuild.result == 'UNSTABLE')
                    currentBuild.result = 'FAILURE'
                throw err
            } finally {
                sh 'cat tests.txt | go2xunit -output tests.xml'
                step([$class: 'JUnitResultArchiver', testResults: 'tests.xml', healthScaleFactor: 1.0])
                //No such DSL method 'publishHTML'
                //publishHTML (target: [
                //    allowMissing: false,
                //    alwaysLinkToLastBuild: false,
                //    keepAll: true,
                //    reportDir: 'coverage',
                //    reportFiles: 'index.html',
                //    reportName: "Junit Report"
                //])
            }
        }

        stage('Build') {
            // Darwin/amd64
            //sh "make build GOOS=darwin GOARCH=amd64 BUILD_FLAGS='-o binaries/amd64/${buildNumber}/darwin/${applicationName}-${buildNumber}.darwin.amd6'"
            // Windows/amd64
            //sh "make build GOOS=windows GOARCH=amd64 BUILD_FLAGS='-o binaries/amd64/${buildNumber}/windows/${applicationName}-${buildNumber}.windows.amd64.exe'"
            // Linux/amd64
            sh "make build GOOS=linux GOARCH=amd64 BUILD_FLAGS='-o binaries/amd64/${buildNumber}/linux/${applicationName}-${buildNumber}.linux.amd64'"
        }

        stage('Archivate Artifacts') {
            // this doesn't works
            //zip dir: '${env.WORKSPACE}/', zipFile: "${env.WORKSPACE}/reel2bits.linux-${buildNumber}.zip", glob: 'binaries/**,conf,LICENSE*,README*,lint.txt,tests.txt', archive: true
            sh 'ls'
            sh """
            mkdir reel2bits.linux-${buildNumber}
            cp binaries/amd64/${buildNumber}/linux/${applicationName}-${buildNumber}.linux.amd64 reel2bits.linux-${buildNumber}
            cp -r conf reel2bits.linux-${buildNumber}
            cp LICENSE* reel2bits.linux-${buildNumber}
            cp README.md reel2bits.linux-${buildNumber}
            cp lint.txt tests.txt reel2bits.linux-${buildNumber}
            zip -r reel2bits.linux-${buildNumber}.zip reel2bits.linux-${buildNumber}
            rm -rf reel2bits.linux-${buildNumber}
            """

            archiveArtifacts artifacts: 'binaries/**,conf,LICENSE*,README*', fingerprint: true
            archiveArtifacts artifacts: 'lint.txt,tests.txt', fingerprint: true
            archiveArtifacts artifacts: "reel2bits.linux-${buildNumber}.zip", fingerprint: true
        }
    } // ws
} // node