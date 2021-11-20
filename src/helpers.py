import os
import yaml


def get_template_set_directories(base_dir):
    """
    Get only directories that are present under provided base directory
    """
    all_files = os.listdir(base_dir)

    # Filterout non-directories
    sub_directory_names = []
    for filename in all_files:
        abs_filename = os.path.join(base_dir, filename)
        if os.path.isdir(abs_filename):
            sub_directory_names.append(abs_filename)
    return sub_directory_names


def load_template_sets_yamls(base_dir):
    template_sub_dirs = get_template_set_directories(base_dir)

    # Ensure we have a valid 'config.yaml' in each found directory. Also do
    # some basic validations on what's found in the YAML and file structure.
    valid_template_sets = []
    template_errors = []

    for template_dir in template_sub_dirs:
        config_path = os.path.join(template_dir, "config.yaml")
        try:
            with open(config_path, "r") as config_yaml_file:
                config_object = yaml.load(config_yaml_file, yaml.Loader)
                valid_template_sets.append((template_dir, config_object))
        except FileNotFoundError as fnfe:
            error_msg = "config.yaml file missing from '{}'".format(
                os.path.basename(template_dir)
            )
            template_errors.append(error_msg)

    # display errors?
    for err_num, err in enumerate(template_errors):
        print(f"#{err_num + 1}: {err}")

    return valid_template_sets, template_errors