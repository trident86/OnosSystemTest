import os
import json
import requests
from requests.auth import HTTPBasicAuth

"""
**************************** SONA Functions START ****************************
"""

def openstack_network_create( main, base_url, config_path ):
    """
    Create openstack network
    """
    if os.path.exists(config_path):
        json_data = open(config_path).read()
    else:
        return False

    main.log.info("data: {}".format( json_data ) )
    payload = json.loads(json_data)

    headers = {'Content-Type': 'application/json'}
    data = json.dumps(payload, sort_keys=True, indent=4)
    main.log.info("payload: {}".format( data ) )
    resp = requests.post(base_url + "/onos/openstacknetworking/networks",
                    headers=headers,
                    auth=HTTPBasicAuth('onos', 'rocks'),
                    data=json.dumps(payload));
    main.log.info("resp: {}, {}".format( resp.status_code, resp.text ) )
    return True if resp.status_code == 201 else False

def openstack_network_update( main, base_url, config_path ):
    """
    Update openstack network
    """
    if os.path.exists(config_path):
        json_data = open(config_path).read()
    else:
        return False

    main.log.info("data: {}".format( json_data ) )
    payload = json.loads(json_data)

    headers = {'Content-Type': 'application/json'}
    data = json.dumps(payload, sort_keys=True, indent=4)
    main.log.info("payload: {}".format( data ) )
    resp = requests.put(base_url + "/onos/openstacknetworking/networks/" + payload["network"]["id"],
                    headers=headers,
                    auth=HTTPBasicAuth('onos', 'rocks'),
                    data=json.dumps(payload));
    main.log.info("resp: {}, {}".format( resp.status_code, resp.text ) )
    return True if resp.status_code == 200 else False

def openstack_network_remove( main, base_url, config_path ):
    """
    Remove openstack network
    """
    if os.path.exists(config_path):
        json_data = open(config_path).read()
    else:
        return False
    main.log.info("data: {}".format( json_data ) )
    payload = json.loads(json_data)

    headers = {'Content-Type': 'application/json'}
    data = json.dumps(payload, sort_keys=True, indent=4)
    main.log.info("payload: {}".format( data ) )
    resp = requests.delete(base_url + "/onos/openstacknetworking/networks/" + data.network.id,
                    headers=headers,
                    auth=HTTPBasicAuth('onos', 'rocks'));
    main.log.info("resp: {}, {}".format( resp.status_code, resp.text ) )
    return True if resp.status_code == 204 else False

def openstack_subnet_create( main, base_url, config_path ):
    """
    Create openstack subnet
    """
    if os.path.exists(config_path):
        json_data = open(config_path).read()
    else:
        return False
    main.log.info("data: {}".format( json_data ) )
    payload = json.loads(json_data)

    headers = {'Content-Type': 'application/json'}
    data = json.dumps(payload, sort_keys=True, indent=4)
    main.log.info("payload: {}".format( data ) )
    resp = requests.post(base_url + "/onos/openstacknetworking/subnets",
                    headers=headers,
                    auth=HTTPBasicAuth('onos', 'rocks'),
                    data=json.dumps(payload));
    main.log.info("resp: {}, {}".format( resp.status_code, resp.text ) )
    return True if resp.status_code == 201 else False

def openstack_subnet_update( main, base_url, config_path ):
    """
    Update openstack subnet
    """
    if os.path.exists(config_path):
        json_data = open(config_path).read()
    else:
        return False
    main.log.info("data: {}".format( json_data ) )
    payload = json.loads(json_data)

    headers = {'Content-Type': 'application/json'}
    data = json.dumps(payload, sort_keys=True, indent=4)
    main.log.info("payload: {}".format( data ) )
    resp = requests.put(base_url + "/onos/openstacknetworking/subnets/" + data.subnet.id,
                    headers=headers,
                    auth=HTTPBasicAuth('onos', 'rocks'),
                    data=json.dumps(payload));
    main.log.info("resp: {}, {}".format( resp.status_code, resp.text ) )
    return True if resp.status_code == 200 else False

