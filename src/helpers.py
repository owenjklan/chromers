import yaml


def client_select_menu(dlg, menu_choices):
    selected_clients = dlg.checklist(
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
