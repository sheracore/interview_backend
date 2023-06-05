import importlib
import logging

logger = logging.getLogger(__name__)


def find_related_module(package, related_name):
    """Find module in package."""
    try:
        module = importlib.import_module(package)
        if not related_name and module:
            return module
    except ImportError:
        package, _, _ = package.rpartition('.')
        if not package:
            raise

    module_name = '{0}.{1}'.format(package, related_name)

    try:
        return importlib.import_module(module_name)
    except ImportError as e:
        import_exc_name = getattr(e, 'name', module_name)
        if import_exc_name is not None and import_exc_name != module_name:
            raise e
        return


def import_attribute(package, attribute, related_name=None):
    module = find_related_module(package, related_name)
    i_m = importlib.import_module(module.__name__)
    try:
        attr = getattr(i_m, attribute)
        return attr
    except AttributeError:
        logger.exception("Cant load attribute")
    return None