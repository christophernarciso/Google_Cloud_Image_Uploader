# Original Author: https://github.com/atif93, Google
# Modified By: Christopher Narciso
# Scraping images and storing them in the Google Cloud Storage

from selenium import webdriver
import re
import os
import json
from urllib.request import *
import time
from google.cloud import storage
import argparse

# Change these to your own files or directories
local_download_path = "images/"
database_storage_name = "anstorage"
private_key_file = "./datastorage-233310-19ff0d1dbeec.json"


def explicit():
    # Explicitly use service account credentials by specifying the private key file.
    storage_client = storage.Client.from_service_account_json(private_key_file)

    # Make an authenticated API request
    buckets = list(storage_client.list_buckets())
    print(buckets)


def upload_blob(bucket_name, source_file_name, destination_blob_name):
    """Uploads a file to the bucket."""
    # Explicitly use service account credentials by specifying the private key file.
    storage_client = storage.Client.from_service_account_json(private_key_file)
    bucket = storage_client.get_bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)

    blob.upload_from_filename(source_file_name)

    print('File {} uploaded to {}.'.format(
        source_file_name,
        destination_blob_name))


def blob_metadata(bucket_name, blob_name):
    """Prints out a blob's metadata."""
    # Explicitly use service account credentials by specifying the private key file.
    storage_client = storage.Client.from_service_account_json(private_key_file)

    bucket = storage_client.get_bucket(bucket_name)
    blob = bucket.get_blob(blob_name)

    print('Blob: {}'.format(blob.name))
    print('Bucket: {}'.format(blob.bucket.name))
    print('Storage class: {}'.format(blob.storage_class))
    print('ID: {}'.format(blob.id))
    print('Size: {} bytes'.format(blob.size))
    print('Updated: {}'.format(blob.updated))
    print('Generation: {}'.format(blob.generation))
    print('Metageneration: {}'.format(blob.metageneration))
    print('Etag: {}'.format(blob.etag))
    print('Owner: {}'.format(blob.owner))
    print('Component count: {}'.format(blob.component_count))
    print('Crc32c: {}'.format(blob.crc32c))
    print('md5_hash: {}'.format(blob.md5_hash))
    print('Cache-control: {}'.format(blob.cache_control))
    print('Content-type: {}'.format(blob.content_type))
    print('Content-disposition: {}'.format(blob.content_disposition))
    print('Content-encoding: {}'.format(blob.content_encoding))
    print('Content-language: {}'.format(blob.content_language))
    print('Metadata: {}'.format(blob.metadata))
    print("Temporary hold: ",
          'enabled' if blob.temporary_hold else 'disabled')
    print("Event based hold: ",
          'enabled' if blob.event_based_hold else 'disabled')
    if blob.retention_expiration_time:
        print("retentionExpirationTime: {}"
              .format(blob.retention_expiration_time))


def main():
    search_text = None
    num_requested = 0

    # Parse arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('--search', type=str,
                        help='Specify the search term that will scrape through google images.')
    parser.add_argument('--amount', type=int,
                        help='Specify the search amount that will download x amount locally '
                             'and to your google cloud storage')

    # Parse our arguments
    args = parser.parse_args()
    print(args)

    # Grab and set the parameters
    num_requested = args.amount
    search_text = args.search
    print("Downloading {} images of {}".format(num_requested, search_text))

    # Stop the program if no search term was provided
    if search_text is None:
        exit(0)

    # Call to check if we can access our bucket, it will exit the program if it failed at this point
    explicit()

    number_of_scrolls = num_requested / 400 + 1
    # Number_of_scrolls * 400 images will be opened in the browser

    # Create local directory to store local image copies images/search_term
    if not os.path.exists(local_download_path + search_text.replace(" ", "_")):
        print("Created directory {}/{}".format(local_download_path, search_text))
        os.makedirs(local_download_path + search_text.replace(" ", "_"))

    url = "https://www.google.co.in/search?q=" + search_text + "&source=lnms&tbm=isch"
    driver = webdriver.Chrome('./chromedriver')
    driver.get(url)

    headers = {
        'User-Agent': "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 "
                      "Safari/537.36"
    }

    # Our specified image file types to look for
    extensions = {"jpg", "jpeg", "png", "gif"}
    img_count = 0
    downloaded_img_count = 0

    for _ in range(int(number_of_scrolls)):
        for __ in range(10):
            # Multiple scrolls needed to show all 400 images
            driver.execute_script("window.scrollBy(0, 1000000)")
            time.sleep(0.2)
        # To load next 400 images
        time.sleep(0.5)
        try:
            driver.find_element_by_xpath("//input[@value='Show more results']").click()
        except Exception as e:
            print("Less images found: {}".format(e))
            break

    images = driver.find_elements_by_xpath('//div[contains(@class,"rg_meta")]')
    print("Total images: {}\n".format(len(images)))

    for img in images:
        img_count += 1
        img_url = json.loads(img.get_attribute('innerHTML'))["ou"]
        img_type = json.loads(img.get_attribute('innerHTML'))["ity"]
        # Modified OG source to make file_name the "id" of the image
        img_name = json.loads(img.get_attribute('innerHTML'))["id"]

        # Removes the colon from the name
        img_name = re.sub(":", "", img_name)
        time_stamp = time.asctime(time.localtime(time.time()))
        print("[{}]\nDownloading image #{} id#{} from the web:{}".format(time_stamp, img_count, img_name, img_url))

        try:
            # Download time tracker using time.clock()
            last_clock = time.clock()

            # If we could not find specified image types. default to .png
            if img_type not in extensions:
                img_type = "jpg"

            req = Request(img_url, headers=headers)
            raw_img = urlopen(req).read()

            # Create local image
            f = open(local_download_path + search_text.replace(" ", "_") + "/" + img_name + "." + img_type,
                     "wb")
            f.write(raw_img)
            f.close()

            # Total download time
            time_taken = time.clock() - last_clock
            print("Downloaded in {}\n".format(time_taken))

            # Implementation of Google Cloud Storage upload modified to upload to a search/img(s) subdirectories
            upload_blob(database_storage_name, './images/{}/{}'.format(search_text.replace(" ", "_"), img_name + "." + img_type),
                        '{}/{}'.format(search_text.replace(" ", "_"), img_name))
            # Print Google Cloud Storage image metadata
            blob_metadata(database_storage_name, '{}/{}'.format(search_text.replace(" ", "_"), img_name))

            downloaded_img_count += 1
        except Exception as e:
            print("Download failed: {}".format(e))
        finally:
            print()

        # If we are over our requested amount, stop
        if downloaded_img_count >= num_requested:
            break

    print("Total downloaded: {}/{}".format(downloaded_img_count, img_count))
    driver.quit()


if __name__ == "__main__":
    main()
