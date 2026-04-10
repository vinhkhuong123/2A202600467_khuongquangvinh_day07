# What is Machine Learning?

**Source:** IBM Cloud Learn - Machine Learning  
**Link:** https://www.ibm.com/cloud/learn/machine-learning  
**Last Updated:** April 2026

---

## Definition

Machine learning is the subset of artificial intelligence (AI) focused on algorithms that can "learn" the patterns of training data and, subsequently, make accurate inferences about new data. This pattern recognition ability enables machine learning models to make decisions or predictions without explicit, hard-coded instructions.

Machine learning has come to dominate the field of AI: it provides the backbone of most modern AI systems, from forecasting models to autonomous vehicles to large language models (LLMs) and other generative AI tools.

---

## Machine Learning vs. Artificial Intelligence

Though "machine learning" and "artificial intelligence" are often used interchangeably, they are not quite synonymous. In short: **all machine learning is AI, but not all AI is machine learning.**

**Artificial Intelligence** is a catch-all term for any program that can use information to make decisions or predictions without active human involvement.

**Machine Learning** specifically refers to systems that learn from experience rather than following explicitly programmed rules.

### Example: Spam Detection

- **Rules-based AI:** A data scientist manually defines criteria for spam (e.g., contains certain keywords, sender not in contacts)
- **Machine Learning:** The system is shown sample emails labeled as spam or not spam, learns patterns automatically, and improves predictions over time

---

## How Machine Learning Works

Machine learning operates through mathematical logic. The characteristics (or "features") of each data point must be expressed numerically so data can be fed into mathematical algorithms.

### Key Steps:

1. **Feature Representation:** Data points are represented as vectors, where each dimension corresponds to a numerical value for a specific feature
2. **Feature Engineering:** The process of selecting and extracting which aspects of data to use in ML algorithms
3. **Model Training:** Algorithms optimize parameters to minimize error through loss functions
4. **Prediction:** The trained model makes inferences on new, unseen data

### Model Parameters and Optimization

Consider a simple linear regression algorithm for predicting home prices:

$$\text{Price} = (A \times \text{square footage}) + (B \times \text{bedrooms}) - (C \times \text{age}) + \text{Base Price}$$

Here, A, B, and C are model parameters. Machine learning finds the optimal values for these parameters so the function outputs the most accurate results.

---

## Types of Machine Learning

All machine learning methods can be categorized into three distinct learning paradigms:

### 1. Supervised Learning

Trains models to predict the "correct" output for a given input by comparing outputs to labeled "ground truth" data.

**Regression Models:** Predict continuous values
- Examples: Linear regression, polynomial regression
- Use cases: Price prediction, temperature forecasting

**Classification Models:** Predict discrete values (categories)
- Examples: Support Vector Machines (SVMs), Naïve Bayes, logistic regression
- Use cases: Email spam detection, image categorization

### 2. Unsupervised Learning

Algorithms discern intrinsic patterns in unlabeled data without any external "correct" output.

**Clustering Algorithms:** Partition data into groups based on similarity
- Examples: K-means clustering, Gaussian mixture models, DBSCAN
- Use cases: Customer segmentation, fraud detection

**Association Algorithms:** Discern correlations and relationships
- Example: E-commerce recommendation engines

**Dimensionality Reduction:** Reduce data complexity while preserving meaningful characteristics
- Examples: Principal Component Analysis (PCA), autoencoders, t-SNE
- Use cases: Data compression, visualization

### 3. Reinforcement Learning (RL)

Models are trained through trial and error, optimizing parameters to maximize reward rather than minimizing error.

**Key Components:**
- **State Space:** All available information relevant to decisions
- **Action Space:** All decisions the model is permitted to make
- **Reward Signal:** Feedback (positive or negative) for each action
- **Policy:** The "decision process" that drives behavior

**Methods:**
- Policy-based methods (e.g., Proximal Policy Optimization)
- Value-based methods (e.g., Q-learning)
- Actor-critic methods (hybrid approaches)

**Applications:** Robotics, video games, reasoning models

### Advanced Variants

**Self-Supervised Learning:** Training on tasks where supervisory signal is obtained directly from unlabeled data
- Example: Autoencoders trained to reconstruct input; LLMs predicting masked words

