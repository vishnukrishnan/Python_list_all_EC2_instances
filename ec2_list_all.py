import boto3
from prettytable import PrettyTable
import threading

ec2 = boto3.client('ec2')
d_regions = ec2.describe_regions()
all_regions = []
threadlist = []
x = PrettyTable()
x.border = False
x.field_names = ['Region/AZ', 'Name', 'Id', 'Type', 'State', 'Public IP',
                 'AMI Id', 'Key', 'Security group', 'Launch Time']


def insta(region):
    ec2r = boto3.resource('ec2', region_name=region)
    for i in ec2r.instances.all():
        a = i.subnet.availability_zone
        b = i.tags[0]['Value']
        c = i.id
        d = i.instance_type
        e = i.state['Name']
        f = i.public_ip_address
        g = i.image_id
        h = i.key_name
        if e == 'terminated':
            j = 'None'
        else:
            j = i.security_groups[0]['GroupName']
        k = i.launch_time.strftime("%Y-%m-%d_%H:%M:%S")
        x.add_row([a, b, c, d, e, f, g, h, j, k])


print("Listing all Instances:\n")

for item in d_regions['Regions']:
    region = item['RegionName']
    all_regions.append(region)

for region in all_regions:
    t = threading.Thread(target=insta, args=(region,))
    t.start()
    threadlist.append(t)

for thread in threadlist:
    thread.join()

print(x)
