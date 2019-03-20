<snippet>

# Uploader.py
Webscraper that uses the Google Cloud Storage API to store images scraped from the web. All credits due to original scraper source, modified by me for suited needs.

## Usage
Program stored images locally and in the cloud storage. Decision made incase it fails to upload. You can then simply upload the local copy.

Scraper should grab multiple file types. At minimum .png

1. Request a google service account credential. Save as .json you will use this to access your storage. 
2. Import the proper parameters. e.g, --search basketball --amount 100 


## Output
``` 
[Wed Mar 20 10:51:34 2019]
Downloading image #100 id#cSS5fMdyX5FRuM from the web:http://img.over-blog-kiwi.com/1/47/73/14/20160709/ob_bcc896_chiot-shiba-inu-a-vendre-2016.jpg
Downloaded in 0.004836999999998426

File ./images/shiba/cSS5fMdyX5FRuM.jpg uploaded to shiba/cSS5fMdyX5FRuM.
Blob: shiba/cSS5fMdyX5FRuM
Bucket: anstorage
Storage class: REGIONAL
ID: anstorage/shiba/cSS5fMdyX5FRuM/1553093495537061
Size: 102779 bytes
Updated: 2019-03-20 14:51:35.536000+00:00
Generation: 1553093495537061
Metageneration: 1
Etag: CKX76pD8kOECEAE=
Owner: None
Component count: None
Crc32c: BHAllA==
md5_hash: fFqk2OAuo6jrTeF/lUERYg==
Cache-control: None
Content-type: image/jpeg
Content-disposition: None
Content-encoding: None
Content-language: None
Metadata: None
Temporary hold:  disabled
Event based hold:  disabled

Total downloaded: 100/100


