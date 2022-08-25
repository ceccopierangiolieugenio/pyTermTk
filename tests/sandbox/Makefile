.PHONY: testSandbox buildSandbox

testSandbox:
	python3 -m http.server --directory ./

www:
	mkdir -p www/pyodide www/xterm/ www/xterm-addon-fit www/codemirror www/codemirror/theme www/codemirror/modes

	wget  -P www/xterm    https://ceccopierangiolieugenio.github.io/binaryRepo/pyTermTk/www/xterm/xterm.css
	wget  -P www/xterm    https://ceccopierangiolieugenio.github.io/binaryRepo/pyTermTk/www/xterm/xterm.js
	wget  -P www/xterm    https://ceccopierangiolieugenio.github.io/binaryRepo/pyTermTk/www/xterm/xterm.js.map

	wget  -P www/xterm-addon-fit   https://ceccopierangiolieugenio.github.io/binaryRepo/pyTermTk/www/xterm-addon-fit/xterm-addon-fit.js
	wget  -P www/xterm-addon-fit   https://ceccopierangiolieugenio.github.io/binaryRepo/pyTermTk/www/xterm-addon-fit/xterm-addon-fit.js.map

	wget  -P www/codemirror   https://ceccopierangiolieugenio.github.io/binaryRepo/pyTermTk/www/codemirror/codemirror.js
	wget  -P www/codemirror   https://ceccopierangiolieugenio.github.io/binaryRepo/pyTermTk/www/codemirror/codemirror.css
	wget  -P www/codemirror/theme   https://ceccopierangiolieugenio.github.io/binaryRepo/pyTermTk/www/codemirror/theme/mbo.css
	wget  -P www/codemirror/modes   https://ceccopierangiolieugenio.github.io/binaryRepo/pyTermTk/www/codemirror/modes/python.js

	wget  -P www/pyodide/   https://ceccopierangiolieugenio.github.io/binaryRepo/pyTermTk/www/pyodide/pyodide_py.tar
	wget  -P www/pyodide/   https://ceccopierangiolieugenio.github.io/binaryRepo/pyTermTk/www/pyodide/pyodide.asm.js
	wget  -P www/pyodide/   https://ceccopierangiolieugenio.github.io/binaryRepo/pyTermTk/www/pyodide/distutils.tar
	wget  -P www/pyodide/   https://ceccopierangiolieugenio.github.io/binaryRepo/pyTermTk/www/pyodide/pyodide.js.map
	wget  -P www/pyodide/   https://ceccopierangiolieugenio.github.io/binaryRepo/pyTermTk/www/pyodide/repodata.json
	wget  -P www/pyodide/   https://ceccopierangiolieugenio.github.io/binaryRepo/pyTermTk/www/pyodide/pyodide.asm.wasm
	wget  -P www/pyodide/   https://ceccopierangiolieugenio.github.io/binaryRepo/pyTermTk/www/pyodide/pyodide.js
	wget  -P www/pyodide/   https://ceccopierangiolieugenio.github.io/binaryRepo/pyTermTk/www/pyodide/pyodide.asm.data


buildSandbox: www
	rm -rf bin
	mkdir -p bin
	find ../../TermTk/  -name "*.py" | sort | xargs tar cvzf bin/TermTk.tgz
	find ../../tutorial -name "*.py" | sort | xargs tar cvzf bin/tutorial.tgz
	find ../../demo/paint.py ../../demo/ttkode.py ../../demo/demo.py ../../demo/showcase/*.* | sort | xargs tar cvzf bin/demo.tgz