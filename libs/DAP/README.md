# Generate the new schema:
using [datamodel-code-generator](https://github.com/koxudaxi/datamodel-code-generator)
```bash
pip install datamodel-code-generator
```
ß
```bash
rm libs/DAP/debug_adapter_protocol.py
datamodel-codegen --input libs/DAP/debugAdapterProtocol.json --input-file-type jsonschema --output libs/DAP/debug_adapter_protocol.py --output-model-type pydantic_v2.BaseModel
```
or
```bash
rm libs/DAP/debug_adapter_protocol.py
datamodel-codegen --url https://microsoft.github.io/debug-adapter-protocol/debugAdapterProtocol.json --output libs/DAP/debug_adapter_protocol.py --output-model-type pydantic_v2.BaseModel
```