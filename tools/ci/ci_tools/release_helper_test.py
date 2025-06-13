#!/usr/bin/env python3
# MIT License
#
# Copyright (c) 2025 Eugenio Parodi <ceccopierangiolieugenio AT googlemail DOT com>
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.


from .release_helper import *

rp_pr_1 = '''{
    "releases_created": "false",
    "paths_released": "[]",
    "prs_created": "true",
    "pr": "{\"headBranchName\":\"release-please--branches--main\",\"baseBranchName\":\"main\",\"number\":397,\"title\":\"chore: release main\",\"body\":\":robot: I have created a release *beep* *boop*\\n---\\n\\n\\n<details><summary>pyTermTk: 0.43.0-a.0</summary>\\n\\n## [0.43.0-a.0](https://github.com/ceccopierangiolieugenio/pyTermTk/compare/pyTermTk-v0.42.1-a.0...pyTermTk-v0.43.0-a.0) (2025-05-28)\\n\\n\\n### ⚠ BREAKING CHANGES\\n\\n* **kodeTab:** reworked iterWidget in iterItems\\n* **TabWidget:** tab request close  event need to be handled inside the app\\n\\n### Fixes\\n\\n* **spinbox:** better check for float, empty strings and negative numbers ([4909bf6](https://github.com/ceccopierangiolieugenio/pyTermTk/commit/4909bf6756000f9450249b28f8c8379a2160415c))\\n\\n\\n### Chores\\n\\n* **kodeTab:** reworked iterWidget in iterItems ([47f73fc](https://github.com/ceccopierangiolieugenio/pyTermTk/commit/47f73fc03a5a049ac3e6073dcadc09018b509328))\\n* **ttk:** workaround timer disconnect in case of error ([d70b2c1](https://github.com/ceccopierangiolieugenio/pyTermTk/commit/d70b2c1c3cf25f7ffb479bc2850b3c9a3ca0fe0c))\\n\\n\\n### Refactors\\n\\n* **TabWidget:** tab request close  event need to be handled inside the app ([9420adf](https://github.com/ceccopierangiolieugenio/pyTermTk/commit/9420adf68e2184482cd71266f280c560ea911f45))\\n* **TTkColor:** improved typings ([711d611](https://github.com/ceccopierangiolieugenio/pyTermTk/commit/711d611a73be0d0a6fce37e4624b5ae30847dd9c))\\n</details>\\n\\n<details><summary>ttkode: 0.4.0-a.2</summary>\\n\\n## [0.4.0-a.2](https://github.com/ceccopierangiolieugenio/pyTermTk/compare/ttkode-v0.3.2-a.2...ttkode-v0.4.0-a.2) (2025-05-28)\\n\\n\\n### ⚠ BREAKING CHANGES\\n\\n* **TabWidget:** tab request close  event need to be handled inside the app\\n\\n### Refactors\\n\\n* **TabWidget:** tab request close  event need to be handled inside the app ([9420adf](https://github.com/ceccopierangiolieugenio/pyTermTk/commit/9420adf68e2184482cd71266f280c560ea911f45))\\n</details>\\n\\n<details><summary>tlogg: 0.7.0-a.0</summary>\\n\\n## [0.7.0-a.0](https://github.com/ceccopierangiolieugenio/pyTermTk/compare/tlogg-v0.6.0-a.0...tlogg-v0.7.0-a.0) (2025-05-28)\\n\\n\\n### ⚠ BREAKING CHANGES\\n\\n* **TabWidget:** tab request close  event need to be handled inside the app\\n\\n### Refactors\\n\\n* move the main routine outside the a folder ([#400](https://github.com/ceccopierangiolieugenio/pyTermTk/issues/400)) ([b1bb71f](https://github.com/ceccopierangiolieugenio/pyTermTk/commit/b1bb71fd1ecd9c41a4cb016de15f1d695ea58ba5))\\n* **TabWidget:** tab request close  event need to be handled inside the app ([9420adf](https://github.com/ceccopierangiolieugenio/pyTermTk/commit/9420adf68e2184482cd71266f280c560ea911f45))\\n</details>\\n\\n---\\nThis PR was generated with [Release Please](https://github.com/googleapis/release-please). See [documentation](https://github.com/googleapis/release-please#release-please).\",\"files\":[],\"labels\":[\"autorelease: pending\"]}",
    "prs": "[{\"headBranchName\":\"release-please--branches--main\",\"baseBranchName\":\"main\",\"number\":397,\"title\":\"chore: release main\",\"body\":\":robot: I have created a release *beep* *boop*\\n---\\n\\n\\n<details><summary>pyTermTk: 0.43.0-a.0</summary>\\n\\n## [0.43.0-a.0](https://github.com/ceccopierangiolieugenio/pyTermTk/compare/pyTermTk-v0.42.1-a.0...pyTermTk-v0.43.0-a.0) (2025-05-28)\\n\\n\\n### ⚠ BREAKING CHANGES\\n\\n* **kodeTab:** reworked iterWidget in iterItems\\n* **TabWidget:** tab request close  event need to be handled inside the app\\n\\n### Fixes\\n\\n* **spinbox:** better check for float, empty strings and negative numbers ([4909bf6](https://github.com/ceccopierangiolieugenio/pyTermTk/commit/4909bf6756000f9450249b28f8c8379a2160415c))\\n\\n\\n### Chores\\n\\n* **kodeTab:** reworked iterWidget in iterItems ([47f73fc](https://github.com/ceccopierangiolieugenio/pyTermTk/commit/47f73fc03a5a049ac3e6073dcadc09018b509328))\\n* **ttk:** workaround timer disconnect in case of error ([d70b2c1](https://github.com/ceccopierangiolieugenio/pyTermTk/commit/d70b2c1c3cf25f7ffb479bc2850b3c9a3ca0fe0c))\\n\\n\\n### Refactors\\n\\n* **TabWidget:** tab request close  event need to be handled inside the app ([9420adf](https://github.com/ceccopierangiolieugenio/pyTermTk/commit/9420adf68e2184482cd71266f280c560ea911f45))\\n* **TTkColor:** improved typings ([711d611](https://github.com/ceccopierangiolieugenio/pyTermTk/commit/711d611a73be0d0a6fce37e4624b5ae30847dd9c))\\n</details>\\n\\n<details><summary>ttkode: 0.4.0-a.2</summary>\\n\\n## [0.4.0-a.2](https://github.com/ceccopierangiolieugenio/pyTermTk/compare/ttkode-v0.3.2-a.2...ttkode-v0.4.0-a.2) (2025-05-28)\\n\\n\\n### ⚠ BREAKING CHANGES\\n\\n* **TabWidget:** tab request close  event need to be handled inside the app\\n\\n### Refactors\\n\\n* **TabWidget:** tab request close  event need to be handled inside the app ([9420adf](https://github.com/ceccopierangiolieugenio/pyTermTk/commit/9420adf68e2184482cd71266f280c560ea911f45))\\n</details>\\n\\n<details><summary>tlogg: 0.7.0-a.0</summary>\\n\\n## [0.7.0-a.0](https://github.com/ceccopierangiolieugenio/pyTermTk/compare/tlogg-v0.6.0-a.0...tlogg-v0.7.0-a.0) (2025-05-28)\\n\\n\\n### ⚠ BREAKING CHANGES\\n\\n* **TabWidget:** tab request close  event need to be handled inside the app\\n\\n### Refactors\\n\\n* move the main routine outside the a folder ([#400](https://github.com/ceccopierangiolieugenio/pyTermTk/issues/400)) ([b1bb71f](https://github.com/ceccopierangiolieugenio/pyTermTk/commit/b1bb71fd1ecd9c41a4cb016de15f1d695ea58ba5))\\n* **TabWidget:** tab request close  event need to be handled inside the app ([9420adf](https://github.com/ceccopierangiolieugenio/pyTermTk/commit/9420adf68e2184482cd71266f280c560ea911f45))\\n</details>\\n\\n---\\nThis PR was generated with [Release Please](https://github.com/googleapis/release-please). See [documentation](https://github.com/googleapis/release-please#release-please).\",\"files\":[],\"labels\":[\"autorelease: pending\"]}]"
  }
'''

