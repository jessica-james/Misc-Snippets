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


def get_rancher_hosts (rancher_auth, verify_ssl):
    session = requests.session()
    response = session.get(f'{rancher_url}/hosts?limit=1500', auth=rancher_auth, verify=verify_ssl)

    return response.json()["data"]


def map_rancher_hosts_to_project (hosts, projects):
    host_env_list = []
    sjc_hosts = []
    rtp_hosts = []
    gpk_hosts = []
    bgl_hosts = []
    for host in hosts:
        project = host["accountId"]
        host_id = host["id"]
        hostname = host["data"]["fields"]["hostname"]

        if "crate.region" in host["data"]["fields"]["labels"]:
            region = host["data"]["fields"]["labels"]["crate.region"]
        else:
            region = "NotFound"
        if "crate.host.name" in host["data"]["fields"]["labels"]:
            short_name = host["data"]["fields"]["labels"]["crate.host.name"]
        else:
            short_name = "NotFound"

        projects[project]["hosts"][host_id] = {
            "hostname"  : hostname,
            "region"    : region,
            "short_name": short_name
        }

        if projects[project]["hosts"][host_id]["region"] == "csc-us-east-rtp5-1":
            rtp_hosts.append(projects[project]["hosts"][host_id]["hostname"])
        elif projects[project]["hosts"][host_id]["region"] == "csc-us-east-rtp5-2":
            rtp_hosts.append(projects[project]["hosts"][host_id]["hostname"])
        elif projects[project]["hosts"][host_id]["region"] == "csc-eu-west-gpk-1":
            gpk_hosts.append(projects[project]["hosts"][host_id]["hostname"])
        elif projects[project]["hosts"][host_id]["region"] == "csc-us-west-sjck-1":
            sjc_hosts.append(projects[project]["hosts"][host_id]["hostname"])
        elif projects[project]["hosts"][host_id]["region"] == "csc-sa-west-bgl11-1":
            bgl_hosts.append(projects[project]["hosts"][host_id]["hostname"])

    for project in projects:
        num_hosts = len(projects[project]["hosts"].values())
        host_env_list.append([num_hosts, projects[project]["env"]])

    print(f'BGL hosts is {len(bgl_hosts)}')
    print(f'GPK hosts is {len(gpk_hosts)}')
    print(f'SJC hosts is {len(sjc_hosts)}')
    print(f'RTP hosts is {len(rtp_hosts)}')


    return projects, host_env_list



rancher_auth = ('<rancher_access_key>', '<rancher_secret_key>')
rancher_url = '<rancher_url>'
verify_ssl = True


projects = get_rancher_projects(rancher_url, rancher_auth, verify_ssl)
hosts = get_rancher_hosts(rancher_auth, verify_ssl)
mapped_projects = map_rancher_hosts_to_project(hosts, projects)


