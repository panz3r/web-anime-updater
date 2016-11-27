import logging

from configs import DEBUG


def ex(e):
    """
    :param e: The exception to convert into a unicode string
    :return: A unicode string from the exception text if it exists
    """

    message = u''

    if not e or not e.args:
        return message

    for arg in e.args:
        if arg is not None:
            if isinstance(arg, (str, unicode)):
                fixed_arg = arg
            else:
                try:
                    fixed_arg = u'error {0}'.format(str(arg))
                except Exception:
                    fixed_arg = None

            if fixed_arg:
                if not message:
                    message = fixed_arg
                else:
                    try:
                        message = u'{0} : {1}'.format(message, fixed_arg)
                    except UnicodeError:
                        message = u'{0} : {1}'.format(
                            unicode(message, errors='replace'),
                            unicode(fixed_arg, errors='replace'))

    return message


def logger_setup(debug=True):
    logger = logging.getLogger()
    if debug:
        logger.setLevel(logging.DEBUG)
    else:
        logger.setLevel(logging.INFO)

    logging.basicConfig(format='[%(asctime)s] [%(levelname)-8s] %(message)s')

    return logger


class Episode:
    series = None
    title = None
    provider = None
    link = None

    def __init__(self):
        pass

    def __str__(self):
        return "{series: %s, title: %s, provider: %s, link: %s}" % (self.series, self.title, self.provider, self.link)

logger = logger_setup(DEBUG)
