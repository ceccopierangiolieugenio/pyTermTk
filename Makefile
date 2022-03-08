.PHONY: doc runGittk runDemo build deploy buildTest deployTest

.venv:
	python3 -m venv .venv
	. .venv/bin/activate ; \
	pip install -r docs/requirements.txt
	# Add "Signal" option in the method domains
	patch -p0  < docs/sphynx.001.signal.patch
	#  Regen requirements;
	#    pip freeze > docs/requirements.txt


doc: .venv
	# old doc gen, using pdoc3 ; \
	# . .venv/bin/activate ; \
	# rm -rf docs/html ; \
	# pdoc --html TermTk -o docs/html ; \
	. .venv/bin/activate ; \
	rm -rf docs/build ; \
	rm -rf docs/source/autogen.* ; \
	# sphinx-apidoc -o docs/source/TermTk/ -e TermTk/ ; \
	make -C docs/ clean ; \
	make -C docs/ html ; \
	cp -a docs/images docs/build/html/_images ;

testDoc:
	python3 -m http.server --directory docs/build/html/

runGittk: .venv
	. .venv/bin/activate ; \
	demo/gittk.py -f

runDemo: .venv
	. .venv/bin/activate ; \
	demo/demo.py -f

build: .venv
	. .venv/bin/activate ; \
	rm -rf dist ; \
	tools/prepareBuild.sh release ; \
	python3 -m build

buildTest: .venv
	. .venv/bin/activate ; \
	rm -rf dist ; \
	tools/prepareBuild.sh test ; \
	python3 -m build ; \

deployDoc:
	git checkout gh-pages
	rm -rf *.inv *.html *.js _* autogen.* tutorial
	cp -a docs/build/html/* .
	find *.html *.inv *.js autogen.TermTk _* tutorial | xargs git add
	git commit -m "Doc Updated"
	git push origin gh-pages
	git checkout main

deployTest: .venv
	. .venv/bin/activate ; \
	python3 -m twine upload --repository testpypi dist/* --verbose

deploy: .venv
	. .venv/bin/activate ; \
	python3 -m twine upload dist/*

test: .venv
	. .venv/bin/activate ; \
	flake8 . --count --select=E9,F63,F7,F82 --show-source --statistics --exclude .venv,build,tmp ; \
	pytest demo/demo.py
