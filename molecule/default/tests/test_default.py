"""Role testing files using testinfra"""


def test_config_directory(host):
    """Check config directory"""
    f = host.file("/etc/influxdb")
    assert f.is_directory
    assert f.user == "influxdb"
    assert f.group == "root"
    assert f.mode == 0o775


def test_data_directory(host):
    """Check data directory"""
    d = host.file("/var/lib/influxdb")
    assert d.is_directory
    assert d.user == "influxdb"
    assert d.group == "root"
    assert d.mode == 0o700


def test_backup_directory(host):
    """Check backup directory"""
    b = host.file("/var/backups/influxdb")
    assert b.is_directory
    assert b.user == "influxdb"
    assert b.group == "root"
    assert b.mode == 0o775


def test_influxdb_service(host):
    """Check InfluxDB service"""
    s = host.service("influxdb")
    assert s.is_running
    assert s.is_enabled


def test_influxdb_docker_container(host):
    """Check InfluxDB docker container"""
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
    cmd = "/usr/local/bin/backup-influxdb.sh"
    f = host.file("/var/spool/cron/crontabs/root").content_string
    assert cmd in f
