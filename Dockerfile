# Pinned analysis environment (docs/STATISTICAL_REVIEW_2026-10-24.md, point 8).
# Base image pinned by digest: python:3.12.15-slim-bookworm, linux/amd64
# (digest from docker-library/repo-info, 24 Oct 2026). Change it only deliberately, logged in
# prereg/DEVIATIONS.md if any published number moves.
FROM python:3.12.15-slim-bookworm@sha256:57d96f71de145a98e7ceca18ee4ade77bba4103a33a72dfaea026b23625c6bf0

# Same results run to run: no bytecode files, fixed hash seed, single-threaded maths libraries
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONHASHSEED=0 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    OMP_NUM_THREADS=1 \
    OPENBLAS_NUM_THREADS=1 \
    MKL_NUM_THREADS=1

WORKDIR /app
COPY requirements.lock ./
RUN pip install --require-hashes -r requirements.lock
COPY . .
RUN pip install --no-deps -e . && python -c "import snapshot, lifelines, statsmodels"
ENV SNAPSHOT_ROOT=/app
CMD ["python", "-m", "pytest", "-q"]
