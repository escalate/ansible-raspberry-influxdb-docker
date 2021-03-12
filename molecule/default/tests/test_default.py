"""Role testing files using testinfra"""


def test_backup_cron_job(host):
    """Check backup cron job"""
    cmd = "/usr/local/bin/backup_influxdb.sh"
    f = host.file("/var/spool/cron/crontabs/root").content_string
    assert cmd in f


def test_influxdb_service(host):
    """Check influxdb service"""
    s = host.service("influxdb")
    assert s.is_running
    assert s.is_enabled
