def task_clean_junk():
    """Remove junk file"""
    return {
        # 'actions': [' %(dependencies)s %(targets)s'],
        'actions': ['rm -rdf $(find . | grep pycache)'],
        'clean': True,
    }
