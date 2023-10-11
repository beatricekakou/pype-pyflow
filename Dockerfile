# use an official Python runtime as a parent image
FROM python:3.9

# set the working directory in the container
WORKDIR /usr/src/app

# copy the local code to the container
COPY . .

# install any needed packages specified in requirements.txt
RUN pip install --trusted-host pypi.python.org -r requirements.txt

# make port 80 available to the world outside this container
EXPOSE 80

# define environment variable (add your own variables here if necessary)
ENV NAME World

# run main.py when the container launches
CMD ["python", "./main.py"]
