# HomeAssistantFiobank


[![hacs_badge](https://img.shields.io/badge/HACS-Default-orange.svg?style=for-the-badge)](https://github.com/custom-components/hacs)

This sensor is shows current FIO bank account status.


## Installation

### Step 1: Download files

#### Option 1: Via HACS

Make sure you have HACS installed. If you don't, run `curl -sfSL https://hacs.xyz/install | bash -` in HA.
Then choose Components under HACS. Choose the menu in the upper right, and select Custom repositories. Then add this repo's URL. You should be able to choose to Install now.

#### Option 2: Manual
Clone this repository or download the source code as a zip file and add/merge the `custom_components/` folder with its contents in your configuration directory.

### Step 2: Configure
Add the following to your `configuration.yaml` file:

```yaml
# Example configuration.yaml entry for showing FIO bank account status
sensor:
  - platform: fiobank_sensor
    api_key: "YOUR API FIO API KEY"
```

#### api_key

&nbsp;&nbsp;&nbsp;&nbsp;_(string) (Required)_ YOUR FIO API KEY.


### Step 3: Restart HA
For the newly added integration to be loaded, HA needs to be restarted.

