from sklearn_porter.language.LanguageABC import LanguageABC


class Go(LanguageABC):
    KEY = 'go'
    LABEL = 'Go'

    DEPENDENCIES = ['go']
    SUFFIX = 'go'

    # go build -o tmp/estimator tmp/estimator.go
    CMD_COMPILE = 'go build -o {dest_path} {src_path}'

    # tmp/estimator <args>
    CMD_EXECUTE = '{dest_path}'

    # yapf: disable
    TEMPLATES = {
        'init':         '{{ name }} := {{ value }}',

        # if/else condition:
        'if':           'if {{ a }} {{ op }} {{ b }} {',
        'else':         '} else {',
        'endif':        '}',

        # Basics:
        'indent':       '\t',
        'join':         '',
        'type':         '{0}',

        # Arrays:
        'in_brackets':  '{{ "{" }}{{ value }}{{ "}" }}',
        # ages := []int {1, 2}
        'arr[]':        '{{ name }} := []{{ type }} {{ "{" }}{{ values }}{{ "}" }}',  # pylint: disable=line-too-long
        'arr[][]':      '{{ name }} := [][]{{ type }} {{ "{" }}{{ values }}{{ "}" }}',  # pylint: disable=line-too-long
        'arr[][][]':    '{{ name }} := [][][]{{ type }} {{ "{" }}{{ values }}{{ "}" }}',  # pylint: disable=line-too-long

        # Primitive data types:
        'int':          'int',
        'double':       'float64'
    }
    # yapf: enable