def openstack_subnet_remove( main, base_url, config_path ):
    """
    Remove openstack subnet
    """
    if os.path.exists(config_path):
        json_data = open(config_path).read()
    else:
        return False
    main.log.info("data: {}".format( json_data ) )
    payload = json.loads(json_data)

    headers = {'Content-Type': 'application/json'}
    data = json.dumps(payload, sort_keys=True, indent=4)
    main.log.info("payload: {}".format( data ) )
    resp = requests.delete(base_url + "/onos/openstacknetworking/subnets/" + data.subnet.id,
                    headers=headers,
                    auth=HTTPBasicAuth('onos', 'rocks'));
    main.log.info("resp: {}, {}".format( resp.status_code, resp.text ) )
    return True if resp.status_code == 204 else False

def openstack_port_create( main, base_url, config_path ):
    """
    Create openstack port
    """
    if os.path.exists(config_path):
        json_data = open(config_path).read()
    else:
        return False
    main.log.info("data: {}".format( json_data ) )
    payload = json.loads(json_data)

    headers = {'Content-Type': 'application/json'}
    data = json.dumps(payload, sort_keys=True, indent=4)
    main.log.info("payload: {}".format( data ) )
    resp = requests.post(base_url + "/onos/openstacknetworking/ports",
                    headers=headers,
                    auth=HTTPBasicAuth('onos', 'rocks'),
                    data=json.dumps(payload));
    main.log.info("resp: {}, {}".format( resp.status_code, resp.text ) )
    return True if resp.status_code == 201 else False

def openstack_port_update( main, base_url, config_path ):
    """
    Update openstack port
    """
    if os.path.exists(config_path):
        json_data = open(config_path).read()
    else:
        return False
    main.log.info("data: {}".format( json_data ) )
    payload = json.loads(json_data)

    headers = {'Content-Type': 'application/json'}
    data = json.dumps(payload, sort_keys=True, indent=4)
    main.log.info("payload: {}".format( data ) )
    resp = requests.put(base_url + "/onos/openstacknetworking/ports/" + data.port.id,
                    headers=headers,
                    auth=HTTPBasicAuth('onos', 'rocks'),
                    data=json.dumps(payload));
    main.log.info("resp: {}, {}".format( resp.status_code, resp.text ) )
    return True if resp.status_code == 200 else False

def openstack_port_remove( main, base_url, config_path ):
    """
    Remove openstack port
    """
    if os.path.exists(config_path):
        json_data = open(config_path).read()
    else:
        return False
    main.log.info("data: {}".format( json_data ) )
    payload = json.loads(json_data)

    headers = {'Content-Type': 'application/json'}
    data = json.dumps(payload, sort_keys=True, indent=4)
    main.log.info("payload: {}".format( data ) )
    resp = requests.delete(base_url + "/onos/openstacknetworking/ports/" + data.port.id,
                    headers=headers,
                    auth=HTTPBasicAuth('onos', 'rocks'));
    main.log.info("resp: {}, {}".format( resp.status_code, resp.text ) )
    return True if resp.status_code == 204 else False

def openstack_floatingip_create( main, base_url, config_path ):
    """
    Create openstack floatingip
    """
    if os.path.exists(config_path):
        json_data = open(config_path).read()
    else:
        return False
    main.log.info("data: {}".format( json_data ) )
    payload = json.loads(json_data)

    headers = {'Content-Type': 'application/json'}
    data = json.dumps(payload, sort_keys=True, indent=4)
    main.log.info("payload: {}".format( data ) )
    resp = requests.post(base_url + "/onos/openstacknetworking/floatingips",
                    headers=headers,
                    auth=HTTPBasicAuth('onos', 'rocks'),
                    data=json.dumps(payload));
    main.log.info("resp: {}, {}".format( resp.status_code, resp.text ) )
    return True if resp.status_code == 201 else False

def openstack_floatingip_update( main, base_url, config_path ):
    """
    Update openstack floatingip
    """
    if os.path.exists(config_path):
        json_data = open(config_path).read()
    else:
        return False
    main.log.info("data: {}".format( json_data ) )
    payload = json.loads(json_data)

    headers = {'Content-Type': 'application/json'}
    data = json.dumps(payload, sort_keys=True, indent=4)
    main.log.info("payload: {}".format( data ) )
    resp = requests.put(base_url + "/onos/openstacknetworking/floatingips/" + data.floatingip.id,
                    headers=headers,
                    auth=HTTPBasicAuth('onos', 'rocks'),
                    data=json.dumps(payload));
    main.log.info("resp: {}, {}".format( resp.status_code, resp.text ) )
    return True if resp.status_code == 200 else False

