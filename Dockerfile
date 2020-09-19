FROM python:3

ADD mooseboard.py /

RUN pip install discord.py python-dotenv

CMD [ "python", "./mooseboard.py" ]
