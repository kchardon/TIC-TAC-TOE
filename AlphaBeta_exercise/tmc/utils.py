import importlib
import sys


# Used to load a module without a main method and if __name__ == "__main__": main()
# When loaded, runs the code immediatly
def load_module(pkg, lang='en'):
    module_not_found = 'File {0} does not exist!'.format(pkg)
    other_exception = 'Running exercise {0} failed. Please make sure that you can run your code.'.format(pkg)
    exit_called = 'Make sure your program does not exit with an exit() command.'

    if lang == 'fi':
        module_not_found = 'Tiedostoa {0} ei löytynyt.'.format(pkg)
        other_exception = 'Tehtävän {0} suorittaminen epäonnistui. '.format(pkg) \
            + 'Varmista, että saat ohjelman suoritettua loppuun.'
        exit_called = 'Varmista, että koodisi ei kutsu exit() komentoa.'

    try:
        return importlib.import_module(pkg)
    except ModuleNotFoundError:
        return AssertionError(module_not_found)
    except Exception:
        return AssertionError(other_exception)
    except SystemExit:
        return AssertionError(exit_called)


# Runs the module code again, used when no main() defined
def reload_module(module):
    if isinstance(module, AssertionError):
        raise module
    importlib.reload(module)


# Loads a method from a module, doesn't run the code, needs to be called in tests.
def load(pkg, method, lang='en', err=None):
    module_not_found = 'Function {1} was not found in file {0}.'.format(pkg, method)
    if lang == 'fi':
        module_not_found = 'Tiedostosta {0} ei löytynyt funktiota {1}.'.format(pkg, method)

    if not err:
        err = module_not_found

    def fail(*args, **kwargs):
        raise AssertionError(err)

    try:
        return getattr(importlib.import_module(pkg), method)
    except Exception:
        return fail


def get_stdout():
    return sys.stdout.getvalue().strip()


def get_stderr():
    return sys.stderr.getvalue().strip()


def any_contains(needle, haystacks):
    any(map(lambda haystack: needle in haystack, haystacks))


# patch_helper code copied from Data Analysis with Python tmc module
# Example:
# from tmc.utils import load, get_out, patch_helper

# module_name="src.file_listing"
# ph = patch_helper(module_name)
# In tests file, if you want to patch "src.file_listing.re.compile" use following:
# def test_content(self):
#   patch(ph('re.compile'), side_effect=re.compile) as c:
#       ...
class patch_helper(object):

    def __init__(self, module_name):
        import importlib
        self.m = module_name

    def __call__(self, d):
        # import importlib
        parts = d.split(".")
        # If e.g. d == package.subpackage.subpackage2.attribute,
        # and our module is called mystery_data.
        try:
            getattr(importlib.import_module(self.m), parts[-1])   # attribute
            p = ".".join([self.m, parts[-1]])
            # p='src.mystery_data.attribute'
        except ModuleNotFoundError:
            raise
        except AttributeError:
            if len(parts) == 1:
                raise
            try:
                getattr(importlib.import_module(self.m), parts[-2])  # subpackage2.attribute
                p = ".".join([self.m] + parts[-2:])
                # p='src.mystery_data.subpackage2.attribute'
            except AttributeError:
                if len(parts) == 2:
                    raise
                try:
                    getattr(importlib.import_module(self.m), parts[-3])  # subpackage.subpackage2.attribute
                    p = ".".join([self.m] + parts[-3:])
                    # p='src.mystery_date.subpackage.subpackage2.attribute'
                except AttributeError:
                    if len(parts) == 3:
                        raise
                    # package.subpackage.subpackage2.attribute
                    getattr(importlib.import_module(self.m), parts[-4])
                    p = ".".join([self.m] + parts[-4:])
                    # p='src.mystery_date.package.subpackage.subpackage2.attribute'
        return p
