# Project Proposal

## Advanced Skin Cancer Detection System Using HAM10000 Dataset

## 1. Project Title

**DermaVision AI: An Explainable Deep Learning System for Skin Lesion Classification and Medical Image Analysis**

---

## 2. Project Overview

This project aims to develop an advanced AI-powered skin lesion analysis system using the **HAM10000 Skin Cancer MNIST dataset**. The system will classify dermoscopic skin lesion images into seven diagnostic categories, provide explainable visual evidence using Grad-CAM, and expose the model through a web/mobile-ready application.

The HAM10000 dataset contains **10,015 dermatoscopic images** across seven skin lesion classes and is publicly available for academic machine learning research.

This project will not be limited to a basic CNN model. It will follow a full production-style pipeline including:

* Data preprocessing
* Image augmentation
* Class imbalance handling
* Deep learning model training
* Segmentation-assisted classification
* Explainable AI
* Model evaluation
* API development
* Web/mobile interface
* Docker deployment
* MLOps experiment tracking

---

## 3. Problem Statement

Skin cancer is one of the most common and dangerous forms of cancer. Early detection is highly important, but diagnosis often requires specialist dermatological knowledge. Manual diagnosis can be time-consuming, subjective, and unavailable in areas with limited medical resources.

This project proposes a computer-aided diagnosis system that can analyze dermoscopic skin lesion images and classify them into possible disease categories. The system will also provide visual explanations to help users understand which image regions influenced the model’s decision.

**Important note:** This system is designed for educational and research purposes only. It must not be used as a replacement for professional medical diagnosis.

---

## 4. Dataset

### Main Dataset

**Dataset Name:** Skin Cancer MNIST: HAM10000
**Source:** Kaggle
**Link:** https://www.kaggle.com/datasets/kmader/skin-cancer-mnist-ham10000
**Size:** 10,015 dermoscopic images
**Classes:** 7 skin lesion categories

### Additional Dataset

**Dataset Name:** HAM10000 Lesion Segmentations
**Source:** Kaggle
**Link:** https://www.kaggle.com/datasets/tschandl/ham10000-lesion-segmentations
**Purpose:** Binary lesion masks for segmentation-assisted classification. The segmentation dataset provides 10,015 binary masks corresponding to HAM10000 images.

---

## 5. Disease Classes

The model will classify images into the following seven categories:

| Code  | Disease Class                                   |
| ----- | ----------------------------------------------- |
| akiec | Actinic keratoses and intraepithelial carcinoma |
| bcc   | Basal cell carcinoma                            |
| bkl   | Benign keratosis-like lesions                   |
| df    | Dermatofibroma                                  |
| mel   | Melanoma                                        |
| nv    | Melanocytic nevi                                |
| vasc  | Vascular lesions                                |

---

## 6. Project Objectives

### Main Objective

To build a complete AI-based skin lesion classification system using deep learning, explainable AI, and full-stack deployment.

### Specific Objectives

1. Preprocess and clean dermoscopic image data.
2. Handle class imbalance using weighted loss, oversampling, and augmentation.
3. Train multiple deep learning models.
4. Compare CNN and transformer-based architectures.
5. Integrate lesion segmentation for improved image focus.
6. Generate Grad-CAM heatmaps for explainability.
7. Build a FastAPI backend for model inference.
8. Build a React or Flutter frontend for image upload and result display.
9. Track experiments using MLflow.
10. Containerize the system using Docker.
11. Prepare technical documentation, model card, and final report.

---

## 7. Proposed System Architecture

```text
User Uploads Skin Image
        |
        v
Frontend Application
        |
        v
FastAPI Backend
        |
        v
Image Validation
        |
        v
Preprocessing Pipeline
        |
        v
Optional Lesion Segmentation
        |
        v
Classification Model
        |
        v
Prediction + Confidence Score
        |
        v
Grad-CAM Explanation
        |
        v
Result Dashboard / Report
```

