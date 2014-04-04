import sublime, sublime_plugin, os

from PhpNamespace.utils import *
from PhpNamespace.namespaces import *
from PhpNamespace.classes import *

global currentView

class PhpNamespaceCopyCommand(sublime_plugin.WindowCommand):
    def run(self):
        if is_php_file(self.window.active_view()):
            sublime.set_clipboard(get_namespace(self.window))
            close_overlay(self.window, currentView)

class PhpNamespaceInsertUseCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        if is_php_file(currentView):
            namespace = get_namespace(currentView.window())
            close_overlay(currentView.window(), currentView)
            if is_php_file(currentView):
                insert_use_statement(currentView, edit, namespace)

class PhpNamespaceInsertNamespaceCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        if is_php_file(self.view):
            insert_namespace_statement(self.view, edit, build_namespace(self.view))

class PhpNamespaceCleanCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        if is_php_file(currentView):
            clean_namespaces(self.view, edit)

class PhpNamespaceExtendCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        panelView = currentView.window().active_view()
        if is_php_file(panelView):
            if is_class(panelView):
                methods = get_abstract_methods(currentView.window().active_view())
                namespace = get_namespace(currentView.window())
                if is_php_file(currentView):
                    close_overlay(currentView.window(), currentView)
                    try:
                        extend_class(currentView, edit, namespace)
                        implement_methods(currentView, edit, methods)
                    except Exception as error:
                        print(error.message)
                        sublime.error_message(error.message)

            if is_interface(panelView):
                methods = get_methods(currentView.window().active_view())
                namespace = get_namespace(currentView.window())
                if is_php_file(currentView):
                    close_overlay(currentView.window(), currentView)
                    implement_interface(currentView, edit, namespace)
                    implement_methods(currentView, edit, methods)

class PhpNamespaceEventListener(sublime_plugin.EventListener):
    def on_activated(self, view):
        global currentView
        if None != view.window():
            if is_file_opened(view.window(), view):
                currentView = view
