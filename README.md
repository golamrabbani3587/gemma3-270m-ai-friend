# AI Friend - AI Chat Companion

A fine-tuned conversational AI model based on Google's Gemma 3 270M, designed for emotional support and companionship.

## 🚀 Features

- **Fine-tuned Model**: Custom-trained Gemma 3 270M for conversational AI
- **Emotional Support**: Designed to provide empathetic and supportive responses
- **Interactive Chat Interface**: Web-based chat application with Gradio
- **Efficient Training**: Uses LoRA (Low-Rank Adaptation) for parameter-efficient fine-tuning

## 📁 Project Structure

```
gemma3-27m-test/
├── chat_interface.py          # Gradio chat application
├── api_server.py             # FastAPI backend server
├── web_server.py             # Web server for frontend
├── start_app.py              # Startup script for both servers
├── train_model.py            # Model training script
├── test_model.py             # Model testing script
├── training_data/            # Training datasets
│   ├── raw_data.json         # Original training data
│   ├── train.json            # Processed training data
│   ├── test.json             # Test dataset
│   └── expanded_train.json   # Enhanced training dataset
├── trained_model/            # Final trained model
├── model_checkpoints/        # Training checkpoints
├── old_model/               # Previous model version
├── old_checkpoints/         # Previous checkpoints
├── static/                  # Frontend static files
│   └── index.html          # Main HTML interface
├── gemma-env/               # Python virtual environment
└── requirements_mac.txt     # Dependencies
```

## 🛠️ Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd gemma3-27m-test
   ```

2. **Set up virtual environment**
   ```bash
   python -m venv gemma-env
   source gemma-env/bin/activate  # On macOS/Linux
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements_mac.txt
   ```

## 🎯 Usage

### Training the Model

```bash
python train_model.py
```

This will:
- Load the Gemma 3 270M base model
- Fine-tune it on the conversational dataset
- Save the trained model to `./trained_model/`

### Testing the Model

```bash
python test_model.py
```

This will test the model with various conversational prompts to verify its performance.

### Running the Chat Interface

#### Option 1: Gradio Interface (Simple)
```bash
python chat_interface.py
```

#### Option 2: Professional Web Interface (Recommended)
```bash
# Start both API and web servers
python start_app.py

# Or start them separately:
python api_server.py    # API server on port 8001
python web_server.py    # Web server on port 3000
```

Then open your browser and go to: `http://localhost:3000`

**Features:**
- 💬 Professional chat interface with voice capabilities
- 🎤 Voice recognition and text-to-speech
- 💕 Beautiful animations and floating hearts
- 📱 Fully responsive design
- 🔄 Real-time conversation with context
- 🎨 Modern gradient animations
- 📱 Fully responsive design for all devices
- 🔄 Real-time conversation with last Q&A context
- 🎯 Efficient message handling and professional animations
- 🎨 Beautiful gradient animations and modern UI

## 🔧 Model Details

- **Base Model**: Google Gemma 3 270M (Instruction-tuned)
- **Fine-tuning Method**: LoRA (Low-Rank Adaptation)
- **Training Data**: 59 conversational examples
- **Training Epochs**: 5
- **Learning Rate**: 5e-4

## 📊 Training Parameters

- **LoRA Rank**: 16
- **LoRA Alpha**: 32
- **Target Modules**: q_proj, v_proj, k_proj, o_proj, gate_proj, up_proj, down_proj
- **Batch Size**: 2
- **Gradient Accumulation**: 4 steps

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📄 License

This project uses the Gemma 3 model which is subject to Google's responsible AI license.

## ⚠️ Disclaimer

This is a research project for educational purposes. The model is designed for conversational AI and emotional support, but should not replace professional mental health services.
