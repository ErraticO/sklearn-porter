from sklearn_porter.language.LanguageABC import LanguageABC


class PHP(LanguageABC):
    KEY = 'php'
    LABEL = 'PHP'

    DEPENDENCIES = ['php']
    SUFFIX = 'php'

    CMD_COMPILE = None

    # php -f {} Estimator.php <args>
    CMD_EXECUTE = 'php -f {src_path}'

    # yapf: disable
    TEMPLATES = {
        'init':         '${{ name }} = {{ value }};',
        # if/else condition:
        'if':           'if ({{ a }} {{ op }} {{ b }}) {',
        'else':         '} else {',
        'endif':        '}',

        # Basics:
        'indent':       '    ',
        'join':         '; ',
        'type':         '{{ value }}',

        # Arrays:
        'in_brackets':  '[{{ value }}]',
        'arr[]':        '${{ name }} = [{{ values }}];',
        'arr[][]':      '${{ name }} = [{{ values }}];',
        'arr[][][]':    '${{ name }} = [{{ values }}];',

        # Primitive data types:
        'int':          '',
        'double':       ''
    }
    # yapf: enable
