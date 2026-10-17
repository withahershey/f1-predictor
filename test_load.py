import fastf1
fastf1.Cache.enable_cache("cache")
fastf1.logger.set_log_level("DEBUG")

s = fastf1.get_session(2024, "Monza", "R")
s.load(telemetry=False, weather=False, messages=False)