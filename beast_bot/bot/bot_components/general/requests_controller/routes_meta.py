from __future__ import annotations

from .structure import RouteMeta, Service, Routes, RequestMethod


class RoutesMeta:

    _instance: RoutesMeta = None

    def __new__(cls: type[RoutesMeta], *args, **kwargs) -> RoutesMeta:
        if cls._instance is None:
            cls._instance = super().__new__(cls, *args, **kwargs)

        return cls._instance

    def __init__(self):
        self._routes: dict[Service, dict[str, RouteMeta]] = {
            service: dict()
            for service in Service
        }
        self._init_linking_server_routes()
        self._init_share_data_service_routes()

    def _init_linking_server_routes(self) -> None:
        service_dict = self._routes[Service.LINKING_SERVER]
        routes = Routes.LinkingServer

        def _init_data_prefix_routes() -> None:
            service_dict[routes.Data.available_statuses] = RouteMeta(
                path=[*routes.Data.prefixes, routes.Data.available_statuses],
                method=RequestMethod.GET
            )
            service_dict[routes.Data.beasts_statuses] = RouteMeta(
                path=[*routes.Data.prefixes, routes.Data.beasts_statuses],
                method=RequestMethod.GET
            )
            service_dict[routes.Data.extended_mode_status] = RouteMeta(
                path=[*routes.Data.prefixes, routes.Data.extended_mode_status],
                method=RequestMethod.GET
            )

        def _init_control_prefix_routes() -> None:
            service_dict[routes.Control.register_machine] = RouteMeta(
                path=[*routes.Control.prefixes,
                      routes.Control.register_machine],
                method=RequestMethod.POST,
                required_fields=[
                    'vm_name',
                    'port'
                ]
            )
            service_dict[routes.Control.update_machine_status] = RouteMeta(
                path=[*routes.Control.prefixes,
                      routes.Control.update_machine_status],
                method=RequestMethod.POST,
                required_fields=[
                    'vm_name',
                    'register_status'
                ]
            )
            service_dict[routes.Control.available_machines] = RouteMeta(
                path=[*routes.Control.prefixes,
                      routes.Control.available_machines],
                method=RequestMethod.GET,
            )
            service_dict[routes.Control.call_worked_to_pausing] = RouteMeta(
                path=[*routes.Control.prefixes,
                      routes.Control.call_worked_to_pausing],
                method=RequestMethod.PATCH,
            )
            service_dict[routes.Control.idles_to_founder] = RouteMeta(
                path=[*routes.Control.prefixes,
                      routes.Control.idles_to_founder],
                method=RequestMethod.POST,
                required_fields=['founder', 'machine_name']
            )

        def _init_status_prefix_routes() -> None:
            service_dict[routes.ServerStatus.server_status] = RouteMeta(
                path=[
                    *routes.ServerStatus.prefixes,
                    routes.ServerStatus.server_status
                ],
                method=RequestMethod.GET
            )

        _init_data_prefix_routes()
        _init_control_prefix_routes()
        _init_status_prefix_routes()

    def _init_share_data_service_routes(self) -> None:
        service_dict = self._routes[Service.SHARE_DATA]
        routes = Routes.ShareData

        service_dict[routes.get_content] = RouteMeta(
            path=[*routes.prefixes, routes.get_content],
            method=RequestMethod.GET
        )

    def get(self, service: Service, endpoint: str) -> RouteMeta:
        try:
            return self._routes[service][endpoint]
        except KeyError:
            raise KeyError(
                f'Cannot find "{endpoint}" endpoint of "{service}" service...'
            )


ROUTES_META = RoutesMeta()
