FROM python:3.8

# Set the working directory in the container
WORKDIR /app

# Copy your Python script and any required files into the container
COPY src.py /app/
COPY requirements.txt /app/
ENV ENV_SERVER_IP='127.0.0.1'

# Install any required Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Define an entry point (the script to run when the container starts)
ENTRYPOINT ["python", "src.py"]

# how to run-> docker run -it --rm -e ENV_SERVER_IP=127.0.0.1 --network=host client_mqtt # allow docker to access host's network



