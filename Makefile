.PHONY: doc runGittk runDemo build deploy buildTest deployTest deploySandbox

.venv:
	python3 -m venv .venv
	. .venv/bin/activate ; \
	pip install -r docs/requirements.txt
	# Add "Signal" option in the method domains
	patch -p3 -d .venv/lib/python3*/ < docs/sphynx.001.signal.patch
	#  Update/Regen
	#    # Docs
	#    pip install sphinx sphinx-epytext sphinx-autodocgen sphinx-rtd-theme
	#    # Test
	#    pip install flake8 pytest
	#    # Build
	#    pip install build twine
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
	tools/prepareBuild.sh release ; \
	cd tmp ; \
	python3 -m build \

deploy: .venv
	. .venv/bin/activate ; \
	python3 -m twine upload tmp/dist/*

buildTest: .venv
	. .venv/bin/activate ; \
	tools/prepareBuild.sh test ; \
	python3 -m build ; \

deployDoc:
	git checkout gh-pages

	# Update the doc files
	rm -rf *.inv *.html *.js _* autogen.* tutorial
	cp -a docs/build/html/* .
	find *.html *.inv *.js autogen.TermTk _* tutorial | xargs git add

	git commit -m "Doc Updated"
	git push origin gh-pages
	git checkout main

deploySandbox:
	cp -a tests/sandbox tmp/

	git checkout gh-pages
	cp tmp/sandbox/*.html sandbox

	git submodule foreach git pull
	git add sandbox

	git commit -m "Sandbox Updated"
	git push origin gh-pages
	git checkout main

deployTest: .venv
	. .venv/bin/activate ; \
	python3 -m twine upload --repository testpypi tmp/dist/* --verbose

test: .venv
	# Record a stream
	#   tests/pytest/test_001_demo.py -r test.input.bin
	# Play the test stream
	#   tests/pytest/test_001_demo.py -p test.input.bin
	mkdir -p tmp
	wget -O tmp/test.input.bin https://github.com/ceccopierangiolieugenio/binaryRepo/raw/master/pyTermTk/tests/test.input.001.bin
	tools/check.import.sh
	. .venv/bin/activate ; \
	flake8 . --count --select=E9,F63,F7,F82 --show-source --statistics --exclude .venv,build,tmp ; \
	pytest tests/pytest/test_002_textedit.py ; \
	pytest tests/pytest/test_001_demo.py ;
