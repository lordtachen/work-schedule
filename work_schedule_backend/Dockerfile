FROM python:3.12.2-alpine3.19 AS builder

RUN pip install --no-cache-dir "poetry==1.7.1"
WORKDIR /work-schedule
COPY . /work-schedule
RUN   poetry build --format wheel -C /work-schedule --no-cache


FROM python:3.12.2-alpine3.19 AS production
COPY --from=builder /work-schedule/dist/*.whl /

RUN pip install --no-cache-dir /*.whl \
    && rm /*.whl
EXPOSE 8000
ENTRYPOINT ["uvicorn","work_schedule_backend.main:app","--host","0.0.0.0"]
