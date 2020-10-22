FILE_LIST = ./.installed_files.txt

.PHONY: install uninstall

default: | install

install:
	@ install -vm 644 -t /srv/http/de/homeinfo/javascript hwdb.mjs

uninstall:
	@ rm -f /srv/http/de/homeinfo/javascript/hwdb.mjs
