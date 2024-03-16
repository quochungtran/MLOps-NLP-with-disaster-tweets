FROM python:3.9

# Create a folder /app if it doesn't exist,
# the /app folder is the current working directory
WORKDIR /app

RUN mkdir /app/models

COPY ../../requirements.txt /app

COPY ../../models/ /app/models

# Disable pip cache to shrink the image size a little bit,
# since it does not need to be re-installed
RUN pip install -r requirements.txt --no-cache-dir

# Copy necessary files to our app
COPY ../../main.py /app

# Set MODEL_DIR env variable
ENV MODEL_PATH /app/models/tfv_regression_model_fold_3.pkl
ENV TFIDF_PATH /app/models/tfidf.pkl


# Port will be exposed, for documentation only
EXPOSE 30000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "30000"]
