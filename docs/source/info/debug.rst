=====
Debug
=====

------------------------------
Notes and tips about debugging
------------------------------


Env Variables
=============

There are few ENV Variables that can be used to force some debugging features;

**TERMTK_FILE_LOG** - Log to a file
---------------------------------

To force logging to a file (i.e. "**session.log**")

.. code:: bash

    TERMTK_FILE_LOG=session.log   python3   demo/demo.py


**TERMTK_STACKTRACE** - Force stacktrace generation with CTRL+C
--------------------------------------------------------------

Use this env variable to force a stacktrace generation to the file defined (i.e. "**stacktrace.txt**")

.. code:: bash

    TERMTK_STACKTRACE=stacktrace.txt   python3   demo/demo.py


Gui
===

`Visual Studio Code <https://code.visualstudio.com>`_
-----------------------------------------------------

vsCode debug feature comes out of the box, it only require the default `**Python** <https://marketplace.visualstudio.com/items?itemName=ms-python.python>`_ extension installed

.. image:: https://github.com/ceccopierangiolieugenio/pyTermTk/assets/8876552/00eab373-c347-45ab-8c40-0b023135946c
   :alt: vsCode debug

`intellij IDEA <https://www.jetbrains.com/help/idea/python.html>`_
---------------------------------------------------------------------------

I haven't tried it recently since my vsCode experience is silk smooth but based on the results of the `issue 102 <https://github.com/ceccopierangiolieugenio/pyTermTk/issues/102>`_ I am pretty confident that intellij debug feature should work as well

`PyCharm <https://www.jetbrains.com/pycharm/>`_
-----------------------------------------------

Same for PyCharm, I mean, I tried both those IDEs at least once.


Profiling
=========

`VizTracer <https://pypi.org/project/viztracer/>`_
--------------------------------------------------

.. image:: https://github.com/ceccopierangiolieugenio/pyTermTk/assets/8876552/34ff9b77-f01b-45bd-a57e-971c7b68c4a2

this tool is able to generate a tracker file that can be viewed using `Perfetto <https://perfetto.dev>`_ (`UI <https://ui.perfetto.dev/>`_)

.. code:: bash

    # install cprofilev:
    #     pip3 install viztracer
    viztracer --tracer_entries 10000010 tests/paint.py

    # View the results
    # loading the "result.json" in https://ui.perfetto.dev
    # or running
    vizviewer result.json


`cProfile <https://docs.python.org/3/library/profile.html>`_, `cProfilev <https://github.com/ymichael/cprofilev>`_
------------------------------------------------------------------------------------------------------------------


.. code:: bash

    python3 -m cProfile -o profiler.bin tests/test.ui.004.py

    # install cprofilev:
    #     pip3 install cprofilev
    cprofilev -f profiler.bin
    # open http://127.0.0.1:4000

`py-spy <https://github.com/benfred/py-spy>`_
---------------------------------------------

.. code:: bash

    # install
    pip install py-spy

    # run the application
    python3 demo/demo.py

    # on another terminal run the py-spy
    sudo env "PATH=$PATH" \
        py-spy top \
        --pid  $(ps -A -o pid,cmd | grep demo.py | grep -v grep | sed 's,python.*,,')

pyroscope
---------

`pyroscope <https://pyroscope.io/>`_ can be used as well (I guess) for profiling