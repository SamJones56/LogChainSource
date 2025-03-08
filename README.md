1. Install Docker
https://docs.docker.com/engine/install/ubuntu/

2. Install git
sudo apt update
sudo apt install git -y


3. Install Vscode
sudo snap install --classic code

4. Get docker, github, python extension on vscode
5. Sign into github on vscode

6. Create directories
  mkdir ~/src
  mkdir ~/src/multichain (this is where the images get saved)

7. Change directory to LogChainSource & clone repo
  cd ~/src/
  Clone the repo:
  git clone https://github.com/SamJones56/LogChainSource.git

8. Build docker
   sudo docker compose build

9. Run the docker
   sudo docker compose up -d (add -d or you cant keep accessing terminal)

10. Enter docker container
  sudo docker exec -it [containerName] /bin/bash
