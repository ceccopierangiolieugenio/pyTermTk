# 0.36.0-a
Single Thread,

```
TTkInputDriver           TTkInput                                TTK
    read() <- stdin
      yield inString  -->  for inString in _readInput.read()
                             key_process(inString)
                               inputEvent.emit(kevt, mevt)  ---->  _processInput
                               pasteEvent.emit(str)         ---->  _pasteInput
```

# 0.xx.0-a +
multithread
Rework key_process to return kevt,mevt,paste

```
TTkInputDriver           TTkInput                                              TTK
                           Thread1       Thread2 (mainn)
    read() <- stdin
      yield inString  -->  for inString in _readInput.read()
                             kevt,mevt,paste = key_process(inString)
                             queue.put(kevt,mevt,paste)
                             
                                         queue.get()
                                         inputEvent.emit(kevt, mevt)  ------>  _processInput
                                         pasteEvent.emit(str)         ------>  _pasteInput
```
