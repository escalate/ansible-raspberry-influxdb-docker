"""Role testing files using testinfra"""


def test_read_only_directories(host):
    """Check read-only directories"""
    f = host.file("/etc/influxdb")
    assert f.is_directory
    assert f.user == "root"
    assert f.group == "root"
    assert f.mode == 0o755


def test_writeable_directories(host):
    """Check writeable directories"""
    d = host.file("/var/lib/influxdb")
    assert d.is_directory
    assert d.user == "nobody"
    assert d.group == "nogroup"
    assert d.mode == 0o700

    b = host.file("/var/backups/influxdb")
    assert b.is_directory
    assert b.user == "nobody"
    assert b.group == "nogroup"
    assert b.mode == 0o755


def test_influxdb_service(host):
    """Check influxdb service"""
    s = host.service("influxdb")
    assert s.is_running
    assert s.is_enabled


def test_influxdb_docker_container(host):
    """Check influxdb docker container"""
    d = host.docker("influxdb.service").inspect()
    assert d["HostConfig"]["Memory"] == 1073741824
    assert d["Config"]["Image"] == "influxdb:latest"
    assert d["Config"]["Labels"]["maintainer"] == "me@example.com"
    assert "INFLUXD_REPORTING_DISABLED=true" in d["Config"]["Env"]
    assert "internal" in d["NetworkSettings"]["Networks"]
    assert \
        "influxdb" in d["NetworkSettings"]["Networks"]["internal"]["Aliases"]


def test_backup_cron_job(host):
    """Check backup cron job"""
    cmd = "/usr/local/bin/backup_influxdb.sh"
    f = host.file("/var/spool/cron/crontabs/root").content_string
    assert cmd in f
