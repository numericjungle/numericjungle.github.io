---
date: 2018-06-20 10:44:19.970664
layout: post
title: Key Mapping for specific apps in Mac
description: "macKeyMapping"
tags: [software, mac, installation]
comments: true
---
Scenario: Keymapping for specific apps in Mac. 


For example, Windows and Mac use control/ command keys differently, it becomes annoying when using Microsoft Remote Desktop on Mac doesn't provide a self-contained working environment, it often jumps to other mac apps easily. Map the mac command key to control key sort out the problem.

* Download [Karabiner](https://pqrs.org/osx/karabiner/) ([source code](https://github.com/tekezo/Karabiner-Elements)).

<!--excerpt-->
* After installation, allow this 3rd party app to make system changes: System Preferences > Security & Privacy button > Allow. If not working, try close Chrome and MagicPrefs if installed. cc [steps](https://pqrs.org/osx/karabiner/document.html).

* In order to map keys only for specific apps, we need the app bundle ID: Go to the application folder (e.g. `/Applications/`)
`mdls -name kMDItemCFBundleIdentifier -r Microsoft\ Remote\ Desktop\ Beta.app`
Then got `"com.microsoft.rdc.osx.beta"`

* Create a new json script under `~/.config/karabiner/assets/complex_modifications/`,
Here is my `sample.json`:

{% highlight json %}
{
  "title": "Remote Desktop new",
  "rules": [
    {
      "description": "Map left command to left control",
      "manipulators": [
        {
          "type": "basic",
          "from": {
            "key_code": "left_gui",
            "modifiers": {
              "optional": [
                "any"
              ]
            }
          },
          "to": [
            {
              "key_code": "left_control"
            }
          ],
          "conditions": [
            {
              "type": "frontmost_application_if",
              "bundle_identifiers": [
                "com\\.microsoft\\.rdc\\.osx\\.beta"
              ]
            }
          ]
        }
        
      ]
    }
  ]
}
{% endhighlight %}

* The new rule should pop in the perference/ complex modification tab:
<img width="903" alt="screen shot 2018-06-20 at 11 20 18 am" src="https://user-images.githubusercontent.com/5177427/41668044-78237de8-747c-11e8-8ba0-5e56a3970214.png">

* Enable the new rule:
<img width="1000" alt="screen shot 2018-06-20 at 11 20 09 am" src="https://user-images.githubusercontent.com/5177427/41668052-7a23feec-747c-11e8-85ad-6a9673df93f4.png">

* Debug: Karabiner has a handy tool `Karabiner-EventViewer` to track all inputs, check the eventType of the desired keys; and bundle names mentioned in the previous step.
<img width="875" alt="screen shot 2018-06-20 at 11 28 02 am" src="https://user-images.githubusercontent.com/5177427/41668293-0b494eb8-747d-11e8-99a4-fb613f546eb7.png">
Also disable/ enable the new rules to make sure it's applied.