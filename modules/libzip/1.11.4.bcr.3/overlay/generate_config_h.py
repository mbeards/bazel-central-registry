import sys

def main():
    if len(sys.argv) < 3:
        print("Usage: generate_config_h.py <config.h.in> <config.h>")
        sys.exit(1)

    in_path = sys.argv[1]
    out_path = sys.argv[2]

    # Defines we want to enable for a standard Linux 64-bit build
    defines = {
        "HAVE_ARC4RANDOM": True,
        "HAVE_EXPLICIT_BZERO": True,
        "HAVE_FCHMOD": True,
        "HAVE_FILENO": True,
        "HAVE_FSEEKO": True,
        "HAVE_FTELLO": True,
        "HAVE_LOCALTIME_R": True,
        "HAVE_RANDOM": True,
        "HAVE_SNPRINTF": True,
        "HAVE_STRCASECMP": True,
        "HAVE_STRDUP": True,
        "HAVE_STRTOLL": True,
        "HAVE_STRTOULL": True,
        "HAVE_STDBOOL_H": True,
        "HAVE_STRINGS_H": True,
        "HAVE_UNISTD_H": True,
        "HAVE_FTS_H": True,
        "HAVE_FTS_OPEN": True,
        "HAVE_LIBBZ2": True,
        "HAVE_LIBLZMA": True,
        "HAVE_LIBZSTD": True,
        "SIZEOF_OFF_T": "8",
        "SIZEOF_SIZE_T": "8",
    }

    variables = {
        "${SIZEOF_OFF_T}": "8",
        "${SIZEOF_SIZE_T}": "8",
        "@CMAKE_PROJECT_NAME@": "libzip",
        "@CMAKE_PROJECT_VERSION@": "1.11.4",
    }

    with open(in_path, 'r') as f:
        lines = f.readlines()

    out_lines = []
    for line in lines:
        processed = False
        
        # Handle @VAR@ and ${VAR}
        for k, v in variables.items():
            if k in line:
                print("repl ", k, v)
                line = line.replace(k, v)
            if f"${{{k}}}" in line:
                print("esrepl ", k, v)
                line = line.replace(f"${{{k}}}", v)

        if line.startswith("#cmakedefine"):
            parts = line.split()
            if len(parts) >= 2:
                var = parts[1]
                if var in defines and defines[var]:
                    if len(parts) > 2:
                        # #cmakedefine VAR VALUE -> #define VAR VALUE
                        out_lines.append(f"#define {var} {' '.join(parts[2:])}\n")
                    else:
                        # #cmakedefine VAR -> #define VAR
                        out_lines.append(f"#define {var}\n")
                #elif var in variables:
                #    out_lines.append(f"#define {var} {variables[var]}\n")
                else:
                    # #cmakedefine VAR -> /* #undef VAR */
                    out_lines.append(f"/* #undef {var} */\n")
            processed = True
        
        if not processed:
            out_lines.append(line)

    with open(out_path, 'w') as f:
        f.writelines(out_lines)

if __name__ == "__main__":
    main()
