import sublime, os

def clean_namespaces(view, edit):
    minClassRegionChar = view.find('^(class|interface|trait|final|abstract) (.*)', 0).begin()
    useRegions = find_all_use_regions(view)
    for region in useRegions:
        classname = view.substr(region).split('\\')[-1].split(';')[0].split(' as ')[-1]
        if not view.find(classname, minClassRegionChar, sublime.LITERAL):
            view.erase(edit, view.full_line(region))

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

# Find all regions situate before class declaration
def find_all_use_regions(view):
    regions = view.find_all('^use (.*);', 0)
    # Detect first class or interface or trait
    minClassRegionChar = view.find('^(class|interface|trait|final|abstract)', 0).begin()
    returnedRegions = []
    for region in regions:
        # If region.begin is superior than minClassRegionChar, it mean that region is after class declaration
        if region.begin() < minClassRegionChar:
            returnedRegions.append(region)
    return returnedRegions

def insert_use_statement(view, edit, namespace):
    instruct = 'use '+ namespace +';'
    regions = find_all_use_regions(view)
    if 0 == len(regions):
        region = view.find('namespace (.*);', 0)
        region = view.full_line(region)
        text = view.substr(region)
        view.replace(edit, region, text + "\n" + instruct + "\n")
    else:
        alreadyExist = False
        for region in regions:
            text = view.substr(region)
            if text == instruct:
                alreadyExist = True
        if alreadyExist is False:
            region = regions[-1]
            text = view.substr(region)
            view.replace(edit, region, text +'\n'+ instruct)

def insert_namespace_statement(view, edit, namespace):
    if '' != namespace:
        full_namespace = "namespace " + namespace + ";"
        region = view.find('namespace (.*);', 0)
        if region is None or (region.a < 0 and region.b < 0):
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
