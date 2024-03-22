.PHONY: testSandbox buildSandbox

testSandbox:
	python3 -m http.server --directory ./

www:
	mkdir -p www/pyodide www/xterm/ www/xterm-addon-fit www/codemirror www/codemirror/theme www/codemirror/modes www/fontawesome www/w2ui www/webfonts www/fonts/nerdfonts

	wget  -P www/pyodide/   https://ceccopierangiolieugenio.github.io/binaryRepo/pyTermTk/www/pyodide/pyodide.js
	wget  -P www/pyodide/   https://ceccopierangiolieugenio.github.io/binaryRepo/pyTermTk/www/pyodide/python_stdlib.zip
	wget  -P www/pyodide/   https://ceccopierangiolieugenio.github.io/binaryRepo/pyTermTk/www/pyodide/pyodide.asm.js
	wget  -P www/pyodide/   https://ceccopierangiolieugenio.github.io/binaryRepo/pyTermTk/www/pyodide/repodata.json
	wget  -P www/pyodide/   https://ceccopierangiolieugenio.github.io/binaryRepo/pyTermTk/www/pyodide/pyodide.asm.wasm

	wget  -P www/xterm/    https://ceccopierangiolieugenio.github.io/binaryRepo/pyTermTk/www/xterm/xterm.css
	wget  -P www/xterm/    https://ceccopierangiolieugenio.github.io/binaryRepo/pyTermTk/www/xterm/xterm.js
	wget  -P www/xterm/    https://ceccopierangiolieugenio.github.io/binaryRepo/pyTermTk/www/xterm/xterm.js.map

	wget  -P www/xterm-addon-fit/   https://ceccopierangiolieugenio.github.io/binaryRepo/pyTermTk/www/xterm-addon-fit/xterm-addon-fit.js
	wget  -P www/xterm-addon-fit/   https://ceccopierangiolieugenio.github.io/binaryRepo/pyTermTk/www/xterm-addon-fit/xterm-addon-fit.js.map

	wget  -P www/xterm-addon-unicode11/   https://ceccopierangiolieugenio.github.io/binaryRepo/pyTermTk/www/xterm-addon-unicode11/xterm-addon-unicode11.js

	wget  -P www/fontawesome/   https://ceccopierangiolieugenio.github.io/binaryRepo/pyTermTk/www/fontawesome/regular.min.css
	wget  -P www/fontawesome/   https://ceccopierangiolieugenio.github.io/binaryRepo/pyTermTk/www/fontawesome/fontawesome.min.css

	wget  -P www/webfonts/      https://ceccopierangiolieugenio.github.io/binaryRepo/pyTermTk/www/webfonts/fa-regular-400.woff2
	wget  -P www/fonts/nerdfonts/     https://ceccopierangiolieugenio.github.io/binaryRepo/pyTermTk/www/nerdfonts/HurmitNerdFontMono-Regular.otf
	wget  -P www/fonts/nerdfonts/     https://ceccopierangiolieugenio.github.io/binaryRepo/pyTermTk/www/nerdfonts/DejaVuSansMNerdFont-Regular.ttf

	wget  -P www/w2ui/   https://ceccopierangiolieugenio.github.io/binaryRepo/pyTermTk/www/w2ui/w2ui-2.0.min.js
	wget  -P www/w2ui/   https://ceccopierangiolieugenio.github.io/binaryRepo/pyTermTk/www/w2ui/w2ui-2.0.min.css

	wget  -P www/codemirror/   https://ceccopierangiolieugenio.github.io/binaryRepo/pyTermTk/www/codemirror/codemirror.js
	wget  -P www/codemirror/   https://ceccopierangiolieugenio.github.io/binaryRepo/pyTermTk/www/codemirror/codemirror.css
	wget  -P www/codemirror/theme/   https://ceccopierangiolieugenio.github.io/binaryRepo/pyTermTk/www/codemirror/theme/mbo.css
	wget  -P www/codemirror/modes/   https://ceccopierangiolieugenio.github.io/binaryRepo/pyTermTk/www/codemirror/modes/python.js

	wget  -P www/   https://ceccopierangiolieugenio.github.io/binaryRepo/pyTermTk/www/favicon.ico

updateXterm: www
	rm -rf node_modules package.json package-lock.json
	npm install xterm
	npm install xterm-addon-fit
	npm install xterm-addon-unicode11
	npm install xterm-addon-canvas
	cp node_modules/xterm/css/xterm.css \
	   node_modules/xterm/lib/xterm.js \
	   node_modules/xterm/lib/xterm.js.map \
	   www/xterm/
	cp node_modules/xterm-addon-unicode11/lib/xterm-addon-unicode11.js \
	   node_modules/xterm-addon-unicode11/lib/xterm-addon-unicode11.js.map \
	   www/xterm-addon-unicode11/
	cp node_modules/xterm-addon-fit/lib/xterm-addon-fit.js \
	   node_modules/xterm-addon-fit/lib/xterm-addon-fit.js.map \
	   www/xterm-addon-fit/
	cp node_modules/xterm-addon-canvas/lib/xterm-addon-canvas.js \
	   node_modules/xterm-addon-canvas/lib/xterm-addon-canvas.js.map \
	   www/xterm-addon-fit/
	rm -rf node_modules package.json package-lock.json

buildSandbox: www
	rm -rf bin
	mkdir -p bin

	$( cd ../../ ; tools/prepareBuild.sh release ; )

	find ../../tmp/TermTk/  -name "*.py" | sed 's,.*tmp/,,' | sort | xargs tar cvzf bin/TermTk.tgz -C ../../tmp
	find ../../tutorial -name "*.py" | sort | xargs tar cvzf bin/tutorial.tgz
	find ../../demo/paint.py ../../demo/ttkode.py ../../demo/demo.py ../../demo/showcase/*.* | sort | xargs tar cvzf bin/demo.tgz

buildTestSandbox: www
	rm -rf bin
	mkdir -p bin

	$( cd ../../ ; tools/prepareBuild.sh release ; )

	find ../../TermTk/  -name "*.py" | sort | xargs tar cvzf bin/TermTk.tgz
	find ../../tutorial -name "*.py" | sort | xargs tar cvzf bin/tutorial.tgz
	find ../../demo/paint.py ../../demo/ttkode.py ../../demo/demo.py ../../demo/showcase/*.* | sort | xargs tar cvzf bin/demo.tgz