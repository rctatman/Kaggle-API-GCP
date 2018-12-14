import os

from kaggle.api.kaggle_api_extended import KaggleApi
from google.cloud import storage

storage = storage.Client()

PATH = "/tmp/kaggle"

PULL_BUCKET = "YOUR-GCS-BUCKET-PULL"
PUSH_BUCKET = "YOUR-GCS-BUCKET-PUSH"
USERNAME = "KERNEL-USERNAME"
KERNEL_SLUG = "KERNEL-SLUG"

def kernel_pull(request):
    api = KaggleApi()
    api.authenticate()
    api.kernels_pull_cli("{}/{}".format(USERNAME, KERNEL_SLUG), path="{}".format(PATH), metadata=True)

    bucket = storage.bucket(PULL_BUCKET)
    metadata_blob = bucket.blob("kernel_metadata.json")
    notebook_blob = bucket.blob("{}.ipynb".format(KERNEL_SLUG))

    metadata_blob.upload_from_filename("{}/kernel-metadata.json".format(PATH))
    notebook_blob.upload_from_filename("{}/{}.ipynb".format(PATH, KERNEL_SLUG))

def kernel_push(request):
    api = KaggleApi()
    api.authenticate()

    bucket = storage.bucket(PUSH_BUCKET)
    metadata_blob = bucket.blob("kernel_metadata.json")
    notebook_blob = bucket.blob("{}.ipynb".format(KERNEL_SLUG))

    metadata_blob.download_to_filename("{}/kernel-metadata.json".format(PATH))
    notebook_blob.download_to_filename("{}/{}.ipynb".format(PATH, KERNEL_SLUG))

    api.kernels_push("{}".format(PATH))