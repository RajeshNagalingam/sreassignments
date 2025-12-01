import boto3
import datetime

s3 = boto3.client('s3')

buckets = s3.list_buckets()['Buckets']

test_buckets = []
for b in buckets:
    if b['Name'].endswith('.test'):
        test_buckets.append(b['Name'])

expire_date = datetime.datetime.now() - datetime.timedelta(days=30)

for bucket in test_buckets:
    print(f"Checking bucket: {bucket}")
    objects = s3.list_objects_v2(Bucket=bucket)
    if 'Contents' in objects:
        for obj in objects['Contents']:
            key = obj['Key']
            last_modified = obj['LastModified']
            if key.endswith('.xml') and last_modified < expire_date:
                print(f"Expired: {bucket}/{key}")




#Listing the buckets, filtering the buckets ends with ".test" in name of the bucket, defining expiration date, 
#listing the objects which last modified date and contains .xml in file/objectname (key) on objects details (Contents), prints the bucket and object name if expired.