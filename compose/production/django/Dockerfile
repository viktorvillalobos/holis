FROM node:10-stretch-slim as client-builder

WORKDIR /app
COPY ./package.json /app
RUN npm install && npm cache clean --force
COPY . /app
RUN npm run build


FROM node:12-stretch-slim as webapp-builder

WORKDIR /app
COPY --from=client-builder /app /app
RUN cd /app/webapp/ && yarn && yarn cache clean && yarn build

# Python build stage
# FROM python:3.9-slim-buster
FROM gcr.io/espazum/holis-full:base

ENV PYTHONUNBUFFERED 1

COPY ./compose/production/django/entrypoint /entrypoint
RUN sed -i 's/\r$//g' /entrypoint
RUN chmod +x /entrypoint
# RUN chown django /entrypoint

COPY ./compose/production/django/start /start
RUN sed -i 's/\r$//g' /start
RUN chmod +x /start
# RUN chown django /start
COPY ./compose/production/django/celery/worker/start /start-celeryworker
RUN sed -i 's/\r$//g' /start-celeryworker
RUN chmod +x /start-celeryworker
# RUN chown django /start-celeryworker

COPY ./compose/production/django/celery/beat/start /start-celerybeat
RUN sed -i 's/\r$//g' /start-celerybeat
RUN chmod +x /start-celerybeat
# RUN chown django /start-celerybeat

COPY ./compose/production/django/celery/flower/start /start-flower
RUN sed -i 's/\r$//g' /start-flower
RUN chmod +x /start-flower
COPY --from=webapp-builder /app /app


WORKDIR /app

ENTRYPOINT ["/entrypoint"]
