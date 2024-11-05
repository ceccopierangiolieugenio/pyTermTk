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

   {% if TTkSignals or TTkSignalsForwarded %}
   :ref:`Signals <Signal and Slots>`
   ---------------------------------
   {% endif %}

   {% if TTkSignalsForwarded %}
   Signals linked to: :py:class:`{{ TTkSignalsForwarded['baseClass'] }}`

   .. autosummary::
   {% for item in TTkSignalsForwarded['signals'] %}
      {{ TTkSignalsForwarded['baseClass'] }}.{{ item }}
   {%- endfor %}

   {% if TTkSignals %}
   :py:class:`{{ objname }}` signals:
   {% endif %}
   {% endif %}

   {% if TTkSignals %}
   .. autosummary::
   {% for item in TTkSignals %}
      {{ item }}
   {%- endfor %}
   {% endif %}

   {% if TTkSlots or TTkSlotsInherited or TTkSlotsForwarded %}
   :ref:`Slots <Signal and Slots>`
   -------------------------------
   {% endif %}

   {% if TTkSlotsForwarded %}
   Slots linked to: :py:class:`{{ TTkSlotsForwarded['baseClass'] }}`

   .. autosummary::
   {% for item in TTkSlotsForwarded['methods'] %}
      {{ TTkSlotsForwarded['baseClass'] }}.{{ item }}
   {%- endfor %}

   {% if TTkSlots or TTkSlotsInherited %}
   :py:class:`{{ objname }}` slots:
   {% endif %}
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

   {% if TTkMethods or TTkMethodsInherited or TTkMethodsForwarded %}
   Methods
   -------
   {% endif %}

   {% if TTkMethodsForwarded %}
   Methods linked to: :py:class:`{{ TTkMethodsForwarded['baseClass'] }}`

   .. autosummary::
   {% for item in TTkMethodsForwarded['methods'] %}
      {{ TTkMethodsForwarded['baseClass'] }}.{{ item }}
   {%- endfor %}

   {% if TTkMethods or TTkMethodsInherited %}
   :py:class:`{{ objname }}` methods:
   {% endif %}
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


