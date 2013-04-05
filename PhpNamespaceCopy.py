import sublime, sublime_plugin

def is_php_file(window):
    if window.active_view().file_name().endswith('.php'):
        return True
    return False

def get_namespace(window):
    rg = window.active_view().find('namespace (.*);', 0)
    snamespace = window.active_view().substr(rg)[10:][:-1]
    rg = window.active_view().find('(class|interface) [a-zA-Z]+', 0)
    sclass = window.active_view().substr(rg)
    sclass = sclass[(sclass.index(' ')+1):]
    return snamespace+'\\'+sclass

def insert_use_statement(window, namespace):
    instruct = 'use '+namespace+';'
    sublime.set_clipboard(instruct)
    window.run_command('close_file', [])
    window.run_command('hide_overlay', [])
    if is_php_file(window):
        edit = window.active_view().begin_edit()
        regions = window.active_view().find_all('use (.*);', 0)
        if 0 == len(regions):
            region = window.active_view().find('namespace (.*);', 0)
            region = window.active_view().full_line(region)
            text = window.active_view().substr(region)
            window.active_view().replace(edit, region, text+"\n"+instruct+"\n")
        else:
            region = window.active_view().full_line(regions[-1])
            text = window.active_view().substr(region)
            window.active_view().replace(edit, region, text+instruct+"\n")

class PhpNamespaceCopyCommand(sublime_plugin.WindowCommand):
    def run(self):
        if is_php_file(self.window):
            sublime.set_clipboard(get_namespace(self.window))
            self.window.run_command('close_file', [])
            self.window.run_command('hide_overlay', [])

class PhpNamespaceInsertUseCommand(sublime_plugin.WindowCommand):
    def run(self):
        print "test"
        if is_php_file(self.window):
            insert_use_statement(self.window, get_namespace(self.window))