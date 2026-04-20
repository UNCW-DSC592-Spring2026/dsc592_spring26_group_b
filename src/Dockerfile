# Use the official Microsoft AML base image
FROM mcr.microsoft.com/azureml/openmpi4.1.0-ubuntu20.04:latest

WORKDIR /app
COPY . /app

# Install your module and core dependencies
RUN pip install azureml-core && pip install -e .

# No mocking needed if the image already contains the studio modules
ENTRYPOINT ["python", "-m", "aml_shared.urldecode"]
