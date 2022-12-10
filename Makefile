MAKE=make
SUBDIRS = 11 12 13

all: $(SUBDIRS)

%: %/*
	cd $@ && $(MAKE)
