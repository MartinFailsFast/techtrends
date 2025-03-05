# TechTreds Web Application

This is a Flask application that lists the latest articles within the cloud-native ecosystem.

## Run 

To run this application there are 2 steps required:

1. Initialize the database by using the `python init_db.py` command. This will create or overwrite the `database.db` file that is used by the web application.
2.  Run the TechTrends application by using the `python app.py` command. The application is running on port `3111` and you can access it by querying the `http://127.0.0.1:3111/` endpoint.

## Run Docker 
docker build -t techtrends .
docker run -d -p 7111:3111 techtrends


# Configure the logging system
 #INFO:werkzeug:127.0.0.1 - - [08/Jan/2021 22:40:06] "GET /metrics HTTP/1.1" 200 -
logging.basicConfig(
    #format='%(asctime)s - %(levelname)s - %(message)s',  # Set the format for log messages
    level=logging.DEBUG,  # Set the logging level
    format='%(levelname)s:%(name)s:%(client_ip)s - - [Timestamp: %(asctime)s] "%(request_method)s %(request_path)s %(http_version)s" '
           ' %(status_code)d -',
    datefmt='%d/%b/%Y %H:%M:%S'
)

logging.basicConfig(
    level=logging.INFO,
    format='%(levelname)s:werkzeug:%(client_ip)s - - [%(asctime)s] "%(request_method)s %(request_path)s %(http_version)s" %(status_code)d -',
    datefmt='%d/%b/%Y %H:%M:%S'
)

logging.basicConfig(
    level=logging.INFO,
    format='%(levelname)s - %(asctime)s - %(message)s',
)

# Sample Log 
log_data = {
    "client_ip": "127.0.0.1",
    "request_method": "GET",
    "request_path": "/metrics",
    "http_version": "HTTP/1.1",
    "status_code": 200
}

Problem Logging:
# Set up logging format to match Werkzeug's style
logging.basicConfig(
    # format="%(levelname)s:%(name)s:%(asctime)s, %(message)s",
    level=logging.INFO, 
    format="%(levelname)s:%(name)s:%(asctime)s, %(message)s",
    datefmt="%d/%m/%Y, %H:%M:%S"  # Optional: Specify date format
)
WSGIRequestHandler.log_format = '%(client_ip)s - - [%(time)s] "%(request_line)s" %(status)d -'

# Create a logger for Werkzeug

werkzeug_handler = logging.StreamHandler()
werkzeug_formatter = logging.Formatter('%(levelname)s:%(name)s:%(message)s')  # No timestamp for werkzeug
werkzeug_handler.setFormatter(werkzeug_formatter)
werkzeug_logger = logging.getLogger('werkzeug') 
werkzeug_logger.addHandler(werkzeug_handler)  # Add the custom handler

app_logger = logging.getLogger('app')
app_logger.setLevel(logging.INFO) 