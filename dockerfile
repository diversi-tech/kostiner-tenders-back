# Use a smaller base Python image
FROM python:slim-buster
# Set the working directory in the container
WORKDIR /Kostiner
# Copy only the requirements file first to leverage Docker cache
COPY requirements.txt .
# Install dependencies
RUN pip install --trusted-host pypi.org --trusted-host files.pythonhosted.org -r requirements.txt --no-cache-dir
# Copy the rest of the application code
COPY . .
# Expose the port on which the Flask app will run
EXPOSE 5000
ENV FLASK_APP=./app/app.py
ENV FLASK_ENV=development
# Run the Flask app
CMD ["flask", "run", "--host=0.0.0.0"]
