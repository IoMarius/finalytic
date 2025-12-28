FROM nvidia/cuda:13.0.2-cudnn-devel-ubuntu24.04

#python environment variables for GPU and PYTHON
ENV NVIDIA_VISIBLE_DEVICES=all
ENV NVIDIA_DRIVER_CAPABILITIES=compute,utility
ENV PYTHONUNBUFFERED=1

RUN apt-get update && apt-get install -y --no-install-recommends \
    python3.12 python3-pip python3.12-dev \
    wget unzip  python3-venv\
    libglib2.0-0 libsm6 libxrender1 libxext6 \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

RUN update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.12 1


WORKDIR /app

RUN python3 -m venv /app/venv
ENV PATH="/app/venv/bin:$PATH"

COPY requirements.txt .

RUN pip3 install --no-cache-dir -r requirements.txt

COPY . .

RUN useradd -m botuser && chown -R botuser:botuser /app
USER botuser

ENTRYPOINT ["python", "-m", "app"]