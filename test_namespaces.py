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
        view.file_name = Mock(return_value='test'+os.sep+'test.html')
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
    def testInsert_namespace_statemenWithoutPhpStatement(self):
        namespace = 'test1\\test2\\test3'
        sel = Mock()
        sel.begin = Mock(return_value=None)
        view = Mock()
        view.find = Mock(return_value=None)
        view.find_all = Mock(return_value=[])
        view.sel = Mock(return_value=[sel])
        insert_namespace_statement(view, None, namespace)
        view.insert.assert_called_once_with(None, unittest.mock.ANY, "namespace " + namespace + ";\n")
    def testInsert_namespace_statemenWithPhpStatement(self):
        namespace = 'test1\\test2\\test3'
        view = Mock()
        view.find_all = Mock(return_value=['0'])
        insert_namespace_statement(view, None, namespace)
        view.replace.assert_called_once_with(None, unittest.mock.ANY, "namespace " + namespace + ";")
if __name__ == "__main__":
    unittest.main()