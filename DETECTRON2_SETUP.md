# Detectron2 Setup Guide

This guide will help you set up Detectron2 to replace Azure Computer Vision API.

## Prerequisites

- Python 3.8 or higher
- CUDA-capable GPU (optional, but recommended for better performance)
- pip

## Installation Steps

### 1. Install PyTorch

First, install PyTorch based on your system:

**For CUDA (GPU support):**
```bash
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
```

**For CPU only:**
```bash
pip install torch torchvision torchaudio
```

### 2. Install Detectron2

**For CUDA (GPU support) or CPU:**
```bash
# Install ninja first (build tool)
pip install ninja

# Then install Detectron2 with --no-build-isolation flag
# This is needed because Detectron2's setup requires torch to be available
pip install 'git+https://github.com/facebookresearch/detectron2.git' --no-build-isolation
```

**Alternative for CPU only (if the above doesn't work):**
```bash
pip install detectron2 -f https://dl.fbaipublicfiles.com/detectron2/wheels/cpu/torch2.0/index.html
```

### 3. Install OCR Libraries

Choose one of the following OCR options:

**Option A: EasyOCR (Recommended - easier to set up)**
```bash
pip install easyocr
```

**Option B: pytesseract (Requires system package)**
```bash
# On macOS:
brew install tesseract

# On Ubuntu/Debian:
sudo apt-get install tesseract-ocr

# Then install Python package:
pip install pytesseract
```

### 4. Install Other Dependencies

```bash
pip install -r requirements.txt
```

## Verification

To verify the installation, run:

```python
python -c "import detectron2; print('Detectron2 installed successfully')"
python -c "import easyocr; print('EasyOCR installed successfully')"
```

## Model Information

By default, the application uses the **Faster R-CNN R50-FPN 3x** model from the COCO dataset, which can detect 80 common object classes including:
- People
- Vehicles (cars, trucks, buses, motorcycles, bicycles)
- Animals
- Furniture
- Electronics
- Food items
- Sports equipment
- And more...

You can change the model by setting the `DETECTRON2_MODEL` environment variable in your `.env` file:

```
DETECTRON2_MODEL=COCO-Detection/faster_rcnn_R_50_FPN_3x.yaml
```

Other available models:
- `COCO-Detection/faster_rcnn_R_101_FPN_3x.yaml` (more accurate, slower)
- `COCO-InstanceSegmentation/mask_rcnn_R_50_FPN_3x.yaml` (includes segmentation)
- `COCO-Keypoints/keypoint_rcnn_R_50_FPN_3x.yaml` (includes keypoint detection)

## Performance Tips

1. **Use GPU if available**: Detectron2 runs much faster on GPU. The service will automatically use GPU if available.

2. **Adjust frame rate**: In `config.py`, you can adjust `FRAME_RATE` to process fewer frames per second if performance is an issue.

3. **Model selection**: Smaller models are faster but less accurate. Choose based on your needs.

## Troubleshooting

### Import Error: "No module named 'detectron2'"
- Make sure you've installed Detectron2 correctly
- Try reinstalling: `pip uninstall detectron2 && pip install 'git+https://github.com/facebookresearch/detectron2.git'`

### CUDA Out of Memory
- Use a smaller model
- Reduce image resolution
- Process fewer frames per second

### OCR Not Working
- For EasyOCR: Make sure it's installed: `pip install easyocr`
- For pytesseract: Make sure tesseract-ocr is installed on your system

## Advantages Over Azure

1. **No API limits**: Process as many images as you want
2. **No internet required**: Runs completely locally
3. **No costs**: Free and open-source
4. **Privacy**: All processing happens on your machine
5. **Customizable**: Can train custom models for your specific needs

## Migration Notes

- The API interface remains the same, so your existing code should work without changes
- Face detection is not included by default (can be added separately if needed)
- Scene descriptions are generated from detected objects rather than using a separate captioning model

