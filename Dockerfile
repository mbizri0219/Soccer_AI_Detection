# ===========================================
# BASE IMAGE (GPU/CUDA VERSION)
# ===========================================
# Using NVIDIA's CUDA image with Ubuntu 22.04
# - cuda:12.1.0 = CUDA version (matches PyTorch cu121)
# - runtime = smaller than 'devel' (no compiler tools)
# - ubuntu22.04 = stable Linux distro
FROM nvidia/cuda:12.1.0-runtime-ubuntu22.04

# ===========================================
# ENVIRONMENT VARIABLES
# ===========================================
# Prevent Python from writing .pyc files and buffering stdout/stderr
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
# Prevent timezone prompts during apt install
ENV DEBIAN_FRONTEND=noninteractive

# ===========================================
# SYSTEM DEPENDENCIES
# ===========================================
# Install Python 3.10 and libraries OpenCV needs
RUN apt-get update && apt-get install -y \
    python3.10 \
    python3-pip \
    python3.10-venv \
    libgl1 \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender-dev \
    libgomp1 \
    ffmpeg \
    && rm -rf /var/lib/apt/lists/* \
    && ln -s /usr/bin/python3.10 /usr/bin/python

# ===========================================
# WORKING DIRECTORY
# ===========================================
WORKDIR /app

# ===========================================
# PYTHON DEPENDENCIES
# ===========================================
COPY requirements.txt .

# Install PyTorch with CUDA 12.1 support FIRST (before requirements.txt)
# This ensures we get GPU-enabled PyTorch, not CPU version
RUN pip install --no-cache-dir torch torchvision --index-url https://download.pytorch.org/whl/cu121

# Install remaining packages (skip torch/torchvision since already installed)
RUN pip install --no-cache-dir -r requirements.txt

# ===========================================
# COPY PROJECT FILES
# ===========================================
COPY . .

# ===========================================
# EXPOSE PORT
# ===========================================
EXPOSE 8888

# ===========================================
# DEFAULT COMMAND
# ===========================================
CMD ["jupyter", "lab", "--ip=0.0.0.0", "--port=8888", "--no-browser", "--allow-root"]
