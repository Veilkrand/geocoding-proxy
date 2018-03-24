# Geocoding Proxy Service App
> Alberto Naranjo alberto.galet@gmail.com
> 3/21/2018

## Overview
Mini project to implement a geocoding proxy with a failover mechanism for 3rd party service providers, using Google Maps API as primary and HERE API as secundary.
The REST interface was implement in Flask and the production deployment is using a Docker container with Ubuntu.


## Installation 

To install, configure and run the app. You need to perform several steps:

### 1. Clone Repo

Clone the github repo to your production machine and access the work directory:

```
$ git clone https://github.com/Veilkrand/geocoding-proxy
$ cd geocoding-proxy
```

### 2. Setup API keys for service providers

Inside the work directory edit the file `env.list` with your Google Maps and HERE API keys. This file will be used in the next steps to build the Docker image and run the container with these environment variables. The file can be deleted afterwards for more security.

### 3. Setup the Docker Container

From the repo work directory, build the container image using a Dockerfile:

```$ docker build -t geocoding-proxy:latest .```

Start the container as a daemon process:

````$ docker run -d -p 5000:5000 --env-file ./env.list geocoding-proxy```

Check the container is up:

```$ docker ps```

Test you can access the local web server with a browser at `http://127.0.0.1:5000/` within the same production network.
If you can't access the local server you can try to debug the container running an interactive session:

```docker run -it -p 5000:5000 --env-file ./env.list geocoding-proxy```


## Using the API

There's only one GET method `find` with one parameter `address` we can use to find the geographic coordinates of the provided address. Multiple results for one requested address could be returned. 
If Google geocoding service is unavailable or is unable to find any result for the provided address it will automatically failover to the HERE geocoding services with the same query. The result object includes a `service_provider` field with the source of the query.

### Curl examples*

Multiple results:

```
curl -H "Accept: application/json" "http://127.0.0.1:5000/find/?address=Toledo%20Street"
```

One well defined result:

```
curl -H "Accept: application/json" "http://127.0.0.1:5000/find/?address=1600%20Amphitheatre%20Parkway,%20Mountain%20View,%20CA"
```

No results:

```
curl -H "Accept: application/json" "http://127.0.0.1:5000/find/?address=braaaa"
```

You can query as well the same service passing the address parameter value as part of the url: `http://127.0.0.1:5000/find/Toledo`. This is particulary useful if we want the users to access the service from their browsers.

### Result Json format

The `results` object includes `service_provider` as the source of the serevice and one or multiple `locations` objects.
Every object inside `locations` will include `coords` with `latitude` and `longitude` and a formalized `address` of the result.

```
{
    "results": [
        {
            "service_provider": "Google",
            "locations": [
                {
                    "coords": {
                        "longitude": -118.1907299,
                        "latitude": 34.1206184
                    },
                    "address": "Toledo St, Los Angeles, CA 90042, USA"
                },
                {
                    "coords": {
                        "longitude": -80.2717777,
                        "latitude": 25.7401912
                    },
                    "address": "Toledo St, Coral Gables, FL, USA"
                },
                {
                    "coords": {
                        "longitude": -83.09981619999999,
                        "latitude": 42.32265599999999
                    },
                    "address": "Toledo St, Detroit, MI, USA"
                },
                {
                    "coords": {
                        "longitude": -73.41973589999999,
                        "latitude": 40.7119616
                    },
                    "address": "Toledo St, Farmingdale, NY 11735, USA"
                },
                {
                    "coords": {
                        "longitude": -84.8818841,
                        "latitude": 41.731147
                    },
                    "address": "Toledo St, Fremont, IN 46737, USA"
                }
            ]
        }
    ]
}
```


### API Errors

*Error 400: Parameter required*
The `address` parameter was not included in the request, was empty or not valid.

```
{
    "errors": [
        {
            "details": "The address parameter is required (and really important) to perform the geocoding search.",
            "status": "400",
            "title": "Parameter required"
        }
    ]
}
```

*Error 404: Address not found*
After checking both service provider no results were found for the supplied address.

```
{
    "errors": [
        {
            "details": "The address provided by the user was not found or no geocoding service provider were available.",
            "status": "404",
            "title": "Address not found"
        }
    ]
}
```


## Command Line App

You can run the Python app `/app/proxy.py` from the command line with additional arguments as `max_results` and `provider_mode`.

```
$ python proxy.py [Address] [Max_results] [Provider_mode]`
```

`max_results` will limit the maximum number of results per provider. `Provider_mode` can be `all` for including results from both providers, or `failover` as default behaviour.

e.g.:

```
$ python proxy.py 'Toledo Street' 2 all
```

### Access bash of the running docker container

Search the name of the running container:

```
$ docker ps
```

Run interactive mode using bash as entry point:

```
sudo docker exec -i -t [container name] /bin/bash
```

## Topics


- Github:
	- Endlines
	- gitignore

