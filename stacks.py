import requests

def get_rancher_projects (rancher_url):
    session = requests.session()
    projects = {}

    response = session.get(f'{rancher_url}/projects/', auth=rancher_auth, verify=verify_ssl)
    for project in response.json()["data"]:
        projects[project["id"]] = {"env": project["name"], "hosts": {}}
    return projects

def parse_rancher_stacks(projects, rancher_url, stack_name):
    session = requests.session()
    env_list = []
    for project in projects:
        #print(project)
        url = f'{rancher_url}/projects/{project}/stacks/'
        response = session.get(url, auth=rancher_auth, verify=verify_ssl)
        data = response.json()["data"]
        print(f'~~~~~ Parsing Stack Data in {projects[project]["env"]}, searching for {stack_name} stack ~~~~~')
        for stack in data:
            if stack['name'] == stack_name:
                env_list.append(projects[project]["env"])
                print(f'~~~~~ Found {stack_name} in the {projects[project]["env"]}~~~')
    return env_list


rancher_auth = ('<rancher_access_key>', '<rancher_secret_key>')
rancher_url = '<rancher_url>'
verify_ssl = True

projects = get_rancher_projects(rancher_url)
print(parse_rancher_stacks(projects, rancher_url, stack_name='<stack_name>'))