import os


def folder_in_project(project_folder='data_files'):
    """ Return folder path in project.  Default return the data_files folder in project."""
    project_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    project_folder = os.path.join(project_path, project_folder)

    return project_folder


def list_files(path, endpoint=None):
    return [f_name for f_name in os.listdir(path) if os.path.isfile(os.path.join(path, f_name)) and f_name.endswith(endpoint)]
