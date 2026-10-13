from pathlib import Path

def test_required_files_exist():
    for p in ['README.md','EVIDENCE.md','BUILDLOG.md','.env.example','capstone.yaml','docker-compose.yml','static/widget.js']:
        assert Path(p).exists(), p

def test_widget_is_versioned():
    text=Path('app/main.py').read_text()
    assert 'max-age=31536000' in text
