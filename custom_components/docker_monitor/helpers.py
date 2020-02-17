import logging
import threading

from .const import (
    CONTAINER_INFO,
    CONTAINER_INFO_CREATED,
    CONTAINER_INFO_ID,
    CONTAINER_INFO_IMAGE,
    CONTAINER_INFO_NETWORKMODE,
    CONTAINER_INFO_STARTED,
    CONTAINER_INFO_STATUS,
    EVENT_INFO_CONTAINER,
    EVENT_INFO_ID,
    EVENT_INFO_IMAGE,
    EVENT_INFO_STATUS,
    VERSION_INFO_API_VERSION,
    VERSION_INFO_ARCHITECTURE,
    VERSION_INFO_CONTAINERS_PAUSED,
    VERSION_INFO_CONTAINERS_RUNNING,
    VERSION_INFO_CONTAINERS_STOPPED,
    VERSION_INFO_CONTAINERS_TOTAL,
    VERSION_INFO_IMAGES,
    VERSION_INFO_KERNEL,
    VERSION_INFO_MEMTOTAL,
    VERSION_INFO_OS,
    VERSION_INFO_VERSION
)

_LOGGER = logging.getLogger(__name__)


class DockerMonitorApi:
    def __init__(self, base_url):
        self._base_url = base_url

        try:
            import docker
        except ImportError as e:
            _LOGGER.error("Missing docker library ({})".format(e))
            raise ImportError()

        self._client = docker.DockerClient(base_url=self._base_url)

        self._containers = {}
        self._stats_listener = DockerContainerStats(self._client, self)

        self._event_listener = None

    def start(self, event_callback=None):
        if event_callback:
            self._event_listener = DockerContainerEventListener(
                self._client, event_callback)
            self._event_listener.start()

        self._stats_listener.start_listen()

    def exit(self):
        if self._event_listener:
            self._event_listener.shutdown()
        if self._stats_listener.isAlive():
            self._stats_listener.shutdown()
        self._client.close()

    def get_containers(self):
        try:
            containers = [container.name
                          for container in self._client.containers.list(all=True) or []]
        except Exception as e:
            _LOGGER.info("Cannot get docker containers")
            _LOGGER.debug("Request exception: {}".format(e))
            raise ConnectionError("Cannot retrieve containers")
        return containers

    def watch_container(self, name, callback):
        if name not in self._containers:
            self._containers[name] = ContainerData(self._client, name)
        self._containers[name].register_callback(callback)
        return self._containers[name]

    def get_info(self):
        result = {}
        try:
            raw_stats = self._client.version()
            info = self._client.info()
            result = {
                VERSION_INFO_VERSION: raw_stats.get('Version', None),
                VERSION_INFO_API_VERSION: raw_stats.get('ApiVersion', None),
                VERSION_INFO_OS: raw_stats.get('Os', None),
                VERSION_INFO_ARCHITECTURE: raw_stats.get('Arch', None),
                VERSION_INFO_KERNEL: raw_stats.get('KernelVersion', None),
                VERSION_INFO_CONTAINERS_TOTAL : info.get('Containers', None),
                VERSION_INFO_CONTAINERS_PAUSED : info.get('ContainersPaused', None),
                VERSION_INFO_CONTAINERS_RUNNING : info.get('ContainersRunning', None),
                VERSION_INFO_CONTAINERS_STOPPED : info.get('ContainersStopped', None),
                VERSION_INFO_IMAGES : info.get('Images', None),
                VERSION_INFO_MEMTOTAL : info.get('MemTotal', None),
            }
        except Exception as e:
            _LOGGER.info("Cannot get docker daemon info")
            _LOGGER.debug("Request exception: {}".format(e))
            raise ConnectionError("Cannot request info")

        return result


