MAKE=make
SUBDIRS = 11 12 13 14

all: $(SUBDIRS)

%: %/*
	cd $@ && $(MAKE)
