# Soccer AI Detection ⚽

AI-powered soccer/football video analysis using YOLO object detection. This project detects and tracks players, referees, and the ball in soccer match footage.

## Features

- **Player Detection** - Detect players on the field using YOLOv8/YOLOv11
- **Custom Training** - Train on your own soccer dataset for improved accuracy
- **Video Processing** - Process full match videos with annotated output
- **Visual Annotations** - Draw player indicators with team-colored arcs

## Quick Start

### Option 1: Docker (Recommended)

**Pull pre-built image from Docker Hub:**

```bash
# Pull the image (includes GPU/CUDA support)
docker pull mbizri/soccer-ai:latest

# Run with GPU support
docker run --gpus all -p 8888:8888 \
  -v ./dataset:/app/dataset \
  -v ./input-videos:/app/input-videos \
  mbizri/soccer-ai:latest
```

**Or build from source:**

```bash
# Clone the repo
git clone https://github.com/YOUR_USERNAME/Soccer_AI_Detection.git
cd Soccer_AI_Detection

# Build the Docker image
docker build -t soccer-ai .

# Run with GPU support
docker run --gpus all -p 8888:8888 \
  -v ./dataset:/app/dataset \
  -v ./input-videos:/app/input-videos \
  soccer-ai
```

Then open **http://localhost:8888** in your browser to access Jupyter Lab.

### Option 2: Local Installation

```bash
# Clone the repo
git clone https://github.com/YOUR_USERNAME/Soccer_AI_Detection.git
cd Soccer_AI_Detection

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# For GPU support, install PyTorch with CUDA:
pip install torch torchvision --index-url https://download.pytorch.org/whl/cu121
```

## Project Structure

```
Soccer_AI_Detection/
├── video_processing.ipynb   # Main video processing notebook
├── yolo_inference.ipynb     # Run inference on videos
├── yolo_train.ipynb         # Train custom YOLO model
├── utils.py                 # Helper functions and classes
├── dataset/                 # Training dataset (YOLO format)
├── input-videos/            # Input video files
├── runs/                    # Training outputs
└── requirements.txt         # Python dependencies
```

## Usage

1. **Run Inference** - Open `yolo_inference.ipynb` to detect objects in soccer videos
2. **Train Model** - Open `yolo_train.ipynb` to train on the included dataset
3. **Process Video** - Open `video_processing.ipynb` to create annotated output videos

## Requirements

- Python 3.10+
- NVIDIA GPU with CUDA 12.1+ (for GPU acceleration)
- Docker (optional, but recommended)

## Dataset

The included dataset contains labeled soccer match images with the following classes:
- Player
- Referee  
- Ball

Dataset provided via [Roboflow](https://roboflow.com/).

## License

MIT License

