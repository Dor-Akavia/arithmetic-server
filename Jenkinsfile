// =============================================================================
// Jenkinsfile — CI/CD pipeline for the Arithmetic Server Docker image
// =============================================================================
// Pipeline stages:
//   1. Checkout   — fetch the latest code from the Git repository
//   2. Lint       — basic Python syntax check
//   3. Build      — build the Docker image and tag it
//   4. Push       — push the image to Docker Hub
//   5. Cleanup    — remove the local image to free disk space (always runs)
//
// Prerequisites (configure in Jenkins → Manage Credentials):
//   • DOCKERHUB_CREDENTIALS — Username/Password credential for Docker Hub
//   • DOCKERHUB_USERNAME    — Plain text credential with your Docker Hub username
// =============================================================================
def dockerImage

pipeline {

    // Run on any available agent (Jenkins worker node)
    agent any

    // ---------------------------------------------------------------------------
    // Environment variables available to all stages
    // ---------------------------------------------------------------------------
    environment {
        IMAGE_NAME = "dorak1234/arithmetic-server"
        IMAGE_TAG  = "${env.BUILD_NUMBER}-${env.GIT_COMMIT?.take(7) ?: 'latest'}"
        FULL_IMAGE = "${IMAGE_NAME}:${IMAGE_TAG}"
    }

    stages {

        // -----------------------------------------------------------------------
        stage('Checkout') {
        // -----------------------------------------------------------------------
            steps {
                script {
                    def scmVars = checkout scm
                    echo "Building commit: ${scmVars.GIT_COMMIT}"
                }
            }
        }

        // -----------------------------------------------------------------------
        stage('Lint') {
            // -----------------------------------------------------------------------
            steps {
                // py_compile is part of Python's standard library — no pip install needed.
                // It catches syntax errors before we waste time building an image.
                script {
                    echo "Running Python syntax check..."
                    sh 'python3 -m py_compile server/server.py server/operations.py client/client.py'
                    echo "Syntax check passed."
                }
            }
        }

        // -----------------------------------------------------------------------
        stage('Build Docker Image') {
            // -----------------------------------------------------------------------
            steps {
                script {
                    echo "Building Docker image: ${env.FULL_IMAGE}"

                    // docker.build() wraps `docker build` and returns a handle
                    dockerImage = docker.build(env.FULL_IMAGE)

                    echo "Build successful: ${env.FULL_IMAGE}"
                }
            }
        }

        // -----------------------------------------------------------------------
        stage('Push to Docker Hub') {
            // -----------------------------------------------------------------------
            steps {
                script {
                    echo "Pushing image to Docker Hub..."
                    docker.withRegistry('https://registry.hub.docker.com', 'DOCKERHUB_CREDENTIALS') {
                        dockerImage.push(env.IMAGE_TAG)   // versioned tag
                    }

                    echo "Image pushed: ${env.FULL_IMAGE}"
                }
            }
        }

    } // end stages

    post {

        always {
            // Clean up the local Docker image to avoid filling the Jenkins disk.
            script {
                echo "Cleaning up local Docker images..."
                sh "docker rmi ${env.FULL_IMAGE} || true"
            }
        }

        success {
            echo "Pipeline SUCCEEDED. Image ${env.FULL_IMAGE} was uploaded to Docker Hub."
        }

        failure {
            echo "Pipeline FAILED. Check the stage logs above for details."
        }

    }

} // end pipeline