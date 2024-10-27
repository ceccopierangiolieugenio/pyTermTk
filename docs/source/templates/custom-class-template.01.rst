{{ objname | escape | underline}}

Pippo CUSTOM_CLASS_TEMPLATE.001

.. currentmodule:: {{ module }}

.. autoclass:: {{ objname }}

   {% if TTkStyle %}
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

   {% if TTkSlots %}
   :ref:`Slots <Signal and Slots>`
   -------------------------------

   .. autosummary::
   {% for item in TTkSlots %}
      {{ item }}
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
