try:
    import starlette
    from starlette.staticfiles import StaticFiles
except ImportError as e:
    raise ImportError(
        "Can't run Bench Server without server dependencies, to install run: "
        "pip install arthur-bench[server]"
    ) from e


class SPAStaticFiles(StaticFiles):
    """
    Because the Bench UI uses React's DOM Routing library, users might reload their page
    at a different path than what the UI is mounted on (eg: /). When this happens,
    FastAPI will try to reconcile the route to a file in the StaticFiles directory,
    and because it doesn't exist will throw a 404. So instead, if we detect that a user
    is trying to load a Bench page and gets a 404, we instead first redirect to the
    / so that the UI is loaded first before re-routing.
    """

    async def get_response(self, path: str, scope):
        try:
            return await super().get_response(path, scope)
        except starlette.middleware.exceptions.HTTPException as ex:
            if ex.status_code == 404 and "bench" in path:
                return await super().get_response("index.html", scope)
            else:
                raise ex
