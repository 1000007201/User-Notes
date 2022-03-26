import logging

# Creating custom logger
logger = logging.getLogger()
logger.setLevel(logging.INFO)
file_handler = logging.FileHandler('app.log')

# create formatters and aad it to handlers
file_format = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
file_handler.setFormatter(file_format)
file_handler.setLevel(logging.INFO)

# Add handlers to logger
logger.addHandler(file_handler)
