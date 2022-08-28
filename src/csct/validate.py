import pathlib

import click
import yaml

@click.command(short_help="Validate dataset metadata and contents.")
@click.argument('dirs', nargs=-1, type=click.Path(exists=True, file_okay=False))
@click.option('-a', '--all', is_flag=True, help="Validate all dataset properties. [default]")
@click.option('-e', '--export', is_flag=True, help="Validate all dataset properties and attempt to export dataset.")
@click.option('-c', '--config', is_flag=True, help="Validate configuration settings.")
@click.option('-m', '--metadata', is_flag=True, help="Validate configuration settings and dataset metadata.")
@click.option('-s', '--structure', is_flag=True, help="Validate dataset subdirectory structure.")
@click.option('-f', '--files', is_flag=True, help="Validate dataset subdirectory structure and files.")
def validate(all, export, config, metadata, structure, files, dirs):
    """
    Validate dataset metadata, subdirectory structure, and contents of subdirectories and files.

    \b
    DIRS    Directories to recursively scan for datasets. 
            [default: current working directory]
    """
    import csct.common

    if not dirs: #default to cwd if no directories supplied
        click.echo("No directory paths supplied.  Searching for datasets in current working directory.")
        dirs = ['.']
    
    found_dirs = csct.common.find_directories(dirs)

    if all or (config == metadata == structure == files): #process flags
        config = True; metadata = True; structure = True; files = True
    
    for dir in found_dirs:
        if validate_single(config, metadata, structure, files, dir) and (config == metadata == structure == files) and export:
            export_single(dir)


def validate_single(config, metadata, structure, files, dir):
    click.echo(f"Validating dataset in path {dir}")

    validate_status = True
    
    if metadata:
        validate_status = validate_status * validate_metadata(dir)
    elif config:
        validate_status = validate_status * validate_config()
    
    if files:
        validate_status = validate_status * validate_files(dir)       
    elif structure:
        validate_status = validate_status * validate_structure(dir)

    return bool(validate_status)

def get_path_type(path):
    """
    Return the type of a supplied path.
    """
    if path.is_file():
        return 'file'
    elif path.is_dir():
        return 'directory'
    else:
        return 'other'

def validate_config():
    """
    Validate configuration settings.
    """

    import csct.common, csct.config, csct.schema, csct.validators

    click.echo("Validating configuration settings".ljust(csct.common.print_width, '.'), nl=False)

    validator = csct.validators.ConfigValidator(csct.schema.get_config_schema())
    validator.validate(csct.config.get_config())

    if validator.errors:
        click.secho("FAILED", fg='red')
        [click.secho(f"{key}: {value[0]}", fg='red') for key, value in validator.errors.items()]
        return False
    else:
        click.secho("PASSED", fg='green')
        return True

def validate_metadata(dir):
    """
    Validate dataset metadata.
    """

    import csct.common, csct.schema, csct.validators

    validate_config_status = validate_config()

    click.echo("Validating metadata".ljust(csct.common.print_width, '.'), nl=False)

    if not validate_config_status:
        click.secho("SKIPPED", fg='yellow')
        click.secho("Metadata validation requires validated configuration options.", fg='yellow')
        return False
    else:
        if (pathlib.Path(dir) / "atbrepo.yaml").exists() and (pathlib.Path(dir) / "atbrepo.yml").exists(): #check for duplicate metadata files
            click.secho("FAILED", fg='red')
            click.secho(f"Two metadata files found in path.  Only one metadata file per dataset is supported.", fg='red')
            return False
        else:
            metadata_path = pathlib.Path(dir) / "atbrepo.yaml" #check for this name first
            if not metadata_path.exists(): #if it's not there...
                metadata_path = pathlib.Path(dir) / "atbrepo.yml" #check for the alternative name
            try: 
                with open(metadata_path, "r") as c: #try to open the metadata file
                    metadata = yaml.safe_load(c)
            except: 
                click.secho("FAILED", fg='red')
                click.secho(f"Could not open metadata file in path {metadata_path}", fg='red')
                return False
        
        validator = csct.validators.MetadataValidator(csct.schema.get_metadata_schema())
        validator.validate(metadata)

        if validator.errors:
            click.secho("FAILED", fg='red')
            [click.secho(f"{key}: {value[0]}", fg='red') for key, value in validator.errors.items()]
            return False
        else:
            click.secho("PASSED", fg='green')
            return True   
           
def validate_structure(dir):
    """
    Validate dataset subdirectory structure.
    """

    import csct.common, csct.schema, csct.validators

    click.echo("Validating subdirectory structure".ljust(csct.common.print_width, '.'), nl=False)
    
    directory_structure = {}

    for subdir in pathlib.Path(dir).glob('*'):
        if subdir.exists() and str(subdir.name) not in ["atbrepo.yaml", "atbrepo.yml"]: 
            directory_structure[str(subdir.name)] = get_path_type(subdir)
          
    validator = csct.validators.DirectoryValidator(csct.schema.get_directory_structure_schema())
    validator.validate(directory_structure)

    if validator.errors:
        click.secho("FAILED", fg='red')
        [click.secho(f"{key}: {value[0]}", fg='red') for key, value in validator.errors.items()]
        return False
    else:
        click.secho("PASSED", fg='green')
        return True

def validate_files(dir):
    """
    Validate dataset files.
    """

    import csct.common, csct.schema, csct.validators

    validate_structure_status = validate_structure(dir)

    click.echo("Validating dataset files".ljust(csct.common.print_width, '.'), nl=False)

    if not validate_structure_status:
        click.secho("SKIPPED", fg='yellow')
        click.secho("Dataset file validation requires validated subdirectory structure.", fg='yellow')
        return False
    else: 
        
        directory_structure = {}

        for subdir in pathlib.Path(dir).glob('*'):
            if subdir.is_dir() and str(subdir.name) not in ["atbrepo.yaml", "atbrepo.yml"]: 
                directory_structure[str(subdir.name)] = {str(key): get_path_type(key) for key in pathlib.Path(subdir).glob('*')}     
        
        validator = csct.validators.DirectoryValidator(csct.schema.get_directory_contents_schema())
        validator.validate(directory_structure)

        if validator.errors:
            click.secho("FAILED", fg='red')
            [click.secho(f"{key}: {value[0]}", fg='red') for key, value in validator.errors.items()]
            return False
        else:
            click.secho("PASSED", fg='green')
            return True  

def export_single(dir):
    """
    Export dataset as archive.
    """
    import tarfile
    #import time

    from tqdm.auto import tqdm

    import csct.common
    from csct.config import get_config

    members = list(pathlib.Path(dir).glob('**/*'))

    export_path = get_config('export_path')

    tar_file = (pathlib.Path(export_path) / pathlib.Path(dir).stem).with_suffix(".tar.gz")

    try:
        with tarfile.open(tar_file, mode="w:gz") as tar:
            
            progress = tqdm(members, unit="files", bar_format='{bar:40}{percentage:3.0f}%  {desc}', ncols=80, leave=False)
            
            for member in progress:
                tar.add(member, arcname=str(member.relative_to(dir)))
                progress.set_description_str(f"Compressing {member.relative_to(dir)}")
                #time.sleep(0.5)
        #click.echo("\rExporting dataset".ljust(csct.common.print_width-1, '.'), nl=False)
        #click.secho("COMPLETE", fg='green')
        click.secho(f"Successfully exported dataset to {tar_file}", fg='green')    
    except:
        click.echo("\rExporting dataset".ljust(csct.common.print_width, '.'), nl=False)
        click.secho("FAILED", fg='red')