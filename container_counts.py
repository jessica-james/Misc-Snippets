import requests

def get_rancher_projects (rancher_url, rancher_auth, verify_ssl):
    session = requests.session()
    projects = {}
    auth = rancher_auth
    verify = verify_ssl
    response = session.get(f'{rancher_url}/projects/', auth=auth, verify=verify)
    for project in response.json()["data"]:
        projects[project["id"]] = {"env": project["name"], "hosts": {}}
    return projects


def map_rancher_hosts_to_project (projects):
    session = requests.session()
    container_projects = projects
    total_system_containers = 0
    total_user_containers = 0


    for project in container_projects:
        container_projects[project]['system_containers'] = 0
        container_projects[project]['user_containers'] = 0
        system = 0
        user = 0
        print(f'~~~~~ Parsing container data for {container_projects[project]["env"]} ~~~~~')
        container_data = session.get(f'{rancher_url}/projects/{project}/containers?limit=1000', auth=rancher_auth, verify=verify_ssl)
        #print(container_data.json()["data"])
        try:
            for key in container_data.json()["data"]:
                container_projects[project]['containers'] = key
                if container_projects[project]['containers']['system'] == True:
                    system += 1
                elif container_projects[project]['containers']['system'] == False:
                    user += 1
            container_projects[project]['system_containers'] = system
            container_projects[project]['user_containers'] = user

        except KeyError:
            pass
        total_system_containers = int(total_system_containers) + int(container_projects[project]['system_containers'])
        total_user_containers = int(total_user_containers) + int(container_projects[project]['user_containers'])

    print(f'~~~~ There are {total_system_containers} total system containers in Rancher ~~~~~')
    print(f'~~~~ There are {total_user_containers} total user containers in Rancher ~~~~~')
    return container_projects


rancher_auth = ('<rancher_access_key>', '<rancher_secret_key>')
rancher_url = '<rancher_url>'
verify_ssl = True


projects = get_rancher_projects(rancher_url, rancher_auth, verify_ssl)
mapped_projects = map_rancher_hosts_to_project(projects)


