FROM python:3.13-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
    libglib2.0-0 libgl1-mesa-glx libxrender1 libsm6 libxext6 \
    && apt-get clean

# Set working directory
WORKDIR /app

# Copy source code
COPY . .

# Install Python packages
RUN pip install --no-cache-dir -r requirements.txt

# Download NLTK tokenizer
RUN python -c "import nltk; nltk.download('punkt'); nltk.download('punkt_tab')"

# Expose Streamlit default port
EXPOSE 8501

# Run the app
CMD ["streamlit", "run", "app/ui/chat_app.py", "--server.port=8501", "--server.address=0.0.0.0"]
