import sys

def main():
    if len(sys.argv) < 3:
        print("Usage: generate_zipconf_h.py <zipconf.h.in> <zipconf.h>")
        sys.exit(1)

    in_path = sys.argv[1]
    out_path = sys.argv[2]

    variables = {
        "${libzip_VERSION}": "1.11.4",
        "${libzip_VERSION_MAJOR}": "1",
        "${libzip_VERSION_MINOR}": "11",
        "${libzip_VERSION_PATCH}": "4",
        "${LIBZIP_TYPES_INCLUDE}": "#include <stdint.h>",
        "${ZIP_INT8_T}": "int8_t",
        "${ZIP_UINT8_T}": "uint8_t",
        "${ZIP_INT16_T}": "int16_t",
        "${ZIP_UINT16_T}": "uint16_t",
        "${ZIP_INT32_T}": "int32_t",
        "${ZIP_UINT32_T}": "uint32_t",
        "${ZIP_INT64_T}": "int64_t",
        "${ZIP_UINT64_T}": "uint64_t",
    }

    with open(in_path, 'r') as f:
        content = f.read()

    for k, v in variables.items():
        content = content.replace(k, v)

    # Handle #cmakedefine ZIP_STATIC
    # For a cc_library we'll assume not static by default in the config but 
    # for simplicity we'll just undefine it as it's optional.
    content = content.replace("#cmakedefine ZIP_STATIC", "/* #undef ZIP_STATIC */")

    with open(out_path, 'w') as f:
        f.write(content)

if __name__ == "__main__":
    main()
