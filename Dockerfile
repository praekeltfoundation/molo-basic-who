FROM praekeltfoundation/django-bootstrap
ENV PYTHONUNBUFFERED 1
RUN mkdir /code
WORKDIR /code
COPY requirements.txt /code/
RUN pip install https://github.com/praekeltfoundation/molo-basic/archive/master.zip#egg=package.json
RUN pip install -r requirements.txt
COPY . /code/

ENV DJANGO_SETTINGS_MODULE=who.settings.docker \
    CELERY_APP=who

# RUN LANGUAGE_CODE=en SECRET_KEY=compilemessages-key django-admin compilemessages && \
#     SECRET_KEY=collectstatic-key django-admin collectstatic --noinput && \
#     SECRET_KEY=compress-key django-admin compress

CMD ["who.wsgi:application", "--timeout", "1800"]
