FROM python:3.12-slim AS builder

# Prevent .pyc files
ENV PYTHONDONTWRITEBYTECODE=1

# Install system dependencies needed for building pygame
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        libsdl2-dev \
        libsdl2-mixer-dev \
        libsdl2-image-dev \
        libsdl2-ttf-dev \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /build

COPY requirements.txt .
RUN pip install --no-cache-dir --prefix=/install -r requirements.txt


FROM python:3.12-slim

# Use dummy SDL drivers so pygame initializes in a headless container
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV SDL_VIDEODRIVER=dummy
ENV SDL_AUDIODRIVER=dummy

# Runtime SDL2 libraries only
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        libsdl2-2.0-0 \
        libsdl2-mixer-2.0-0 \
        libsdl2-image-2.0-0 \
        libsdl2-ttf-2.0-0 \
        vlc \
    && rm -rf /var/lib/apt/lists/*

# Copy installed packages from builder
COPY --from=builder /install /usr/local

WORKDIR /app

COPY pomodoro.py new_task.py sql_file.py config.py countdown_timer.py tone.py ./
COPY end-alarm-tone.mp3 start-alarm-tone.mp3 ./
COPY test_pomodoro.py ./

RUN useradd --create-home --shell /bin/bash appuser && \
    chown -R appuser:appuser /app
USER appuser

HEALTHCHECK --interval=30s --timeout=5s --start-period=5s --retries=3 \
    CMD python -c "import pomodoro" || exit 1

CMD ["python", "pomodoro.py", "-i"]
