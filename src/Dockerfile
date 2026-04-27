# Use the official Microsoft AML base image
FROM mcr.microsoft.com/azureml/openmpi4.1.0-ubuntu20.04:latest

WORKDIR /app

# 1. Install System Dependencies & Azure CLI
RUN apt-get update && apt-get install -y curl && \
    curl -sL https://aka.ms/InstallAzureCLIDeb | bash && \
    az extension add -n ml

# 2. Copy repository (Ensure .amlignore handles the 17MB CSV!)
COPY . /app

# 3. Install Python dependencies
# We install azureml-core and the local package in editable mode
RUN pip install --no-cache-dir azureml-core && \
    pip install --no-cache-dir -e .

# 4. Entrypoint Script
# We use a shell script as the entrypoint to handle the multi-step
# process of versioning and launching the job.
RUN chmod +x /app/run_pipeline.sh
ENTRYPOINT ["/app/run_pipeline.sh"]
