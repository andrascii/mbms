FROM ubuntu:jammy as builder

ENV container="docker"
ENV DEBIAN_FRONTEND=noninteractive

RUN apt update && apt upgrade -y

# gcc-12/g++-12 requires to build marzbanpp with glaze library
RUN apt install git -y
RUN apt install openssl -y
RUN apt install libssl-dev -y
RUN apt install linux-libc-dev -y
RUN apt install pkg-config -y
# install ca-certificates to allow curl verify ssl certificates of a remote hosts
RUN apt install ca-certificates -y

# Set the working directory.
WORKDIR /mbms

# copy local scripts
COPY . .

RUN rm -rf venv .venv
RUN pip3 install -r requirements.txt

FROM ubuntu:jammy

WORKDIR /mbms

COPY --from=builder /mbms .

CMD ["python /mbms/main.py"]
