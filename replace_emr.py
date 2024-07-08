# Verify that emr-manager-app is running for the correct region and that you can access the swagger page at port 9461

from urllib import request, parse, error
import json
import sys

if(len(sys.argv) < 3):
    print("Use the format: python3 replace_emr.py <list/replace/status> <read_goals/read/read_large>")
    sys.exit(1)

supported_cluster_types = ["read_goals", "read", "read_large"]
supported_op_types = ["list", "replace", "status"]

op_type = sys.argv[1]
cluster_type = sys.argv[2]

if cluster_type not in supported_cluster_types:
    print("Cluster type should be one of: " + ",".join(supported_cluster_types))
    sys.exit(1)

if op_type not in supported_op_types:
    print("Operation type should be one of: " + ",".join(supported_op_types))
    sys.exit(1)

if(op_type == "list"):
    try:
        with request.urlopen("http://localhost:9461/api/1/emr/cluster?managedOnly=true&type=" + cluster_type) as url:
            data = json.load(url)
            print("Clusters found:")
            print(json.dumps(data, indent=4))
    except error.URLError:
        print("Connection error! Verify that emr-manager-app is running locally")
        sys.exit(1)

if(op_type == "status"):
    try:
        with request.urlopen("http://localhost:9461/api/1/emr/cluster/replace/status") as url:
            data = json.load(url)
            print(json.dumps(data, indent=4))
    except error.URLError:
        print("Connection error! Verify that emr-manager-app is running locally")
        sys.exit(1)

if(op_type == "replace"):
    try:
        with request.urlopen("http://localhost:9461/api/1/emr/cluster?managedOnly=true&type=" + cluster_type) as url:
            data = json.load(url)
        for cluster in data:
            print("Going to replace:" + cluster)    
            req_data = parse.urlencode("").encode()
            replace_req = request.Request("http://localhost:9461/api/1/emr/cluster/replace?clusterId=" + cluster + "&forceDuplicateReplacement=false");
            with request.urlopen(replace_req, data=req_data) as url:
                data = json.load(url)
                print("Response for cluster "+ cluster + ":" + data)
    except error.URLError:
        print("Connection error! Verify that emr-manager-app is running locally")
        sys.exit(1)
