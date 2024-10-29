{{ objname | escape | underline }}

Pippo CUSTOM_CLASS_TEMPLATE.001

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
   Inherited from: :py:class:`{{ name }}`

   .. autosummary::

   {% for item in TTkSlotsInherited[name] %}
      {{ item }}
   {%- endfor %}

   {%- endfor %}

   {% endif %}

   {% if TTkSignals %}
   Members
   -------

   {% for item in TTkSignals %}
   .. autoattribute:: {{ item }}
   {%- endfor %}
   {% endif %}

   {% if TTkMethods %}
   Methods
   -------

   {% for item in TTkMethods %}
   .. automethod:: {{ item }}
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


