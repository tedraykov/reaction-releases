import os
import pytest
import yaml

def yaml_files():
    found = []
    for root, dirs, files in os.walk(os.getcwd()):
        for f in files:
            path = os.path.relpath(os.path.join(root, f))
            if path.startswith('charts/') and path.find('/templates'):
                continue
            if path.endswith('.yaml'):
                found.append(path)
    return found

@pytest.mark.parametrize("path", yaml_files())
class TestYamlSyntax(object):
    def test_parser(self, path):
        try:
            with open(path, 'r') as stream:
                data =  yaml.safe_load_all(stream)
        except Exception as e:
            pytest.fail(str(e), pytrace=False)
