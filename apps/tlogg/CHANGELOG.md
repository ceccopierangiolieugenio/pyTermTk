# Changelog

## [0.49.0-a0](https://github.com/ceccopierangiolieugenio/pyTermTk/compare/tlogg-v0.48.2-a0...tlogg-v0.49.0-a0) (2026-09-08)


### ⚠ BREAKING CHANGES

* **keyevent:** TTkKeyEvent construction and matching changed. Code that created events with TTkKeyEvent(type=..., key=..., code=..., mod=...) must now instantiate TTkKeyEvent_Character(key=..., code=..., mod=...) or TTkKeyEvent_SpecialKey(key=..., code=..., mod=...). Event-dispatch code should migrate from evt.type == TTkK.Character or TTkK.SpecialKey to isinstance(evt, TTkKeyEvent_Character) or isinstance(evt, TTkKeyEvent_SpecialKey) for compatibility with the new model.
* Python 3.9 is no longer supported. The minimum supported Python version is now Python 3.10.

### Refactors

* Drop Python 3.9 support and update for Python 3.10 ([#648](https://github.com/ceccopierangiolieugenio/pyTermTk/issues/648)) ([6784c7c](https://github.com/ceccopierangiolieugenio/pyTermTk/commit/6784c7c93ee1781bd94ce7f2a1f11af03ae69358))
* **keyevent:** split key events into character and special-key classes ([#656](https://github.com/ceccopierangiolieugenio/pyTermTk/issues/656)) ([dd35aea](https://github.com/ceccopierangiolieugenio/pyTermTk/commit/dd35aea7e302c79558a2c460742896c2259d8003))

## [0.48.2-a0](https://github.com/ceccopierangiolieugenio/pyTermTk/compare/tlogg-v0.48.1-a0...tlogg-v0.48.2-a0) (2026-05-08)


### Chores

* fix single entry slots ([#623](https://github.com/ceccopierangiolieugenio/pyTermTk/issues/623)) ([02f621d](https://github.com/ceccopierangiolieugenio/pyTermTk/commit/02f621d8afdaddb13f5a591b760613d3c8889d7f))

## [0.48.1-a0](https://github.com/ceccopierangiolieugenio/pyTermTk/compare/tlogg-v0.7.1-a.0...tlogg-v0.48.1-a0) (2025-11-10)


### Chores

* release 0.48.1-a0 ([7a9e1b4](https://github.com/ceccopierangiolieugenio/pyTermTk/commit/7a9e1b411242d61b5d034abb2256eb4a0caa4558))
* release 0.48.1-a0 ([#523](https://github.com/ceccopierangiolieugenio/pyTermTk/issues/523)) ([a6b5f5d](https://github.com/ceccopierangiolieugenio/pyTermTk/commit/a6b5f5d1309516c44719577a8468fb21f0804b72))
* release main ([#524](https://github.com/ceccopierangiolieugenio/pyTermTk/issues/524)) ([373f26d](https://github.com/ceccopierangiolieugenio/pyTermTk/commit/373f26dc37e4c3b6c47a460d109de34de90bfa23))

## [0.7.1-a.0](https://github.com/ceccopierangiolieugenio/pyTermTk/compare/tlogg-v0.7.0-a.0...tlogg-v0.7.1-a.0) (2025-07-20)


### Fixes

* color picker crash ([#423](https://github.com/ceccopierangiolieugenio/pyTermTk/issues/423)) ([af5bce3](https://github.com/ceccopierangiolieugenio/pyTermTk/commit/af5bce3d6a76d3ba35453c759a57f277bdf2b1ca))

## [0.7.0-a.0](https://github.com/ceccopierangiolieugenio/pyTermTk/compare/tlogg-v0.6.0-a.0...tlogg-v0.7.0-a.0) (2025-06-03)


### ⚠ BREAKING CHANGES

* **TabWidget:** tab request close  event need to be handled inside the app

### Refactors

* move the main routine outside the a folder ([#400](https://github.com/ceccopierangiolieugenio/pyTermTk/issues/400)) ([b1bb71f](https://github.com/ceccopierangiolieugenio/pyTermTk/commit/b1bb71fd1ecd9c41a4cb016de15f1d695ea58ba5))
* **TabWidget:** tab request close  event need to be handled inside the app ([9420adf](https://github.com/ceccopierangiolieugenio/pyTermTk/commit/9420adf68e2184482cd71266f280c560ea911f45))
