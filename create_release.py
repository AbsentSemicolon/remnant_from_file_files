import os
import zipfile

def create_zip_file(release):
    # convert to underscores
    new_release = release.replace('.', '_')


    zf = zipfile.ZipFile(f'remnant_from_the_files_v_{new_release}.zip', 'w')
    FILES = ['config.ini', 'license.md', 'main.py', 'print_statement.py', 'README.md', 'rem_config.py']

    for filename in FILES:
        zf.write(os.path.join('./', filename))

    zf.close()


if __name__ == '__main__':
    release = input('Release tag (#.#.#): ')
    create_zip_file(release)