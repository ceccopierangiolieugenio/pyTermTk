/*
MIT License

Copyright (c) 2023 Eugenio Parodi <ceccopierangiolieugenio AT googlemail DOT com>

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
*/

async function permissionsCheck() {
  if (navigator.clipboard){
    const read = await navigator.permissions.query({
        name: 'clipboard-read',
    });
    const write = await navigator.permissions.query({
        name: 'clipboard-write',
    });
    return write.state === 'granted' && read.state !== 'denied';
  }
  return false
}

// Declaration
class TTkProxy {
    constructor(term) {
        this.term = term
        document.getElementById("file-input").addEventListener("change", (e) => {
          e.preventDefault();
          const file = e.target.files[0]
          let reader = new FileReader()
          reader.onload = (event) => {
            let data = {
                  'type':file.type,
                  'name':file.name,
                  'size':file.size,
                  'data':event.target.result}
            this.ttk_fileOpen(data)
          }
          if (file.type.startsWith('application/json') ||
              file.type.startsWith('text')){
            reader.readAsText(file);
          }
          if (file.type.startsWith('image') ||
            file.type.startsWith('text')){
            //reader.readAsBinaryString(file);
            reader.readAsArrayBuffer(file);
          }
        })
        document.getElementById("terminal").addEventListener("dragover", (e) => {
          e.preventDefault(); //preventing from default behaviour
          //dropArea.classList.add("active");
          //dragFile.textContent = "Release to Upload File";
        })
        document.getElementById("terminal").addEventListener("dragleave", () => {
          //dropArea.classList.remove("active");
          // dragFile.textContent = "Drag files here to upload";
        })
        document.getElementById("terminal").addEventListener("drop", (e) => {
          e.preventDefault();
          const target = e.dataTransfer;
          const file = target.files[0]
          let reader = new FileReader()
          reader.onload = (event) => {
            let data = {
                  'type':file.type,
                  'name':file.name,
                  'size':file.size,
                  'data':event.target.result}
            this.ttk_dragOpen(data)
          }
          if (file.type.startsWith('application/json') ||
              file.type.startsWith('text')){
            reader.readAsText(file);
          }
        })
    }

    pyodideProxy = {
        openFile: function(encoding){
          let input = document.getElementById("file-input")
          input.accept = encoding
          input.click();
        },
        saveFile: function(name, content, encoding){
          const blob = new Blob([content], {type: encoding});
          saveAs(blob, name);
        },
        copy: async function(text){
          console.log("Copying:",text)
          const permission = await permissionsCheck()
          if(permission){
              navigator.clipboard.writeText(text)
              return //codes below wont be executed
          }
          const active = document.activeElement
          const textArea = document.createElement("textarea")
          textArea.value = text

          document.body.appendChild(textArea)

          textArea.focus()
          textArea.select()

          document.execCommand('copy')

          document.body.removeChild(textArea)
          active.focus()
        },
        paste: function(){
          /*
          const permission = await permissionsCheck()
          if(permission){
            try {
              // let text = null
              let text = await navigator.clipboard.readText().then((txt) => txt)
              // const text = navigator.clipboard.readText()
              console.log('Pasted content: ', text)
              return text
            } catch (err) {
              console.error('Failed to read clipboard contents: ', err);
            }
          }
          */
          return null
        },
        consoleLog: function(m){
          console.log("TTk:",m)
        },
        termPush: function (s) {
          this.term.write(s);
        },
        termSize: function () {
          return [this.term.cols, this.term.rows]
        },
        setTimeout: function(t, i) {
          // console.log("TIME (Start)",i,t)
          return setTimeout(() => this.ttk_timer(i), t)
        },
        stopTimeout: function(t) {
          // console.log("TIME (Stop)",t)
          clearTimeout(t)
        },
        clearTimeout: function(){
          let highestTimeoutId = setTimeout(";");
          for (let i = 0 ; i < highestTimeoutId ; i++) {
            clearTimeout(i);
          }
        },
        setInterval: function(t, i) {
          setTinterval(() => console.log('WIP -> Interval' + i), t)
        }
    };

    async init(){
        this.pyodide = await loadPyodide();
        this.ttk_timer = (i) => console.log("ttk_timer unimplemented")
        this.term.write('Pyodide ('+this.pyodide.version+') - Loaded\n\r')

        this.pyodide.registerJsModule("pyodideProxy", this.pyodideProxy);
        this.term.write('Pyodide Proxy - Loaded\n\r')
    }

    async loadLib(lib) {
        let zipResponse = await fetch(lib);
        let zipBinary = await zipResponse.arrayBuffer();
        this.pyodide.unpackArchive(zipBinary, ".tar.gz");
    }

    async loadPackage(pkg) {
      await this.pyodide.loadPackage(pkg);
    }

    async loadFile(fileUri,file){
        this.pyodide.FS.writeFile(this.pyodide.FS.currentPath+'/'+file, await (await fetch(fileUri)).text());
    }

    readFile(file){
        return this.pyodide.FS.readFile(file, {encoding:'utf8'})
    }

    currentPath(){
        return this.pyodide.FS.currentPath
    }

