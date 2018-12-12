FROM navikt/python-fasttext:0.8.22

ENV REQUESTS_CA_BUNDLE /etc/pki/tls/certs/ca-bundle.crt
ENV VKS_SECRET_DEST_PATH /var/run/secrets/nais.io/vault

COPY ca-bundle.crt /etc/pki/tls/certs/ca-bundle.crt
COPY . /app

WORKDIR /app

RUN pip3.6 install --proxy http://webproxy-utvikler.nav.no:8088 --cert /etc/pki/tls/certs/ca-bundle.crt -r requirements.txt

CMD ["python", "app.py"]
