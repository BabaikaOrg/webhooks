
FROM python:3.11-slim-bookworm

# Set environment variables for Python and Poetry
ENV PYTHONUNBUFFERED=1 \
    PYTHONFAULTHANDLER=1 \
    POETRY_VERSION=1.7.1 \
    POETRY_NO_INTERACTION=1 \
    POETRY_VIRTUALENVS_CREATE=1 \
    POETRY_VIRTUALENVS_IN_PROJECT=true \
    PATH="$HOME/.local/bin:$PATH"

ARG INSTALL_DEBUGGER=false

# Keeps Python from generating .pyc files in the container
ENV PYTHONDONTWRITEBYTECODE=1

ENV APP_HOME /app
WORKDIR $APP_HOME

# Install Poetry
RUN pip install "poetry==$POETRY_VERSION"

# Copy the project's pyproject.toml (and poetry.lock if it exists) to the /app directory
COPY pyproject.toml poetry.lock* $APP_HOME

# Install project dependencies
RUN poetry export --without-hashes -o requirements.txt
RUN pip install -r requirements.txt

RUN if [ "$INSTALL_DEBUGGER" = "true" ] ; then pip install debugpy ; fi

# Copy the rest of the project
COPY app ./app
COPY interface ./interface

ARG UID=1000
ARG GID=1000

#create non-root user
RUN set -ex \
    # Create a non-root user
    && addgroup --system --gid $GID appgroup \
    && adduser --system --uid $UID --gid $GID --no-create-home appuser

RUN chown -R appuser:appgroup /app
RUN chmod 755 /app
USER appuser

CMD uvicorn interface.web.main:create_app --workers 2 --host 0.0.0.0 --port 9090
