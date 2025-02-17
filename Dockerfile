# For more information, please refer to https://aka.ms/vscode-docker-python
FROM python:3-slim

EXPOSE 7000

# Keeps Python from generating .pyc files in the container
ENV PYTHONDONTWRITEBYTECODE=1

# Turns off buffering for easier container logging
ENV PYTHONUNBUFFERED=1

RUN apt-get update && apt-get install -y git-lfs
RUN git lfs install

WORKDIR /app
RUN git clone https://github.com/buithihatien2711/image-search.git . && git lfs pull

# Install pip requirements
COPY requirements.txt .
RUN python -m pip install -r requirements.txt
RUN pip install opencv-python-headless
RUN apt-get update && apt-get install -y \
    libgl1-mesa-glx \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

# WORKDIR /app
# COPY . /app

# Navigate to the course folder where main.py is located
WORKDIR /app/course

# Creates a non-root user with an explicit UID and adds permission to access the /app folder
# For more info, please refer to https://aka.ms/vscode-docker-python-configure-containers
RUN adduser -u 5678 --disabled-password --gecos "" appuser && chown -R appuser /app
USER appuser

# Use Gunicorn with default workers for Flask (WSGI app)
# CMD ["gunicorn", "--bind", "0.0.0.0:7000", "course.image_processing_api:app"]
# CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0:7000"]
CMD ["python", "image_processing_api.py"]