rp_release_1 = '''{
    "releases_created": "true",
    "libs/pyTermTk--release_created": "true",
    "libs/pyTermTk--id": "222844982",
    "libs/pyTermTk--name": "pyTermTk: v0.43.0-a.0",
    "libs/pyTermTk--tag_name": "pyTermTk-v0.43.0-a.0",
    "libs/pyTermTk--sha": "edce717e527f2fe93a8a0c7f17e08a6b5fecd7bd",
    "libs/pyTermTk--body": "## [0.43.0-a.0](https://github.com/ceccopierangiolieugenio/pyTermTk/compare/pyTermTk-v0.42.1-a.0...pyTermTk-v0.43.0-a.0) (2025-06-03)\n\n\n### ⚠ BREAKING CHANGES\n\n* **kodeTab:** reworked iterWidget in iterItems\n* **TabWidget:** tab request close  event need to be handled inside the app\n\n### Fixes\n\n* **spinbox:** better check for float, empty strings and negative numbers ([4909bf6](https://github.com/ceccopierangiolieugenio/pyTermTk/commit/4909bf6756000f9450249b28f8c8379a2160415c))\n\n\n### Chores\n\n* autogen code for scrollarea classes ([#406](https://github.com/ceccopierangiolieugenio/pyTermTk/issues/406)) ([fef1b0e](https://github.com/ceccopierangiolieugenio/pyTermTk/commit/fef1b0ea5bd6ddc8f3e8f93a23ea156071e77493))\n* **Input:** add support for ctrl and other key comination ([#404](https://github.com/ceccopierangiolieugenio/pyTermTk/issues/404)) ([5c2bb92](https://github.com/ceccopierangiolieugenio/pyTermTk/commit/5c2bb9202cd819aa573e9f0d9ea966a4d0e5c485))\n* **kodeTab:** reworked iterWidget in iterItems ([47f73fc](https://github.com/ceccopierangiolieugenio/pyTermTk/commit/47f73fc03a5a049ac3e6073dcadc09018b509328))\n* **spinbox:** fix return type ([ddc53a0](https://github.com/ceccopierangiolieugenio/pyTermTk/commit/ddc53a07653a6f3aa958509d7d400cc6c6264d91))\n* **spinbox:** handle left/right wheel  event ([ce961a6](https://github.com/ceccopierangiolieugenio/pyTermTk/commit/ce961a657573ee520b73fca7d4ae721a8837a1d0))\n* **ttk:** workaround timer disconnect in case of error ([d70b2c1](https://github.com/ceccopierangiolieugenio/pyTermTk/commit/d70b2c1c3cf25f7ffb479bc2850b3c9a3ca0fe0c))\n\n\n### Refactors\n\n* **TabWidget:** tab request close  event need to be handled inside the app ([9420adf](https://github.com/ceccopierangiolieugenio/pyTermTk/commit/9420adf68e2184482cd71266f280c560ea911f45))\n* **TTkColor:** improved typings ([711d611](https://github.com/ceccopierangiolieugenio/pyTermTk/commit/711d611a73be0d0a6fce37e4624b5ae30847dd9c))",
    "libs/pyTermTk--html_url": "https://github.com/ceccopierangiolieugenio/pyTermTk/releases/tag/pyTermTk-v0.43.0-a.0",
    "libs/pyTermTk--draft": "false",
    "libs/pyTermTk--upload_url": "https://uploads.github.com/repos/ceccopierangiolieugenio/pyTermTk/releases/222844982/assets{?name,label}",
    "libs/pyTermTk--path": "libs/pyTermTk",
    "libs/pyTermTk--version": "0.43.0-a.0",
    "libs/pyTermTk--major": "0",
    "libs/pyTermTk--minor": "43",
    "libs/pyTermTk--patch": "0",
    "libs/pyTermTk--prNumber": "397",
    "apps/ttkode--release_created": "true",
    "apps/ttkode--id": "222844984",
    "apps/ttkode--name": "ttkode: v0.4.0-a.2",
    "apps/ttkode--tag_name": "ttkode-v0.4.0-a.2",
    "apps/ttkode--sha": "edce717e527f2fe93a8a0c7f17e08a6b5fecd7bd",
    "apps/ttkode--body": "## [0.4.0-a.2](https://github.com/ceccopierangiolieugenio/pyTermTk/compare/ttkode-v0.3.2-a.2...ttkode-v0.4.0-a.2) (2025-06-03)\n\n\n### ⚠ BREAKING CHANGES\n\n* **TabWidget:** tab request close  event need to be handled inside the app\n\n### Features\n\n* add save feature ([#407](https://github.com/ceccopierangiolieugenio/pyTermTk/issues/407)) ([26ff9b2](https://github.com/ceccopierangiolieugenio/pyTermTk/commit/26ff9b2f0a81bddadeb6849d5d560ae67406f973))\n\n\n### Refactors\n\n* **TabWidget:** tab request close  event need to be handled inside the app ([9420adf](https://github.com/ceccopierangiolieugenio/pyTermTk/commit/9420adf68e2184482cd71266f280c560ea911f45))",
    "apps/ttkode--html_url": "https://github.com/ceccopierangiolieugenio/pyTermTk/releases/tag/ttkode-v0.4.0-a.2",
    "apps/ttkode--draft": "false",
    "apps/ttkode--upload_url": "https://uploads.github.com/repos/ceccopierangiolieugenio/pyTermTk/releases/222844984/assets{?name,label}",
    "apps/ttkode--path": "apps/ttkode",
    "apps/ttkode--version": "0.4.0-a.2",
    "apps/ttkode--major": "0",
    "apps/ttkode--minor": "4",
    "apps/ttkode--patch": "0",
    "apps/ttkode--prNumber": "397",
    "apps/tlogg--release_created": "true",
    "apps/tlogg--id": "222844986",
    "apps/tlogg--name": "tlogg: v0.7.0-a.0",
    "apps/tlogg--tag_name": "tlogg-v0.7.0-a.0",
    "apps/tlogg--sha": "edce717e527f2fe93a8a0c7f17e08a6b5fecd7bd",
    "apps/tlogg--body": "## [0.7.0-a.0](https://github.com/ceccopierangiolieugenio/pyTermTk/compare/tlogg-v0.6.0-a.0...tlogg-v0.7.0-a.0) (2025-06-03)\n\n\n### ⚠ BREAKING CHANGES\n\n* **TabWidget:** tab request close  event need to be handled inside the app\n\n### Refactors\n\n* move the main routine outside the a folder ([#400](https://github.com/ceccopierangiolieugenio/pyTermTk/issues/400)) ([b1bb71f](https://github.com/ceccopierangiolieugenio/pyTermTk/commit/b1bb71fd1ecd9c41a4cb016de15f1d695ea58ba5))\n* **TabWidget:** tab request close  event need to be handled inside the app ([9420adf](https://github.com/ceccopierangiolieugenio/pyTermTk/commit/9420adf68e2184482cd71266f280c560ea911f45))",
    "apps/tlogg--html_url": "https://github.com/ceccopierangiolieugenio/pyTermTk/releases/tag/tlogg-v0.7.0-a.0",
    "apps/tlogg--draft": "false",
    "apps/tlogg--upload_url": "https://uploads.github.com/repos/ceccopierangiolieugenio/pyTermTk/releases/222844986/assets{?name,label}",
    "apps/tlogg--path": "apps/tlogg",
    "apps/tlogg--version": "0.7.0-a.0",
    "apps/tlogg--major": "0",
    "apps/tlogg--minor": "7",
    "apps/tlogg--patch": "0",
    "apps/tlogg--prNumber": "397",
    "paths_released": "[\"libs/pyTermTk\",\"apps/ttkode\",\"apps/tlogg\"]",
    "prs_created": "false"
  }'''