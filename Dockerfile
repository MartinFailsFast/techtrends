FROM python:3.8
LABEL maintainer="Martin Book"

COPY . /app
WORKDIR /app
RUN pip install -r requirements.txt

# Expose the application port
#EXPOSE 3111

# command to run on container start
CMD ["sh", "-c", "python init_db.py && python app.py"]