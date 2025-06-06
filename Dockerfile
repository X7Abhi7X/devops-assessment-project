# Start with a lightweight official Python image. This is our base.
FROM python:3.9-slim

# Set the working directory inside the container to /app
# All subsequent commands will run from this directory.
WORKDIR /app

# Copy the requirements file first. This is a clever trick for Docker caching.
# If we don't change our requirements, Docker won't re-install them every time.
COPY requirements.txt .

# Install the Python libraries from the requirements file
RUN pip install --no-cache-dir -r requirements.txt

# Now, copy all the other files from your project folder into the container's /app directory
COPY . .

# Tell Docker that our application listens on port 5000
EXPOSE 5000

# This is the command that will be run when the container starts.
# It's the same as running "python app.py" but better for production.
CMD ["python", "app.py"]