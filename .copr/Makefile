.PHONY: srpm

srpm:
	mkdir -p $(outdir)/
	cp -a flutter.spec $(outdir)/
	spectool -g -C $(outdir)/ flutter.spec
	rpmbuild -bs --define "_sourcedir $(outdir)" --define "_srcrpmdir $(outdir)" $(outdir)/flutter.spec
