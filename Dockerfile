FROM praekeltfoundation/django-bootstrap
ENV PYTHONUNBUFFERED 1
# RUN mkdir /code
# WORKDIR /code
# COPY requirements.txt /code/
RUN apt-get update && apt-get install -y gettext libgettextpo-dev
RUN pip install https://github.com/praekeltfoundation/molo-basic/archive/master.zip#egg=package.json

COPY . /app/
COPY requirements.txt /requirements/
RUN pip install -r /requirements/requirements.txt
RUN pip install -e .

ENV PROJECT_ROOT /app/
ENV DJANGO_SETTINGS_MODULE=who.settings.docker \
    CELERY_APP=who

RUN LANGUAGE_CODE=en SECRET_KEY=compilemessages-key django-admin compilemessages && \
    SECRET_KEY=collectstatic-key django-admin collectstatic --noinput && \
    SECRET_KEY=compress-key django-admin compress

CMD ["who.wsgi:application", "--timeout", "1800"]
