import os

def is_php_file(view):
    if view.file_name().endswith('.php'):
        return True
    return False

def get_namespace(window):
    rg = window.active_view().find('namespace (.*);', 0)
    snamespace = window.active_view().substr(rg)[10:][:-1]
    rg = window.active_view().find('\n(class|interface) [a-zA-Z]+', 0)
    sclass = window.active_view().substr(rg)
    sclass = sclass[(sclass.index(' ')+1):]
    return snamespace+'\\'+sclass

def build_namespace(view):
    settings = view.settings()
    limits = settings.get('php_namespace.stop_folders')
    folders = view.file_name().split(os.sep)
    for limit in limits:
        if limit in folders:
            folders = folders[folders.index(limit):]
    return "\\".join(folders[1:-1])
    
def insert_use_statement(window, namespace):
    instruct = 'use '+namespace+';'
    window.run_command('close_file', [])
    window.run_command('hide_overlay', [])
    if is_php_file(window.active_view()):
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

def insert_namespace_statement(view, edit, namespace):
    if '' != namespace:
        full_namespace = "namespace " + namespace + ";\n"
        regions = view.find_all('<\?php', 0)
        if 0 == len(regions):
            for sel in view.sel():
                view.insert(edit, sel.begin(), full_namespace)
        else:
            region = view.line(regions[-1])
            view.insert(edit, region.end(), "\n"+full_namespace)