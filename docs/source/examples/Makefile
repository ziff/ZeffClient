.POSIX:
.PHONY: archive clean

archive: zeffclient_example_yaml.tar.bz2 \
         zeffclient_example_csv.tar.bz2 \
		 zeffclient_example_rdbms.tar.bz2

clean:
	@rm zeffclient_example_*.tar.bz2


%.tar.bz2: % %/*
	tar -c $< | bzip2 > $@
