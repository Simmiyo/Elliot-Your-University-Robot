import logging

logging.basicConfig(filename="./logs/interface.log",
                    filemode='a',   # append
                    level=logging.DEBUG,
                    format=' %(asctime)s - %(levelname)s - %(message)s',
                    )


logger = logging.getLogger(__name__)


def log_exception(e):
    if hasattr(e, "message"):
        logging.error("Exception raised {exception_class} ({exception_docstring}): {exception_message}".format(
            exception_class=e.__class__,
            exception_docstring=e.__doc__,
            exception_message=e.message))
    else:
        logger.error(e)
