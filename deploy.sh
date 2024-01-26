#!/bin/sh

if ["$1" == ""]; then
    echo "Please enter version"
    exit 1
fi

echo "Upgrading material_server to v-${1}"

wget https://github.com/1md3nd/materials_backend/archive/refs/tags/${1}.zip -O demo.zip
# wget https://github.com/1md3nd/materials_backend/archive/refs/tags/v0.1.0-alpha.zip -0 demo.zip
 
unzip demo.zip
cd material_backend-${1}

sudo apt-get install docker
sudo docker build -t server:${1} .
sudo docker run -p 8000:8000 server:${1}
 