class DockerContainerEventListener(threading.Thread):
    """Docker monitor container event listener thread."""

    def __init__(self, client, callback):
        super().__init__(name='DockerContainerEventListener')

        self._client = client
        self._callback = callback

        self._event_stream = None
        self._stopper = threading.Event()

    def shutdown(self):
        """Signal shutdown of processing event."""
        self._stopper.set()
        if self._event_stream:
            self._event_stream.close()
        self.join()

        _LOGGER.info("Event listener thread stopped")

    def run(self):
        while not self._stopper.isSet():
            try:
                self._event_stream = self._client.events(decode=True)
                for event in self._event_stream:
                    _LOGGER.debug("Event: ({})".format(event))
                    try:
                        # Only interested in container events
                        if event['Type'] == 'container':
                            message = {
                                EVENT_INFO_CONTAINER:
                                    event['Actor']['Attributes'].get('name'),
                                EVENT_INFO_IMAGE: event['from'],
                                EVENT_INFO_STATUS: event['status'],
                                EVENT_INFO_ID: event['id'],
                            }
                            _LOGGER.info(
                                "Container event: ({})".format(message))

                            self.__notify(message)
                    except KeyError as e:
                        _LOGGER.error("Key error: ({})".format(e))
            except Exception as e:
                _LOGGER.info("Cannot open event stream")
                _LOGGER.debug("Request exception: {}".format(e))

    def __notify(self, message):
        if self._callback:
            self._callback(message)


class ContainerData:
    def __init__(self, client, name):
        self._client = client
        self._name = name

        self._stats = None
        self._subscribers = []

        self._container = None

    def get_name(self):
        return self._name

    def register_callback(self, callback):
        if callback not in self._subscribers:
            self._subscribers.append(callback)

    def _reload_container(self):
        try:
            if not self._container:
                self._container = self._client.containers.get(self._name)
            self._container.reload()
        except Exception as ex:
            self._container = None
            _LOGGER.info("Cannot get get container")
            _LOGGER.debug("Request exception: {}".format(ex))
            raise ConnectionError("Cannot request container info")

    def get_info(self):
        from dateutil import parser

        self._reload_container()
        info = {
            CONTAINER_INFO_ID:
                self._container.id,
            CONTAINER_INFO_IMAGE:
                self._container.image.tags,
            CONTAINER_INFO_STATUS:
                self._container.attrs['State']['Status'],
            CONTAINER_INFO_CREATED:
                parser.parse(self._container.attrs['Created']),
            CONTAINER_INFO_STARTED:
                parser.parse(self._container.attrs['State']['StartedAt']),
            CONTAINER_INFO_NETWORKMODE:
                self._container.attrs['HostConfig']['NetworkMode'] == 'host'
        }

        return info

    def start(self):
        if not self._container:
            self._reload_container()

        try:
            self._container.start()
        except Exception as ex:
            self._container = None

            _LOGGER.info("Cannot start container")
            _LOGGER.debug("Request exception: {}".format(ex))
            raise ConnectionError("Cannot start container")
        self._notify()

    def stop(self, timeout=10):
        if not self._container:
            self._reload_container()

        try:
            self._container.stop(timeout=timeout)
            self._container.wait(timeout=timeout)
        except Exception as ex:
            self._container = None
            _LOGGER.info("Cannot stop container")
            _LOGGER.debug("Request exception: {}".format(ex))
            raise ConnectionError("Cannot stop container")

        self._notify()

    def get_stats(self):
        return self._stats

    def set_stats(self, stats):
        self._stats = stats
        self._notify()

    def _notify(self):
        for callback in self._subscribers:
            callback()


