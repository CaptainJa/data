# -*- coding: utf-8 -*-
# 用Google Storage中转数据
from google.cloud import storage
import console
import time


# 创建bucket
def create_bucket(bucket_name):
    storage_client = storage.Client()
    bucket = storage_client.create_bucket(bucket_name)
    print('bucket {} created.'.format(bucket.name))


# 查看bucket中的文件
def list_bucket_files(bucket_name):
    """Lists all the blobs in the bucket."""
    storage_client = storage.Client()
    bucket = storage_client.get_bucket(bucket_name)

    blobs = bucket.list_blobs()

    for blob in blobs:
        print(blob.name)


# 从本地向google drive传输数据
def upload_blob(bucket_name, src_file_name, dst_bucket_file_name):
    """Uploads a file to the bucket."""
    storage_client = storage.Client()
    bucket = storage_client.get_bucket(bucket_name)
    blob = bucket.blob(dst_bucket_file_name)

    blob.upload_from_filename(src_file_name)
    print('File {} uploaded to {}.'.format(
        src_file_name, dst_bucket_file_name))


# 将google drive的数据下载到本地
def download_blob(bucket_name, src_bucket_file_name, dest_local_file_name):
    """Downloads a blob from the bucket."""
    storage_client = storage.Client()
    bucket = storage_client.get_bucket(bucket_name)
    blob = bucket.blob(src_bucket_file_name)

    blob.download_to_filename(dest_local_file_name)

    print('Blob {} downloaded to {}.'.format(
        src_bucket_file_name,
        dest_local_file_name))


# 删除google drive中的数据
def delete_blob(bucket_name, blob_file_name):
    """Deletes a blob from the bucket."""
    storage_client = storage.Client()
    bucket = storage_client.get_bucket(bucket_name)
    blob = bucket.blob(blob_file_name)

    blob.delete()
    print('Blob {} deleted.'.format(blob_file_name))


# 重命名bucket中的文件
def rename_blob(bucket_name, old_name, new_name):
    """Renames a blob."""
    storage_client = storage.Client()
    bucket = storage_client.get_bucket(bucket_name)
    blob = bucket.blob(old_name)

    new_blob = bucket.rename_blob(blob, new_name)

    print('Blob {} has been renamed to {}'.format(
        blob.name, new_blob.name))


# 拷贝到另一个bucket
def copy_blob(bucket_name, blob_name, new_bucket_name, new_blob_name):
    """Copies a blob from one bucket to another with a new name."""
    storage_client = storage.Client()
    source_bucket = storage_client.get_bucket(bucket_name)
    source_blob = source_bucket.blob(blob_name)
    destination_bucket = storage_client.get_bucket(new_bucket_name)

    new_blob = source_bucket.copy_blob(
        source_blob, destination_bucket, new_blob_name)

    print('Blob {} in bucket {} copied to blob {} in bucket {}.'.format(
        source_blob.name, source_bucket.name, new_blob.name,
        destination_bucket.name))


if __name__ == '__main__':
    bucket_name = 'data-transfer-station'

    console.info('upload shop-list.tar.gz ...')
    src_file_name = 'shop-list.tar.gz '
    dst_file_name = src_file_name
    t1 = time.time()
    upload_blob(bucket_name, src_file_name, dst_file_name)
    t2 = time.time()
    diff1 = t2 - t1
    console.info('download shop-list.tar.gz ...')
