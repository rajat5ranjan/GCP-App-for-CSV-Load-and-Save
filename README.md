# GCP Application for CSV Load and Save
Google Cloud Platform Simple Basic configured applictaion for CSV uploading and saving it in Database (MySQL), as a part of Interview Assignment by Searce.

## Code Structure

```
. App
├── app.yaml
├── main.py
├── maintest.py
├── requirements.txt
├── static
|   ├── b.png
└── template
    ├── upload.html
    └── ack.html
    └── error.html
```

# Steps
* Create GCP account and add billing, Create a sample 'Hello World' Project [Link To Google Cloud App Engine Python](https://cloud.google.com/appengine/docs/standard/python3/quickstart)

* After cloning follow below commands
  * Create virtual env
  ```
  virtualenv --python python3 ~/envs/hello_world
  source ~/envs/hello_world/bin/activate
  ```
  * Install requirements
  ```
  pip install requirements.txt
  ```
  * Run main.py
  ```
  python main.py
  ```
* Deploy to glcoud
  *  Deploy
  ```
  gcloud app create
  gcloud app deploy app.yaml --project
  ```
  
# Application Specs

## Validations and Limitations
* **File size less than 10 MB**
* **File extension should be csv**
* **Number of columns should be less than 4 and number of rows less than 5 Lacs**
* **All columns are treated as VARCHAR(100), if more than that, it will throw error**

## Highlights
* **Generic application for all kinds of CSV**
* **Deployed on Google Cloud App Engine**
* **Remote Database, configurable for Local**
* **Error handlers**
* **Flask Web App**

# Hosted App
[Application Link](https://proj-searce.appspot.com)

### Application Screenshots
![title](/screenshots/1.png)
![title](/screenshots/2.png)
![title](/screenshots/3.png)
![title](/screenshots/4.png)

### Database
## Remote Mysql [Link](https://remotemysql.com/)

Details
![title](/screenshots/db.png)

# Further Enhancements
* Size extended
* Unit Test cases for api
