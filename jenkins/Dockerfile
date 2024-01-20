# Utilisation d'Ubuntu 22.04 comme image de base
FROM ubuntu:22.04

# Mise à jour des paquets et installation de Java, Python et du paquet python3-venv pour les environnements virtuels Python
RUN apt-get update -y && \
    apt-get install -y openjdk-11-jre python3 python3-pip python3.10-venv && \
    java --version && \
    python3 --version


# Installation de Docker
RUN apt-get update && \
    apt-get install -y docker.io

# Vérification et création du groupe docker si nécessaire
RUN getent group docker || groupadd docker

# Création des utilisateurs et ajout au groupe docker
# Remarque : Remplacer 'ubuntu' par un utilisateur pertinent si nécessaire
RUN useradd -m jenkins || true && \
    useradd -m ubuntu || true && \
    usermod -aG docker jenkins && \
    usermod -aG docker ubuntu

# Installation de Trivy
RUN apt-get install -y wget apt-transport-https gnupg lsb-release && \
    wget -qO - https://aquasecurity.github.io/trivy-repo/deb/public.key | apt-key add - && \
    echo "deb https://aquasecurity.github.io/trivy-repo/deb $(lsb_release -sc) main" | tee -a /etc/apt/sources.list.d/trivy.list && \
    apt-get update && \
    apt-get install -y trivy

# Installation de curl (nécessaire pour télécharger kubectl et Prometheus)
RUN apt-get install -y curl

# Téléchargement de la dernière version stable de kubectl
RUN curl -sL https://dl.k8s.io/release/stable.txt > /tmp/kubectl_version.txt && \
    KUBECTL_VERSION=$(cat /tmp/kubectl_version.txt) && \
    curl -LO "https://dl.k8s.io/release/${KUBECTL_VERSION}/bin/linux/amd64/kubectl" && \
    chmod +x ./kubectl && \
    mv ./kubectl /usr/local/bin/kubectl

# Téléchargement de Jenkins
RUN mkdir /usr/share/jenkins/ && \
    curl -L https://get.jenkins.io/war-stable/latest/jenkins.war -o /usr/share/jenkins/jenkins.war

# Exposition du port par défaut de Jenkins
EXPOSE 8080

# Démarrage de Jenkins
CMD ["java", "-jar", "/usr/share/jenkins/jenkins.war"]
