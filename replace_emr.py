# Verify that emr-manager-app is running for the correct region and that you can access the swagger page at port 9461

from urllib import request, parse, error
import json
import sys

if(len(sys.argv) < 3):
    print("Use the format: python3 replace_emr.py <list/replace/status> <read_goals/read/read_large/all>")
    sys.exit(1)

supported_cluster_types = ["read_goals", "read", "read_large", "all"]
supported_op_types = ["list", "replace", "status"]

#op_type = sys.argv[1]
#cluster_type = sys.argv[2]

if sys.argv[1] not in supported_op_types:
    print("Operation type should be one of: " + ",".join(supported_op_types))
    sys.exit(1)

if sys.argv[2] not in supported_cluster_types:
    print("Cluster type should be one of: " + ",".join(supported_cluster_types))
    sys.exit(1)

op_type = sys.argv[1]
cluster_type_list = []

if (sys.argv[2] == "all"):
    cluster_type_list.extend(["read_goals", "read", "read_large"])
else:
    cluster_type_list.append(sys.argv[2])

for cluster_type in cluster_type_list:
    if(op_type == "list"):
        try:
            with request.urlopen("http://localhost:9461/api/1/emr/cluster?managedOnly=true&type=" + cluster_type) as url:
                data = json.load(url)
                print("Clusters found for type: {}:".format(cluster_type))
                print(json.dumps(data, indent=4))
        except error.URLError:
            print("Connection error! Verify that emr-manager-app is running locally")
            sys.exit(1)

    if(op_type == "status"):
        try:
            with request.urlopen("http://localhost:9461/api/1/emr/cluster/replace/status") as url:
                data = json.load(url)
                print("Status found for type: {}:".format(cluster_type))
                print(json.dumps(data, indent=4))
        except error.URLError:
            print("Connection error! Verify that emr-manager-app is running locally")
            sys.exit(1)

    if(op_type == "replace"):
        try:
            with request.urlopen("http://localhost:9461/api/1/emr/cluster?managedOnly=true&type=" + cluster_type) as url:
                data = json.load(url)
            print("Replacing clusters for type: {}:".format(cluster_type))
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
