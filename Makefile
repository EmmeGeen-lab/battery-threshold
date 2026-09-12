VERSION := 0.1.0
BETA := beta1

.PHONY: check clean deb rpm source

check:
	python3 -m py_compile src/battery_threshold.py
	python3 -m unittest discover -s tests -v
	sh -n src/battery-threshold-helper src/battery-threshold-restore install.sh uninstall.sh services/battery-threshold.sysv

source:
	mkdir -p dist
	tar --exclude=.git --exclude=build --exclude=dist --transform='s,^,battery-threshold-$(VERSION)/,' -czf dist/battery-threshold-$(VERSION).tar.gz .

deb: check
	./packaging/build-deb.sh

rpm: check source
	./packaging/build-rpm.sh

clean:
	rm -rf build dist src/__pycache__ tests/__pycache__
