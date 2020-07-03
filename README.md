# Python code for deployment to a Cloud Foundry target

This repo contains 2 different processes.
1. A flask web app that exposes a frontend app and a REST API for invoking commands and making requests to a Fibanacci number generator

2. A backend Python app running a Fibonacci generator for confirming that the setup is working fine (using RabbitMQ as a messaging backend)

## Dependencies
 - Service marketplace binding of RabbitMQ to act as the glue layer between REST API and backend service
 - Cloud Foundry target to deploy this Python application to (you can sign up for a free account at https://run.pivotal.io)

## Runtime Support
- ### For running locally (natively on MacOS)
```
1. Start RabbitMQ Server
```
docker run -p 5672:5672 -p 4369:4369 -p 15672:15672 -p 25672:25672 -d bitnami/rabbitmq
```

2. Check out this git repo and cd into the repo folder
```
git checkout https://github.com/sharadg/cf-python-app
cd cf-python-app
```

3. Create a virtual env for tracking python modules required for pip installation
```
python -m venv bare-env
```

4. Activate the venv!
```
source ./bare-env/bin/activate
```

5. Install the pip modules
```
pip install -r requirements.txt
```

6. Set ENV `profile` to `local` (to point to the RabbitMQ server running in the docker container)
```
export profile=local
```

7. Start main Flask REST API server
```
python app.py                                                                                                                                                                                                                                       ✭
 * Serving Flask app "app" (lazy loading)
 * Environment: production
   WARNING: This is a development server. Do not use it in a production deployment.
   Use a production WSGI server instead.
 * Debug mode: on
 * Running on http://0.0.0.0:8080/ (Press CTRL+C to quit)
 * Restarting with stat
 * Debugger is active!
 * Debugger PIN: 298-015-168
```

8. In a separate terminal window (change into the same folder as cf-python-app and follow steps #4 & #6, and then, run the following for fibonacci RPC server)
```
python rpc_server.py
 [*] Awaiting RPC requests. To exit press CTRL+C
```

9. Test fibonacci server
```
http -v :8080/fib/23                                                                                                                                                                                                                               ⏎
GET /fib/23 HTTP/1.1
Accept: */*
Accept-Encoding: gzip, deflate
Connection: keep-alive
Host: localhost:8080
User-Agent: HTTPie/2.2.0


HTTP/1.0 200 OK
Content-Length: 6
Content-Type: application/json
Date: Fri, 03 Jul 2020 16:56:00 GMT
Server: Werkzeug/1.0.1 Python/3.6.10

28657
```

