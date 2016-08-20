'''
    File used to insert utility or support method used in many part of code
'''

def sizeof_fmt(num, suffix='B'):
    '''
        Format a size of file in human readable
    '''
    for unit in ['','Ki','Mi','Gi','Ti','Pi','Ei','Zi']:
        if abs(num) < 1024.0:
            return "%3.1f%s%s" % (num, unit, suffix)
        num /= 1024.0
    return "%.1f%s%s" % (num, 'Yi', suffix)
