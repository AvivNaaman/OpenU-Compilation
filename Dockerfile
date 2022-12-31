FROM ubuntu:latest

RUN apt update && \
	apt install -y build-essential flex bison cmake g++ vim git gdb

CMD ['bash']
