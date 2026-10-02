import contextlib
import io
import json
import tempfile
import unittest
import zipfile
from pathlib import Path
from unittest.mock import patch

from scripts import practice_resources as resources
from scripts import validate_site_sources as validator


class PracticeResourceTests(unittest.TestCase):
    def make_package(self, root):
        source = root / 'source'
        for relative in ('README.md','data_dictionary.md','sources.md','exercises.md','outputs/README.md','scripts/demo.py'):
            target = source / relative
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text('# local practice\n',encoding='utf-8')
        (source/'bundle.json').write_text(json.dumps({'chapter':5,'title':'读取','version':'2026-10-02','entrypoints':['scripts/demo.py'],'encodings':{'data/raw/gb.csv':'gb18030'}}),encoding='utf-8')
        data = source/'data/raw/gb.csv'
        data.parent.mkdir(parents=True)
        data.write_text('编号,数值\n甲,0\n',encoding='gb18030',newline='\n')
        (source/'outputs/stale.csv').write_text('old result',encoding='utf-8')
        target=root/'docs/downloads/chapter-05-practice.zip'
        return source,target,resources.build_package(source,target)

    def test_package_keeps_declared_encoding_and_excludes_old_outputs(self):
        with tempfile.TemporaryDirectory() as temp:
            source,target,registration=self.make_package(Path(temp))
            manifest=resources.inspect_package(target,registration,validator.SENSITIVE_PATTERNS)
            names={row['path'] for row in manifest['files']}
            self.assertNotIn('outputs/stale.csv',names)
            self.assertIn('data/raw/gb.csv',names)
            # Independent reconstruction detects changed input after packaging.
            with zipfile.ZipFile(target) as archive:
                self.assertEqual(archive.read('data/raw/gb.csv').decode('gb18030'),'编号,数值\n甲,0\n')

    def test_unregistered_archive_and_changed_hash_are_rejected(self):
        with tempfile.TemporaryDirectory() as temp:
            root=Path(temp)
            source,target,registration=self.make_package(root)
            registry=target.parent/'registry.json'
            registry.write_text(json.dumps({'packages':[registration]}),encoding='utf-8')
            with patch.object(validator,'DOCS_ROOT',root/'docs'),patch.object(validator,'REPO_ROOT',root):
                validator.validate_practice_packages()
                (target.parent/'unknown.zip').write_bytes(target.read_bytes())
                with contextlib.redirect_stderr(io.StringIO()),self.assertRaises(SystemExit):
                    validator.validate_practice_packages()
                (target.parent/'unknown.zip').unlink()
                target.write_bytes(target.read_bytes()+b'changed')
                with contextlib.redirect_stderr(io.StringIO()),self.assertRaises(SystemExit):
                    validator.validate_practice_packages()

    def test_path_traversal_is_rejected_even_when_archive_hash_matches(self):
        with tempfile.TemporaryDirectory() as temp:
            source,target,registration=self.make_package(Path(temp))
            with zipfile.ZipFile(target,'a') as archive:
                archive.writestr('../escape.py','pass')
            registration['sha256']=resources.digest(target.read_bytes())
            with self.assertRaisesRegex(ValueError,'Unsafe ZIP member'):
                resources.inspect_package(target,registration)

    def test_sensitive_text_inside_archive_is_checked(self):
        with tempfile.TemporaryDirectory() as temp:
            source,target,registration=self.make_package(Path(temp))
            (source/'scripts/demo.py').write_text('address="192.168.1.23"',encoding='utf-8')
            registration=resources.build_package(source,target)
            with self.assertRaisesRegex(ValueError,'private IPv4'):
                resources.inspect_package(target,registration,validator.SENSITIVE_PATTERNS)

if __name__=='__main__':
    unittest.main()
