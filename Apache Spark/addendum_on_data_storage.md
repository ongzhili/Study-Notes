# Addendum on Data Storage

## Protocol Buffer vs JSON

Comparison between 2 data serialization formats.

### Protocol Buffer

Protobuf uses a binary format.

Requires schema in a `.proto` file. This file defines structure of data.
- Fields
- Type of field
    - Type safety is achieved here.
- Optional modifiers

1. Schema is defined
2. Protobuf compiler generates native language code
3. This generated code is used to:
    - Serialize (data -> binary)
    - Deserialize (binary -> data
4. Serialized data can be sent across a network / stored in a file

### JSON

JSON uses a text-based format
- Raw json is human-readable
- No type safety
    - Additional tooling required for validation

### Comparison

JSON tends to be slower and occupies more space than Protobuf.
However, the raw JSON is more human-readable.
- Easier to understand
- Easier to debug

We can consider Protobuf on applications that require this additional speed and efficiency
- Performance-critical applications
    - Real-time data processing
    - Large data volume data processing