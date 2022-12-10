
# Compile all bison parsers with respective output prefixes
%: %.y
	bison --file-prefix="$@" -v $@.y

all: cpl

clean:
	rm -rf *.tab.c *.output