def openstack_floatingip_remove( main, base_url, config_path ):
    """
    Remove openstack floatingip
    """
    if os.path.exists(config_path):
        json_data = open(config_path).read()
    else:
        return False
    main.log.info("data: {}".format( json_data ) )
    payload = json.loads(json_data)

    headers = {'Content-Type': 'application/json'}
    data = json.dumps(payload, sort_keys=True, indent=4)
    main.log.info("payload: {}".format( data ) )
    resp = requests.delete(base_url + "/onos/openstacknetworking/floatingips/" + data.floatingip.id,
                    headers=headers,
                    auth=HTTPBasicAuth('onos', 'rocks'));
    main.log.info("resp: {}, {}".format( resp.status_code, resp.text ) )
    return True if resp.status_code == 204 else False

def openstack_security_group_rule_create( main, base_url, config_path ):
    """
    Create openstack security_group_rule
    """
    import json
    import requests
    from requests.auth import HTTPBasicAuth

    json_data=open(config_path).read()
    main.log.info("data: {}".format( json_data ) )
    payload = json.loads(json_data)

    headers = {'Content-Type': 'application/json'}
    data = json.dumps(payload, sort_keys=True, indent=4)
    main.log.info("payload: {}".format( data ) )
    resp = requests.post(base_url + "/onos/openstacknetworking/security-group-rules",
                    headers=headers,
                    auth=HTTPBasicAuth('onos', 'rocks'),
                    data=json.dumps(payload));
    main.log.info("resp: {}, {}".format( resp.status_code, resp.text ) )
    return True if resp.status_code == 201 else False

def openstack_security_group_rule_remove( main, base_url, config_path ):
    """
    Remove openstack security_group_rule
    """
    import json
    import requests
    from requests.auth import HTTPBasicAuth

    json_data=open(config_path).read()
    main.log.info("data: {}".format( json_data ) )
    payload = json.loads(json_data)

    headers = {'Content-Type': 'application/json'}
    data = json.dumps(payload, sort_keys=True, indent=4)
    main.log.info("payload: {}".format( data ) )
    resp = requests.delete(base_url + "/onos/openstacknetworking/security-group-rules" + data.security_group_rule.id,
                    headers=headers,
                    auth=HTTPBasicAuth('onos', 'rocks'));
    main.log.info("resp: {}, {}".format( resp.status_code, resp.text ) )
    return True if resp.status_code == 204 else False

def openstack_security_group_create( main, base_url, config_path ):
    """
    Create openstack security_group
    """
    import json
    import requests
    from requests.auth import HTTPBasicAuth

    json_data=open(config_path).read()
    main.log.info("data: {}".format( json_data ) )
    payload = json.loads(json_data)

    headers = {'Content-Type': 'application/json'}
    data = json.dumps(payload, sort_keys=True, indent=4)
    main.log.info("payload: {}".format( data ) )
    resp = requests.post(base_url + "/onos/openstacknetworking/security-groups",
                    headers=headers,
                    auth=HTTPBasicAuth('onos', 'rocks'),
                    data=json.dumps(payload));
    main.log.info("resp: {}, {}".format( resp.status_code, resp.text ) )
    return True if resp.status_code == 201 else False

def openstack_security_group_update( main, base_url, config_path ):
    """
    Update openstack security_group
    """
    import json
    import requests
    from requests.auth import HTTPBasicAuth

    json_data=open(config_path).read()
    main.log.info("data: {}".format( json_data ) )
    payload = json.loads(json_data)

    headers = {'Content-Type': 'application/json'}
    data = json.dumps(payload, sort_keys=True, indent=4)
    main.log.info("payload: {}".format( data ) )
    resp = requests.put(base_url + "/onos/openstacknetworking/security-groups/" + data.security_group.id,
                    headers=headers,
                    auth=HTTPBasicAuth('onos', 'rocks'),
                    data=json.dumps(payload));
    main.log.info("resp: {}, {}".format( resp.status_code, resp.text ) )
    return True if resp.status_code == 200 else False

def openstack_security_group_remove( main, base_url, config_path ):
    """
    Remove openstack security_group
    """
    import json
    import requests
    from requests.auth import HTTPBasicAuth

    json_data=open(config_path).read()
    main.log.info("data: {}".format( json_data ) )
    payload = json.loads(json_data)

    headers = {'Content-Type': 'application/json'}
    data = json.dumps(payload, sort_keys=True, indent=4)
    main.log.info("payload: {}".format( data ) )
    resp = requests.delete(base_url + "/onos/openstacknetworking/security-groups/" + data.security_group.id,
                    headers=headers,
                    auth=HTTPBasicAuth('onos', 'rocks'));
    main.log.info("resp: {}, {}".format( resp.status_code, resp.text ) )
    return True if resp.status_code == 204 else False

