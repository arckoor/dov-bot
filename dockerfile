FROM python:3.10-slim

WORKDIR /DovBot

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY loader.sh /usr/local/bin/

RUN chmod +x /usr/local/bin/loader.sh

COPY . .

ENTRYPOINT [ "loader.sh" ]
CMD [ "python", "DovBot/DovBot.py" ]
