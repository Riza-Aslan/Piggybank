ARG BUILD_FROM
# Stage 1: Build the Vue 3 Frontend (optimized for layer caching)
FROM node:24-alpine AS frontend-builder
WORKDIR /app

# Copy only dependency files first – Docker caches this layer until package.json changes
COPY frontend/package*.json ./

# npm ci is faster and reproducible (uses package-lock.json strictly)
RUN npm ci --quiet

# Now copy the rest of the source and build
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
# Copy built frontend assets from stage 1
COPY --from=frontend-builder /app/dist /app/backend/static

# Register run.sh as s6 service so the base image (s6-overlay) starts it as PID 1
RUN mkdir -p /etc/services.d/piggybank
COPY run.sh /etc/services.d/piggybank/run
RUN chmod a+x /etc/services.d/piggybank/run
