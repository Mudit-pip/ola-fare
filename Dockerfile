# Base Python image
FROM python:3.11-slim

# Set the working directory
WORKDIR /app

# Install system dependencies for Chrome and Selenium
RUN apt-get update && apt-get install -y \
    wget \
    unzip \
    curl \
    libglib2.0-0 \
    libnss3 \
    libgconf-2-4 \
    libfontconfig1 \
    libxrender1 \
    libxi6 \
    libxrandr2 \
    libxss1 \
    libxtst6 \
    libasound2 \
    libatk-bridge2.0-0 \
    libpangocairo-1.0-0 \
    fonts-liberation \
    libappindicator3-1 \
    xdg-utils \
    --no-install-recommends && \
    rm -rf /var/lib/apt/lists/*

# Install Chrome
RUN wget -q -O - https://dl.google.com/linux/linux_signing_key.pub | apt-key add - && \
    echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" > /etc/apt/sources.list.d/google-chrome.list && \
    apt-get update && apt-get install -y google-chrome-stable && \
    rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code
COPY . .

# Expose port 5000 for the Flask app
EXPOSE 5000

# Set the command to run the application
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "ola_api:app"]
