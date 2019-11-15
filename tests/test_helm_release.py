import helmrelease
import os
import pytest
import re

META_PATTERN = re.compile(r"(?P<project>.+)/(?P<environment>.+)/(?P<cluster>.+)/releases/(?P<name>.+)\.yaml$")

def yaml_files():
    found = []
    for root, dirs, files in os.walk(os.getcwd()):
        for f in files:
            path = os.path.relpath(os.path.join(root, f))
            if root.endswith('/releases') and path.endswith('.yaml'):
                found.append(path)
    return found

@pytest.fixture
def valid_api_versions():
    return [
        'flux.weave.works/v1beta1',
    ]

@pytest.fixture
def valid_namespaces():
    return [
        'default',
        'kafka',
        'kube-system',
        'logging',
        'monitoring',
        'serverless',
    ]

class HelmReleaseMetadata(object):
    def __init__(self, path):
        abspath = os.path.abspath(path)
        try:
            meta = META_PATTERN.match(abspath).groupdict()
            self.environment = meta.get('environment')
            self.project = meta.get('project')
            self.cluster = meta.get('cluster')
            self.basename = meta.get('name')
        except AttributeError:
            self.error = True
            self.reason = "Failed to extract metadata from file path: {}. This usually means wrong location for the manifest file. ".format(abspath)
            return

@pytest.mark.parametrize("path", yaml_files())
class TestHelmReleaseSpec(object):
    @pytest.fixture(autouse=True)
    def loader(self, path):
        self.yaml = helmrelease.load(path)
        self.meta = HelmReleaseMetadata(path)
        self.path = path

    def test_loaded(self):
        assert self.path

    def test_namespace(self, valid_namespaces):
         assert self.yaml.namespace in valid_namespaces\
             or self.yaml.namespace == self.meta.environment

    def test_name(self):
        assert self.meta.basename == self.yaml.name

    def test_release_name(self):
        assert self.meta.basename == self.yaml.release_name

    def test_api_version(self, valid_api_versions):
        assert self.yaml.api_version in valid_api_versions

    def test_kind(self):
        assert self.yaml.kind == 'HelmRelease'
