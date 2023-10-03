# Use an official Python runtime as a parent image
FROM python:3.10-slim-buster


WORKDIR /Task/evadellaapp.py


COPY requirements.txt .


RUN pip install --no-cache-dir -r requirements.txt


COPY . .

EXPOSE 8501

# Run Streamlit when the container launches
CMD ["streamlit", "run", "Task/evadellaapp.py"]