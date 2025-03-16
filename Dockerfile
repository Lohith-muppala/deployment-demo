FROM python:3.9-slim

ARG TRAINING=True
ENV TRAINING=$TRAINING

COPY . .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 80

CMD ["sh", "-c", "if [ \"$TRAINING\" = \"False\" ]; then python /src/predict.py; else python /src/train.py; fi"]