class DockerContainerStats(threading.Thread):
    """Docker monitor container stats listener thread."""

    def __init__(self, client, api):
        super().__init__(name='DockerContainerStats')

        self._client = client
        self._api = api

        self._stopper = threading.Event()
        self._interval = None
        self._old = {}

    def start_listen(self, interval=10):
        """Start event-processing thread."""
        self._interval = interval
        self.start()

    def shutdown(self):
        """Signal shutdown of processing event."""
        self._stopper.set()
        self.join()
        _LOGGER.debug("Stats listener thread stopped")

    def run(self):
        streams = {}
        while not self._stopper.isSet():
            _LOGGER.info("Stats runner")
            for name, container in self._api._containers.items():
                # Empty stats
                stats = None
                try:
                    containerinfo = container.get_info()
                    status = containerinfo[CONTAINER_INFO_STATUS]

                    if status in ('running', 'paused'):
                        _LOGGER.info("Running {}".format(name))
                        if name not in streams:
                            streams[name] = self._client.containers.get(
                                name).stats(stream=True, decode=True)

                        for raw in streams[name]:
                            stats = self.__parse_stats(name, containerinfo, raw)

                            # Break from event to streams other streams
                            break
                    elif name in streams:
                        _LOGGER.info("Stopped {}".format(name))
                        streams[name].close()
                        streams.pop(name)

                        # Remove old stats from this container
                        if name in self._old:
                            self._old.pop(name)
                except Exception as ex:
                    _LOGGER.error("Cannot get docker container info")
                    _LOGGER.debug("Request exception: {}".format(ex))

                    if name in streams:
                        # Close stream as we cannot access container
                        streams[name].close()
                        streams.pop(name)

                        # Remove old stats from this container
                        if name in self._old:
                            self._old.pop(name)

                container.set_stats(stats)

            # Wait before read
            self._stopper.wait(self._interval)

        # Cleanup
        for stream in streams.values():
            stream.close()

    def __parse_stats(self, name, containerinfo, raw):
        from dateutil import parser

        stats = {}
        stats['read'] = parser.parse(raw['read'])

        old = self._old.get(name, {})

        # CPU stats
        cpu = {}
        try:
            cpu_new = {}
            cpu_new['total'] = raw['cpu_stats']['cpu_usage']['total_usage']
            cpu_new['system'] = raw['cpu_stats']['system_cpu_usage']

            # Compatibility wih older Docker API
            if 'online_cpus' in raw['cpu_stats']:
                cpu['online_cpus'] = raw['cpu_stats']['online_cpus']
            else:
                cpu['online_cpus'] = len(
                    raw['cpu_stats']['cpu_usage']['percpu_usage'] or [])
        except KeyError as e:
            # raw do not have CPU information
            _LOGGER.debug(
                "Cannot grab CPU usage for container {} ({})".format(name, e))
        else:
            if 'cpu' in old:
                cpu_delta = cpu_new['total'] - old['cpu']['total']
                system_delta = cpu_new['system'] - old['cpu']['system']

                cpu['total'] = 0.0
                if cpu_delta > 0 and system_delta > 0:
                    cpu['total'] = (
                        float(cpu_delta) / float(system_delta)
                    ) * float(cpu['online_cpus']) * 100.0

            old['cpu'] = cpu_new

        # Memory stats
        memory = {}
        try:
            memory['usage'] = raw['memory_stats']['usage'] - raw['memory_stats']['stats']['cache']
            memory['limit'] = raw['memory_stats']['limit']
            memory['max_usage'] = raw['memory_stats']['max_usage']
        except (KeyError, TypeError) as e:
            # raw_stats do not have memory information
            _LOGGER.debug(
                "Cannot grab memory usage for container {} ({})".format(name, e))
        else:
            memory['usage_percent'] = float(
                memory['usage']) / float(memory['limit']) * 100.0

        # Network stats
        network = {}
        if not containerinfo[CONTAINER_INFO_NETWORKMODE]:
            try:
                network['total_tx'] = 0
                network['total_rx'] = 0
                for if_name, data in raw["networks"].items():
                    network['total_tx'] += data["tx_bytes"]
                    network['total_rx'] += data["rx_bytes"]
            except KeyError as e:
                # raw_stats do not have network information
                _LOGGER.debug(
                    "Cannot grab network usage for container {} ({})".format(name, e))

        stats['cpu'] = cpu
        stats['memory'] = memory
        stats['network'] = network

        # Update stats history
        self._old[name] = old

        return stats
