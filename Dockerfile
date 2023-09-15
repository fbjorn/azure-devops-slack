FROM fbjorn/python-base:ubuntu-python3.10

USER ${USER}

WORKDIR /src

ADD . ./
RUN poetry install

EXPOSE 8000

ENTRYPOINT ["poetry", "run", "invoke", "backend"]
