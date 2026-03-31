FROM public.ecr.aws/lambda/python:3.12

# Copy and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY app/ ${LAMBDA_TASK_ROOT}/app/

# Lambda handler entrypoint
CMD ["app.handler.handler"]
