import re
import sys

def main():
    if len(sys.argv) < 4:
        print("Usage: generate_zip_err_str.py <zip.h> <zipint.h> <output.c>")
        sys.exit(1)

    zip_h_path = sys.argv[1]
    zipint_h_path = sys.argv[2]
    output_path = sys.argv[3]

    with open(zip_h_path, 'r') as f:
        zip_h = f.read()

    with open(zipint_h_path, 'r') as f:
        zipint_h = f.read()

    # Regex from CMake: #define ZIP_ER_([A-Z0-9_]+) ([0-9]+)[ \t]+/([-*0-9a-zA-Z, ']*)/
    # The comment part contains the type and the description.
    error_regex = re.compile(r'#define\s+ZIP_ER_([A-Z0-9_]+)\s+([0-9]+)\s+/\*\s*([LNSZ]+)\s+([-*0-9a-zA-Z, \'\.]+)\s*\*/')
    
    # Detail regex: #define ZIP_ER_DETAIL_([A-Z0-9_]+) ([0-9]+)[ \t]+/([-*0-9a-zA-Z, ']*)/
    detail_regex = re.compile(r'#define\s+ZIP_ER_DETAIL_([A-Z0-9_]+)\s+([0-9]+)\s+/\*\s*([EG]+)\s+([-*0-9a-zA-Z, \'\.]+)\s*\*/')

    zip_err_str = [
        '/*',
        '  This file was generated automatically by generate_zip_err_str.py',
        '  from zip.h and zipint.h; make changes there.',
        '*/',
        '',
        '#include "zipint.h"',
        '',
        '#define L ZIP_ET_LIBZIP',
        '#define N ZIP_ET_NONE',
        '#define S ZIP_ET_SYS',
        '#define Z ZIP_ET_ZLIB',
        '',
        '#define E ZIP_DETAIL_ET_ENTRY',
        '#define G ZIP_DETAIL_ET_GLOBAL',
        '',
        'const struct _zip_err_info _zip_err_str[] = {'
    ]

    for match in error_regex.finditer(zip_h):
        name = match.group(1)
        # types = match.group(3) # Not used in output but matched
        code = match.group(3).strip()
        description = match.group(4).strip()
        #zip_err_str.append(f'    {{ {name}, "{description}" }},')
        zip_err_str.append(f'    {{ {code}, "{description}" }},')

    zip_err_str.append('};')
    zip_err_str.append('')
    zip_err_str.append('const int _zip_err_str_count = sizeof(_zip_err_str)/sizeof(_zip_err_str[0]);')
    zip_err_str.append('')
    zip_err_str.append('const struct _zip_err_info _zip_err_details[] = {')

    for match in detail_regex.finditer(zipint_h):
        name = match.group(1)
        types = match.group(3)
        description = match.group(4).strip()
        zip_err_str.append(f'    {{ {types}, "{description}" }},')

    zip_err_str.append('};')
    zip_err_str.append('')
    zip_err_str.append('const int _zip_err_details_count = sizeof(_zip_err_details)/sizeof(_zip_err_details[0]);')

    with open(output_path, 'w') as f:
        f.write('\n'.join(zip_err_str) + '\n')

if __name__ == "__main__":
    main()
