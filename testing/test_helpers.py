import unittest 
from datetime import datetime
from tools.get_kaggle_dataset import _extract_dataset_slug, _create_error_response

class TestHelpers(unittest.TestCase):
    def test_extract_dataset_slug(self):
        self.assertEqual(_extract_dataset_slug("https://www.kaggle.com/datasets/user/dataset-name"), "user/dataset-name")
        self.assertEqual(_extract_dataset_slug("https://www.kaggle.com/datasets/user/dataset-name/"), "user/dataset-name")
        self.assertEqual(_extract_dataset_slug("https://www.kaggle.com/datasets/user/dataset-name?param=value"), "user/dataset-name")
        self.assertEqual(_extract_dataset_slug("https://www.kaggle.com/datasets/user/dataset-name/"), "user/dataset-name")

    def test_error_response_structure(self):
        """Test that error response has correct structure (keys only)"""
        result = _create_error_response("Error parsing dataset slug", "url_parsing")
        
        expected_keys = {"status", "error_message", "dataset_slug", 
                        "folder_path", "csv_files", "schemas", "metadata"}
        self.assertEqual(set(result.keys()), expected_keys)
        
        expected_metadata_keys = {"timestamp", "error_step"}
        self.assertEqual(set(result["metadata"].keys()), expected_metadata_keys)
        
   
        self.assertIsInstance(result["status"], str)
        self.assertIsInstance(result["error_message"], str)
        self.assertIsInstance(result["csv_files"], list)
        self.assertIsInstance(result["schemas"], dict)
        self.assertIsInstance(result["metadata"], dict)

if __name__ == '__main__':
    unittest.main()