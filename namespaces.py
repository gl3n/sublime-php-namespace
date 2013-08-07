import os

def is_php_file(view):
    if view.file_name().endswith('.php'):
        return True
    return False

def is_file_opened(window, view):
    for wview in window.views():
        if wview.id() == view.id():
            return True
    return False

def close_overlay(window, currentView):
    if not is_file_opened(window, window.active_view()):
        window.run_command('close', [])
    else:
        window.focus_view(currentView)
    window.run_command('hide_overlay', [])

def get_namespace(window):
    rg = window.active_view().find('namespace (.*);', 0)
    snamespace = window.active_view().substr(rg)[10:][:-1]
    rg = window.active_view().find('\n([a-z ]+)?(class|interface|trait) [a-zA-Z0-9]+', 0)
    sclass = window.active_view().substr(rg)
    sclass = sclass[(sclass.rindex(' ')+1):]
    return snamespace+'\\'+sclass

def build_namespace(view):
    settings = view.settings()
    limits = settings.get('php_namespace.stop_folders')
    folders = view.file_name().split(os.sep)
    for limit in limits:
        if limit in folders:
            folders = folders[folders.index(limit):]
    return "\\".join(folders[1:-1])

def insert_use_statement(view, edit, namespace):
    instruct = 'use '+namespace+';'
    regions = view.find_all('\nuse (.*);', 0)
    if 0 == len(regions):
        region = view.find('namespace (.*);', 0)
        region = view.full_line(region)
        text = view.substr(region)
        view.replace(edit, region, text + "\n" + instruct + "\n")
    else:
        region = view.full_line(regions[-1])
        text = view.substr(region)
        view.replace(edit, region, text + instruct + "\n")

def insert_namespace_statement(view, edit, namespace):
    if '' != namespace:
        full_namespace = "namespace " + namespace + ";"
        region = view.find('namespace (.*);', 0)
        if region is None:
            regions = view.find_all('<\?php', 0)

            if 0 == len(regions):
                for sel in view.sel():
                    view.insert(edit, sel.begin(), full_namespace + "\n")
            else:
                region = view.line(regions[-1])
                view.insert(edit, region.end(), "\n\n" + full_namespace)
        else:
            region = view.line(region)
            view.replace(edit, region, full_namespace)
