FROM python:3.11.2-slim

# Install system packages
RUN apt-get update && \
    apt-get install -y \
        apt-transport-https \
        build-essential \
        cmake \
        curl \
        gcc \
        g++ \
        git \
        libpq-dev \
        python3-dev \
        tree \
        sudo \
        unzip \
        wget \
    && apt-get autoremove -yqq --purge \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Install Python packages
COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir --ignore-installed -r requirements.txt

# Configure workdir
WORKDIR /home/evidently-monitoring-ui
# Copy the python script to collect and load reports
ADD reporting.py .
ADD start.sh .
RUN chmod 777 start.sh

EXPOSE 8001
# Load the reports to the dashboard
#RUN python -m reporting
CMD ["./start.sh"]
