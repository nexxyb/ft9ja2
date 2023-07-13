# syntax=docker/dockerfile:1
# Use a Windows base image that matches your Windows version
FROM mcr.microsoft.com/windows/nanoserver:ltsc2022

# Set the working directory
WORKDIR /app

# Copy the requirements file and install the dependencies using PowerShell
COPY requirements.txt .
RUN powershell -Command "pip install -r requirements.txt"

# Copy the Python script and the MT5 terminal executable
COPY app.py .
COPY mt5setup.exe .

# Install and run the MT5 terminal using the specified login credentials
RUN mt5setup.exe /login:123456 /server:BrokerName-Demo /password:qwerty
CMD ["python.exe", "app.py"]