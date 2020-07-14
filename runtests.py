import sys


def convert_settings():
    from tests import settings
    settings_dict = {}

    for x in dir(settings):
        if not x.startswith("_"):
            if x.upper() == x:
                if x not in ["APP_NAME", "APP_DIR"]:
                    settings_dict[x] = getattr(settings, x)

    return settings_dict


def run_tests():
    import django

    from django.conf import settings as settings
    from django.test.utils import get_runner

    settings.configure(**convert_settings())
    django.setup()
    runner = get_runner(settings)

    test_runner = runner(verbosity=2, interactive=True)
    failures = test_runner.run_tests(["tests"])
    sys.exit(bool(failures))


if __name__ == "__main__":
    run_tests()
