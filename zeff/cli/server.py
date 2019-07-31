"""Zeff commandline server access."""
__docformat__ = "reStructuredText en"


def subparser_server(parser, config):
    """Add CLI arguments necessary for accessing a server."""

    parser.add_argument(
        "--server-url",
        default=config["server"]["server_url"],
        help=f"""Zeff Cloud REST server URL (default: `{config["server"]["server_url"]}`).""",
    )
    parser.add_argument(
        "--org-id",
        default=config["server"]["org_id"],
        help="""Organization id for access to Zeff Cloud (default: ``org_id``
            in configuration).""",
    )
    parser.add_argument(
        "--user-id",
        default=config["server"]["user_id"],
        help="""user id for access to Zeff Cloud (default: ``user_id`` in
            configuration).""",
    )
