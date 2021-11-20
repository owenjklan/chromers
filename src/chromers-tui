#!/usr/bin/env python3
import os
import base64
import textwrap
import time

import yaml
import sys

from jinja2 import Template

from dialog import Dialog

from templates.available import SWITCH_FLAGS


client_specs = {}


def get_random_prefix(size=8):
    """
    Generate random bytes and take a base64-like representation for
    random prefix suggestion.
    """
    rand_bytes = os.urandom(size)
    rand_str = base64.b64encode(rand_bytes).decode('ascii')
    rand_str = rand_str.replace("+", "_")
    rand_str = rand_str.replace("/", "_")
    rand_str = rand_str.split('=', 1)[0]
    return rand_str


def switch_flags_menu(d):
    menu_options = []
    for flag_var, flag_meta in SWITCH_FLAGS.items():
        menu_options.append((flag_meta['var_name'], flag_meta['help'], False))
    selected_switches = d.checklist(
        ("Select optional 'switch flags' to include. Switch flags essentially"
         " enable a feature if they are present."),
        choices=menu_options,
        title=" Select common 'switch' flags ",
        width=60,
        list_height=5,
        height=12,
        backtitle="Click Cookie-Cutter",
    )
    return selected_switches


def client_select_menu(d, menu_choices):
    selected_clients = d.checklist(
        ("Select API Clients to add to the generated script."),
        choices=menu_choices,
        title=" Select included clients ",
        width=70,
        backtitle="Click Cookie-Cutter",
    )
    return selected_clients


def load_client_spec_yamls():
    client_choices_menu = []
    base_dir = "client_specs"
    files = os.listdir(base_dir)
    yaml_files = [f for f in files if f.endswith(".yml") or f.endswith(".yaml")]

    for yaml_file in yaml_files:
        yaml_path = os.path.join(base_dir, yaml_file)
        with open(yaml_path, "r") as yaml_file_obj:
            info = yaml.load(yaml_file_obj, Loader=yaml.Loader)
            client_specs[info['short_name']] = info

        client_choices_menu.append(
            (info['short_name'], info['description'], False, )
        )

    return client_choices_menu


def get_default_for_option(d, opt):
    use_default = d.yesno(
        f"Would you like to provide a default for:\n{opt['varname']} (type: {opt['type']})",
        title=" Specify Default? ",
        width="60",
        height=7,
        backtitle="Click Cookie-Cutter",
    )
    if use_default == d.OK:
        status, default_value = d.inputbox(
            f"Default for: {opt['varname']}",
            title="Enter Default value",
            height=7,
            width=40,
            backtitle="Click Cookie-Cutter",
        )
        return default_value, True  # Force  show_default=True
    else:
        return None, None


def wrap_main_args(main_args_list):
    ma = ", ".join(main_args_list)
    wrapped = textwrap.wrap(ma, subsequent_indent="         ", width=70,
                            break_on_hyphens=False, break_long_words=False)
    return "\n".join(wrapped)


def main():
    d = Dialog(dialog="dialog")

    status, script_name = d.inputbox("Name of script")

    envvar_file = {}

    main_args = []  # Args that will go into generated scripts' main()
                    # signature
    # These will generate the options in click script, based on the options
    # defined for the client specifications we choose in the beginning menu.
    client_args_list = []

    # Load available CLient specifications
    client_choices_menu = load_client_spec_yamls()

    # Get list of client spec 'short_name' values using Dialog menu
    status, selected_clients = client_select_menu(d, client_choices_menu)
    if status != 'ok':
        print("\nAborted on client selection!\n")
        sys.exit(1)

    imports_list = []
    instance_templates = []
    for client in selected_clients:
        current_client = client_specs[client]  # by shortname
        if "instance_template" in current_client:
            instance_templates.append(current_client['instance_template'])
        option_varnames = [opt['varname'] for opt in current_client['options']]
        main_args.extend(option_varnames)
        client_args_list.extend(current_client['options'])

        if "imports" in current_client:
            imports_list.extend(current_client['imports'])
            print(f"Added imports for {current_client['name']}: {current_client['imports']}")

        # While we have an options list, ask for defaults for each option
        for opt in current_client['options']:
            default, show_default = get_default_for_option(d, opt)
            opt['default'] = default


    # Get prefix for all environment variables
    status, entered_prefix = d.inputbox(
        "Environment variables prefix",
        init=get_random_prefix()
    )

    # Display optional selection for "switch flags" that are commonly useful
    status, chosen_switches = switch_flags_menu(d)

    if status != 'ok':
        print("\nAborted on Switch Flags selection\n")
        sys.exit(1)

    switch_flags = [SWITCH_FLAGS[switch] for switch in chosen_switches]
    main_args.extend(chosen_switches)
    script_template = Template(
        open('templates/base_script.j2', 'r').read().strip(),
    )

    wrapped_main_args = wrap_main_args(main_args)

    output = script_template.render(
        switch_flags=switch_flags,
        main_args=main_args,
        wrapped_main_args=wrapped_main_args,
        instance_templates=instance_templates,
        prefix=entered_prefix,
        client_args_list=client_args_list,
        imports_list=imports_list,
        app_title=script_name,
    )

    with open(f"output/{script_name}", "w") as output_script:
        output_script.write(output)


if __name__ == "__main__":
    main()
