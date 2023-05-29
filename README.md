## Правила описание переменных 

это для переменных который сгруппированы в  hosts.ini для prod среды
```    
group_vars/prod
 ```
vars_nginx.yml для ролей nginx и nginx_config
vars_php.yml для ролей связанные с apache php
vault_db.yml здесь указываем секреты в шифрованном ввиде 
vars.yml здесь описывается структура по котороый сделается root каталог vhost для сервисов , для ролей users,nginx_config,apache_php_[7-9]_conf


# Ansible_simple_projects

- [Дока по репе](https://docs.google.com/document/d/1eD3OtcpRB86voVRGBhQZfd2lFFoWIwGgJF5zUsH_yaw/edit?usp=sharing)

## Установка завимостей 

```sh

ansible-galaxy install -r requirements.yml
```

## Описание host в 
```
hosts.ini
``` 

## Группировка переменных описывается через hosts.ini
```
Сами переменные для ролей находться в group_vars
```
переменные можно описывать и применять в rc 



## Назначение каждой роли переменной 

vars.yml самое главная на основе внесенных пременных зависимые роли nginx_config/apache_*_conf/users



## Для первичной утсновки основных компанентов (перед жтим lxc/vm должны быть создвны и доступны по ssh)

```sh
ansible-playbook -i hosts.ini apache_php7.4.yml --vault-id devops@.pass
ansible-playbook -i hosts.ini apache_php8.0.yml --vault-id devops@.pass
ansible-playbook -i hosts.ini mysql.yml --vault-id devops@.pass
ansible-playbook -i hosts.ini nginx.yml --vault-id devops@.pass
ansible-playbook -i hosts.ini postfix.yml --vault-id devops@.pass
```

## Упрваллвние конфигурацией через переменные в group_vars

```sh
group_vars/prod/*
```

## Для распечатки файла group_vars/prod/vault_db.yml 

```sh
ansible-vault decrypt group_vars/prod/vault_db.yml --vault-id devops@.pass
```

!!! перед этим нужно взять секрет в VAULT с значением VAULT_PASS и содержимое поместить в .pass

и потом не забыть после того как добавили значения нова запечать 

```sh
ansible-vault encrypt group_vars/prod/vault_db.yml --vault-id devops@.pass
```

## Создания сайта и его необходимых компанентов (создание vhost на nginx и apache , создание бд и пользователей в mysql):

```sh
ansible-playbook -i hosts.ini apache_php8.0_conf.yml --vault-id devops@.pass
ansible-playbook -i hosts.ini mysql_config.yml --vault-id devops@.pass
ansible-playbook -i hosts.ini nginx_config.yml --vault-id devops@.pass
```


## Резервное копирование выполняется в контейнере mysql 
переменные для загрузки в s3 описываються в   
```
roles/backup-functions/templates/rclone.conf.j2
```
секреты распологаются в group_vars/prod/vault_db.yml

## Нюансы по интгерации с vaultwarden 
1. На runenr должен быть python не ниже 3.6 + мородули pyyaml, json, subprocess
2. На runenr должен быть установлен bw client cli  (https://bitwarden.com/download/)
3. В CI указаны переменный BW_CLIENTID, BW_CLIENTSECRET, BW_PASSWORD. (https://bitwarden.com/help/cli/)
4. Расшифровка фвайла group_vars/prod/vault_db.yml


## Мониторинг 
1. apache php8  10.213.65.124:8081/server-status
2. apahce php7.4  10.213.65.121:8081/server-status 
3. nginx vts exporter (https://github.com/hnlq715/nginx-vts-exporter) (https://github.com/vozlt/nginx-module-vts) метрики достпны http://10.213.65.137:9913/metrics
4. mysql exporter ( создать пользователя  для  сбора метрик https://learn.netdata.cloud/docs/agent/collectors/go.d.plugin/modules/mysql)
5. netdata [netdata docs](https://learn.netdata.cloud/docs/agent/collectors/go.d.plugin/modules/apache)

## Для просмотра метрик
[netdata](http://status-test.w6p.ru/live)
[nginx_vts](http://status-test.w6p.ru/nginx_status)
[apache_php7.4](http://status-test.w6p.ru/server-status)


## TODO 

1. генерация ssl/tls сертификата , если не указывать alias а просто чисто основное доменное имя то норм , а если нет то выдает ся ошибка так как там ставиться, что в приниципе все и портит , нужно переделаить логику так чтобы анализировать вх. переменную alias_domain и уже на основе нее генерить /tmp/'{{ item.site }}'.ini для послед генерации сертификата
2. Автоматизировать установку goteleport в lxc контейнеры. 


