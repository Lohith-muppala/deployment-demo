FROM python:3.9-slim

ARG TRAINING=True
WORKDIR /app

COPY . /app

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

WORKDIR /app/src

# Use CMD to specify the startup command based on the TRAINING argument
CMD ["python", "train.py"]
#overriding CMD if training is false.
RUN if [ "$TRAINING" = "False" ]; then echo "Overriding CMD for prediction"; CMD ["python", "predict.py"]; fi
