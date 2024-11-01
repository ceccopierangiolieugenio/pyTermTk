{{ objname | escape | underline }}

.. currentmodule:: {{ module }}

.. autoclass:: {{ objname }}
   :show-inheritance:

   {% if TTkStyle %}

   .. _{{ module }}.{{ objname }}.classStyle:

   Style
   -----

   .. code-block:: python

      {% for line in TTkStyle %}
      {{ line }}
      {%- endfor %}
   {% endif %}

   {% if TTkSignals %}
   :ref:`Signals <Signal and Slots>`
   ---------------------------------

   .. autosummary::
   {% for item in TTkSignals %}
      {{ item }}
   {%- endfor %}
   {% endif %}

   {% if TTkSlots or TTkSlotsInherited %}
   :ref:`Slots <Signal and Slots>`
   -------------------------------
   {% endif %}

   {% if TTkSlots %}
   .. autosummary::
   {% for item in TTkSlots %}
      {{ item }}
   {%- endfor %}
   {% endif %}

   {% if TTkSlotsInherited %}
   {% for name in TTkSlotsInherited %}
   {% if TTkSlotsInherited[name] %}
   Slots Inherited from: :py:class:`{{ name }}`

   .. autosummary::

   {% for item in TTkSlotsInherited[name] %}
      {{ item }}

   {%- endfor %}
   {% endif %}
   {%- endfor %}
   {% endif %}

   {% if TTkSignals %}
   Members
   -------

   {% for item in TTkSignals %}
   .. autoattribute:: {{ item }}
   {%- endfor %}
   {% endif %}

   {% if TTkMethods or TTkMethodsInherited %}
   Methods
   -------
   {% endif %}

   {% if TTkMethods %}

   {% for item in TTkMethods %}
   .. automethod:: {{ item }}
   {%- endfor %}

   {% endif %}

   {% if TTkMethodsInherited %}
   {% for name in TTkMethodsInherited %}
   {% if TTkMethodsInherited[name] %}
   Methods Inherited from: :py:class:`{{ name }}`

   .. autosummary::

   {% for item in TTkMethodsInherited[name] %}
      {{ item }}

   {%- endfor %}
   {% endif %}
   {%- endfor %}
   {% endif %}


{% if TTkClasses %}

{{ objname }} Classes
---------------------
{% for item in TTkClasses %}

.. currentmodule::  {{ module }}.{{ objname }}

.. autoclass::  {{ item }}
   :show-inheritance:
   :members:

{%- endfor %}
.. py:currentmodule::  {{ module }}
{% endif %}

{% if TTkAttributes %}

{{ objname }} Attributes
------------------------

.. currentmodule::  {{ module }}.{{ objname }}

.. autosummary::

{% for item in TTkAttributes %}
  {{ item }}
{%- endfor %}

.. currentmodule::  {{ module }}
{% endif %}


