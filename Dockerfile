# 1. Base image
FROM python:3.11-slim

# 2. Set environment
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# 3. Working directory
WORKDIR /app

# 4. Install system dependencies
RUN apt-get update && \
    apt-get install -y --fix-missing \
        build-essential \
        curl \
        nodejs \
        npm && \
    apt-get clean && \
    rm -rf /var/lib/apt/list

    

# 5. Install Python dependencies
COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# 6. Install Node + Tailwind CSS
COPY package.json .
COPY package-lock.json .
RUN npm install

RUN chmod +x node_modules/.bin/tailwindcss

COPY . .
RUN chmod +x ./node_modules/.bin/tailwindcss && \
    ./node_modules/.bin/tailwindcss -i ./static/src/input.css -o ./static/dist/output.css

# 7. Collect static files
RUN python manage.py collectstatic --noinput

# 8. Expose port and run Daphne (ASGI)
EXPOSE 8000


COPY start.sh ./start.sh
RUN chmod +x ./start.sh
CMD ["./start.sh"]

