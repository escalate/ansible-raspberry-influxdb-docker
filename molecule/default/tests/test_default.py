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


def test_influxdb_config(host):
    """Check influxdb config file"""
    f = host.file("/etc/influxdb/influxdb.env")
    assert f.is_file
    assert f.user == "root"
    assert f.group == "root"

    config = (
                "INFLUX_CONFIGS_PATH=/var/lib/influxdb/configs\n"
                "INFLUX_PATH=/var/backups/influxdb\n"
                "INFLUXD_BOLT_PATH=/var/lib/influxdb/influxd.bolt\n"
                "INFLUXD_ENGINE_PATH=/var/lib/influxdb/engine\n"
                "INFLUXD_REPORTING_DISABLED=true\n"
    )
    assert config in f.content_string


def test_influxdb_service(host):
    """Check influxdb service"""
    f = host.file("/etc/systemd/system/influxdb.service")
    assert "--memory=1G" in f.content_string
    assert "quay.io/influxdb/influxdb:v2.0.4" in f.content_string

    s = host.service("influxdb")
    assert s.is_running
    assert s.is_enabled


def test_backup_cron_job(host):
    """Check backup cron job"""
    cmd = "/usr/local/bin/backup_influxdb.sh"
    f = host.file("/var/spool/cron/crontabs/root").content_string
    assert cmd in f