    getAllFiles(p){
        let ls = this.pyodide.FS.readdir(p)
        let ret = []
        for(let i=0 ; i<ls.length; i++){
            let n = p+"/"+ls[i]
            if(ls[i]=='.' || ls[i]=='..' || n==(this.pyodide.FS.currentPath+"/TermTk")) continue;
            if( this.pyodide.FS.isDir(this.pyodide.FS.lstat(n).mode)){
                ret.push({id:n, text:ls[i], expanded: true, nodes:this.getAllFiles(n)})
            }else{
                if(n.endsWith('.py')){
                   ret.push({id:n, text:ls[i]})
                }
            }
        }
        return ret
    }

    preRun(){
        this.namespace = this.pyodide.globals.get("dict")();
        this.pyodide.runPython(`
            import sys
            import TermTk as ttk
            from TermTk.TTkCore.TTkTerm.input import TTkInput
            import pyodideProxy

            def ttk_dragOpen(data):
              data = data.to_py()
              ttk.ttkEmitDragOpen(data['type'],data)
              # ttk_log(f"{type(data.to_py())=}, {str(data.to_py())}")

            def ttk_fileOpen(data):
              data = data.to_py()
              ttk.ttkEmitFileOpen(data['type'],data)
              # ttk_log(f"{type(data.to_py())=}, {str(data.to_py())}")

            def ttk_input(val):
              kevt,mevt,paste = TTkInput.key_process(val)
              if kevt or mevt:
                TTkInput.inputEvent.emit(kevt, mevt)
              if paste:
                TTkInput.pasteEvent.emit(paste)

            def ttk_resize(w,h):
              ttk.TTkLog.debug(f"Resize: {w=} {h=}")
              if ttk.TTkHelper._rootWidget:
                ttk.TTkHelper._rootWidget._win_resize_cb(w,h)
                ttk.TTkHelper.rePaintAll()
              ttk.TTkTerm.cont()

            def ttk_timer(tid):
              ttk.TTkTimer.triggerTimerId(tid)

            def ttk_log(val):
              # hex = [f"0x{ord(x):02x}" for x in val]
              ttk.TTkLog.debug("---> "+val.replace("\\033","<ESC>") + " - ")
              # ttk.TTkHelper.paintAll()

            def ttk_clean():
              if ttk.TTkHelper._rootWidget:
                ttk.TTkTimer.pyodideQuit()
                ttk.TTkHelper._rootWidget.quit()
                ttk.TTkHelper._focusWidget = None
                ttk.TTkHelper._rootCanvas = None
                ttk.TTkHelper._rootWidget = None
                ttk.TTkHelper._updateBuffer = set()
                ttk.TTkHelper._updateWidget = set()
                ttk.TTkHelper._overlay = []
                ttk.TTkHelper._shortcut = []
                ttk.TTkLog._messageHandler = [message_handler]

            def ttk_init():
              ttk.TTkToolTip.toolTipTimer = ttk.TTkTimer()
              ttk.TTkToolTip.toolTipTimer.timeout.connect(ttk.TTkToolTip._toolTipShow)

            def message_handler(mode, context, message):
                msgType = "DEBUG"
                if mode == ttk.TTkLog.InfoMsg:       msgType = "[INFO]"
                elif mode == ttk.TTkLog.WarningMsg:  msgType = "[WARNING]"
                elif mode == ttk.TTkLog.CriticalMsg: msgType = "[CRITICAL]"
                elif mode == ttk.TTkLog.FatalMsg:    msgType = "[FATAL]"
                elif mode == ttk.TTkLog.ErrorMsg:    msgType = "[ERROR]"
                pyodideProxy.consoleLog(f"{msgType} {context.file} {message}")
            # Register the callback to the message handler
            ttk.TTkLog.installMessageHandler(message_handler)
        `,{ globals: this.namespace }
        );

        this.ttk_log      = this.namespace.get("ttk_log");
        this.ttk_input    = this.namespace.get("ttk_input");
        this.ttk_timer    = this.namespace.get("ttk_timer");
        this.ttk_resize   = this.namespace.get("ttk_resize");
        this.ttk_clean    = this.namespace.get("ttk_clean");
        this.ttk_init     = this.namespace.get("ttk_init");
        this.ttk_dragOpen = this.namespace.get("ttk_dragOpen");
        this.ttk_fileOpen = this.namespace.get("ttk_fileOpen");

        this.pyodideProxy.ttk_timer = this.ttk_timer
        this.pyodideProxy.term      = this.term

        this.term.onResize( (obj) => {
            this.term.reset()
            this.ttk_resize(obj.cols, obj.rows)
        });
        this.term.onData((d, evt) => { this.ttk_input(d) })

        this.pyodide.runPython(`
          import sys,os
          sys.path.append(os.path.join(sys.path[0],'demo'))
          __name__ = "__main__"
        `,{ globals: this.namespace }
        );
    }

    run(code,filename,fps) {
        this.ttk_clean()
        console.log("Run App")

        let pwd  = this.pyodide.PATH.dirname(filename)
        let file = this.pyodide.PATH.basename(filename)

        this.pyodide.runPython(`
          __file__='`+file+`'
          os.chdir('`+pwd+`')
          ttk.TTkCfg.maxFps = `+fps,{ globals: this.namespace })

        this.ttk_init()

        this.pyodide.runPython(code,{ globals: this.namespace });

        this.ttk_log(filename + " - LOADED")
    }
}