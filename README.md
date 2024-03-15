# What is this?

This project is a dependency scanner, it will consist of 2 micro-services: A producer and the scanner itself.

## Architecture

The app will work as follows:
1. The user submits a manifest file through a specific end point - it can be either a file or text.
2. The endpoint (/submit) will be handled by the producer.
3. Producer will publish the input to a redis stream and assign it a unique task id.
4. Scanner will pick the task from the stream, and will output the result to a frontend endpoint (/scans).

The scanner will use caching in redis to reduce the amount of requests to the NIST vuln DB, and will save output as key-value pairs of task ID and output in MongoDB. 

## How to submit requests to the producer?
1. Using curl, some string data:
> curl -X POST -F 'data=some data' http://localhost:8000/submit/

2. Still curl, just a file this time:
> curl -X POST -F 'file=@/path/to/requirements.txt' http://localhost:8000/submit/