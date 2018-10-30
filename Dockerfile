FROM python:3.5
WORKDIR /app/
ADD requirements.txt /app/requirements.txt
RUN pip install -r requirements.txt
ADD . /app/
ENV TZ=Europe/Kiev
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone
