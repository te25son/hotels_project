from import_export.formats import base_formats


class SCSV(base_formats.CSV):
    """
    A format class to be used when importing csv data
    from the admin site to the models.

    This class is used to parse csv files which
    use the semicolon as their delimiter.
    """

    def get_title(self):
        """
        Display the class as 'csv'. The default
        csv class will be decativated when importing
        data.
        """
        return "csv"

    def create_dataset(self, in_stream, **kwargs):
        """
        Returns a csv dataset whereby the delimiter
        is a semicolon.
        """
        kwargs['delimiter'] = ';'
        return super().create_dataset(in_stream, **kwargs)


def return_preferred_import_formats(*args, **kwargs):
    """
    Returns a list of importable formats
    that can be selected when importing
    data from the admin.
    """

    formats = (
        SCSV,
    )
    return [f for f in formats if f().can_import()]
