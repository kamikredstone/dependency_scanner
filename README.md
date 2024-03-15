# What is this?

This project is a dependency scanner, currently for python, in the future for more.

## Architecture

This project consists of 3 microservices:
1. A producer, which takes in user requests and publishes them as message on a redis stream.
2. A consumer, which checks for new messages on the stream and processes them as needed.

As I mentioned, this project utilises Redis streams, and will write the processed data to MongoDB.


The app will work as follows:
1. The user submits a manifest file through a specific end point - it can be either a file or text.
2. The endpoint (/submit) will be handled by the producer.
3. Producer will publish the input to a redis stream and assign it a unique task id.
4. Scanner will pick the task from the stream, will process it, and save the processed data in MongoDB.
5. Producer will publish processed data on the /scans endpoint in a table of somesort.


The scanner will use caching in redis to reduce the amount of requests to the NIST vuln DB, and will save output as key-value pairs of task ID and output in MongoDB. 

## How to submit requests to the producer?
1. Using curl, some string data:
> curl -X POST -F 'data=some data' http://localhost:8000/submit/

2. Still curl, just a file this time:
> curl -X POST -F 'file=@/path/to/requirements.txt' http://localhost:8000/submit/

### How does it look like on redis?
When we submit a requirements.txt file to redis, it will save the value like this:
> "annotated-types==0.6.0\nanyio==4.3.0\nasync-timeout==4.0.3\nclick==8.1.7\nexceptiongroup==1.2.0\nfastapi==0.110.0\nh11==0.14.0\nidna==3.6\niniconfig==2.0.0\npackaging==23.2\npluggy==1.4.0\npydantic==2.6.2\npydantic_core==2.16.3\npytest==8.0.2\npytest-asyncio==0.23.5\npython-multipart==0.0.9\nredis==5.0.1\nsniffio==1.3.1\nstarlette==0.36.3\ntomli==2.0.1\ntyping_extensions==4.10.0\nuvicorn==0.27.1\n"