# Maloja plugin for Funkwhale

Submit your listens to your [Maloja](https://github.com/krateng/maloja) server
when listening to music on a [Funkwhale](https://funkwhale.audio/) pod.


## Installation

Place the `maloja` directory with all included files in the Funkwhale
plugins directory in `FUNKWHALE_PLUGINS_PATH`. By default this is `/srv/funkwhale/plugins`.

Then enable the Maloja plugin by adding it to the `FUNKWHALE_PLUGINS`
environment variable, e.g.

    FUNKWHALE_PLUGINS=maloja

See the [Funkwhale plugin documentation](https://docs.funkwhale.audio/developers/plugins.html) for details.


## Usage

The Maloja plugins needs to be configured per user. Each user needs to
configure their Maloja server URL and API key in the user's settings.


## License

Maloja plugin for Funkwhale © 2021 Philipp Wolfer <ph.wolfer@gmail.com>

Published under the MIT license, see LICENSE for details.