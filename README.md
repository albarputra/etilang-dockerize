
## fastapi_timbangan
## etilang-dockerize

$ docker build -t <image-name> .
$ docker run -d --name <container_name> -p 8082:8082 <image_name>
## deploy to server # (ubuntu server)

1. install git
    $ sudo apt-get update.
    $ sudo apt-get install git-all.
    $ git version.

2. install python
    $ sudo apt-get update.
    $ sudo apt-get python
$ python3 --version

3. clone repo
    $ git clone https://github.com/oillypump/fastapi_timbangan-master.git

4. create env
    $ cd <dir>
    $ python3 -m venv server_env

5. activate env
    $ source server_env/bin/activate

6. install requirement
    $ pip install -r /path/to/requirements.txt
    "-r, --requirement < filename >"

7. run server
    $ python3 run.py

8. create systemd 

    [Unit]
    Description=Etilang
    After=multi-user.target

    [Service]
    Type=simple
    ExecStart=/home/api/fast_dev/fastapi_timbangan-master/serv_env/bin/python3 /home/api/fast_dev/fastapi_timbangan-master/run.py
    StandardOutput=file:/home/api/fast_dev/api.log
    StandardInput=tty-force
    #Restart=always

    [Install]
    WantedBy=multi-user.target


9. enable systemd

    $ sudo systemctl enable systemd 
