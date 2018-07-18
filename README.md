# CEO Health Project
This repo is dedicated to code related to Professor Malmendier's CEO Health Project.

# Instructions for downloading pictures, uploading pictures to S3, and using Face APIs.

1.	Create an AWS account, login to the console, search for “s3” and create a bucket with default settings. Note the AWS access key id and access key secret (under My Security Credentials), and s3 bucket name.
2.	Create a new folder and put download.py, upload.py, api.py, utils.py, credentials.txt, and the excel files with picture links in it.
3.	Edit credentials.txt with your AWS access key id and access key secret and s3 bucket name.
4.	Open the terminal (Mac) or GitBash (Windows) and navigate to the folder.
5.	Install python 3.0 and pip. Then run “pip install ___” for requests, pandas, and boto3.
6.	Run “python download.py ____” with the name of the original excel file. When the script is finished, the downloaded pictures will be in a folder named ceo_pictures. Pictures with multiple faces will be in subfolders called MULTI_FACE.
7.	Go through the subfolders of CEOs and crop pictures with multiple faces so that only one face remains.
8.	Run “python upload.py ____” with the name of the excel file, file_upload_ready. When the script is finished, the pictures will be uploaded to the s3 bucket. There will also be a new excel file with a new column of the s3 urls for each picture called file_api_ready.
9.	Run “python api.py ____” with the names of the excel file: file_api_ready. When the script is finished, there will be a new excel file with the facial recognition API data appended called file_api_finished. If the script detects multiple faces for an image, crop the image and manually upload it to s3, then rerun api.py.
