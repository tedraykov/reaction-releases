import git
import helm_release
import os
import pytest
import subprocess
import tempfile
import ruamel.yaml
import pathlib
from pprint import pprint

api_versions = 'monitoring.coreos.com/v1'
charts_dir = 'charts'
releases_dir = 'sdi-*/*/application'
target_branch = 'origin/develop'
target_repository_url = git.Repo().remotes.origin.url
target_repository_name = os.path.splitext(os.path.basename(target_repository_url))[0]

def diff(match):
    repo = git.Repo()
    sha1 = repo.merge_base(target_branch, 'HEAD')[0]
    retval = repo.git.diff(sha1, match, name_only=True, find_renames=True).split()
    return retval

def helm_template(path, name, values):
    retval = subprocess.run(['helm', 'template', name, path, '-a', api_versions, '-f', values ])
    return retval

def releases_by_chart_path(chart_path):
    retval = []
    for root, dirs, files in os.walk(releases_dir):
        for f in files:
            path = os.path.relpath(os.path.join(root, f))
            if not path.endswith('.yaml'):
                continue

            yaml = helmrelease.load(path)
            if yaml.chart_path == chart_path:
                retval.append(path)
    return retval

yaml_files = diff(releases_dir)
for chart in diff(charts_dir):
    path = pathlib.Path(chart).relative_to(charts_dir).parts[0]
    path = "{}/{}".format(charts_dir, path)
    releases = releases_by_chart_path(path)
    yaml_files = yaml_files + releases

yaml_files = list(set(yaml_files))

@pytest.mark.skipif(len(yaml_files) == 0, reason="no changes detected")
@pytest.mark.parametrize("path", yaml_files)
class TestHelmTemplate(object):
    @pytest.fixture(autouse=True)
    def autoloader(self, path):
        self.yaml = helmrelease.load(path)
        pprint(self.yaml.data)
        assert self.yaml is not None, "HelmRelease: not loaded"
        assert self.yaml.version, "HelmRelease: apiVersion not detected"

    def test_chart_compilation(self, path):
        chart_path = self.yaml.chart_path
        chart_git = self.yaml.chart_git

        yaml = ruamel.yaml.YAML()
        with self.yaml as hr:
            with tempfile.NamedTemporaryFile(delete=False, suffix='.yaml') as tmpfile:
                yaml.dump(hr.values, tmpfile)
                tmpfile.close()

            if hr.version == 'v1':
                if hr.chart_git != target_repository_url:
                    pytest.skip("Unrecognized repository url")

            if hr.version == 'v2':
                if hr.chart_source_ref_kind != 'GitRepository':
                    pytest.skip("Chart source is not a git repository")

                if hr.chart_source_ref_name != target_repository_name:
                    pytest.skip("Unrecognized repository name: {} - {}".format(hr.chart_source_ref_name, target_repository_name))

            result = helm_template(hr.chart_path, hr.release_name, tmpfile.name)
            assert result.returncode == 0, "The chart failed to compile"
