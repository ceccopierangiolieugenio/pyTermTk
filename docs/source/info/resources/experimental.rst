.. _experimental_features:

=====================
Experimental Features
=====================

PyTermTk provides several experimental features to enhance functionality and user interaction.
These features are not enabled by default and must be activated via environment variables.
Below is a list of the currently available experimental features.

.. _mouse_visual_feedback:

---------------------
Mouse Visual Feedback
---------------------

Enable mouse visual feedback glyph ('✠') in PyTermTk.

To enable this feature,
set the environment variable **TERMTK_MOUSE** to `1` and run your application:

.. code:: bash

    TERMTK_MOUSE=1  demo/demo.py

----------------------------------------------------------------------------
`GPM <https://wiki.archlinux.org/title/General_purpose_mouse>`__ Integration
----------------------------------------------------------------------------

`GPM <https://wiki.archlinux.org/title/General_purpose_mouse>`__ (General Purpose Mouse) support enables mouse interaction in Linux TTY environments without requiring a graphical user interface.

To activate GPM support, set the **TERMTK_GPM** environment variable to `1`:

.. code:: bash

    TERMTK_GPM=1  demo/demo.py

.. note::

    The :ref:`mouse_visual_feedback` is enabled my default when the GPM driver is loaded

.. note::

    GPM must be installed and running on your system for this feature to work.
    Install GPM using your system's package manager and ensure it is started with

    .. code:: bash

        sudo systemctl start gpm

.. seealso::

    * https://github.com/telmich/gpm
    * https://wiki.archlinux.org/title/General_purpose_mouse
    * https://www.geeksforgeeks.org/gpm-command-in-linux-with-examples

--------------
Serial Console
--------------

PyTermTk can detect the terminal size also on a serial console (i.e. ttyUSBx).

To force serial console compatibility,
set the **TERMTK_FORCESERIAL** environment variable to `1`:

.. code:: bash

    TERMTK_FORCESERIAL=1  demo/demo.py

--------------------
Feedback and Support
--------------------

Since these features are experimental,
they may not work as expected in all environments.
If you encounter issues or have suggestions,
please report them to the PyTermTk issue tracker or contribute to the project.