---

## 8. Technology Stack

### Programming Language

* Python

### Machine Learning / Deep Learning

* PyTorch
* TorchVision
* TensorFlow/Keras, optional
* Scikit-learn
* NumPy
* Pandas
* OpenCV
* Albumentations

### Model Architectures

* EfficientNet-B0/B3
* ResNet50
* DenseNet121
* ConvNeXt-Tiny
* Vision Transformer, optional
* U-Net for segmentation

### Explainable AI

* Grad-CAM
* Score-CAM, optional
* SHAP, optional

### MLOps

* MLflow for experiment tracking
* DVC for dataset/model versioning
* GitHub Actions for CI/CD
* Docker for containerization

### Backend

* FastAPI
* Uvicorn
* Pydantic

### Frontend

* React.js, recommended
* Tailwind CSS
* Chart.js/Recharts

### Database

* PostgreSQL, optional
* SQLite for lightweight prototype

### Deployment

* Docker
* Render / Railway / AWS EC2 / Google Cloud Run
* Hugging Face Spaces, optional demo deployment

---

## 9. Methodology

### Phase 1: Data Collection

Download the HAM10000 dataset and segmentation masks from Kaggle.

Required files:

```text
HAM10000_metadata.csv
HAM10000_images_part_1/
HAM10000_images_part_2/
HAM10000_segmentations/
```

---

### Phase 2: Exploratory Data Analysis

Perform analysis on:

* Class distribution
* Age distribution
* Gender distribution
* Lesion localization
* Image resolution
* Missing values
* Duplicate lesion IDs
* Class imbalance

Expected output:

* EDA notebook
* Dataset summary report
* Visual charts
* Class imbalance analysis

---

### Phase 3: Data Preprocessing

Steps:

1. Merge metadata with image paths.
2. Resize images to 224×224 or 384×384.
3. Normalize pixel values.
4. Remove or handle missing metadata.
5. Encode class labels.
6. Split dataset into training, validation, and test sets.
7. Use stratified splitting to preserve class distribution.
8. Apply image augmentation only to training data.

Preprocessing techniques:

* Resizing
* Normalization
* Hair artifact reduction, optional
* Contrast enhancement, optional
* CLAHE, optional
* Lesion cropping using segmentation masks

---

### Phase 4: Data Augmentation

Use Albumentations for strong medical image augmentation:

```text
RandomRotate90
HorizontalFlip
VerticalFlip
ShiftScaleRotate
RandomBrightnessContrast
HueSaturationValue
GaussianBlur
CoarseDropout
ElasticTransform
```

Purpose:

* Reduce overfitting
* Improve generalization
* Balance minority classes

---

### Phase 5: Class Imbalance Handling

HAM10000 is class-imbalanced, so the project will use:

* Class-weighted cross entropy loss
* Focal loss
* Weighted random sampler
* Oversampling minority classes
* Macro F1-score for evaluation

---

### Phase 6: Baseline Model

Train a simple baseline CNN first.

Purpose:

* Establish initial benchmark
* Verify data pipeline
* Compare against advanced models

Baseline model:

```text
Conv2D
BatchNorm
ReLU
MaxPooling
Dropout
Fully Connected Layer
Softmax
```

---

### Phase 7: Advanced Classification Models

Train and compare:

1. ResNet50
2. DenseNet121
3. EfficientNet-B0
4. EfficientNet-B3
5. ConvNeXt-Tiny
6. Vision Transformer, optional

Recommended final model:

```text
EfficientNet-B3 + Focal Loss + Grad-CAM
```

Why EfficientNet?

* Strong performance on image classification
* Efficient parameter usage
* Suitable for deployment
* Good balance between accuracy and speed

---

### Phase 8: Segmentation-Assisted Classification

Use HAM10000 segmentation masks to isolate lesion regions.

Pipeline:

