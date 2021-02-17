import sys, os
import logging

sys.path.append(os.path.join(sys.path[0],'..'))
import ttk.libbpytop as lbt
import ttk

def message_handler(mode, context, message):
    if mode == ttk.InfoMsg:       mode = 'INFO'
    elif mode == ttk.WarningMsg:  mode = 'WARNING'
    elif mode == ttk.CriticalMsg: mode = 'CRITICAL'
    elif mode == ttk.FatalMsg:    mode = 'FATAL'
    else: mode = 'DEBUG'
    logging.debug(f"{mode} {context.file} {message}")

logging.basicConfig(level=logging.DEBUG,
                    format='(%(threadName)-9s) %(message)s',)
ttk.installMessageHandler(message_handler)

ttk.info("Retrieve Keyboard, Mouse press/drag/wheel Events")
ttk.info("Press q or <ESC> to exit")

lbt.Term.push(lbt.Term.mouse_on)
lbt.Term.echo(False)

def keyCallback(kevt=None, mevt=None):
    if kevt is not None:
        ttk.info(f"Key Event: {kevt}")
    if mevt is not None:
        ttk.info(f"Mouse Event: {mevt}")

def winCallback(width, height):
    ttk.info(f"Resize: w:{width}, h:{height}")

lbt.Term.registerResizeCb(winCallback)
lbt.Input.get_key(keyCallback)

lbt.Term.push(lbt.Term.mouse_off, lbt.Term.mouse_direct_off)
lbt.Term.echo(True)