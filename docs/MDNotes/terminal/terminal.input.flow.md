# Terminal input rework:

## How it was:

```
TerminalViewer
  runShell ---> Thread
                loop -------> inputGenerator()
                                while input (io read, termio)
                    <----------   yeld inTxt
                generator.next()
```

## How it should be:

```
TerminalViewer            TerminalHelper
    genPush = _genPush      runShell ---> Thread
                                          loopRead
    write(intput)  <---------------------   while input
      genPush.send(input)
        _genPush
          out = yeld
```