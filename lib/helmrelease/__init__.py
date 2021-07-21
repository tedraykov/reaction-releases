import dpath.util
import ruamel.yaml
import sys

class HelmReleaseItem(object):
    def __init__(self, key):
        self.key = key

    def __get__(self, instance, owner):
        return dpath.util.get(instance.data, self.key)

    def __set__(self, instance, value):
        dpath.util.set(instance.data, self.key, value)

class HelmRelease(object):
    api_version = HelmReleaseItem('/apiVersion')
    image_repository = HelmReleaseItem('/spec/values/image/repository')
    image_tag = HelmReleaseItem('/spec/values/image/tag')
    kind = HelmReleaseItem('/kind')
    name = HelmReleaseItem('/metadata/name')
    namespace = HelmReleaseItem('/metadata/namespace')
    release_name = HelmReleaseItem('/spec/releaseName')
    values = HelmReleaseItem('/spec/values')

    path = None
    separator = '/'

    def __init__(self, path, data):
        self.data = data
        self.path = path

    def __enter__(self):
        return self

    def __exit__(self, type, value, tb):
        return None

    def delete(self, key, separator=separator):
        try:
            dpath.util.delete(self.data, key, separator)
        except dpath.exceptions.PathNotFound:
            pass

    def dump(self):
        self.yaml.dump(self.data, sys.stdout)

    def get(self, key, separator=separator):
        return dpath.util.get(self.data, key, separator)

    def add(self, key, value, separator=separator):
        dpath.util.new(self.data, key, value, separator)

    def set(self, key, value, separator=separator):
        dpath.util.set(self.data, key, value, separator)

    def write(self):
        with open(self.path, 'w') as fp:
            self.yaml.dump(self.data, fp)

class HelmReleaseV2(HelmRelease):
    chart_path = HelmReleaseItem('/spec/chart/spec/chart')
    chart_source_ref_kind = HelmReleaseItem('/spec/chart/spec/sourceRef/kind')
    chart_source_ref_name = HelmReleaseItem('/spec/chart/spec/sourceRef/name')
    version = 'v2'

class HelmReleaseV1(HelmRelease):
    chart_git = HelmReleaseItem('/spec/chart/git')
    chart_name = HelmReleaseItem('/spec/chart/name')
    chart_path = HelmReleaseItem('/spec/chart/path')
    chart_ref = HelmReleaseItem('/spec/chart/ref')
    chart_repository = HelmReleaseItem('/spec/chart/repository')
    chart_version = HelmReleaseItem('/spec/chart/version')
    version = 'v1'

    path = None
    separator = '/'

def load(path):
    yaml = ruamel.yaml.YAML()
    yaml.indent(mapping=2, sequence=4, offset=2)
    yaml.preserve_quotes = True
    data = None

    with open(path, 'r') as stream:
        data = yaml.load(stream)

    api_version = data['apiVersion']
    if api_version == 'helm.fluxcd.io/v1':
        hr = HelmReleaseV1(path, data)
    elif api_version == 'helm.toolkit.fluxcd.io/v2beta1':
        hr = HelmReleaseV2(path, data)
    else:
        raise RuntimeError("Unsupported apiVersion: {}".format(api_version))

    return hr
