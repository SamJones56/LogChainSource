# Installing Application and Tools

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

# Using the Application
Okay so I have made a few changes to the app to acomodate user generated passwords.

> Start docker: `./init.sh`
>     Docker compose starts, output `x UP`
> 
> Enter docker containers `sudo docker exec -it [name] /bin/bash`
> 
> To initiate Genesis: `python3 genesisInit.py`
>     You will be prompted for password, this encrypts the kyber private key file.
>     Wait for `GENESIS DONE`
> 
> To initiate Nodes: `python3 nodeInit.py`
>     Wait for `NODE DONE`
> 
> To upload from Node do `python3 logPoster.py`
>     You will be prompted for path to log file, path for generating a copy of the log file, stream name `data`, and to start a listener on the log file `y` or `no`
>         Example file path `/var/log/alternatives.log`
> 
> To start the web app and read from the `data` stream on Genesis do `./web.sh`
>     You will be prompted for two passwords: 
>         1. Kyber private key file password you set earlier
>         2. New password to encrypt downloaded log file
>     Access the webpage at `http://172.18.0.2:8000/` to view log files