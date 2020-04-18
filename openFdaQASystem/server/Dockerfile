FROM python:3.7

RUN mkdir /code
WORKDIR /code
ADD . /code/
RUN pip install -r requirements.txt
RUN python -m spacy download en_core_web_sm

EXPOSE 5000
CMD ["python", "/code/app.py"]