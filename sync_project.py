from urllib import request, parse, error
import json
import sys
import time
import traceback


org_id = "cf55d629-88aa-4f05-a338-c2d32358efb9"

# use -m flag to just monitor. i.e python3 sync_project.py -m
just_monitor = True if len(sys.argv) > 1 and sys.argv[1] == '-m' else False

# max hours to monitor per batch
hours_to_monitor = 5
# seconds to sleep between checks
sleep_seconds = 300

#number of projects to sync per batch, default 10
batch_size = 10
#the number BSD queue for this org should reduce to, before the next batch of projects are synced, default 10000
bsd_feelgood_count = 200000
#the number location queue for this org should reduce to, before the next batch of projects are synced, default 1000
location_feelgood_count = 20000


# Uncomment below block to get project list and add to projects array. This is so we know where it stops and can delete rest of the array when reprocessing
'''
with request.urlopen("http://localhost:9021/project/org/" + org_id+"?withScope=false") as url:
    print("Getting list of projects!")
    project_list = []
    data = json.load(url)
    for proj_item in data:
        for proj_line_item in proj_item:
            if(proj_line_item == "uuid"):
                project_list.append(proj_item[proj_line_item])
    print(project_list)
    print("Got {} projects. Verify count".format(len(project_list)))
    sys.exit(1)
'''

# Leave this blank and change just_monitor = True to just monitor the integrator/locator queues
projects = [
]

count = 0
total_proj_count = len(projects)
bsd_feelgood = False
location_feelgood = False
skipped_projects = []

print("Starting sync on {} projects".format(total_proj_count))
while(just_monitor or (count < total_proj_count)):
    
    print("Batch from {} to {} projects".format(count, count+batch_size-1))

    # run sync on all the projects
    sliced_projects = projects[count:count+batch_size]
    count += batch_size

    bsd_feelgood = False
    location_feelgood = False

    for project_uuid in sliced_projects:
        try:
            print("Syncing project:" + project_uuid)
            req = request.Request("http://localhost:9021/api/2/sync/explore/" + org_id + "/" + project_uuid, method='POST')
            resp = request.urlopen(req)
            data = json.load(resp)

            print(json.dumps(data, indent=4))
        except error.URLError:
            print("Connection error!")
            print(traceback.format_exc())
            skipped_projects.append(project_uuid)
        except ValueError:
            print("Value error!")
            print(traceback.format_exc())
            skipped_projects.append(project_uuid)

    # loop and monitor aggregation and integration stats every 5 mins
    # monitor for 1 hour
    monitor_loop_counter = hours_to_monitor * 12

    while monitor_loop_counter > 0 and (bsd_feelgood == False or location_feelgood == False):

        bsd_feelgood = False
        location_feelgood = False

        try:
            monitor_loop_counter -= 1
            with request.urlopen("http://localhost:9021/api/1/aggregation/queue/queue/" + org_id + "/_stats?type=bsd-type") as url:
                try:
                    #print(json.dumps(data, indent=4))
                    data = json.load(url)
                    print("AGGREGATION:")
                    if('numberMessages' not in data):
                        print(">>>>>>> NO MORE BSDS QUEUED UP FOR THIS ORG <<<<<")
                        bsd_feelgood = True
                    else:
                        num_messages = int(data['numberMessages'])
                        print("         Number of bsd-type messages: {}".format(num_messages))
                        if(num_messages < bsd_feelgood_count):
                            print("         LESS THAN {}!".format(bsd_feelgood_count))
                            bsd_feelgood = True
                except ValueError:
                    #print(traceback.format_exc())
                    print("         >>>>>> No BSDS at all! <<<<<<<")
                    bsd_feelgood = True
            
            with request.urlopen("http://localhost:9021/api/1/integration/queue/queue/_stats/_topQueuesBySize?limit=100&metadataLimit=10&type=location-type&asc=false") as url:
                try:
                    data = json.load(url)
                    print("INTEGRATION:")
                    org_found = False
                    for loc_items in data['queueStats']:
                        if(loc_items.startswith("location-type:"+org_id)):
                            org_found = True
                            num_messages = int(data['queueStats'][loc_items]['numberMessages'])
                            print("     Queue: {}".format(loc_items))
                            print("         Number of location-type messages: {}".format(num_messages))
                            if(num_messages < location_feelgood_count):
                                print("     LESS THAN {}!".format(location_feelgood_count))
                                location_feelgood = True
                    
                    if(org_found == False):
                        print("         Negligible count in location-type for this batch of projects")
                        location_feelgood = True

                except ValueError:
                    print(traceback.format_exc())
                    print(">>>>>> No Location Data at all! <<<<<<<")
                    location_feelgood = True

            # sleep 300 seconds/ 5 minutes        
            if(bsd_feelgood == False or location_feelgood == False):
                print("Sleeping for {} seconds".format(sleep_seconds))
                time.sleep(sleep_seconds)
            else:
                print("Everything is within limits. Moving to next batch")

        except error.URLError:
            print("Connection error!")
            print(traceback.format_exc())

print("Skipped projects {}".format(skipped_projects))
