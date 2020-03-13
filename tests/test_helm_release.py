import helmrelease
import os
import pytest
import re

META_PATTERN = re.compile(r"(?P<project>.+)/(?P<environment>.+)/(?P<cluster>.+)/releases/(?P<name>.+)\.yaml$")

PATTERN_SHA1_LONG = re.compile(r'^[0-9a-f]{40}$')
PATTERN_SHA1_SHORT = re.compile(r'^[0-9a-f]{8}$')

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
        'helm.fluxcd.io/v1',
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

@pytest.fixture
def valid_image_tag():
    return {
        'reaction-core-etl-consumer-inventory': PATTERN_SHA1_LONG,
        'reaction-core-etl-consumer-loyalty': PATTERN_SHA1_LONG,
        'reaction-core-etl-consumer-pricing': PATTERN_SHA1_LONG,
        'reaction-core-master-publisher': PATTERN_SHA1_LONG,
        'reaction-core-web': PATTERN_SHA1_LONG,
        'reaction-core-worker': PATTERN_SHA1_LONG,
        'reaction-storefront': PATTERN_SHA1_SHORT,
    }

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

    def test_loaded(self, path):
        assert self.path

    def test_namespace(self, path, valid_namespaces):
         assert self.yaml.namespace in valid_namespaces\
             or self.yaml.namespace == self.meta.environment

    def test_name(self, path):
        assert self.meta.basename == self.yaml.name

    def test_release_name(self, path):
        assert self.meta.basename == self.yaml.release_name

    def test_api_version(self, path, valid_api_versions):
        assert self.yaml.api_version in valid_api_versions

    def test_kind(self, path):
        assert self.yaml.kind == 'HelmRelease'

    def test_image_tag(self, path, valid_image_tag):
        pattern = valid_image_tag.get(self.yaml.name)
        try:
            image_tag = self.yaml.image_tag
        except KeyError:
            pytest.skip("Image.tag not defined.")

        if pattern is None:
            pytest.skip("Pattern for image.tag not defined.")

        assert pattern.match(image_tag) is not None, "Wrong image.tag specified."
