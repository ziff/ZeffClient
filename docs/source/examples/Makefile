.POSIX:
.PHONY: archive clean

archive: zeffclient_example_yaml.tar.bz2 \
         zeffclient_example_csv.tar.bz2 \
		 zeffclient_example_rdbms.tar.bz2

clean:
	@rm -f zeffclient_example_*.tar.bz2


%.tar.bz2: % %/*
	@echo Build $@
	@find $< -name .venv -exec rm -rf {} \;
	@tar -c $< | bzip2 > $@
