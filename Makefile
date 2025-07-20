.PHONY: doc runGittk runDemo build deploy buildTest deployTest deploySandbox

.venv:
	python3 -m venv .venv
	. .venv/bin/activate ; \
	pip install -r docs/requirements.txt
	# Add "Signal" option in the method domains
	# patch -p3 -d .venv/lib/python3*/ < docs/sphynx.001.signal.patch
	#  Update/Regen
	#    # Docs
	#    pip install sphinx sphinx-epytext sphinx-autodocgen sphinx-rtd-theme
	#    # Test
	#    pip install flake8 pytest
	#    # Build
	#    pip install build twine
	#  Regen requirements;
	#    pip freeze > docs/requirements.txt

.venv.ttkDesigner:
	python3 -m venv .venv.ttkDesigner
	. .venv.ttkDesigner/bin/activate ; \
	pip install pyperclip Pillow

doc: .venv
	. .venv/bin/activate ; \
	make -C docs/source/ clean ; \
	make -C docs/source/ html ;

testDoc:
	python3 -m http.server --directory docs/source/_build/html/

runTtkDesigner: .venv.ttkDesigner
	. .venv.ttkDesigner/bin/activate ; \
	python -m ttkDesigner

runGittk: .venv
	. .venv/bin/activate ; \
	demo/gittk.py -f

runDemo: .venv
	. .venv/bin/activate ; \
	demo/demo.py -f

runDumbImageTool: .venv
	. .venv/bin/activate ; \
	tools/dumb.image.tool.py

build: .venv
	. .venv/bin/activate ; \
	tools/prepareBuild.sh release ; \
	cd tmp ; \
	python3 -m build

deploy: .venv
	. .venv/bin/activate ; \
	python3 -m twine upload tmp/dist/*

buildTest: .venv
	. .venv/bin/activate ; \
	tools/prepareBuild.sh test ; \
	cd tmp ; \
	python3 -m build

buildTTkDesigner: .venv
	. .venv/bin/activate ; \
	tools/prepareBuild.sh ttkDesigner ; \
	cd tmp ; \
	python3 -m build

buildDumbPaintTool: .venv
	. .venv/bin/activate ; \
	tools/prepareBuild.sh dumbPaintTool ; \
	cd tmp ; \
	python3 -m build

deployTTkDesigner: .venv
	. .venv/bin/activate ; \
	python3 -m twine upload tmp/dist/*

pyTermTk-Docs:
	git clone git@github.com:ceccopierangiolieugenio/pyTermTk-Docs.git

deployDoc: pyTermTk-Docs
	cd pyTermTk-Docs ; \
	git checkout main ; \
	git pull ; \
	rm -rf _* info tutorial ;

	cp -a docs/source/_build/html/* \
	      docs/source/_build/html/.buildinfo \
	      docs/source/_build/html/.nojekyll \
		  pyTermTk-Docs ; \
	cd pyTermTk-Docs ; \
	git add . ; \
	git commit -m "Updated Docs" ; \
	git push origin main ; \
	git checkout gh-pages ; \
	git merge main ; \
	git push origin gh-pages ;

	echo "Docs Deployed!!!"

deploySandbox:
	rm -rf tmp/sandbox
	mkdir -p tmp/sandbox
	cp -a tests/sandbox/*.html tmp/sandbox
	cp -a tools/webExporter/js tmp/sandbox

	git checkout gh-pages
	git pull
	cp tmp/sandbox/*.html sandbox
	cp -r tmp/sandbox/js  sandbox

	git submodule update --init
	git submodule foreach git checkout gh-pages
	git submodule foreach git pull
	git add sandbox

	git commit -m "Sandbox Updated"
	git push origin gh-pages
	git checkout main

deployTest: .venv
	. .venv/bin/activate ; \
	python3 -m twine upload --repository testpypi tmp/dist/* --verbose

itchDumbPaintToolexporter:
	tools/webExporterInit.sh
	python3 -m http.server --directory tmp

test: .venv
	# Record a stream
	#   tests/pytest/test_001_demo.py -r test.input.bin
	# Play the test stream
	#   tests/pytest/test_001_demo.py -p test.input.bin
	mkdir -p tmp
	wget -O tmp/test.input.001.bin https://github.com/ceccopierangiolieugenio/binaryRepo/raw/master/pyTermTk/tests/test.input.001.bin
	wget -O tmp/test.input.002.bin https://github.com/ceccopierangiolieugenio/binaryRepo/raw/master/pyTermTk/tests/test.input.002.bin
	wget -O tmp/test.input.003.bin https://github.com/ceccopierangiolieugenio/binaryRepo/raw/master/pyTermTk/tests/test.input.003.bin
	tools/check.import.sh
	. .venv/bin/activate ; \
	    flake8 . --count --select=E9,F63,F7,F82 --show-source --statistics --exclude .venv,build,tmp,experiments ;
	. .venv/bin/activate ; \
	    pytest tests/pytest/test_003_string.py ;
	. .venv/bin/activate ; \
	    pytest tests/pytest/test_002_textedit.py ;
	. .venv/bin/activate ; \
	    pytest -v tests/pytest/test_001_demo.py ;

