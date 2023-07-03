FROM python:3.10

ENV PYTHONUNBUFFERED 1
ENV PATH="/bioinfweb_backend/bin:$PATH"
ENV PYTHONPATH /bioinfweb_backend


RUN mkdir -p /bioinfweb_backend

# Update working directory
WORKDIR /bioinfweb_backend

# copy everything from this directory to server docker container
COPY ./requirements.txt /bioinfweb_backend/

# Install the Python libraries
RUN --mount=type=cache,target=/root/.cache pip install -r requirements.txt

CMD python3 manage.py runserver 0.0.0.0:8081

