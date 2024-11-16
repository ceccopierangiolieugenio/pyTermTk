{{ fullname | escape | underline}}

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
.. rubric:: {{ _('Modules') }}

.. autosummary::
   :toctree:
   :template: custom-module-template.01.rst
   :recursive:

{% for item in TTkSubModules %}
   {{ item }}
{%- endfor %}
{% endif %}
