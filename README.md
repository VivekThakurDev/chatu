# ⚡ Next-Gen AI Chat & Vision Application

![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=Streamlit&logoColor=white)
![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![NVIDIA AI](https://img.shields.io/badge/NVIDIA-76B900?style=for-the-badge&logo=nvidia&logoColor=white)
![OpenAI](https://img.shields.io/badge/OpenAI_SDK-412991?style=for-the-badge&logo=openai&logoColor=white)

A feature-rich, high-performance conversational AI and computer vision web application. Built with **Streamlit**, this application leverages the power of **NVIDIA's AI Endpoints** to deliver real-time streaming chat capabilities using the `Llama-3.1-8B-Instruct` model and advanced image analysis driven by NVIDIA's `Nemotron-Page-Elements-v3` vision model. 

It features a custom-built, modern dark-themed UI design that completely transforms the standard Streamlit interface into a premium web application.

---

## 🌟 Key Features

* **💬 Streaming Conversational AI:** Real-time chat functionality powered by `meta/llama-3.1-8b-instruct` via the NVIDIA AI API.
* **🖼️ Advanced Image Analysis:** Upload images (PNG/JPG) for structural and element analysis using NVIDIA's `nemotron-page-elements-v3` computer vision API.
* **✨ Premium Custom UI:** Fully overridden CSS to provide a modern, glassmorphic dark theme, custom chat bubbles, auto-sizing chat inputs, and fluid animations.
* **🚀 High Performance Updates:** Built with stream batching techniques to provide zero-lag UI updates during text generation.
* **🔒 Secure Configuration:** Environment variable-driven configuration to ensure your API keys remain secure.

## 🛠️ Tech Stack

* **Frontend & Backend Frame:** Python / [Streamlit](https://streamlit.io/)
* **AI Integration:** [OpenAI Python SDK](https://github.com/openai/openai-python) (configured for NVIDIA Endpoints), Requests
* **Models Utilized:** 
  * `meta/llama-3.1-8b-instruct` (Text Generation)
  * `nemotron-page-elements-v3` (Computer Vision)
* **Environment Management:** `python-dotenv`

---

## 🚀 Getting Started

Follow these instructions to set up the project locally on your machine.

### Prerequisites

* **Python 3.8+** installed on your system.
* An active **NVIDIA AI API Key**.

### Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/VivekThakurDev/chatu.git
   cd chatu
   ```

2. **Create a virtual environment (Recommended):**
   ```bash
   python -m venv venv
   # On Windows:
   venv\Scripts\activate
   # On macOS/Linux:
   source venv/bin/activate
   ```

3. **Install the dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up Environment Variables:**
   Create a `.env` file in the root directory of the project and add your NVIDIA API key:
   ```env
   Nvd_API=your_nvidia_api_key_here
   ```

### Running the Application

Once your dependencies are installed and the API key is secured in your `.env` file, launch the application:

```bash
streamlit run app.py
```

The app will automatically open in your default browser at `http://localhost:8501`.

---

## 💻 Usage Guide

1. **Conversational Chat**: Type your queries into the chat input at the bottom of the screen. The Llama 3.1 model will respond in real time, with the UI dynamically sliding up.
2. **Image Analysis**: Open the sidebar on the left. Upload a valid image (.jpg, .jpeg, or .png). Click **Analyze Image** to pass the image to the Nemotron Vision model. The structural bounding box payload will appear in the sidebar, and a log entry will be appended to your main chat. Note: Very large files must be kept under ~180KB base64 encoded as currently structured.

---

## 📸 Screenshots

*(Add your screenshots here before uploading to GitHub)*

* **Main Chat Interface:**
  <!-- ![Main Chat Interface](assets/chat_interface.png) -->
* **Image Analysis Sidebar:**
  <!-- ![Image Analysis](assets/nemotron_sidebar.png) -->

---

## 🤝 Contributing

Contributions, issues, and feature requests are welcome! 
Feel free to check [issues page](https://github.com/VivekThakurDev/chatu/issues).

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
