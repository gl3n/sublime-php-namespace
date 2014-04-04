import sublime

from PhpNamespace.namespaces import *

def is_interface(view):
    return view.find('^interface', 0).begin() > 0

def is_class(view):
    return view.find('^(class|final|abstract)(.*)', 0).begin() > 0

def get_abstract_methods(view):
    regions = view.find_all('\n([ ]*)?abstract (.*) function [_a-zA-Z0-9]+\([_$a-zA-Z0-9, ]*\)', 0)
    returnedRegions = []
    for region in regions:
        print(region)
        returnedRegions.append(view.substr(region))
    return returnedRegions

def get_methods(view):
    regions = view.find_all('\n([ ]*)?public function [_a-zA-Z0-9]+\([_$a-zA-Z0-9, ]*\)', 0)
    returnedRegions = []
    for region in regions:
        returnedRegions.append(view.substr(region))
    return returnedRegions

def extend_class(view, edit, namespace):
    classname = namespace.split('\\')[-1]

    if view.find('extends ' + classname, 0):
        return

    extendRegion = view.find('extends (.*)', 0)
    if extendRegion:
        try:
            raise Exception
        except Exception as error:
            error.message = 'This class already extends another class'
            raise
    else:
        insert_use_statement(view, edit, namespace)
        implementsRegion = view.find('implements (.*)', 0)
        if implementsRegion:
            view.insert(edit, implementsRegion.begin(), 'extends ' + classname + ' ')
        else:
            classRegion = view.find('^(class|interface|final|abstract)(.*)', 0)
            view.insert(edit, classRegion.end(), ' extends ' + classname)

def implement_interface(view, edit, namespace):
    classname = namespace.split('\\')[-1]

    if view.find('implements (.*)' + classname, 0):
        return

    insert_use_statement(view, edit, namespace)
    implementsRegion = view.find('implements (.*)', 0)
    if implementsRegion:
        view.insert(edit, implementsRegion.end(), ', ' + classname)
    else:
        classRegion = view.find('^(class|interface|final|abstract)(.*)', 0)
        view.insert(edit, classRegion.end(), ' implements ' + classname)

def implement_methods(view, edit, methods):
    endRegion = view.find('^\}', 0)
    for method in methods:
        if view.find(method.strip(), 0, sublime.LITERAL).begin() < 0:
            view.insert(edit, endRegion.begin(), '\n\t/**\n\t * {@inheritdoc}\n\t */' + method + '\n\t{\n\t}\n')