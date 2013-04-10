import unittest
from unittest.mock import Mock
from namespaces import *

class namespaceTestCase(unittest.TestCase):
    def testIs_php_fileTrue(self):
        view = Mock()
        view.file_name = Mock(return_value='test.php')
        assert is_php_file(view) == True
    def testIs_php_fileFalse(self):
        view = Mock()
        view.file_name = Mock(return_value='test.html')
        assert is_php_file(view) == False
    def testGet_namespaceClass(self):
        view = Mock()
        view.find = Mock()
        view.substr = Mock(side_effect=['namespace test1\\test2;','class test3'])
        window = Mock()
        window.active_view = Mock(return_value=view)
        assert get_namespace(window) == 'test1\\test2\\test3'
    def testGet_namespaceInterface(self):
        view = Mock()
        view.find = Mock()
        view.substr = Mock(side_effect=['namespace test1\\test2\\test3;','interface test4'])
        window = Mock()
        window.active_view = Mock(return_value=view)
        assert get_namespace(window) == 'test1\\test2\\test3\\test4'
    def testBuild_namespace(self):
        file_path = ['folder1','folder2','src','folder3','folder4','test.php']
        settings = Mock()
        settings.get = Mock(return_value=['src','tests'])
        view = Mock()
        view.settings = Mock(return_value=settings)
        view.file_name = Mock(return_value=os.sep.join(file_path))
        assert build_namespace(view) == 'folder3\\folder4'

if __name__ == "__main__":
    unittest.main()