def openstack_router_create( main, base_url, config_path ):
    """
    Create openstack router
    """
    import json
    import requests
    from requests.auth import HTTPBasicAuth

    json_data=open(config_path).read()
    main.log.info("data: {}".format( json_data ) )
    payload = json.loads(json_data)

    headers = {'Content-Type': 'application/json'}
    data = json.dumps(payload, sort_keys=True, indent=4)
    main.log.info("payload: {}".format( data ) )
    resp = requests.post(base_url + "/onos/openstacknetworking/routers",
                    headers=headers,
                    auth=HTTPBasicAuth('onos', 'rocks'),
                    data=json.dumps(payload));
    main.log.info("resp: {}, {}".format( resp.status_code, resp.text ) )
    return True if resp.status_code == 201 else False

def openstack_router_update( main, base_url, config_path ):
    """
    Update openstack router
    """
    import json
    import requests
    from requests.auth import HTTPBasicAuth

    json_data=open(config_path).read()
    main.log.info("data: {}".format( json_data ) )
    payload = json.loads(json_data)

    headers = {'Content-Type': 'application/json'}
    data = json.dumps(payload, sort_keys=True, indent=4)
    main.log.info("payload: {}".format( data ) )
    resp = requests.put(base_url + "/onos/openstacknetworking/routers/" + data.id,
                    headers=headers,
                    auth=HTTPBasicAuth('onos', 'rocks'),
                    data=json.dumps(payload));
    main.log.info("resp: {}, {}".format( resp.status_code, resp.text ) )
    return True if resp.status_code == 200 else False

def openstack_router_add_interface( main, base_url, config_path ):
    """
    Update openstack router with adding router interface
    """
    import json
    import requests
    from requests.auth import HTTPBasicAuth

    json_data=open(config_path).read()
    main.log.info("data: {}".format( json_data ) )
    payload = json.loads(json_data)

    headers = {'Content-Type': 'application/json'}
    data = json.dumps(payload, sort_keys=True, indent=4)
    main.log.info("payload: {}".format( data ) )
    resp = requests.put(base_url + "/onos/openstacknetworking/routers/" + data.id + "/add_router_interface",
                    headers=headers,
                    auth=HTTPBasicAuth('onos', 'rocks'),
                    data=json.dumps(payload));
    main.log.info("resp: {}, {}".format( resp.status_code, resp.text ) )
    return True if resp.status_code == 200 else False

def openstack_router_remove_interface( main, base_url, config_path ):
    """
    Update openstack router with removing router interface
    """
    import json
    import requests
    from requests.auth import HTTPBasicAuth

    json_data=open(config_path).read()
    main.log.info("data: {}".format( json_data ) )
    payload = json.loads(json_data)

    headers = {'Content-Type': 'application/json'}
    data = json.dumps(payload, sort_keys=True, indent=4)
    main.log.info("payload: {}".format( data ) )
    resp = requests.put(base_url + "/onos/openstacknetworking/routers/" + data.id + "/remove_router_interface",
                    headers=headers,
                    auth=HTTPBasicAuth('onos', 'rocks'),
                    data=json.dumps(payload));
    main.log.info("resp: {}, {}".format( resp.status_code, resp.text ) )
    return True if resp.status_code == 200 else False

def openstack_router_remove( main, base_url, config_path ):
    """
    Remove openstack router
    """
    import json
    import requests
    from requests.auth import HTTPBasicAuth

    json_data=open(config_path).read()
    main.log.info("data: {}".format( json_data ) )
    payload = json.loads(json_data)

    headers = {'Content-Type': 'application/json'}
    data = json.dumps(payload, sort_keys=True, indent=4)
    main.log.info("payload: {}".format( data ) )
    resp = requests.delete(base_url + "/onos/openstacknetworking/routers/" + data.id,
                    headers=headers,
                    auth=HTTPBasicAuth('onos', 'rocks'));
    main.log.info("resp: {}, {}".format( resp.status_code, resp.text ) )
    return True if resp.status_code == 204 else False

"""
**************************** SONA Functions END ****************************
"""

