{{ fullname | escape | underline}}

Pippo CUSTOM_MODULE_TEMPLATE.001

.. automodule:: {{ fullname }}

   {% if TTkSubClasses %}
   .. rubric:: {{ _('Classes') }}

   .. autosummary::
      :caption: Classes:
      :toctree:
      :template: custom-class-template.01.rst

   {% for item in TTkSubClasses %}
      {{ item }}
   {%- endfor %}
   {% endif %}

{% if TTkSubModules %}
.. rubric:: Modules

.. autosummary::
   :toctree: Modules:
   :template: custom-module-template.01.rst
   :recursive:

{% for item in TTkSubModules %}
   {{ item }}
{%- endfor %}
{% endif %}
