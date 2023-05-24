FROM debian:10
RUN apt-get update -y && \
    apt-get install -y \
      gcc make patchelf wget tar git
RUN git clone "https://github.com/Devil666face/ExporterExample.git"
WORKDIR /ExporterExample
RUN ./init.sh
RUN ./venv/bin/pip install nuitka
CMD ["/bin/bash", "-c", "./venv/bin/python -m nuitka --follow-imports --standalone --onefile main.py && \ 
      mkdir -p bin && \
      mv main.bin bin/"]
# docker build . -t ksc && docker run --rm -v `pwd`/bin:/KscNextcloud/bin --name ksc_build -it ksc