```text
Original Image
        |
        v
Segmentation Mask
        |
        v
Lesion Cropping / Background Removal
        |
        v
Classification Model
```

Optional advanced model:

```text
U-Net for lesion segmentation
+
EfficientNet for classification
```

This creates a two-stage medical image analysis pipeline.

---

### Phase 9: Explainable AI

Use Grad-CAM to visualize the regions that influenced the model prediction.

Output:

* Original image
* Heatmap
* Overlay image
* Predicted class
* Confidence score

Example result:

```text
Prediction: Melanoma
Confidence: 87.4%
Explanation: The model focused on the irregular dark lesion region.
```

---

### Phase 10: Model Evaluation

Use the following metrics:

| Metric           | Purpose                          |
| ---------------- | -------------------------------- |
| Accuracy         | Overall correctness              |
| Precision        | False positive control           |
| Recall           | False negative control           |
| F1-score         | Balanced performance             |
| Macro F1-score   | Important for imbalanced classes |
| ROC-AUC          | Class separation ability         |
| Confusion Matrix | Error analysis                   |
| Inference Time   | Deployment performance           |

Main evaluation focus:

```text
Macro F1-score
Recall for melanoma
ROC-AUC
Confusion matrix
```

---

## 10. System Modules

### Module 1: Data Module

Responsibilities:

* Load images
* Load metadata
* Create train/validation/test splits
* Apply transformations
* Handle class labels

Files:

```text
src/data/dataset.py
src/data/preprocessing.py
src/data/augmentation.py
```

---

### Module 2: Training Module

Responsibilities:

* Train models
* Validate models
* Save checkpoints
* Log metrics
* Use early stopping

Files:

```text
src/training/train.py
src/training/validate.py
src/training/losses.py
```

---

### Module 3: Model Module

Responsibilities:

* Define CNN models
* Load pretrained models
* Define segmentation model
* Export final model

Files:

```text
src/models/classifier.py
src/models/segmentation.py
src/models/model_factory.py
```

---

### Module 4: Explainability Module

Responsibilities:

* Generate Grad-CAM heatmaps
* Overlay heatmaps on images
* Save explanation images

Files:

```text
src/explainability/gradcam.py
src/explainability/visualize.py
```

---

### Module 5: API Module

Responsibilities:

* Accept image uploads
* Preprocess image
* Run inference
* Generate explanation
* Return prediction response

Files:

```text
backend/main.py
backend/routes/predict.py
backend/schemas.py
backend/utils.py
```

---

### Module 6: Frontend Module

Responsibilities:

* Upload image
* Display prediction
* Display confidence
* Display Grad-CAM heatmap
* Show safety disclaimer
* Show history dashboard, optional

Files:

```text
frontend/src/App.jsx
frontend/src/components/ImageUpload.jsx
frontend/src/components/PredictionCard.jsx
frontend/src/components/HeatmapViewer.jsx
```

---

## 11. Proposed Folder Structure

```text
dermavision-ai/
│
├── data/
│   ├── raw/
│   ├── processed/
│   └── external/
│
├── notebooks/
│   ├── 01_eda.ipynb
│   ├── 02_baseline_model.ipynb
│   ├── 03_advanced_training.ipynb
│   └── 04_explainability.ipynb
│
├── src/
│   ├── data/
│   │   ├── dataset.py
│   │   ├── preprocessing.py
│   │   └── augmentation.py
│   │
│   ├── models/
│   │   ├── classifier.py
│   │   ├── segmentation.py
│   │   └── model_factory.py
│   │
│   ├── training/
│   │   ├── train.py
│   │   ├── validate.py
│   │   ├── losses.py
│   │   └── metrics.py
│   │
│   ├── explainability/
│   │   ├── gradcam.py
│   │   └── visualize.py
│   │
│   └── utils/
│       ├── config.py
│       └── logger.py
│
├── backend/
│   ├── main.py
│   ├── routes/
│   │   └── predict.py
│   ├── schemas.py
│   └── requirements.txt
│
├── frontend/
│   ├── src/
│   ├── package.json
│   └── vite.config.js
│
├── models/
│   ├── checkpoints/
│   └── final_model.pt
│
├── reports/
│   ├── figures/
│   ├── model_card.md
│   └── final_report.pdf
│
├── tests/
│   ├── test_preprocessing.py
│   ├── test_api.py
│   └── test_inference.py
│
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── README.md
├── dvc.yaml
├── mlflow_tracking/
└── .github/
    └── workflows/
        └── ci.yml
```

