1. Install Docker

  https://docs.docker.com/engine/install/ubuntu/

2. Install git
 
  sudo apt update

  sudo apt install git -y


4. Install Vscode

  sudo snap install --classic code

5. Get docker, github, python extension on vscode
6. Sign into github on vscode

7. Create directories

  mkdir ~/src
  
  mkdir ~/src/multichain (this is where the images get saved)

9. Change directory to LogChainSource & clone repo

  cd ~/src/
  
  Clone the repo:
  
  git clone https://github.com/SamJones56/LogChainSource.git

10. Build and run
  
  cd LogChainSource
  
  sudo ./init.sh

11. Enter docker container
  
  sudo docker exec -it [containerName] /bin/bash

12. Prune for debugging
  
  sudo docker system prune -a

