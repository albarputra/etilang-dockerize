# 
FROM python:3.8.10

# 
WORKDIR /code

# 
COPY ./requirements.txt /code/requirements.txt

# 
RUN apt-get update && \
    apt-get install -yq tzdata && \
    ln -fs /usr/share/zoneinfo/Asia/Jakarta /etc/localtime && \
    dpkg-reconfigure -f noninteractive tzdata 

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

# 
COPY ./fastapi_timbangan-master /code/fastapi_timbangan-master

# 
# CMD ["uvicorn", "code.main:app", "--host", "0.0.0.0", "--port", "8080"]
CMD ["python", "fastapi_timbangan-master/run.py"]