---

## 12. Model Training Strategy

### Step 1: Baseline

Train a simple CNN.

### Step 2: Transfer Learning

Train pretrained models:

```text
ResNet50
DenseNet121
EfficientNet-B0
EfficientNet-B3
ConvNeXt-Tiny
```

### Step 3: Fine-Tuning

Unfreeze deeper layers and fine-tune with a lower learning rate.

### Step 4: Class Imbalance Optimization

Use:

```text
Weighted Cross Entropy
Focal Loss
WeightedRandomSampler
```

### Step 5: Hyperparameter Tuning

Tune:

```text
Learning rate
Batch size
Optimizer
Dropout
Image size
Loss function
Scheduler
```

Recommended tools:

```text
Optuna
Ray Tune
MLflow
```

---

## 13. API Design

### Endpoint 1: Health Check

```http
GET /health
```

Response:

```json
{
  "status": "ok"
}
```

### Endpoint 2: Predict Skin Lesion

```http
POST /predict
```

Input:

```text
Image file
```

Output:

```json
{
  "predicted_class": "mel",
  "diagnosis_name": "Melanoma",
  "confidence": 0.874,
  "top_3_predictions": [
    {
      "class": "mel",
      "confidence": 0.874
    },
    {
      "class": "bkl",
      "confidence": 0.081
    },
    {
      "class": "bcc",
      "confidence": 0.045
    }
  ],
  "gradcam_url": "/outputs/gradcam/image_001.png",
  "disclaimer": "This result is for educational purposes only and is not a medical diagnosis."
}
```

---

## 14. Frontend Features

The frontend will include:

1. Image upload interface
2. Image preview
3. Prediction result card
4. Confidence score visualization
5. Top-3 class probabilities
6. Grad-CAM explanation viewer
7. Class information section
8. Medical disclaimer
9. Dark/light mode, optional
10. Prediction history, optional

---

## 15. MLOps Pipeline

The project will include an MLOps workflow:

```text
Data Versioning: DVC
Experiment Tracking: MLflow
Model Registry: MLflow
Containerization: Docker
CI/CD: GitHub Actions
Deployment: Cloud Run / Render / AWS EC2
```

Pipeline:

```text
Raw Data
   |
   v
DVC Versioning
   |
   v
Preprocessing
   |
   v
Training
   |
   v
MLflow Experiment Tracking
   |
   v
Model Evaluation
   |
   v
Model Registry
   |
   v
FastAPI Deployment
   |
   v
Frontend Integration
```

---

## 16. Testing Plan

### Unit Testing

Test:

* Image preprocessing
* Label encoding
* Model loading
* API response format

### Integration Testing

Test:

* Image upload to prediction pipeline
* Backend and frontend communication
* Grad-CAM generation

### Performance Testing

Test:

* Inference latency
* API response time
* Memory usage
* Docker container performance

---

## 17. Expected Results

Expected outputs:

1. Trained skin lesion classification model
2. Segmentation-assisted preprocessing pipeline
3. Grad-CAM explainability system
4. FastAPI backend
5. React frontend
6. Dockerized deployment
7. MLflow experiment dashboard
8. Final technical report
9. GitHub repository
10. Demo video

Expected performance target:

