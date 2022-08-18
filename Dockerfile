FROM python:3.9

WORKDIR /fortristest

COPY ./requirements.txt /fortristest/requirements.txt

RUN pip3 install --no-cache-dir --upgrade -r /fortristest/requirements.txt

COPY ./app /fortristest/app

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]
