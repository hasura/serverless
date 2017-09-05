import json, subprocess

fui = {
    '/': {
        'enableAuth': True,
        'enableCORS': True,
        'enableWebsockets': True,
        'restrictToRoles': ['admin'],
        'upstreamService': {
            'name': 'fission-ui',
            'namespace': 'fission'
        },
        'upstreamServicePath': '/',
        'upstreamServicePort': 80
    }
}

frouter = {
    '/': {
        'enableAuth': True,
        'enableCORS': True,
        'enableWebsockets': True,
        'restrictToRoles': ['user'],
        'upstreamService': {
            'name': 'router',
            'namespace': 'fission'
        },
        'upstreamServicePath': '/',
        'upstreamServicePort': 80
    }
}


print "get configmap"
proc = subprocess.Popen("kubectl get configmaps hasura-project-conf -o json", stdout=subprocess.PIPE, shell=True)

project_conf = proc.stdout.read()

print "modifying hasura project conf"

j = json.loads(project_conf)

project = json.loads(j['data']['project'])
project['gateway']['httpRoutes']['fission-ui'] = fui
project['gateway']['httpRoutes']['fission-router'] = frouter
j['data']['project'] = json.dumps(project)

new_project_conf = json.dumps(j)

print "replace configmap"
proc = subprocess.Popen(["kubectl", "replace", "-f", "-"], stdin=subprocess.PIPE)
proc.communicate(new_project_conf)
