# official Python runtime as a parent image
FROM python:3

# Sets the working directory for container
WORKDIR /app

# Copying the current directory contents into container at /app
COPY src/ /app/

# Installs necessary packages in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# exposing port 8080
EXPOSE 8080

# Run app.py
CMD ["python", "app.py"]
