# Utilisation d'Ubuntu 22.04 comme image de base
FROM ubuntu:22.04

# Mise à jour des paquets et installation des dépendances nécessaires
RUN apt-get update && \
    apt-get install -y wget tar

# Définition de la version de Prometheus à utiliser
ARG PROMETHEUS_VERSION="2.32.1"
ARG PROMETHEUS_USER="prometheus"

# Création d'un utilisateur pour Prometheus (sécurité)
RUN useradd --no-create-home --shell /bin/false ${PROMETHEUS_USER}

# Téléchargement et installation de Prometheus
RUN cd /tmp && \
    wget https://github.com/prometheus/prometheus/releases/download/v${PROMETHEUS_VERSION}/prometheus-${PROMETHEUS_VERSION}.linux-amd64.tar.gz && \
    tar xvf prometheus-${PROMETHEUS_VERSION}.linux-amd64.tar.gz && \
    mv prometheus-${PROMETHEUS_VERSION}.linux-amd64 /etc/prometheus && \
    chown -R ${PROMETHEUS_USER}:${PROMETHEUS_USER} /etc/prometheus

# Exposer le port par défaut de Prometheus
EXPOSE 9090

# Configuration des chemins de stockage et des fichiers de configuration
VOLUME [ "/etc/prometheus" ]

RUN mkdir -p /prometheus && chown -R prometheus:prometheus /prometheus


# Définition de l'utilisateur
USER ${PROMETHEUS_USER}

# Définition du point d'entrée pour démarrer Prometheus
ENTRYPOINT [ "/etc/prometheus/prometheus" ]
CMD [ "--config.file=/etc/prometheus/prometheus.yml", "--storage.tsdb.path=/prometheus" ]