```text
Accuracy: 85%+
Macro F1-score: 75%+
Melanoma recall: high priority
Inference time: under 2 seconds per image
```

---

## 18. Evaluation and Validation

The model will be evaluated using:

* Train/validation/test split
* Confusion matrix
* Per-class precision
* Per-class recall
* Per-class F1-score
* Macro F1-score
* ROC-AUC
* Grad-CAM visual inspection

Special focus will be placed on melanoma recall because false negatives in high-risk classes are more serious.

---

## 19. Ethical and Safety Considerations

This system must include clear safety warnings.

Important limitations:

1. The model is trained on a limited public dataset.
2. It may not generalize well to real-world clinical images.
3. It may be biased due to dataset imbalance.
4. It cannot replace a dermatologist.
5. It should only be used for education, research, and demonstration.

Required disclaimer:

```text
This application is for educational and research purposes only. It is not a medical device and must not be used as a substitute for professional medical diagnosis, treatment, or advice. Please consult a qualified dermatologist for medical concerns.
```

---

## 20. Project Timeline

### Week 1: Research and Setup

* Study HAM10000 dataset
* Set up GitHub repository
* Set up Python environment
* Download dataset
* Prepare folder structure

### Week 2: EDA and Preprocessing

* Analyze metadata
* Visualize class imbalance
* Create preprocessing pipeline
* Create train/validation/test split

### Week 3: Baseline Model

* Train simple CNN
* Evaluate baseline results
* Create first confusion matrix

### Week 4: Advanced Models

* Train ResNet50
* Train DenseNet121
* Train EfficientNet
* Compare results

### Week 5: Optimization

* Apply focal loss
* Use weighted sampling
* Tune hyperparameters
* Improve minority-class performance

### Week 6: Segmentation and Explainability

* Add segmentation masks
* Generate lesion-focused inputs
* Implement Grad-CAM
* Compare segmentation-assisted vs normal classification

### Week 7: Backend Development

* Build FastAPI backend
* Add prediction endpoint
* Add Grad-CAM endpoint
* Test API with sample images

### Week 8: Frontend Development

* Build React interface
* Add upload page
* Display prediction results
* Display Grad-CAM heatmap

### Week 9: MLOps and Deployment

* Add MLflow
* Add DVC
* Add Docker
* Add GitHub Actions
* Deploy application

### Week 10: Final Report and Presentation

* Write final report
* Create model card
* Prepare presentation slides
* Record demo video

---

## 21. Final Deliverables

The final submission will include:

1. Full GitHub repository
2. Clean source code
3. EDA notebook
4. Training notebooks
5. Final trained model
6. API backend
7. Frontend application
8. Docker setup
9. MLflow experiment logs
10. Model evaluation report
11. Grad-CAM explainability outputs
12. Final project report
13. Presentation slides
14. Demo video

---

## 22. Innovation / Advanced Features

This project is advanced because it includes:

* Transfer learning
* Medical image preprocessing
* Segmentation-assisted classification
* Explainable AI
* Class imbalance handling
* MLOps
* API deployment
* Full-stack application
* Model monitoring-ready architecture
* Ethical AI documentation

---

## 23. Possible Future Enhancements

Future improvements may include:

1. Mobile app using Flutter
2. Real-time camera-based lesion capture
3. Doctor review dashboard
4. Patient history management
5. Integration with ISIC datasets
6. Federated learning for privacy-preserving training
7. Model quantization for mobile deployment
8. Skin tone fairness evaluation
9. Multimodal model using image + patient metadata
10. LLM-generated patient-friendly explanation report

---

## 24. Conclusion

This project proposes a complete advanced skin cancer detection system using the HAM10000 dataset. It combines computer vision, deep learning, explainable AI, backend development, frontend development, MLOps, and deployment. The final product will be a portfolio-quality AI system rather than a simple machine learning notebook.

The project will demonstrate strong skills in machine learning engineering, software engineering, medical AI, and responsible AI development.
