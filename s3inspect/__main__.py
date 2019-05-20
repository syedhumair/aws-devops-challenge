"""
    Example of usage.
    To run do in the command line: s3inspect -h

    The tool must return the following information
        Bucket name - Done
        Creation date (of the bucket) - Done
        Number of files - Done
        Total size of files - Done
        Last modified date (most recent file of a bucket) - Done
        And the most important of all, how much does it cost
    The following options should be supported
        Ability to get the size results in bytes, KB, MB, ... - Done
        Organize the information by storage type (Standard, IA, RR) - Done
        Filter the results in a list of buckets (bonus point for regex support)
        Ability to group information by regions - Done
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
import datetime
import re
def main():
    parser = argparse.ArgumentParser(description='Inspect S3 Bucket')

    # parser.add_argument('-t', '--top', type=int,
    #                    default=10,
    #                    help='Top n files to return in the output')
    parser.add_argument('-u', '--unit', type=str,
                       default='mb', choices=['b','kb','mb','gb'],
                       help='Return files sizes in these units: b (bytes), \
                            kb (kilobytes), mb (megabytes), gb (gigabytes)'
                        )
    parser.add_argument('regex', type=str,
                       help='Regex Support for Buckets list)'
                        )

    parser.add_argument('-p', '--prefix', type=str,
                       default='',
                       help='Add prefix for the keys. Example: \
                            images/'
                        )
    parser.add_argument('-g', '--groubystoragetype', action='store_true',
                       help='When this is set information is grouped by Storage\
                       Type'
                        )
    # parser.add_argument('-s', '--suffix', type=str,
    #                    default='',
    #                    help='Add suffix for the keys. Example: \
    #                         .jpg'
    #                     )
    parser.add_argument('-l', '--list', action='store_true',
                       help='Displays a list of available S3 Buckets in account'
                        )
    # parser.add_argument('bucket_name', type=str,
    #                    help='Name of the bucket to inspect')


    args = parser.parse_args()


    s = S3Inspect(args)
    total_size = 0
    file_count = 0
    filtered_bucket_list = []
    bucket_found = False

    bucket_list = s._list_buckets()


    if args.list:
        print("------------------------------------------------------------------")
        print("List of All buckets in account")
        print("Bucket Name\t\t\t|\t\t CreationDate")
        for bucket in bucket_list:
            print("{}\t\t\t|\t\t\t {}".format(bucket['Name'], bucket['CreationDate']))
    elif args.regex is not None:
        # r = re.compile(args.regex)
        for buckets in bucket_list:
            if re.match(args.regex, buckets['Name']):
                filtered_bucket_list.append({'Name':buckets['Name'], 'CreationDate': buckets['CreationDate']})
                bucket_found = True




    # else:

        if bucket_found:
            print("------------------------------------------------------------------")
            print("S3 Bucket Inspection Report:")
            print("------------------------------------------------------------------")
            for buckets in filtered_bucket_list:
                # if args.bucket_name in buckets['Name']:
                # print("List of Matching keys in the selected bucket: {}".format(args.bucket_name))
                bucket_region = s._get_bucket_location(Bucket=buckets['Name'])
                s.report={}
                try:
                    for key, size, storage_class in \
                            s._get_matching_s3_keys(
                                    bucket=buckets['Name'],
                                        # maxkeys=2,
                                        prefix=args.prefix):
                        # print(key, size, storage_class)
                        # s.report.setdefault('StorageClasses',{})
                        # print(s.report)

                        s.report['StorageClasses'][storage_class]['Total_Size'] += size
                        s.report['StorageClasses'].setdefault(storage_class, {})
                        s.report['StorageClasses'][storage_class]['File_Count'] += 1
                        s.report['BucketRegion'] = bucket_region
                    # print(s.report)
                    s.report['Name'] = buckets['Name']
                    s.report['CreationDate'] = buckets['CreationDate']
                    s._show_bucket_details(args)
                    print("------------------------------------------------------------------")
                except Exception as e:
                    print ("Failed to fetch keys in S3 Bucket Regex Requested: {}".format(args.regex))
                    # raise e

                # break
        # if bucket_found:

        else:
            print("------------------------------------------------------------------")
            print("No Buckets found with matching Regex: {}. \
                    \nPlease choose from the available bucket list. Using: \
                    \n\t-l or --list option Or \
                    \n\t-h or --help for more options \
                    ".format(args.regex))
            print("------------------------------------------------------------------")
if __name__== "__main__":
    main()
