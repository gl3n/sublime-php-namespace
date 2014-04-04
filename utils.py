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