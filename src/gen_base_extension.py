#!/usr/bin/env python3
import json
import os

from jinja2 import Template

import click
from click import secho


# (<Template source file path>, <Human-description>, <output filename>)
TEMPLATES_LIST = [
    ("template_sets/manifest.json.j2", "JSON Manifest", "manifest.json"),
    ("template_sets/popup.html.j2", "Main popup HTML", "popup.html"),
    ("template_sets/popup.js.j2", "Main popup Javascript", "popup.js"),
]


def fail_if_missing_args(name, description, version):
    """
    If any of the supplied arguments are None, then a suitable error message
    is displayed and the program will exit. Note that all values are checked
    before exiting, to make a more thorough report in one go ;)
    """
    fail = False

    if name is None:
        fail = True
        secho("A plugin name must be provided! "
              "Use the --name/-n 'option'", fg="red", err=True)
    if description is None:
        fail = True
        secho("A plugin description must be provided! "
              "Use the --description/-d 'option'", fg="red", err=True)
    if version is None:
        fail = True
        secho("A plugin version string must be provided! "
              "Use the --version/-v 'option'", fg="red", err=True)

    if fail is True:
        secho("Aborting", err=True)
        exit(1)


# Despite being mandatory, we'll use click.option() so that users must
# provide the long-option names for command-lines, in an effort to make
# invocations more self-documenting, in a hopefully-useful way.
@click.command()
@click.option("--name", "-n", "plugin_name",
              type=str, metavar="NAME",
              default=None, show_default=False,
              help=("Specify the Human-friendly name for the new plugin."))
@click.option("--description", "-d", "plugin_description",
              type=str, metavar="DESCRIPTION",
              default=None, show_default=False,
              help=("Specify the descriptive text for the new plugin."))
@click.option("--version", "-v", "plugin_version",
              type=str, metavar="VERSION",
              default=None, show_default=False,
              help=("Specify the initial version string for the new plugin."))
@click.option("--output-dir", "-o", "output_dir",
              type=str, metavar="OUTPUT_DIR",
              default=".", show_default=True,
              help=("Specify the base directory to write generated files to."))
@click.option("--add-permission", "-p", "permissions_list",
              type=str, metavar="PERMISSION_NAME",
              default=[], show_default=False,
              help=("Specify the list of permissions this extension will "
                    "require."))
def main(plugin_name, plugin_description, plugin_version, output_dir,
         permissions_list):
    """
    Generate the basic files and directory structure for creating a minimal-
    functionality but mostly-complete Chrome extension that can be loaded
    locally.

    Note that despite the "options" all being essentially mandatory, this is
    a deliberate choice. Use of the long option names makes invocations of
    this command more self-documenting. That is the hope, anyway.
    """

    fail_if_missing_args(plugin_name, plugin_description, plugin_version)

    plugin_manifest_details = {
        "name": plugin_name,
        "description": plugin_description,
        "version": plugin_version,
    }

    # Load templates
    for current_template in TEMPLATES_LIST:
        loaded_template = Template(
            open(current_template[0], 'r').read().strip(),
        )
        current_output = loaded_template.render(
            permissions_list=permissions_list,
            plugin=plugin_manifest_details
        )

        output_path = os.path.join(output_dir, current_template[2])
        secho(f"Path: {output_path}")
        with open(output_path, "w") as output_file:
            output_file.write(current_output)
            secho(f"Wrote {len(current_output)} bytes to {output_file.name}.",
                  fg="green")


if __name__ == "__main__":
    main()
