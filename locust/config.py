from influxdb_client import InfluxDBClient
from influxdb_client.client.write_api import WriteOptions


class Config:
    conf_name: str = "Heisenbug"
    pacing_sec: float = 0.1
    api_host: str = "http://localhost:8080"
    influx_bucket: str = "demo_bucket"
    influx_org: str = "demo_org"
    influx_client = InfluxDBClient(
        url="http://localhost:8086",
        token="demo_token",
        org=influx_org,
    )

    influxdb = influx_client.write_api(
        write_options=WriteOptions(
            batch_size=10,
            flush_interval=10_000,
            jitter_interval=2_000,
            retry_interval=5_000,
        )
    )

    location_name: list[str] = ["SPb", "NY", "Berlin", "London"]
    user_login: str = "user@example.com"
    user_password: str = "string"


cfg = Config()
