def remove_www(hostname):
    """
        Removes www. from the beginning of the address. Only for
            routing purposes. www.test.com/login/ and test.com/login/ should
                find the same tenant.
    """
    if hostname.startswith("www."):
        return hostname[4:]

    return hostname
    """
    """
