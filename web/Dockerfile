from alpine:latest

WORKDIR /app

# RUN mkdir /app
COPY main.py /app/main.py
RUN apk add python3 py3-flask

# ENTRYPOINT /app
# RUN flask --app main.py run
CMD ["flask", "--app", "main.py", "run"]
EXPOSE 5000
#CMD ["ls"]