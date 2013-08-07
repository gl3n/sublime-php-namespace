import sublime, sublime_plugin, os

from PhpNamespace.namespaces import *

global currentView

class PhpNamespaceCopyCommand(sublime_plugin.WindowCommand):
    def run(self):
        if is_php_file(self.window.active_view()):
            sublime.set_clipboard(get_namespace(self.window))
            close_overlay(self.window, currentView)

class PhpNamespaceInsertUseCommand(sublime_plugin.WindowCommand):
    def run(self):
        if is_php_file(self.window.active_view()):
            namespace = get_namespace(self.window)
            close_overlay(self.window, currentView)
            if is_php_file(self.window.active_view()):
                insert_use_statement(self.window.active_view(), namespace)

class PhpNamespaceInsertNamespaceCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        if is_php_file(self.view):
            insert_namespace_statement(self.view, edit, build_namespace(self.view))

class PhpNamespaceEventListener(sublime_plugin.EventListener):
    def on_activated(self, view):
        global currentView
        if None != view.window():
            if is_file_opened(view.window(), view):
                currentView = view
