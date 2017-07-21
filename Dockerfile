# Using the official python 2.7 as a Base Image
FROM python:2

ADD . /edx-e2e-tests
WORKDIR /edx-e2e-tests

# Configuration
RUN apt-get update && apt-get install git
RUN pip install virtualenv==1.10.1
RUN pip install virtualenvwrapper
ENV PATH $PATH:venv/bin/activate

# Install requirements and pages
RUN pip install -r requirements/base.txt
RUN paver install_pages

# Set up environment variables
CMD ["sleep", "infinity"]
