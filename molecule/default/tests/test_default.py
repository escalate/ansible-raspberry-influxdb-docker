"""Role testing files using testinfra"""


import pytest


def test_read_only_directories(host):
    """Check read-only directories"""
    f = host.file("/etc/influxdb")
    assert f.is_directory
    assert f.user == "root"
    assert f.group == "root"
    assert f.mode == 0o755


@pytest.mark.parametrize("directory", [
    ("/var/backups/influxdb"),
    ("/var/lib/influxdb")
])
def test_writeable_directories(host, directory):
    """Check writeable directories"""
    f = host.file(directory)
    assert f.is_directory
    assert f.user == "nobody"
    assert f.group == "nogroup"
    assert f.mode == 0o755


def test_influxdb_service(host):
    """Check influxdb service"""
    s = host.service("influxdb")
    assert s.is_running
    assert s.is_enabled


def test_influxdb_docker_container(host):
    """Check influxdb docker container"""
    d = host.docker("influxdb.service").inspect()
    assert d["HostConfig"]["Memory"] == 1073741824
    assert d["Config"]["Image"] == "quay.io/influxdb/influxdb:v2.0.4"
    assert d["Config"]["Labels"] == {'maintainer': '"me@example.com"'}
    assert "INFLUXD_REPORTING_DISABLED=true" in d["Config"]["Env"]


def test_backup_cron_job(host):
    """Check backup cron job"""
    cmd = "/usr/local/bin/backup_influxdb.sh"
    f = host.file("/var/spool/cron/crontabs/root").content_string
    assert cmd in f
