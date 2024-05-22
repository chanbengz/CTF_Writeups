FROM python:3.8.8-slim

RUN useradd -m ctf

WORKDIR /chal

COPY app/ .

ENV PORT 9999
ENV FLAG "flag{this_is_a_test}"

RUN pip3 install --upgrade --no-cache-dir -r requirements.txt

RUN chown -R root:ctf /chal && \
    echo $FLAG > /flag && \
    chmod 777 /chal /chal/server.py /flag

USER ctf
CMD ["/usr/local/bin/python", "/chal/server.py"]

EXPOSE 9999