**Semi-Supervised Learning:** Uses both labeled and unlabeled data
- Leverages assumptions from limited labeled data to incorporate unlabeled data

---

## Deep Learning

Deep learning employs artificial neural networks with many layers (hence "deep") rather than explicitly designed algorithms.

### Neural Networks Architecture

- Comprise interconnected layers of "neurons" or nodes
- Each node performs mathematical operations (activation functions)
- Output of one layer feeds into the next layer
- **Key Feature:** Activation functions are nonlinear, enabling modeling of complex patterns

### How Parameters Are Optimized

- Each connection has a unique weight (multiplier controlling contribution)
- Neurons also have bias terms
- **Backpropagation algorithm** enables computation of how each node contributes to overall error
- **Gradient descent** algorithms adjust weights to minimize loss
- Deep learning requires large amounts of data and computational resources

### Notable Deep Learning Architectures

**Convolutional Neural Networks (CNNs)**
- Apply weighted "filters" to extract important features
- Primarily used for computer vision tasks
- Success in image classification, object detection, image segmentation

**Recurrent Neural Networks (RNNs)**
- Designed for sequential data
- Create internal "memory" (hidden state) to understand context and order
- Use cases: Time series analysis, speech recognition, text generation

**Transformers**
- Introduced in 2017; revolutionized NLP
- Use innovative attention mechanism to focus on relevant parts of input
- Foundation of modern LLMs and generative AI
- Achieve state-of-the-art results across most ML subdomains

**Mamba Models**
- Relatively new architecture (2023)
- Based on state space models
- Emerging as rival to transformers, especially for LLMs

---

## Machine Learning Use Cases

### Computer Vision

Subdomain of AI for image data, video data, and visual perception tasks
- **Subfields:** Image classification, object detection, image segmentation, OCR
- **Applications:** Healthcare diagnostics, facial recognition, autonomous vehicles

### Natural Language Processing (NLP)

Diverse array of tasks concerning text, speech, and language data
- **Subdomains:** Chatbots, speech recognition, machine translation, sentiment analysis, text generation, summarization
- **Recent Advances:** Large language models advancing NLP at unprecedented pace

### Time Series Analysis

Pattern recognition and prediction on sequential data over time
- **Applications:** Anomaly detection, market analysis, forecasting

### Image Generation

Generative models create original images from patterns learned during training
- **Techniques:** Diffusion models, Variational Autoencoders (VAEs), Generative Adversarial Networks (GANs)

---

## Machine Learning Operations (MLOps)

MLOps is a set of practices for implementing an assembly-line approach to building, deploying, and maintaining ML models.

**Key Practices:**

1. **Data Curation & Preprocessing:** Careful preparation of training data
2. **Model Selection:** Choosing appropriate algorithms for the task
3. **Validation & Testing:** Using benchmark datasets; monitoring key performance metrics
4. **Monitoring & Maintenance:** Post-deployment tracking for model drift and performance degradation
5. **Model Governance:** Ensuring continued efficacy, especially in regulated industries

---

## ML Libraries & Frameworks

### Deep Learning Frameworks
- **PyTorch:** Flexible framework with dynamic computation graphs
- **TensorFlow:** Production-ready framework by Google
- **Keras:** High-level API for neural networks
- **Hugging Face Transformers:** Specialized for NLP and LLMs

### Traditional ML Libraries
- **Scikit-learn:** General-purpose ML algorithms
- **XGBoost:** Gradient boosting for structured data
- **Pandas:** Data manipulation and analysis
- **NumPy:** Numerical computing
- **SciPy:** Scientific computing

### Visualization & Utilities
- **Matplotlib:** Data visualization
- **Jupyter:** Interactive notebooks for experimentation

---

## Key Takeaways

1. **Pattern Learning:** ML systems learn patterns from data rather than following explicit rules
2. **Three Paradigms:** Supervised, unsupervised, and reinforcement learning serve different purposes
3. **Deep Learning Dominance:** Neural networks with multiple layers dominate modern AI applications
4. **Data & Computation:** Success requires high-quality data and computational resources
5. **Generalization:** The goal is to make accurate predictions on new data, not just memorize training data

---

## References

- IBM Cloud Learn: https://www.ibm.com/cloud/learn/machine-learning
- Arthur L. Samuel (1959): "Some Studies in Machine Learning Using the Game of Checkers," IBM Journal
