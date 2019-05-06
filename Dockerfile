FROM python:3.7

COPY ./python_chess_ai /python_chess_ai
WORKDIR ./python_chess_ai/

RUN pip install -r requirements.txt
CMD ["python", "main.py", "-s"]
