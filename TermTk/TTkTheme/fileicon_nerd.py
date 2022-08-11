# The MIT License (MIT)
#
# Copyright (c) 2014 Ryan L McIntyre - ( https://github.com/ryanoasis/vim-devicons )
# Copyright (c) 2022 Eugenio Parodi  - ( https://github.com/ceccopierangiolieugenio/pyTermTk )
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


# Using the icons from:
#  https://www.nerdfonts.com/#home
#
# Extension/Matches list from:
#  https://github.com/ryanoasis/vim-devicons/blob/master/plugin/webdevicons.vim

import re
import os


class FileIcon():
    folderClose = ''
    folderOpen  = ''
    home = ''
    computer = ''

    file_node_exact_matches = (
        ('.bashprofile'                     , ''),
        ('.bashrc'                          , ''),
        ('.ds_store'                        , ''),
        ('.gitattributes'                   , ''),
        ('.gitconfig'                       , ''),
        ('.gitignore'                       , ''),
        ('.gitlab-ci.yml'                   , ''),
        ('.gvimrc'                          , ''),
        ('.vimrc'                           , ''),
        ('.zprofile'                        , ''),
        ('.zshenv'                          , ''),
        ('.zshrc'                           , ''),
        ('_gvimrc'                          , ''),
        ('_vimrc'                           , ''),
        ('cmakelists.txt'                   , ''),
        ('config.ru'                        , ''),
        ('docker-compose.yml'               , ''),
        ('dockerfile'                       , ''),
        ('dropbox'                          , ''),
        ('exact-match-case-sensitive-1.txt' , '1'),
        ('exact-match-case-sensitive-2'     , '2'),
        ('favicon.ico'                      , ''),
        ('gemfile'                          , ''),
        ('gruntfile.coffee'                 , ''),
        ('gruntfile.js'                     , ''),
        ('gruntfile.ls'                     , ''),
        ('gulpfile.coffee'                  , ''),
        ('gulpfile.js'                      , ''),
        ('gulpfile.ls'                      , ''),
        ('license'                          , ''),
        ('makefile'                         , ''),
        ('mix.lock'                         , ''),
        ('node_modules'                     , ''),
        ('procfile'                         , ''),
        ('rakefile'                         , ''),
        ('react.jsx'                        , ''),
        ('robots.txt'                       , 'ﮧ'))

    file_node_pattern_matches = (
        (r'.*angular.*\.js$'      , ''),
        (r'.*backbone.*\.js$'     , ''),
        (r'.*jquery.*\.js$'       , ''),
        (r'.*materialize.*\.css$' , ''),
        (r'.*materialize.*\.js$'  , ''),
        (r'.*mootools.*\.js$'     , ''),
        (r'.*require.*\.js$'      , ''),
        (r'.*vimrc.*'             , ''),
        (r'Vagrantfile$'          , ''))

    file_node_extensions = (
        # Archives
        ('.bz2'         , ''),
        ('.bzip2'       , ''),
        ('.gz'          , ''),
        ('.gzip'        , ''),
        ('.lza'         , ''),
        ('.rar'         , ''),
        ('.tar'         , ''),
        ('.tgz'         , ''),
        ('.xz'          , ''),
        ('.zip'         , ''),

        ('.ai'          , ''),
        ('.awk'         , ''),
        ('.bash'        , ''),
        ('.bat'         , ''),
        ('.bmp'         , ''),
        ('.c'           , ''),
        ('.c++'         , ''),
        ('.cc'          , ''),
        ('.clj'         , ''),
        ('.cljc'        , ''),
        ('.cljs'        , ''),
        ('.coffee'      , ''),
        ('.conf'        , ''),
        ('.cp'          , ''),
        ('.cpp'         , ''),
        ('.cs'          , ''),
        ('.csh'         , ''),
        ('.css'         , ''),
        ('.cxx'         , ''),
        ('.d'           , ''),
        ('.dart'        , ''),
        ('.db'          , ''),
        ('.diff'        , ''),
        ('.dump'        , ''),
        ('.edn'         , ''),
        ('.eex'         , ''),
        ('.ejs'         , ''),
        ('.elm'         , ''),
        ('.erl'         , ''),
        ('.ex'          , ''),
        ('.exe'         , ''),
        ('.exs'         , ''),
        ('.f#'          , ''),
        ('.fish'        , ''),
        ('.fs'          , ''),
        ('.fsi'         , ''),
        ('.fsscript'    , ''),
        ('.fsx'         , ''),
        ('.gemspec'     , ''),
        ('.gif'         , ''),
        ('.go'          , ''),
        ('.h'           , ''),
        ('.haml'        , ''),
        ('.hbs'         , ''),
        ('.hh'          , ''),
        ('.hpp'         , ''),
        ('.hrl'         , ''),
        ('.hs'          , ''),
        ('.htm'         , ''),
        ('.html'        , ''),
        ('.hxx'         , ''),
        ('.ico'         , ''),
        ('.ini'         , ''),
        ('.java'        , ''),
        ('.jl'          , ''),
        ('.jpeg'        , ''),
        ('.jpg'         , ''),
        ('.js'          , ''),
        ('.json'        , ''),
        ('.jsx'         , ''),
        ('.ksh'         , ''),
        ('.leex'        , ''),
        ('.less'        , ''),
        ('.lhs'         , ''),
        ('.lua'         , ''),
        ('.markdown'    , ''),
        ('.md'          , ''),
        ('.mdx'         , ''),
        ('.mjs'         , ''),
        ('.mk'          , ''),
        ('.ml'          , 'λ'),
        ('.mli'         , 'λ'),
        ('.mustache'    , ''),
        ('.nix'         , ''),
        ('.pem'         , ''),
        ('.pdf'         , ''),
        ('.php'         , ''),
        ('.pl'          , ''),
        ('.pm'          , ''),
        ('.png'         , ''),
        ('.pp'          , ''),
        ('.ps1'         , ''),
        ('.psb'         , ''),
        ('.psd'         , ''),
        ('.py'          , ''),
        ('.pyc'         , ''),
        ('.pyd'         , ''),
        ('.pyo'         , ''),
        ('.r'           , 'ﳒ'),
        ('.rake'        , ''),
        ('.rb'          , ''),
        ('.rlib'        , ''),
        ('.rmd'         , ''),
        ('.rproj'       , '鉶'),
        ('.rs'          , ''),
        ('.rss'         , ''),
        ('.rst'         , ''),
        ('.sass'        , ''),
        ('.scala'       , ''),
        ('.scss'        , ''),
        ('.sh'          , ''),
        ('.slim'        , ''),
        ('.sln'         , ''),
        ('.sol'         , 'ﲹ'),
        ('.sql'         , ''),
        ('.styl'        , ''),
        ('.suo'         , ''),
        ('.svg'         , 'ﰟ'),
        ('.swift'       , ''),
        ('.t'           , ''),
        ('.tex'         , 'ﭨ'),
        ('.txt'         , ''),
        ('.toml'        , ''),
        ('.ts'          , ''),
        ('.tsx'         , ''),
        ('.twig'        , ''),
        ('.vim'         , ''),
        ('.vue'         , '﵂'),
        ('.webmanifest' , ''),
        ('.webp'        , ''),
        ('.xcplayground', ''),
        ('.xul'         , ''),
        ('.yaml'        , ''),
        ('.yml'         , ''),
        ('.zsh'         , ''))

    @staticmethod
    def getIcon(fileName):
        fileName = os.path.basename(str(fileName))

        fileName = fileName.lower()
        # Check the exact match
        for m, i in FileIcon.file_node_exact_matches:
          if m == fileName:
            return i

        # Check the pattern match
        for m, i in FileIcon.file_node_pattern_matches:
          if re.match(m,fileName):
            return i

        # Check the file extension
        for m, i in FileIcon.file_node_extensions:
          if fileName.endswith(m):
            return i

        return ''