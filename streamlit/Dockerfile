FROM python:3.11-slim

WORKDIR /app

# Copy requirements and install
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy all streamlit files
COPY . .

EXPOSE 8501

# Streamlit run needs the main file
CMD ["streamlit", "run", "Library_App.py", "--server.address=0.0.0.0"]
