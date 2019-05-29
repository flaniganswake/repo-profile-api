# RepoProfileAPI

## Overview

This app makes API calls to Github and Bitbucket retrieving repository data for a particular user. That data is then cherry-picked for certain information building a repo profile of the user. Each host API is initially queried with the following RESTful endpoints for the entire JSON data:

```
http://localhost:5000/api/v1.0/repos/?user1=host1
```

And for aggregated results for both hosts:

```
http://localhost:5000/api/v1.0/repos/?user1=host1&user2=host2
```

The app makes appropriate API calls to the hosts parsing the JSON response. The user profile is then built upon these values - when available:

* Total number of public repos separated by original and forked repos
* Total count of watchers and followers
* A list and count of languages used across all public repos
* A list and count of repo topics

## Implementation

The JSON response format with types is of the form:

```
    response = [{
        "repos": {
            "original": {
                "originals_count": <int>,
                "originals": <list>,
            },
            "forked": {
                "forks_count": <int>,
                "forks": <list>,
            },
        },
        "watchers": <int>,
        "followers": <int>,
        "languages": {
            "languages_count": <int>,
            "languages": <list>,
        },
        "topics": {
            "topics_count": <int>,
            "topics": <list>,
        },
    }]
```

## Usage

Run the app with the following:

```
python3 -m run
```
The API JSON is available in a browser or by using curl at the root.

```
http://localhost:5000/api/v1.0/
```


## Unit Testing

Test all combinations of API queries for each host/user combination plus aggregated calls for the users. The test users are *mailchimp* and *pygame*.

```
./test_app.py
```

## Docker Usage

Running the docker container

```
docker run --name repo-app -p 5000:5000 -d flaniganswake/repo-profile-app
```
