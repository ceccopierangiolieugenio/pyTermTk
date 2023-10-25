# How it Was
TTk:
- __init__()
  ```python
  self._input = TTkInput()
  self._input.inputEvent.connect(self._processInput)  
  self._input.pasteEvent.connect(self._processPaste)
  ```
- mainLoop()
  ```python
  TTkTerm.registerResizeCb(self._win_resize_cb)
  TTkTerm.init(
        title=self._title,
        sigmask=self._sigmask,
        mouse=self._termMouse,
        directMouse=self._termDirectMouse )
  ```
  
# How it Should Be
- __init__()
  ```python
  TTkInput.inputEvent.connect(self._processInput)
  TTkInput.pasteEvent.connect(self._processPaste)
  TTkSignalDriver.sigStop.connect(self._SIGSTOP)
  TTkSignalDriver.sigCont.connect(self._SIGCONT)
  TTkSignalDriver.sigInt.connect( self._SIGINT)
  ```
- mainLoop()
  ```python
  TTkInput.init(
        mouse=self._termMouse,
        directMouse=self._termDirectMouse)
  TTkTerm.init(
        title=self._title,
        sigmask=self._sigmask)
  ```