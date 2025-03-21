"""
Provide an entrypoint for configuring development tooling to make life easier
"""

from decouple import config

from app.environments import is_production, is_staging


def configure_debugging():
    if is_production() or is_staging():
        return

    # TODO can we prevent rich from installing syshook?
    # TODO can we detect if excepthook has been mutated?
    # if sys.excepthook != sys.__excepthook__:
    #     raise RuntimeError("sys.excepthook has been overridden.")
    #
    #     print(
    #         f"sys.excepthook has been overridden by {sys.excepthook.__module__}.{sys.excepthook.__qualname__}"
    #     )
    #     print(
    #         f"Source: {getattr(sys.excepthook, '__code__', None) and sys.excepthook.__code__.co_filename}:{getattr(sys.excepthook, '__code__', None) and sys.excepthook.__code__.co_firstlineno}"
    #     )

    try:
        import pretty_traceback

        pretty_traceback.install(
            local_stack_only=config(
                "PRETTY_TRACEBACK_LOCAL_ONLY", default=False, cast=bool
            )
        )
    except ImportError:
        pass

    if config("PYTHON_DEBUG_TRAPS", default=False, cast=bool):
        from app.utils.debug import install_traps

        install_traps()
