"""Build and inspect the registered, local student practice archives."""
from __future__ import annotations

import hashlib
import json
import re
import zipfile
from pathlib import Path, PurePosixPath

TEXT_SUFFIXES = {'.md', '.txt', '.csv', '.json', '.yml', '.yaml', '.py', '.r', '.tsv'}
ALLOWED_SUFFIXES = TEXT_SUFFIXES | {'.xlsx', '.png', '.svg', '.pdf', '.rds', '.mtx', '.gz', '.fasta', '.fa', '.fastq', '.fq', '.vcf'}


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def package_files(root: Path) -> list[Path]:
    selected = []
    for path in sorted(root.rglob('*')):
        if not path.is_file():
            continue
        relative = path.relative_to(root)
        if any(part.startswith('.') or part == '__pycache__' for part in relative.parts):
            continue
        if relative.parts[0] == 'outputs' and relative.as_posix() != 'outputs/README.md':
            continue
        if path.name == 'manifest.json':
            continue
        if path.suffix.lower() not in ALLOWED_SUFFIXES:
            raise ValueError(f'Unexpected student file: {relative}')
        if any(word in relative.as_posix() for word in ('教师', '答案', 'token', '.env')):
            raise ValueError(f'Teacher/private file in student package: {relative}')
        selected.append(path)
    return selected


def build_package(root: Path, destination: Path) -> dict:
    spec = json.loads((root / 'bundle.json').read_text(encoding='utf-8-sig'))
    files = package_files(root)
    relative_names = {p.relative_to(root).as_posix() for p in files}
    for required in ('README.md', 'data_dictionary.md', 'sources.md', 'exercises.md', 'outputs/README.md'):
        if required not in relative_names:
            raise ValueError(f'Missing {required} in chapter {spec["chapter"]}')
    for entry in spec['entrypoints']:
        if entry not in relative_names:
            raise ValueError(f'Missing entrypoint: {entry}')
    manifest = {**spec, 'files': [
        {'path': p.relative_to(root).as_posix(), 'size': p.stat().st_size, 'sha256': digest(p.read_bytes())}
        for p in files
    ]}
    destination.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(destination, 'w', compression=zipfile.ZIP_DEFLATED, compresslevel=9) as archive:
        for path in files:
            name = path.relative_to(root).as_posix()
            info = zipfile.ZipInfo(name, date_time=(2026, 10, 2, 0, 0, 0))
            info.compress_type = zipfile.ZIP_DEFLATED
            archive.writestr(info, path.read_bytes())
        archive.writestr('manifest.json', json.dumps(manifest, ensure_ascii=False, indent=2).encode('utf-8'))
    return {'chapter': spec['chapter'], 'title': spec['title'], 'version': spec['version'],
            'file': destination.name, 'sha256': digest(destination.read_bytes()), 'size': destination.stat().st_size,
            'entrypoints': spec['entrypoints']}


def inspect_package(path: Path, registration: dict, sensitive_patterns: dict | None = None) -> dict:
    if digest(path.read_bytes()) != registration['sha256']:
        raise ValueError(f'Archive hash mismatch: {path.name}')
    with zipfile.ZipFile(path) as archive:
        names = archive.namelist()
        if len(set(names)) != len(names):
            raise ValueError('Duplicate ZIP member')
        for name in names:
            member = PurePosixPath(name)
            if member.is_absolute() or '..' in member.parts or '\\' in name or ':' in name:
                raise ValueError(f'Unsafe ZIP member: {name}')
            if member.suffix.lower() not in ALLOWED_SUFFIXES:
                raise ValueError(f'Unexpected ZIP member type: {name}')
            if any(word in name for word in ('教师', '答案', 'token', '.env', '__pycache__')):
                raise ValueError(f'Private ZIP member: {name}')
        manifest = json.loads(archive.read('manifest.json').decode('utf-8'))
        if manifest['chapter'] != registration['chapter'] or manifest['version'] != registration['version']:
            raise ValueError('Registration/manifest mismatch')
        by_name = {row['path']: row for row in manifest['files']}
        if set(names) != set(by_name) | {'manifest.json'}:
            raise ValueError('Manifest does not cover all ZIP members')
        for name, row in by_name.items():
            data = archive.read(name)
            if len(data) != row['size'] or digest(data) != row['sha256']:
                raise ValueError(f'Member hash mismatch: {name}')
            if PurePosixPath(name).suffix.lower() in TEXT_SUFFIXES:
                encoding = manifest.get('encodings', {}).get(name, 'utf-8-sig')
                content = data.decode(encoding)
                for label, pattern in (sensitive_patterns or {}).items():
                    if pattern.search(content):
                        raise ValueError(f'{label} in ZIP member {name}')
        for entry in manifest['entrypoints']:
            if entry not in by_name:
                raise ValueError(f'Entrypoint absent from manifest: {entry}')
    return manifest


def load_registry(path: Path) -> dict:
    return json.loads(path.read_text(encoding='utf-8')) if path.exists() else {'packages': []}


def resource_index(titles: dict[int, str], registry: dict) -> str:
    packages = {p['chapter']: p for p in registry['packages']}
    lines = ['# 全书学生练习包', '', '下载对应章节的ZIP，解压后先读 `README.md`。输入保存在 `data/`，运行结果写入 `outputs/`。每个包的 `manifest.json` 列出版本、运行入口、编码与文件校验值。', '',
             f'已发布 {len(packages)} / 15 章；正文与练习包按批同步更新。', '',
             '| 章节 | 练习包 | 版本 | 大小 |', '| --- | --- | --- | --- |']
    for number, title in titles.items():
        p = packages.get(number)
        if p:
            link = f'[下载ZIP](../downloads/{p["file"]})'
            version, size = p['version'], f'{p["size"] / 1024:.0f} KB'
        else:
            link, version, size = '本批尚未发布', '待发布', '待发布'
        lines.append(f'| [第{number}章 {title}](../chapters/chapter-{number}/index.md) | {link} | {version} | {size} |')
    lines.extend(['', '前期练习以Python为主，R用于已有对照与适合的领域分析。RNA-seq、单细胞和进阶章节在README中区分实际运行入口、轻量练习与大型数据拓展。基础练习使用本地文件。', ''])
    return '\n'.join(lines)
