FROM python:3.9

WORKDIR /fortristest

COPY ./requirements.txt /fortristest/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /fortristest/requirements.txt

COPY ./main.py /fortristest/

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]
