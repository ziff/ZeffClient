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


docs: uml example_archive apidoc
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


uml:
	@echo Update UML diagrams
	@plantuml source/**/*.uml


man:
	@echo Update man pages
	@mkdir -p source/man/man1
	@python -c 'import zeff; print(zeff.__doc__)' | \
		sed '1,3d' | \
		rst2man.py > source/man/man1/zeff.1


example_archive:
	@echo Create example archives
	@$(MAKE) -C source/examples archive


clean:
	@$(MAKE) -C source/examples clean


.PHONY: help docs apidoc uml man example_archive clean Makefile

# Catch-all target: route all unknown targets to Sphinx using the new
# "make mode" option.  $(O) is meant as a shortcut for $(SPHINXOPTS).
%: Makefile
	@$(SPHINXBUILD) -M $@ "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)
