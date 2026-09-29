import tempfile
import unittest
from pathlib import Path
from server import asset_path, models, safe_model_path


class AssetSafetyTests(unittest.TestCase):
    def test_only_declared_routes_are_exposed(self):
        with tempfile.TemporaryDirectory() as tmp:
            data = Path(tmp)
            for path in ['/../README.md', '/node_modules/', '/full-model.json', '/.env', '/unknown']:
                self.assertIsNone(asset_path(path, data))
            self.assertEqual(asset_path('/', data).name, 'viewer.html')

    def test_manifest_cannot_escape_data_directory(self):
        with tempfile.TemporaryDirectory() as tmp:
            parent = Path(tmp)
            data = parent / 'data'
            data.mkdir()
            outside = parent / 'private.ply'
            outside.write_bytes(b'private')
            self.assertIsNone(safe_model_path(data, '../private.ply'))
            self.assertIsNone(safe_model_path(data, str(outside)))
            inside = data / 'model.ply'
            inside.write_bytes(b'ply')
            self.assertEqual(safe_model_path(data, 'model.ply'), inside)

    def test_empty_data_lists_no_models(self):
        with tempfile.TemporaryDirectory() as tmp:
            self.assertEqual(models(Path(tmp)), [])


if __name__ == '__main__':
    unittest.main()
