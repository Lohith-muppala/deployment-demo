FROM python:3.9-slim

ARG TRAINING=True

COPY . .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Use CMD to specify the startup command based on the TRAINING argument
CMD ["python", "/src/train.py"]
#overriding CMD if training is false.

EXPOSE 80

RUN if [ "$TRAINING" = "False" ]; then python /src/predict.py; fi
