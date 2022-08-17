import os
import shutil
from argparse import ArgumentParser, Namespace
from pathlib import Path

import uvicorn
from alembic.config import main as run_alembic

from taskiq_collector.settings import settings


def set_multiproc_dir() -> None:
    """
    Sets mutiproc_dir env variable.

    This function cleans up the multiprocess directory
    and recreates it. This actions are required by prometheus-client
    to share metrics between processes.

    After cleanup, it sets two variables.
    Uppercase and lowercase because different
    versions of the prometheus-client library
    depend on different environment variables,
    so I've decided to export all needed variables,
    to avoid undefined behaviour.
    """
    shutil.rmtree(settings.prometheus_dir, ignore_errors=True)
    os.makedirs(settings.prometheus_dir, exist_ok=True)
    os.environ["prometheus_multiproc_dir"] = str(
        settings.prometheus_dir.expanduser().absolute(),
    )
    os.environ["PROMETHEUS_MULTIPROC_DIR"] = str(
        settings.prometheus_dir.expanduser().absolute(),
    )


def parse_args() -> Namespace:
    """
    Parse CLI args.

    Parse CLI parameters and
    return custom namespace.

    :return: parsed parameters.
    """
    parser = ArgumentParser()
    subparsers = parser.add_subparsers(dest="subparser_name")
    migrate_parser = subparsers.add_parser(
        "migrate",
        help="Apply migrations",
    )
    migrate_parser.add_argument(
        "--raiseerr",
        action="store_true",
        help="Raise a full stack trace on error",
    )
    migrate_parser.add_argument(
        "revision",
        nargs="?",
        default=None,
        type=str,
        help="Alembic revision identifier",
    )
    downgrade_parser = subparsers.add_parser(
        "downgrade",
        help="Revert migrations",
    )
    downgrade_parser.add_argument(
        "revision",
        type=str,
        help="Alembic revision identifier",
    )
    downgrade_parser.add_argument(
        "--raiseerr",
        action="store_true",
        help="Raise a full stack trace on error",
    )
    return parser.parse_args()


def run_migrations(args: Namespace) -> None:
    """
    Upgrade or downgrade migrations.

    this function will applies or reverts migrations.

    :param args: current CLI arguments.
    """
    alembic_args = [
        "-c",
        str(Path(__file__).parent / "alembic.ini"),
    ]

    if args.subparser_name == "migrate":
        if args.raiseerr:
            alembic_args.append("--raiseerr")
        alembic_args.extend(
            [
                "upgrade",
                args.revision or "head",
            ],
        )
    elif args.subparser_name == "downgrade":
        if args.raiseerr:
            alembic_args.append("--raiseerr")
        alembic_args.extend(
            [
                "downgrade",
                args.revision,
            ],
        )
    run_alembic(alembic_args)


def main() -> None:
    """Entrypoint of the application."""
    args = parse_args()
    if args.subparser_name is not None:
        run_migrations(args)
        return
    set_multiproc_dir()
    uvicorn.run(
        "taskiq_collector.web.application:get_app",
        workers=settings.workers_count,
        host=settings.host,
        port=settings.port,
        reload=settings.reload,
        log_level=settings.log_level.value.lower(),
        factory=True,
    )


if __name__ == "__main__":
    main()
