import yaml
import json
import subprocess

# yaml парсер 
def main():
    with open("group_vars/prod/vault_db.yml", "r") as yaml_file:
        yaml_conf = yaml.safe_load(yaml_file) 
    #print(yaml_conf)    
    #print(type(yaml_conf))
    for key, value in yaml_conf.items():
        #print(value)
        #print(type(value))
        for projects in value:
            #print(projects)
            for item in projects.items():
                if item[0] == 'project':
                    name_project = item[1]
                if item[0] == 'db_user':    
                    db_user = item[1]
                if item[0] == 'db_pass':   
                    db_pass = item[1]   
                    #print(f"Project: {name_project}, User_DB: {db_user}, DB_PASSWORD: {db_pass}")  
                    with open('.gitlab-ci/test.json', 'r+') as f:
                        data = json.load(f)    
                        data['name'] = "DB_" + name_project # <--- add `id` value.
                        data['login']['username'] = db_user  
                        data['login']['password'] = db_pass
                        data['login']['notes'] = "mysql server 10.213.65.221 port 3306"
                        f.seek(0)  # <--- should reset file position to the beginning.
                        json.dump(data, f, indent=4)
                        f.truncate() # remove remaining part
                        ###
                        send_bw = subprocess.Popen([".gitlab-ci/send_to_bw.sh", "\"name\":\"DB_" + name_project] , stdout=subprocess.PIPE)
                        data = send_bw.communicate()
                        #print(f"Project: {name_project}, User_DB: {db_user}, DB_PASSWORD: {db_pass}")    
                        print(data)
                        ###


if __name__ == '__main__':
    main()