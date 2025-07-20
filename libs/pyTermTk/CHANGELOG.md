# Changelog

## [0.43.3-a.0](https://github.com/ceccopierangiolieugenio/pyTermTk/compare/pyTermTk-v0.43.2-a.0...pyTermTk-v0.43.3-a.0) (2025-07-20)


### Fixes

* **treeWidget:** avoid crash when the content size is required for empty models ([#426](https://github.com/ceccopierangiolieugenio/pyTermTk/issues/426)) ([bd8f60f](https://github.com/ceccopierangiolieugenio/pyTermTk/commit/bd8f60f65e53ba41e806b1dca0ffa6fd5259f55c))


### Chores

* fix log typing ([14e7739](https://github.com/ceccopierangiolieugenio/pyTermTk/commit/14e77397ce1ea7bfa9af27ada4ccbfdbd971b8c3))
* improve typing ([#417](https://github.com/ceccopierangiolieugenio/pyTermTk/issues/417)) ([833005a](https://github.com/ceccopierangiolieugenio/pyTermTk/commit/833005acd115f2a5cb467b614ff208bda013c043))
* **KodeTab:** fix hover highlight ([c944b4d](https://github.com/ceccopierangiolieugenio/pyTermTk/commit/c944b4d14603f35756fb2e7154eb8cda0ec58f4b))
* reworked autogen ([f2d35ae](https://github.com/ceccopierangiolieugenio/pyTermTk/commit/f2d35ae24a5e27885febe56ab25e50a884d516b6))
* **Typing:** improved TTkHelper typings ([849ab5a](https://github.com/ceccopierangiolieugenio/pyTermTk/commit/849ab5afe61e2519fb3e8c89dbd21cdf7f8a252c))
* **Typing:** improved typings in the base widget class ([9da8d3c](https://github.com/ceccopierangiolieugenio/pyTermTk/commit/9da8d3c1cf5108deb057bd7f747d100a0c24e759))
* **Typing:** Reworked TTkColor  to solve all the typing issues ([c94c114](https://github.com/ceccopierangiolieugenio/pyTermTk/commit/c94c114faac878c9c5f99619eaf9fd79bc285c42))
* **Typing:** solved typing issues in the unsupported Fancy widgets ([e27b2af](https://github.com/ceccopierangiolieugenio/pyTermTk/commit/e27b2afb0bb4c6d295f223c0f83b8ddab6f5d0e3))

## [0.43.2-a.0](https://github.com/ceccopierangiolieugenio/pyTermTk/compare/pyTermTk-v0.43.1-a.0...pyTermTk-v0.43.2-a.0) (2025-06-04)


### Chores

* autogen signals and rewrite forwarded as properties ([#410](https://github.com/ceccopierangiolieugenio/pyTermTk/issues/410)) ([7597980](https://github.com/ceccopierangiolieugenio/pyTermTk/commit/759798025624a692af24170475d1f3f253d31689))

## [0.43.1-a.0](https://github.com/ceccopierangiolieugenio/pyTermTk/compare/pyTermTk-v0.43.0-a.0...pyTermTk-v0.43.1-a.0) (2025-06-03)


### Chores

* update hero image ([ae3a37f](https://github.com/ceccopierangiolieugenio/pyTermTk/commit/ae3a37ffab812fb2c174065997e64b8c565e76d3))

## [0.43.0-a.0](https://github.com/ceccopierangiolieugenio/pyTermTk/compare/pyTermTk-v0.42.1-a.0...pyTermTk-v0.43.0-a.0) (2025-06-03)


### ⚠ BREAKING CHANGES

* **kodeTab:** reworked iterWidget in iterItems
* **TabWidget:** tab request close  event need to be handled inside the app

### Fixes

* **spinbox:** better check for float, empty strings and negative numbers ([4909bf6](https://github.com/ceccopierangiolieugenio/pyTermTk/commit/4909bf6756000f9450249b28f8c8379a2160415c))


### Chores

* autogen code for scrollarea classes ([#406](https://github.com/ceccopierangiolieugenio/pyTermTk/issues/406)) ([fef1b0e](https://github.com/ceccopierangiolieugenio/pyTermTk/commit/fef1b0ea5bd6ddc8f3e8f93a23ea156071e77493))
* **Input:** add support for ctrl and other key comination ([#404](https://github.com/ceccopierangiolieugenio/pyTermTk/issues/404)) ([5c2bb92](https://github.com/ceccopierangiolieugenio/pyTermTk/commit/5c2bb9202cd819aa573e9f0d9ea966a4d0e5c485))
* **kodeTab:** reworked iterWidget in iterItems ([47f73fc](https://github.com/ceccopierangiolieugenio/pyTermTk/commit/47f73fc03a5a049ac3e6073dcadc09018b509328))
* **spinbox:** fix return type ([ddc53a0](https://github.com/ceccopierangiolieugenio/pyTermTk/commit/ddc53a07653a6f3aa958509d7d400cc6c6264d91))
* **spinbox:** handle left/right wheel  event ([ce961a6](https://github.com/ceccopierangiolieugenio/pyTermTk/commit/ce961a657573ee520b73fca7d4ae721a8837a1d0))
* **ttk:** workaround timer disconnect in case of error ([d70b2c1](https://github.com/ceccopierangiolieugenio/pyTermTk/commit/d70b2c1c3cf25f7ffb479bc2850b3c9a3ca0fe0c))


### Refactors

* **TabWidget:** tab request close  event need to be handled inside the app ([9420adf](https://github.com/ceccopierangiolieugenio/pyTermTk/commit/9420adf68e2184482cd71266f280c560ea911f45))
* **TTkColor:** improved typings ([711d611](https://github.com/ceccopierangiolieugenio/pyTermTk/commit/711d611a73be0d0a6fce37e4624b5ae30847dd9c))

## [0.42.1-a.0](https://github.com/ceccopierangiolieugenio/pyTermTk/compare/pyTermTk-v0.42.0-a.0...pyTermTk-v0.42.1-a.0) (2025-05-01)


### Fixes

* **driver:** allow different signal masks between darwin and Linux ([7fc8725](https://github.com/ceccopierangiolieugenio/pyTermTk/commit/7fc8725ced906fb120bc086ffac10cb607859039))

## [0.42.0-a.0](https://github.com/ceccopierangiolieugenio/pyTermTk/compare/pyTermTk-v0.41.18-a.0...pyTermTk-v0.42.0-a.0) (2025-04-29)


### Fixes

* textEdit release control for unhandled shortcuts ([f5c60f9](https://github.com/ceccopierangiolieugenio/pyTermTk/commit/f5c60f9d5a4e47108e5a05063c40418c750b6778))
* ttkLineEdit broadcast textChanged after deletion ([#388](https://github.com/ceccopierangiolieugenio/pyTermTk/issues/388)) ([4857cb3](https://github.com/ceccopierangiolieugenio/pyTermTk/commit/4857cb31cbd0bac49fd6464879a4590c0fc97550))


### Features

* add iterWidgets to KodeTab ([#390](https://github.com/ceccopierangiolieugenio/pyTermTk/issues/390)) ([40ad352](https://github.com/ceccopierangiolieugenio/pyTermTk/commit/40ad3524782cfe0330be7d5d3507a39b5042fd54))
* add nerd_1 theme to the tab widget ([0da3881](https://github.com/ceccopierangiolieugenio/pyTermTk/commit/0da38814f153d062c347ac44cc9250fd6f2db5a2))
* added expandAll,collapseAll to TTkTree ([f3d8205](https://github.com/ceccopierangiolieugenio/pyTermTk/commit/f3d8205dcbddc54e7f50055128125bdf3cc939ae))
* added hinting and bgcolor to TTkLineEdit ([5afecec](https://github.com/ceccopierangiolieugenio/pyTermTk/commit/5afecec62d6061e5ba14b3d93a008cf5b9733579))
* Allow configurable closing glyph in the tab button ([ebab624](https://github.com/ceccopierangiolieugenio/pyTermTk/commit/ebab624779c7853c7831614d028cbe35a055ab1a))
* prototyping Nerd_1 style to KodeTab ([a5fb669](https://github.com/ceccopierangiolieugenio/pyTermTk/commit/a5fb6698fdd33d4cde34bb04855fbdce501aeafe))
* tab button resize accordingly if the text change ([7aa6627](https://github.com/ceccopierangiolieugenio/pyTermTk/commit/7aa6627fd2acb533a83a0975d6cc3cc75dbcd333))


### Refactors

* adapted ttkode to the latest pyTermTk ([542ecd7](https://github.com/ceccopierangiolieugenio/pyTermTk/commit/542ecd7f7798b10bca29a7e856e85aa91bb3bc74))

## [0.41.18-a.0](https://github.com/ceccopierangiolieugenio/pyTermTk/compare/pyTermTk-v0.41.17-a.0...pyTermTk-v0.41.18-a.0) (2025-04-04)


### Refactors

* moved the sandbox to pyTermTk-docs ([2cac91d](https://github.com/ceccopierangiolieugenio/pyTermTk/commit/2cac91d259c193badf676bdd1373a53f5db3557e))

## [0.41.17-a.0](https://github.com/ceccopierangiolieugenio/pyTermTk/compare/pyTermTk-v0.41.16-a.0...pyTermTk-v0.41.17-a.0) (2025-04-03)


### Chores

* release main ([#376](https://github.com/ceccopierangiolieugenio/pyTermTk/issues/376)) ([9b85fc4](https://github.com/ceccopierangiolieugenio/pyTermTk/commit/9b85fc4d4f3a5997811f10ca5b87cf756c8dd621))

## [0.41.16-a.0](https://github.com/ceccopierangiolieugenio/pyTermTk/compare/pyTermTk-v0.41.15-a.0...pyTermTk-v0.41.16-a.0) (2025-04-02)


### Chores

* add pkgs uri for pypi ([0363708](https://github.com/ceccopierangiolieugenio/pyTermTk/commit/0363708cd969d6495192459031ac5be12d035328))
* merge main ([761f608](https://github.com/ceccopierangiolieugenio/pyTermTk/commit/761f608e77ed5b2b31c7e4434b95094609eb9794))

## [0.41.15-a.0](https://github.com/ceccopierangiolieugenio/pyTermTk/compare/pyTermTk-v0.41.14-a.0...pyTermTk-v0.41.15-a.0) (2025-04-02)


### Chores

* bump version ([9c2940a](https://github.com/ceccopierangiolieugenio/pyTermTk/commit/9c2940a2703ba605e4d4ffbfe89e473d29043e75))
* merge main ([5a82301](https://github.com/ceccopierangiolieugenio/pyTermTk/commit/5a82301291fe06e9c4d2a13911982b427c8a232e))

## [0.41.14-a.0](https://github.com/ceccopierangiolieugenio/pyTermTk/compare/pyTermTk-v0.41.13-a.0...pyTermTk-v0.41.14-a.0) (2025-04-02)


### Chores

* fix broken symlink ([5c9818a](https://github.com/ceccopierangiolieugenio/pyTermTk/commit/5c9818ac358c6a82689a7ab53708b372de7dcc29))
* fix deploy ([d0d1746](https://github.com/ceccopierangiolieugenio/pyTermTk/commit/d0d1746864307b5e1a7a8e422a144b19e894dbdc))
* merge main ([f16d4eb](https://github.com/ceccopierangiolieugenio/pyTermTk/commit/f16d4ebff79216c9f3fa27cb2f2cee745de0e38c))

## [0.41.11-a.0](https://github.com/ceccopierangiolieugenio/pyTermTk/compare/pyTermTk-v0.41.10-a.0...pyTermTk-v0.41.11-a.0) (2025-03-30)


### Chores

* bump version ([ffad7d1](https://github.com/ceccopierangiolieugenio/pyTermTk/commit/ffad7d153d5cd5a7a78fb4ee7fb0a108315e7af4))

## [0.41.10-a.0](https://github.com/ceccopierangiolieugenio/pyTermTk/compare/pyTermTk-v0.41.9-a.0...pyTermTk-v0.41.10-a.0) (2025-03-29)


### Chores

* bump version ([51c89d8](https://github.com/ceccopierangiolieugenio/pyTermTk/commit/51c89d88dc18bbdf08fb4eda334ec100a0f3caeb))

## [0.41.9-a.0](https://github.com/ceccopierangiolieugenio/pyTermTk/compare/pyTermTk-v0.41.8-a.0...pyTermTk-v0.41.9-a.0) (2025-03-29)


### Chores

* bump version ([5884f69](https://github.com/ceccopierangiolieugenio/pyTermTk/commit/5884f69a276e9fca20b9413d17b7ce368d1cc8bd))

## [0.41.8-a.0](https://github.com/ceccopierangiolieugenio/pyTermTk/compare/pyTermTk-v0.41.7-a.0...pyTermTk-v0.41.8-a.0) (2025-03-29)


### Chores

* bumbed version ([e401e73](https://github.com/ceccopierangiolieugenio/pyTermTk/commit/e401e73633c2e32fe0eb0b7302fd93f57aaeb9af))

## [0.41.7-a.0](https://github.com/ceccopierangiolieugenio/pyTermTk/compare/pyTermTk-v0.41.6-a.0...pyTermTk-v0.41.7-a.0) (2025-03-29)


### Chores

* adapted the version ([e13a0ea](https://github.com/ceccopierangiolieugenio/pyTermTk/commit/e13a0ea514139688f239c482c019852e605e4d70))

## [0.41.6-a.0](https://github.com/ceccopierangiolieugenio/pyTermTk/compare/pyTermTk-v0.41.5-a.0...pyTermTk-v0.41.6-a.0) (2025-03-29)


### Chores

* let's see if the version actually update ([4fb9280](https://github.com/ceccopierangiolieugenio/pyTermTk/commit/4fb928051ecb7518aebbfbe04fe99b17240f892d))

## [0.41.5-a.0](https://github.com/ceccopierangiolieugenio/pyTermTk/compare/pyTermTk-v0.41.4-a.0...pyTermTk-v0.41.5-a.0) (2025-03-29)


### Chores

* added version updater ([96ae50c](https://github.com/ceccopierangiolieugenio/pyTermTk/commit/96ae50c58add78d633887aa6aed95c1077194a9a))
* test release 7 ([84b7c75](https://github.com/ceccopierangiolieugenio/pyTermTk/commit/84b7c755e368732577a056f8f8d9786e294255f7))

## [0.41.4-a.0](https://github.com/ceccopierangiolieugenio/pyTermTk/compare/pyTermTk-v0.41.3-a.0...pyTermTk-v0.41.4-a.0) (2025-03-29)


### Chores

* test release 4 ([3875ee0](https://github.com/ceccopierangiolieugenio/pyTermTk/commit/3875ee0c23345fbfcbd1a341c0878ebb50661bf1))
* test release 5 ([36b99e2](https://github.com/ceccopierangiolieugenio/pyTermTk/commit/36b99e2bc9386b460010eee1155cf86456c972c9))
* test release 6 ([59420b4](https://github.com/ceccopierangiolieugenio/pyTermTk/commit/59420b4edffcaab9f4ae7f02184fa7a456018916))

## [0.41.3-a.0](https://github.com/ceccopierangiolieugenio/pyTermTk/compare/pyTermTk-v0.41.2-a.0...pyTermTk-v0.41.3-a.0) (2025-03-26)


### Chores

* testing deploy ([#341](https://github.com/ceccopierangiolieugenio/pyTermTk/issues/341)) ([3668ae3](https://github.com/ceccopierangiolieugenio/pyTermTk/commit/3668ae3c226f5aa316b8b769829f499f9b3a007a))

## [0.41.2-a.0](https://github.com/ceccopierangiolieugenio/pyTermTk/compare/pyTermTk-v0.41.1-a.0...pyTermTk-v0.41.2-a.0) (2025-03-26)


### Chores

* testing deploy ([#338](https://github.com/ceccopierangiolieugenio/pyTermTk/issues/338)) ([4dc5d73](https://github.com/ceccopierangiolieugenio/pyTermTk/commit/4dc5d733eefd9377dfd90dc0927941f46465a62f))

## [0.41.1-a.0](https://github.com/ceccopierangiolieugenio/pyTermTk/compare/pyTermTk-v0.41.0-a.0...pyTermTk-v0.41.1-a.0) (2025-03-26)


### Chores

* testing release 01 ([#336](https://github.com/ceccopierangiolieugenio/pyTermTk/issues/336)) ([61b7b9c](https://github.com/ceccopierangiolieugenio/pyTermTk/commit/61b7b9c05f9c102bdae52137fdcc2aa236fc8391))

## [0.41.0-a.0](https://github.com/ceccopierangiolieugenio/pyTermTk/compare/pyTermTk-v0.40.0-a.0...pyTermTk-v0.41.0-a.0) (2025-03-26)


### Fixes

* [#326](https://github.com/ceccopierangiolieugenio/pyTermTk/issues/326) crash adding row in the TTkTableModelList ([#327](https://github.com/ceccopierangiolieugenio/pyTermTk/issues/327)) ([b0feaa1](https://github.com/ceccopierangiolieugenio/pyTermTk/commit/b0feaa139ee8fb19d475e1cf267ff7b6c182dc72))


### Features

* added find in the text edit ([#320](https://github.com/ceccopierangiolieugenio/pyTermTk/issues/320)) ([d809d0b](https://github.com/ceccopierangiolieugenio/pyTermTk/commit/d809d0bcca544e42e3bb1b89f55481bb646c1a90))
