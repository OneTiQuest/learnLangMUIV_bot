FROM python:3.9

WORKDIR /var/www/bot

COPY . .

RUN python -m venv .venv
RUN chmod +x .venv/bin/activate
RUN .venv/bin/activate

RUN python -m pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8000

ENTRYPOINT ["python"]

CMD ["init.py"]