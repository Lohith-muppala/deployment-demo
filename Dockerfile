
FROM python:3.9-slim


ARG TRAINING=True

ENV APP_HOME /app
WORKDIR $APP_HOME

# Copy requirements file
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy source code
COPY src /app/src

# Conditionally install packages based on the environment
RUN if [ "$TRAINING" = "True" ]; then \
    CMD ["python", "/app/src/train.py"] \
    else \
    CMD ["python", "/app/src/predict.py"] \
    exit 1; \
    fi

