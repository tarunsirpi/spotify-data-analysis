# Spotify data analysis

## Aim:

This project aims to get data from the [Spotify API](https://developer.spotify.com/documentation/web-api) and do a data analysis on the acquired data. The inspiration behind this is to analyse the tracks of my favourite artist (A.R.Rahman) , which is done using the features provided by Spotify for each track.

 

## Technologies used:

1. Python (version 3.9)
2. AWS lambda
3. AWS S3 
4. Power BI



## Setup for AWS lambda function:
- A lambda function is created with the contents of the file, ```get_data_lambda_function.py``` with python 3.9 runtime. This lambda function will get the data using Spotify API and store it in an S3 bucket.

- A layer needs to be created and added to the lambda function for using the ```pandas``` and ```spotipy``` libraries. This can be done in the AWS cloud shell as follows,

```
mkdir spotify_layer
cd spotify_layer
mkdir python

pip install pandas spotipy -t python/
zip -r spotify_layer.zip python/
```
```
aws lambda publish-layer-version --layer-name my_spotify_layer --zip-file fileb://spotify_layer.zip --compatible-runtimes python3.9
```

- The runtime configuration of the lambda function is set to 15 minutes.

- In the execution role configuration, ```AmazonS3FullAccess```  policy is attached to it. 

- Under Configurations, the Environment variables (*client_id* and *client_secret*)are created 


## Data analysis using PowerBI:

- The data is then downloaded from the S3 bucket and imported into PowerBI.
- The data is cleaned and the report is generated.


## Files and directories:

```spotify_get_data.py``` : python file for generating Spotify data.

```get_data_lambda_function.py``` : AWS lambda function for generating Spotify data.

```spotify-report-powerBI.pbix``` : PowerBI report created using the data generated.

```data/ ```: contains the CSV files generated 

```requirements.txt``` : python libraries required to get the data.



Note : While using ```spotify_get_data.py``` to get the data, the *client ID* and *client secret* credentials are stored in a CSV file(spotify-keys.csv) and is hidden using the ```.gitignore``` file.