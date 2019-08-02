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

class HelmRelease():
    api_version = HelmReleaseItem('/apiVersion')
    chart_git = HelmReleaseItem('/spec/chart/git')
    chart_name = HelmReleaseItem('/spec/chart/name')
    chart_path = HelmReleaseItem('/spec/chart/path')
    chart_ref = HelmReleaseItem('/spec/chart/ref')
    chart_repository = HelmReleaseItem('/spec/chart/repository')
    chart_version = HelmReleaseItem('/spec/chart/version')
    image_repository = HelmReleaseItem('/spec/values/image/repository')
    image_tag = HelmReleaseItem('/spec/values/image/tag')
    kind = HelmReleaseItem('/kind')
    name = HelmReleaseItem('/metadata/name')
    namespace = HelmReleaseItem('/metadata/namespace')
    release_name = HelmReleaseItem('/spec/releaseName')

    path = None
    separator = '/'
    yaml = ruamel.yaml.YAML()

    def __init__(self, path):
        self.path = path
        self.yaml.indent(mapping=2, sequence=4, offset=2)
        self.yaml.preserve_quotes = True
        with open(path, 'r') as stream:
            self.data = self.yaml.load(stream)

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

def load(path):
    return HelmRelease(path)
