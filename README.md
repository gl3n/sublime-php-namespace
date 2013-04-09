# Sublime2 PHP Namespace #

This package provides essential features for using **PHP Namespaces** with **SublimeText2**.

## Installation ##

Use git to install the package : move to your SublimeText2 Packages folder and then clone it.

<pre>
git clone https://github.com/gl3n/sublime-php-namespace PhpNamespace
</pre>

The package will be soon available via **Sublime Package Control**.

## Usage ##

Three commands are available :

- `php_namespace_copy` (via *Goto File Overlay*) : build the focused file namespace and copy it in the clipboard. (Default shortcut : `alt+c`)
- `php_namespace_insert_use` (via *Goto File Overlay*) : build the "use" statement of the focused file namespace and insert it on the last active file. (Default shortcut : `alt+u`)
- `php_namespace_insert_namespace` : build and insert the current file namespace. (Default shortcut : `alt+i`)

## Settings ##

<pre>
{
    "php_namespace.stop_folders": [
        "src",
        "workspace"
    ]
}
</pre>

The `php_namespace.stop_folders` setting is used for `php_namespace_insert_namespace` command. It defines the folders where the namespace building has to stop.