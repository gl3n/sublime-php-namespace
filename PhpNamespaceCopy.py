import sublime, sublime_plugin, os
from namespaces import *

class PhpNamespaceCopyCommand(sublime_plugin.WindowCommand):
    def run(self):
        if is_php_file(self.window.active_view()):
            sublime.set_clipboard(get_namespace(self.window))
            self.window.run_command('close_file', [])
            self.window.run_command('hide_overlay', [])

class PhpNamespaceInsertUseCommand(sublime_plugin.WindowCommand):
    def run(self):
        if is_php_file(self.window.active_view()):
            insert_use_statement(self.window, get_namespace(self.window))

class PhpNamespaceInsertNamespaceCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        if is_php_file(self.view):
            insert_namespace_statement(self.view, edit, build_namespace(self.view))