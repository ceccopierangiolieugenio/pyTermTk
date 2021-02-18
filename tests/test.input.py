import sys, os
import logging

sys.path.append(os.path.join(sys.path[0],'..'))
import TermTk.libbpytop as lbt
from TermTk.TTk import TTkLog

def message_handler(mode, context, message):
    log = logging.debug
    if mode == TTkLog.InfoMsg:       log = logging.info
    elif mode == TTkLog.WarningMsg:  log = logging.warning
    elif mode == TTkLog.CriticalMsg: log = logging.critical
    elif mode == TTkLog.FatalMsg:    log = logging.fatal
    elif mode == TTkLog.ErrorMsg:    log = logging.error
    log(f"{context.file} {message}")

logging.basicConfig(level=logging.DEBUG,
                    format='%(levelname)s:(%(threadName)-9s) %(message)s',)
TTkLog.installMessageHandler(message_handler)

TTkLog.info("Retrieve Keyboard, Mouse press/drag/wheel Events")
TTkLog.info("Press q or <ESC> to exit")

lbt.Term.push(lbt.Term.mouse_on)
lbt.Term.echo(False)

def keyCallback(kevt=None, mevt=None):
    if kevt is not None:
        TTkLog.info(f"Key Event: {kevt}")
    if mevt is not None:
        TTkLog.info(f"Mouse Event: {mevt}")

def winCallback(width, height):
    TTkLog.info(f"Resize: w:{width}, h:{height}")

lbt.Term.registerResizeCb(winCallback)
lbt.Input.get_key(keyCallback)

lbt.Term.push(lbt.Term.mouse_off, lbt.Term.mouse_direct_off)
lbt.Term.echo(True)