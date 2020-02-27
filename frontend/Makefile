FILE_LIST = ./.installed_files.txt

.PHONY: install uninstall

default: | install

install:
	@ install -dm 755 /srv/http/de/homeinfo/javascript/terminallib
	@ install -m 644 *.js /srv/http/de/homeinfo/javascript/terminallib/

uninstall:
	@ rm -rf /srv/http/de/homeinfo/javascript/terminallib
