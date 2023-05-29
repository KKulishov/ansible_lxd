#!/bin/bash

project_name=$1

## organizationId Webpractik
## collectionIds Ansible

organizationId="9176a30f-c1b1-4261-ad47-5946403eeb03"
collectionIds="8ce06304-3cd6-4b98-a777-615ef8bf0ec0"

bw config server https://bw.w6p.ru

bw login --apikey
bw unlock --passwordenv BW_PASSWORD > .env_vault
export `cat .env_vault | grep env:BW_SESSION | awk {'print$2'} | awk -F ":" {'print$2'}`

#обновить индексы
bw sync --session $BW_SESSION

project_name_bw=$(bw list items --collectionid $collectionIds --session $BW_SESSION | grep $project_name)

#echo project_name_bw: $project_name_bw
#echo "\n"
echo project_name: $project_name

if [[ -z "$project_name_bw" ]]; then
	echo "create $project_name"
	cat .gitlab-ci/test.json | bw encode --session $BW_SESSION | bw create item --session $BW_SESSION
else
	echo "Project Creation Skip $project_name , this project already exists in vaultwarden"
fi	
