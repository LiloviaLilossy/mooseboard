FROM python:3

ADD mooseboard-executable.py /

RUN pip install discord.py python-dotenv

CMD [ "python", "./mooseboard-executable.py" ]
