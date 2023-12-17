# Use a Python base image
FROM python:3.12

# Set the working directory
WORKDIR /app

# Install bot dependencies
RUN pip install --upgrade pip
COPY requirements /requirements
RUN pip install -r /requirements/base.txt

COPY . .

# Run the bot script
CMD ["python", "main.py"]
