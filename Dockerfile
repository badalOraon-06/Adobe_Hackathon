# Use official Python slim image (small and fast)
FROM --platform=linux/amd64 python:3.10-slim

# Set working directory inside container
WORKDIR /app

# Copy all source files from local to container
COPY app/ ./

# Upgrade pip
RUN pip install --upgrade pip


# Install torch first (CPU version)
RUN pip install torch==2.0.0 torchvision==0.15.1 torchaudio==2.0.1 --index-url https://download.pytorch.org/whl/cpu

# Install detectron2 from official CPU wheel link
RUN pip install detectron2 -f https://dl.fbaipublicfiles.com/detectron2/wheels/cpu/torch2.0/index.html



# Install other dependencies
RUN pip install layoutparser==0.3.4 Pillow PyMuPDF
RUN pip install "layoutparser[layoutmodels]==0.3.4"


# Install Python dependencies from requirements.txt
# RUN pip install --no-cache-dir -r requirements.txt

# Run the main script when container starts
# CMD ["python", "main.py"]
