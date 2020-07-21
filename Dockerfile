# FROM raphaelguzman/djbase:py3.8-alpine
FROM raphaelguzman/djlab:py3.8-alpine

COPY ./apk_requirements.txt /apk_requirements.txt
COPY ./pip_requirements.txt /pip_requirements.txt
RUN /entrypoint.sh echo "Requirements updated..."
# COPY --chown=dja:anaconda . /src

# RUN pip install /src && rm -R /src/*

