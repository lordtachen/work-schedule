from 3.12.2-alpine3.19 as builder

RUN pip install "poetry==1.7.1"


WORKDIR /
COPY . .
RUN poetry install --without dev
RUN poetry build --format wheel


FROM 3.12.2-alpine3.19 as production
COPY --from=builder /dist/*.whl /
RUN pip install /*.whl
RUN rm /*.whl

EXPOSE 8000

ENTRYPOINT ["uvicorn"]

CMD ["--host","0.0.0.0","main:app"]
