

from py_basic_commands.json_scripts.read_json       import read_json
from py_basic_commands.json_scripts.write_json      import write_json



def prettify_json(file_path:str, indent:int=4, do_print:bool=True, encoding:str='utf-8', **kwargs) -> bool:
    """Prettify a JSON file.
    
    Parameters
    ----------
    file_path : str
        The path of the JSON file to prettify.
    indent : int, optional
        The number of spaces to use for indentation in the JSON file. Default is 4.
    do_print : bool, optional
        Whether to print information about the data writing process. Default is True.
    encoding : str, optional
        The encoding of the JSON file. Default is 'utf-8'.
        
    Returns
    -------
    bool
        Whether the file was prettified.
    """
    return write_json(
        read_json(
            file_path,
            do_print=do_print,
            encoding=encoding,
            **kwargs
        ),
        file_path,
        indent=indent,
        do_print=do_print,
        encoding=encoding,
        **kwargs
    )