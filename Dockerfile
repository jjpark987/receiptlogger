# Use Python 3.12.9 slim as the base image
FROM python:3.12.9-slim

# Set the working directory inside the container
WORKDIR /app

# Ensure pip, setuptools, and wheel are installed
RUN pip install --no-cache-dir --upgrade pip setuptools wheel

# Copy the requirements file into the container
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Install PaddlePaddle (CPU version)
RUN pip install paddlepaddle==3.0.0b1 -i https://www.paddlepaddle.org.cn/packages/stable/cpu/

# Copy the rest of the application files
COPY . .

# Command to keep the container running
CMD ["tail", "-f", "/dev/null"]
