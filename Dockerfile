# load python image
FROM python:3.9.18

# define the working directory
WORKDIR /app

# copy the requirements file
COPY requirements.txt .

# copy the initializer file
COPY initializer.sh .

# update pip version
RUN pip install --upgrade pip


# install the requirements
RUN pip install -r requirements.txt

# copy the api code
COPY src/ ./src

# copy initializer file
COPY initializer.sh .

RUN chmod +x initializer.sh

# define the point of entry
EXPOSE 8000
ENTRYPOINT ["/bin/sh", "./initializer.sh"]