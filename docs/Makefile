# Minimal makefile for Sphinx documentation
#

# You can set these variables from the command line, and also
# from the environment for the first two.
SPHINXOPTS    ?=
SPHINXBUILD   ?= sphinx-build
SOURCEDIR     = source
BUILDDIR      = ../build

# Put it first so that "make" without argument is like "make help".
help:
	@$(SPHINXBUILD) -M help "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)


docs: example_archive apidoc
	@$(SPHINXBUILD) -M html $(SPHINXOPTS) "$(SOURCEDIR)" "$(BUILDDIR)"


docs_OFF:
	#@$(SPHINXBUILD) -M singlehtml $(SPHINXOPTS) "$(SOURCEDIR)" "$(BUILDDIR)"
	#@$(SPHINXBUILD) -M epub $(SPHINXOPTS) "$(SOURCEDIR)" "$(BUILDDIR)"
	#@$(SPHINXBUILD) -M latex $(SPHINXOPTS) "$(SOURCEDIR)" "$(BUILDDIR)"
	#@$(SPHINXBUILD) -M latexpdf $(SPHINXOPTS) "$(SOURCEDIR)" "$(BUILDDIR)"
	#@$(SPHINXBUILD) -M doctest $(SPHINXOPTS) "$(SOURCEDIR)" "$(BUILDDIR)"
	#@$(SPHINXBUILD) -M doctest $(SPHINXOPTS) "$(SOURCEDIR)" "$(BUILDDIR)"


apidoc:
	sphinx-apidoc -o $(SOURCEDIR)/ ../zeff


example_archive:
	tar -c -C source/examples zeffclient_example_yaml | bzip2 > source/examples/zeffclient_example_yaml.tar.bz2
	tar -c -C source/examples zeffclient_example_csv | bzip2 > source/examples/zeffclient_example_csv.tar.bz2
	tar -c -C source/examples zeffclient_example_rdbms | bzip2 > source/examples/zeffclient_example_rdbms.tar.bz2


.PHONY: help docs apidoc example_archive Makefile

# Catch-all target: route all unknown targets to Sphinx using the new
# "make mode" option.  $(O) is meant as a shortcut for $(SPHINXOPTS).
%: Makefile
	@$(SPHINXBUILD) -M $@ "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)
