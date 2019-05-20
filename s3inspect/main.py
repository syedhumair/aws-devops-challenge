"""
    Example of usage.
    To run do in the command line: s3inspect main.py

    The tool must return the following information
        Bucket name
        Creation date (of the bucket)
        Number of files
        Total size of files
        Last modified date (most recent file of a bucket)
        And the most important of all, how much does it cost
    The following options should be supported
        Ability to get the size results in bytes, KB, MB, ...
        Organize the information by storage type (Standard, IA, RR)
        Filter the results in a list of buckets (bonus point for regex support)
        Ability to group information by regions
    Some additional features that could be useful (optional)
        It would be nice to support prefix in the bucket filter
        (e.g.: s3://mybucket/Folder/SubFolder/log*).
        It may also be useful to organize the results according to the
        encryption type, get additional buckets information (life cycle,
        cross-region replication, etc.) or take into account the previous
        file versions in the count + size calculation.

        Some statistics to check the percentage of space used by a bucket,
        or any other good ideas you could have, are more than welcome.


"""
import sys
from s3inspect import S3Inspect
import argparse
import boto3

parser = argparse.ArgumentParser(description='Process some integers.')

# parser.add_argument('-t', '--top', type=int,
#                    default=10,
#                    help='Top n files to return in the output')
parser.add_argument('-u', '--unit', type=str,
                   default='mb', choices=['b','kb','mb','gb'],
                   help='Return files sizes in these units: b (bytes), \
                        kb (kilobytes), mb (megabytes), gb (gigabytes)'
                    )
parser.add_argument('-p', '--prefix', type=str,
                   default='',
                   help='Add prefix for the keys. Example: \
                        images/'
                    )
parser.add_argument('-s', '--suffix', type=str,
                   default='',
                   help='Add suffix for the keys. Example: \
                        .jpg'
                    )
parser.add_argument('-l', '--list', action='store_true',
                   help='Displays a list of available S3 Buckets in account'
                    )
parser.add_argument('bucket_name', type=str,
                   help='Name of the bucket to inspect')


args = parser.parse_args()
s3_client = boto3.client('s3')

s = S3Inspect(s3_client, args.unit)
total_size = 0
print("List of Matching keys in the selected bucket: {}".format(args.bucket_name))
for key, size, storage_class in s._get_matching_s3_keys(bucket=args.bucket_name, prefix=args.prefix, suffix=args.suffix):
    print(key, size, storage_class)
    total_size += size

s._print_total_size(total_size)



bucket_list = s._list_buckets()


if args.list:
    print("------------------------------------------------------------------")
    print("List of All buckets in account")
    print("Bucket Name\t\t\t|\t\t CreationDate")
    for bucket in bucket_list:
        print("{}\t\t\t|\t\t\t {}".format(bucket['Name'], bucket['CreationDate']))


print("------------------------------------------------------------------")
print("S3 Bucket Inspection Report:")
print("------------------------------------------------------------------")
for buckets in bucket_list:
    if args.bucket_name == buckets['Name']:
        s._show_bucket_details(buckets['Name'], buckets['CreationDate'])
        break


        # raise



# print()


# #buckets = s._read_s3_buckets(s3_connection=s3_client)
# #print ("Printing List of buckets")
# #for bucket in buckets:
#     print ("Bucket Name: {}".format(bucket.name))
#     files = s._read_files(bucket=bucket, s3_connection=s3_client)
#     for file in files:
#         print(file)
