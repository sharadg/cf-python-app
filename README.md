# Python code for deployment to a Cloud Foundry target

This repo contains 2 different processes.
1. A flask web app that exposes a frontend app and a REST API for invoking commands and making requests to a Fibanacci number generator

2. A backend Python app running a Fibonacci generator for confirming that the setup is working fine (using RabbitMQ as a messaging backend)

## Dependencies
 - Service marketplace binding of RabbitMQ to act as the glue layer between REST API and backend service
 - Cloud Foundry target to deploy this Python application to (you can sign up for a free account at https://run.pivotal.io)

## Runtime Support
- ### For running locally (on MacOS or Linux)

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
python3 -m venv bare-env
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
python app.py
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
http -v :8080/fib/23
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

- ### For deployment to Cloud Foundry (using [PWS](https://run.pivotal.io) as example here!)
**Note: this example assumes you are using [v7 of cf cli](https://github.com/cloudfoundry/cli/blob/master/README.md#downloading-the-latest-v7-cf-cli) **

1. Target your cf api, org & space
```
cf login -a https://api.run.pivotal.io --sso
```

2. Push `cf-python-app` but don't start it yet
```
cf push --no-start

Pushing app cf-python-app to org mordor / space development as shgupta@pivotal.io...
Applying manifest file /Users/sgupta/development/python/cf-python-app/manifest.yml...
Manifest applied
Packaging files to upload...
Uploading files...
 44.30 KiB / 44.30 KiB [==========================================================================================================================================================================================================================] 100.00% 1s

Waiting for API to complete processing files...

name:              cf-python-app
requested state:   stopped
routes:            cf-python-app-palm-wallaby-yh.cfapps.io
last uploaded:
stack:
buildpacks:

type:           web
sidecars:
instances:      0/1
memory usage:   128M
     state   since                  cpu    memory   disk     details
#0   down    2020-07-03T18:15:48Z   0.0%   0 of 0   0 of 0

type:           worker
sidecars:
instances:      0/1
memory usage:   128M
     state   since                  cpu    memory   disk     details
#0   down    2020-07-03T18:15:48Z   0.0%   0 of 0   0 of 0
```

2. Search marketplace for a RabbitMQ service broker and create a new service instance, and bind it to the python app
```
# If you are using PWS, then it offers RabbitMQ service by CloudAMQP
cf marketplace -e cloudamqp
# Else you are most likely to find RabbitMQ service provided through Pivotal Service Marketplace
cf marketplace -e rabbitmq

# Crete a new service instance
cf create-service cloudamqp lemur rabbitmq-service

# Bind this instance to previously pushed (but not yet started) python app
cf bind-service cf-python-app rabbitmq-service
```

3. Start the `cf-python-app`
```
cf start cf-python-app
                                                                                                                                                                                                                 ⏎ ✹ ✭
Starting app cf-python-app in org mordor / space development as shgupta@pivotal.io...

Staging app and tracing logs...
   Downloading python_buildpack...
   Downloaded python_buildpack
   Cell 65a71ce1-e630-4765-8f60-adebfa730268 creating container for instance 784e7e5b-2771-48e1-a150-2c9cddfd2c46
   Cell 65a71ce1-e630-4765-8f60-adebfa730268 successfully created container for instance 784e7e5b-2771-48e1-a150-2c9cddfd2c46
   Downloading app package...
   Downloaded app package (1.1M)
   -----> Python Buildpack version 1.7.15
   -----> Supplying Python
   -----> Installing python 3.8.3
          Copy [/tmp/buildpacks/b39d17c18faebf9d907ba9c926b74cf9/dependencies/992e82a3a463b9082ed5087ca2ff7eb0/python_3.8.3_linux_x64_cflinuxfs3_b4dbe926.tgz]
   -----> Installing pip-pop 0.1.4
          Copy [/tmp/buildpacks/b39d17c18faebf9d907ba9c926b74cf9/dependencies/1cd0187e0e714e99bef932d4c22f6515/pip-pop-0.1.4-0a3b0f1b.tar.gz]
   -----> Running Pip Install
          Collecting cfenv==0.5.3 (from -r /tmp/app/requirements.txt (line 1))
            Downloading https://files.pythonhosted.org/packages/15/b0/5fc4d8dc9fd0807b240cab217c26bb8a37ca22e8f86d0b0e896e6fc16655/cfenv-0.5.3-py2.py3-none-any.whl
          Collecting click==7.1.2 (from -r /tmp/app/requirements.txt (line 2))
            Downloading https://files.pythonhosted.org/packages/d2/3d/fa76db83bf75c4f8d338c2fd15c8d33fdd7ad23a9b5e57eb6c5de26b430e/click-7.1.2-py2.py3-none-any.whl (82kB)
          Collecting Flask==1.1.2 (from -r /tmp/app/requirements.txt (line 3))
            Downloading https://files.pythonhosted.org/packages/f2/28/2a03252dfb9ebf377f40fba6a7841b47083260bf8bd8e737b0c6952df83f/Flask-1.1.2-py2.py3-none-any.whl (94kB)
          Collecting furl==2.1.0 (from -r /tmp/app/requirements.txt (line 4))
            Downloading https://files.pythonhosted.org/packages/9f/c7/e9dc30914bf048bcd06284bb93d9650d318ecac8668b684fc41e975558ff/furl-2.1.0-py2.py3-none-any.whl
          Collecting gunicorn==20.0.4 (from -r /tmp/app/requirements.txt (line 5))
            Downloading https://files.pythonhosted.org/packages/69/ca/926f7cd3a2014b16870086b2d0fdc84a9e49473c68a8dff8b57f7c156f43/gunicorn-20.0.4-py2.py3-none-any.whl (77kB)
          Collecting itsdangerous==1.1.0 (from -r /tmp/app/requirements.txt (line 6))
            Downloading https://files.pythonhosted.org/packages/76/ae/44b03b253d6fade317f32c24d100b3b35c2239807046a4c953c7b89fa49e/itsdangerous-1.1.0-py2.py3-none-any.whl
          Collecting Jinja2==2.11.2 (from -r /tmp/app/requirements.txt (line 7))
            Downloading https://files.pythonhosted.org/packages/30/9e/f663a2aa66a09d838042ae1a2c5659828bb9b41ea3a6efa20a20fd92b121/Jinja2-2.11.2-py2.py3-none-any.whl (125kB)
          Collecting MarkupSafe==1.1.1 (from -r /tmp/app/requirements.txt (line 8))
            Downloading https://files.pythonhosted.org/packages/4b/20/f6d7648c81cb84815d0be935d5c74cd1cc0239e43eadb1a61062d34b6543/MarkupSafe-1.1.1-cp38-cp38-manylinux1_x86_64.whl
          Collecting orderedmultidict==1.0.1 (from -r /tmp/app/requirements.txt (line 9))
            Downloading https://files.pythonhosted.org/packages/04/16/5e95c70bda8fe6ea715005c0db8e602400bdba50ae3c72cb380eba551289/orderedmultidict-1.0.1-py2.py3-none-any.whl
          Collecting pika==1.1.0 (from -r /tmp/app/requirements.txt (line 10))
            Downloading https://files.pythonhosted.org/packages/a1/ae/8bedf0e9f1c0c5d046db3a7428a4227fe36ec1b8e25607f3c38ac9bf513c/pika-1.1.0-py2.py3-none-any.whl (148kB)
          Collecting six==1.15.0 (from -r /tmp/app/requirements.txt (line 11))
            Downloading https://files.pythonhosted.org/packages/ee/ff/48bde5c0f013094d729fe4b0316ba2a24774b3ff1c52d924a8a4cb04078a/six-1.15.0-py2.py3-none-any.whl
          Collecting Werkzeug==1.0.1 (from -r /tmp/app/requirements.txt (line 12))
            Downloading https://files.pythonhosted.org/packages/cc/94/5f7079a0e00bd6863ef8f1da638721e9da21e5bacee597595b318f71d62e/Werkzeug-1.0.1-py2.py3-none-any.whl (298kB)
          Collecting setuptools>=3.0 (from gunicorn==20.0.4->-r /tmp/app/requirements.txt (line 5))
            Downloading https://files.pythonhosted.org/packages/52/b4/2b8decca516c7139f2d262b6a0c5dcd6388d0a2d2c760c6bbc830e49347e/setuptools-48.0.0-py3-none-any.whl (786kB)
          Installing collected packages: six, orderedmultidict, furl, cfenv, click, MarkupSafe, Jinja2, itsdangerous, Werkzeug, Flask, setuptools, gunicorn, pika
          Successfully installed Flask-1.1.2 Jinja2-2.11.2 MarkupSafe-1.1.1 Werkzeug-1.0.1 cfenv-0.5.3 click-7.1.2 furl-2.1.0 gunicorn-20.0.4 itsdangerous-1.1.0 orderedmultidict-1.0.1 pika-1.1.0 setuptools-48.0.0 six-1.15.0
   Exit status 0
   Uploading droplet, build artifacts cache...
   Uploading droplet...
   Uploading build artifacts cache...
   Uploaded build artifacts cache (1.8M)
   Uploaded droplet (58.2M)
   Uploading complete
   Cell 65a71ce1-e630-4765-8f60-adebfa730268 stopping instance 784e7e5b-2771-48e1-a150-2c9cddfd2c46
   Cell 65a71ce1-e630-4765-8f60-adebfa730268 destroying container for instance 784e7e5b-2771-48e1-a150-2c9cddfd2c46
   Cell 65a71ce1-e630-4765-8f60-adebfa730268 successfully destroyed container for instance 784e7e5b-2771-48e1-a150-2c9cddfd2c46

Starting app cf-python-app in org mordor / space development as shgupta@pivotal.io...

Waiting for app to start...

Instances starting...
Instances starting...
Instances starting...
Instances starting...
Instances starting...
Instances starting...

name:              cf-python-app
requested state:   started
routes:            cf-python-app-palm-wallaby-yh.cfapps.io
last uploaded:     Fri 03 Jul 13:17:19 CDT 2020
stack:             cflinuxfs3
buildpacks:        python

type:           web
sidecars:
instances:      1/1
memory usage:   128M
     state     since                  cpu    memory        disk        details
#0   running   2020-07-03T18:17:40Z   0.0%   32K of 128M   31M of 1G

type:           worker
sidecars:
instances:      1/1
memory usage:   128M
     state     since                  cpu    memory        disk       details
#0   running   2020-07-03T18:17:35Z   0.0%   32K of 128M   8K of 1G
```

4. You will notice that we have a separate process `worker` as part of our app which has been specified as part of `Procfile` and is also specified in `manifest.yml`
```
# Procfile
cat Procfile
web: gunicorn -w 2 -t 600 app:app
worker: python rpc_server.py

# manifest.yml
cat manifest.yml
---
applications:
  - name: cf-python-app
    buildpacks:
      - python_buildpack
    random-route: true
    processes:
      - type: web
        memory: 128M
        instances: 1
      - type: worker
        memory: 128M
        instances: 1
    env:
      PIP_DISABLE_PIP_VERSION_CHECK: 1
      PIP_NO_WARN_SCRIPT_LOCATION: 0
```

5. *OPTIONAL* - The `web` process runs our REST API and `worker` process runs the Fibonacci Server. In case, if when we `cf push` the app and the `worker` process doesn't run then, we need to scale it's process instance to 1 or more.
```
cf scale cf-python-app --process worker -i 1                                                                                                                                                                                                      ✹ ✭

Scaling app cf-python-app in org mordor / space development as shgupta@pivotal.io...

Instances starting...
Instances starting...

Showing current scale of app cf-python-app in org mordor / space development as shgupta@pivotal.io...

name:              cf-python-app
requested state:   started
routes:            cf-python-app-palm-wallaby-yh.cfapps.io
last uploaded:     Fri 03 Jul 13:17:19 CDT 2020
stack:             cflinuxfs3
buildpacks:        python

type:           web
sidecars:
instances:      1/1
memory usage:   128M
     state     since                  cpu    memory          disk           details
#0   running   2020-07-03T18:17:41Z   0.5%   45.6M of 128M   208.2M of 1G

type:           worker
sidecars:
instances:      1/1
memory usage:   128M
     state     since                  cpu    memory          disk           details
#0   running   2020-07-03T18:17:36Z   0.4%   16.6M of 128M   208.2M of 1G
```

6. Test the REST API
```
# Substitute the application url below with the url where you deployed your app and invoke /fib/<number> endpoint
http -v https://cf-python-app-palm-wallaby-yh.cfapps.io/fib/42                                                                                                                                                                                      ✭
GET /fib/42 HTTP/1.1
Accept: */*
Accept-Encoding: gzip, deflate
Connection: keep-alive
Host: cf-python-app-palm-wallaby-yh.cfapps.io
User-Agent: HTTPie/2.2.0



HTTP/1.1 200 OK
Connection: keep-alive
Content-Length: 10
Content-Type: application/json
Date: Fri, 03 Jul 2020 18:24:24 GMT
Server: gunicorn/20.0.4
X-Vcap-Request-Id: 1b478d65-bed3-47fe-480e-ef55dafc087d

267914296
```

7. In case you make any changes to the Python code and you end up installing more python modules, then you need to update the `requirements.txt` file
```
pip freeze > requirements.txt
```