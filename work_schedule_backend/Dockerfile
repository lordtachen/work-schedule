FROM python:3.13-alpine3.21 AS builder

RUN pip install --no-cache-dir "poetry==2.0.1"
WORKDIR /work-schedule
COPY . /work-schedule
RUN   poetry build --format wheel -C /work-schedule --no-cache


FROM python:3.13-alpine3.21 AS production
COPY --from=builder /work-schedule/dist/*.whl /

RUN pip install --no-cache-dir /*.whl \
    && rm /*.whl
EXPOSE 8000
ENTRYPOINT ["uvicorn","work_schedule_backend.main:app","--host","0.0.0.0"]
