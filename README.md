# Pasos para montar todo el proyecto con docker en Linux-Ubuntu

## Actualiza la lista de paquetes disponibles desde los repositorios configurados:
sudo apt-get update

## Instalar los paquetes necesarios para que apt pueda utilizar repositorios sobre HTTPS:
sudo apt-get install apt-transport-https ca-certificates curl software-properties-common

## Agregar la clave GPG oficial de Docker en sistemas Linux basados en Ubuntu:
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg

## Agregar el repositorio de Docker al sistema:
echo "deb [arch=amd64 signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

## Actualizar nuevamente el índice de paquetes:
sudo apt-get update

## Instalar Docker:
sudo apt-get install docker-ce

## Con docker instalado ejecutamos el docker-compose:
docker compose up -d --build

# Nota: Construye y ejecuta en segundo plano todos los servicios definidos en el archivo docker-compose.yml
