
## Build And Deploy Fast Api Python Application On CICD DevOps Pipeline

![](https://cdn-images-1.medium.com/max/2560/1*aI8LOIw4HmhnmD1vIzRqiw.png)

**Introduction**:

In this article, we delve into the intricacies of setting up a Continuous Integration and Continuous Deployment (CI/CD) pipeline for a Fast API Python application. This pipeline exemplifies the integration of various tools and platforms to automate and streamline the development and deployment processes.

**Section: Pipeline Overview**

This pipeline is an example of a continuous integration and deployment (CI/CD) process using various tools and platforms. Here are the steps shown in the image:

![](https://cdn-images-1.medium.com/max/3000/1*byp1Yb1ySwLBYDq32frTAg.png)

**Development of Application Codes:**

The application code is developed and maintained in a version control system like Git.

**Jenkins Server (docker-compose on Host Machine):**

![](https://cdn-images-1.medium.com/max/3610/1*pePh7Pmaak6hW68S8e3kDw.png)

Jenkins, an integration server, automates code testing and deployments.
It can be hosted on docker-compose.
Jenkins can integrate with tools like Grafana and Prometheus for monitoring, with capabilities for sending email alerts if issues are detected.

**Code Analysis with SonarQube:**

![](https://cdn-images-1.medium.com/max/3794/1*5QaFg4fyGyj9OlC-BCH8Qg.png)

SonarQube is utilized for code quality analysis to identify bugs, vulnerabilities, and code smells.

![](https://cdn-images-1.medium.com/max/3774/1*KIkHet9lgkWVgQF6yjk5CA.png)

Steps include setting up the workspace, pulling the code from Git, and analyzing it with SonarQube.

**Checking Dependencies and Security:**

Dependencies are installed, often using a package manager like pip.
A dependency check is performed using tools like OWASP Dependency-Check to identify known vulnerabilities.
Security scanning of Docker images is carried out using Trivy, a vulnerability scanner.

**Construction and Deployment:**

![](https://cdn-images-1.medium.com/max/2694/1*zqLsoSNwBzmB0tDez8pa3Q.png)

A Docker image containing the application code is built.
The image is then stored on Docker Hub.
Deployment involves deploying the Docker image into a container for execution.
Kubernetes, a container orchestration platform, is often used for deployment, managing clusters of virtual machines or deployed containers.

**Monitoring Kubernetes Clusters:**

Kubernetes Master Nodes and Worker Nodes are monitored to ensure efficient deployment.

![](https://cdn-images-1.medium.com/max/3206/1*xBZDzidvN9hhezki97kZWw.png)

Performance metrics for each stage of the pipeline are tracked, aiding in the identification of bottlenecks and the enhancement of the CI/CD process.

![](https://cdn-images-1.medium.com/max/3274/1*lNCfLwEPKqWG5v-EqC3tCg.png)

**Prometheus and Grafana:**

![](https://cdn-images-1.medium.com/max/3106/1*s0uI_dqYfvAt1PhKekZl3Q.png)

![](https://cdn-images-1.medium.com/max/3832/1*d8Pl82p22heleolCKMnZbQ.png)

## How to Get Started

## Setting Up the Project

 1. Clone the Repository: Begin by cloning the repository from GitHub:

* git clone https://github.com/Stefen-Taime/build_api_devops_pipeline cd build_api_devops_pipeline

 1. Start the Services: Launch the services using Docker Compose:

* docker-compose up --build

## Installing Kubernetes Locally

 1. Navigate to Kubernetes Directory: Go to the k8/kind directory.

 2. Install Kubernetes with Kind:

* Download the Kind binary:

* curl -Lo ./kind [https://kind.sigs.k8s.io/dl/v0.11.1/kind-linux-amd64](https://kind.sigs.k8s.io/dl/v0.11.1/kind-linux-amd64)

* Make it executable:

* chmod +x ./kind

* Move it to a system directory:

* sudo mv ./kind /usr/local/bin/kind

 1. Configure the Kubernetes Cluster:

* Update the .yaml file with your host machine's IP address, which can be obtained via ifconfig.

* Create a Kubernetes cluster with two nodes (one master and one worker):

* kind create cluster --config kind-cluster-config.yaml

 1. Verify the Cluster:

* Check the pods:

* kubectl get pods

* Check the nodes:

* kubectl get nodes -o wide

* To delete the cluster, use:

* kind delete cluster

## Setting Up Jenkins for CI/CD Pipeline

 1. Access Jenkins: Go to Jenkins on localhost:8080 and complete the initial setup (install default plugins, set up an admin user).

 2. Install Required Plugins: Install the following plugins:

* Prometheus

* Email Extension Template

* SonarQube Scanner

* nodejs

* docker-workflow

* kubernetes

* docker-commons

* docker-pipeline

* docker-api

* docker-build-step

* kubernetes-credentials

* kubernetes-client-api

* kubernetes-cli

* kubernetes-credential-provider

* owasp-dependency-check

 1. Restart Jenkins: Apply the changes by restarting Jenkins.

 2. Configure Credentials: Create four credentials as shown in :

![](https://cdn-images-1.medium.com/max/3812/1*dKQw0J6ZGEV9J8CqUVPNBg.png)

* Docker credentials (ID: docker) with your DockerHub email and password.

* Mail credentials (ID: mail) with your Gmail address and an app password obtained from Gmail security settings.

* SonarQube token (ID: sonar-token). Generate this by creating a project on SonarQube, setting a webhook to http://172.20.0.2:8080/sonarqube-webhook, and creating a user token starting with sqp_.

* Kubernetes config file (ID: kubeconfig-file). Use your kubeconfig file or the output of cat ~/.kube/config on your host machine.

 1. Jenkins Tool Configuration: Add installations for JDK, Node.js, Docker, Dependency-Check, and SonarQube Scanner (version 4.8.1).

 2. Configure Environment Variables: In Jenkins system settings, add an environment variable sonar-server with the URL http://172.20.0.3:9000 and use the sonar-token.

 3. Email Notification Setup:

* Set SMTP server to smtp.gmail.com, port to 465, default content type to HTML.

* In advanced settings, enable SMTP authentication with your Gmail credentials and SSL protocol.

 1. Create a Jenkins Pipeline: Create a new pipeline item and configure it using the Jenkinsfile. Ensure to modify it with your Docker username and SonarQube token.

 2. Deploy and Test: After a successful build, you should receive an email notification. For API testing, execute:

* kubectl port-forward pod/api-devops-68bf7cf4f6-45l8p 5000:8000

 1. Then, navigate to localhost:5000/docs to access the FastAPI endpoints.

 2. Monitoring with Grafana: Access Grafana on localhost:3000, add Prometheus (http://172.20.0.4:9090) as a data source, and import dashboard ID 9964 from [Grafana Dashboard](https://grafana.com/grafana/dashboards/9964-jenkins-performance-and-health-overview/).
