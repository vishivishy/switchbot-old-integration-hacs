# switchbot-old-integration-hacs
Old switchbot integration where the entity would remember the state of the device in press mode. 

requires following config:

```yaml
switch:
  - platform: switchbot_old_hacs
    name: device_name
    mac: 'DD:BB:33:22:11:44'
    password: device_password
```

Trying new lib in place of depricated libs