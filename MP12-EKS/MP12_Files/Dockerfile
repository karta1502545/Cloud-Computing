FROM --platform=linux/amd64 python:3.6

# Creating Application Source Code Directory
RUN mkdir /app

# Setting Home Directory for containers
WORKDIR /app

# Copy src files folder (requirements.txt and classify.py)
COPY requirements.txt classify.py train.py data_preload.py utils.py server.py models.py /app

# Installing python dependencies
RUN pip3 install --no-cache-dir -r requirements.txt

# create directories for models and data
RUN mkdir /app/models
RUN mkdir /app/data

# Preload the data
RUN python3 /app/data_preload.py

# Pretrain the models
RUN DATASET=mnist TYPE=ff python3 train.py
RUN DATASET=kmnist TYPE=ff python3 train.py
RUN DATASET=mnist TYPE=cnn python3 train.py
RUN DATASET=kmnist TYPE=cnn python3 train.py


# Application Environment variables. 
# These variables will be used when you run the image. 
# You will also need to pass corresponding DATASET and TYPE variables from the job yaml files of both free-service and default types of jobs.
ENV APP_ENV development
ENV DATASET mnist
ENV TYPE ff

# Exposing Ports
EXPOSE 5035

# Setting Persistent data
VOLUME ["/app-data"]

# Running Python Application (classify.py)
CMD ["python3", "classify.py"]