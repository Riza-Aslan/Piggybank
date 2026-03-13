ARG BUILD_FROM
# Stage 1: Build the Vue 3 Frontend
FROM node:20-alpine AS frontend-builder
WORKDIR /app/frontend

# Provide package.json and install dependencies
COPY frontend/package*.json ./
RUN npm install

# Build the frontend application
COPY frontend/ ./
RUN npm run build


# Stage 2: Final Home Assistant Add-on Image
FROM $BUILD_FROM

# Install Python 3 and SQLite
RUN apk add --no-cache \
    python3 \
    py3-pip \
    sqlite

# Create virtual environment
RUN python3 -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

WORKDIR /app

# Install Python dependencies
COPY backend/requirements.txt /app/backend/
RUN pip3 install --no-cache-dir -r /app/backend/requirements.txt

# Copy source tree for backend
COPY backend/ /app/backend/
COPY run.sh /app/

# Copy built frontend assets from stage 1
COPY --from=frontend-builder /app/frontend/dist /app/backend/static

RUN chmod a+x /app/run.sh

CMD [ "/app/run.sh" ]
