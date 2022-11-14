# GoldHEN Patch Repository
Patches for PlayStation 4 Games.

## Features
* `.json` support

## Usage

#### Manual Installation
- Download [patch zip](https://github.com/GoldHEN/GoldHEN_Patch_Repository/raw/gh-pages/patch1.zip)
- Extract it to `/data/GoldHEN/`

#### Easy Installation
- Patches can be configured, install/update via:
  - [GoldHEN Cheat Manager](https://github.com/GoldHEN/GoldHEN_Cheat_Manager/releases/latest)
  - Itemzflow Game Manager
- Run your game.

### Storage
* Use `FTP` to upload patch files to:
  * `/user/data/GoldHEN/patches/json/`
* Naming conversion for single or multiple games: `GameName.{format}` (English name only)
  * e.g. `ExampleGame.json`
  * e.g. `Example Game 2.json`

## Developing patches

Plugin system and GoldHEN Cheat Manager looks for patches by `TitleID.json`. (this is automatically generated from a python script using `app_titleid` when downloading/updating)
<br>You may edit the individual file for your Title ID or edit the base file and upload it to your PS4 as `TitleID.json`.

```bash
export PS4_IP=192.168.1.138 # your PS4 ip address
export PS4_FTP_PORT=2121 # your PS4 ftp port (2121 via GoldHEN payload)
# sending base file as CUSA00000.json
curl -T ExampleGame.json ftp://$PS4_IP:$PS4_FTP_PORT/data/GoldHEN/patches/json/CUSA00000.json
# sending CUSA00000.json as CUSA00000.json
curl -T CUSA00000.json ftp://$PS4_IP:$PS4_FTP_PORT/data/GoldHEN/patches/json/CUSA00000.json
```

### Creating a patch

Set base address to `0x00400000` when importing binaries for consistency with PS4 memory address. (ASLR disabled)
* [Ghidra](https://ghidra-sre.org/)
  * [GhidraOrbis](https://github.com/astrelsky/GhidraOrbis/releases/latest)
* [IDA Pro](https://hex-rays.com/ida-pro/)
  * [PS4 Module Loader / IDA 7.0-7.7](https://github.com/SocraticBliss/ps4_module_loader/releases/latest)
* Text editors:
  * [Visual Studio Code](https://code.visualstudio.com/)
  * [VSCodium](https://vscodium.com/)

### Submission Guidelines
* Patch must be named `GameTitle.json` and be in `/patches/json`.
<br>For example, a patch file for Gravity Rush 2 must be called `GravityRush2.json`.
* If you are making a patch for a game that already has a file, then add to it.
* Submitting patches:
  * No whitespace.
  * Lowercase hex for address/value hex, uppercase for Title ID.

### Patch types

| `type`    | Info                      | Value (example)        |
|-----------|---------------------------|------------------------|
| `byte`    | Hex, 1 byte               | `"0x00"`               |
| `bytes16` | Hex, 2 bytes              | `"0x0000"`             |
| `bytes32` | Hex, 4 bytes              | `"0x00000000"`         |
| `bytes64` | Hex, 8 bytes              | `"0x0000000000000000"` |
| `bytes`   | Hex, any size (no spaces) | `"####"`               |
| `float32` | Float, single             | `"1.0"`                |
| `float64` | Float, double             | `"1.0"`                |
| `utf8`    | String, UTF-8*            | `"string"`             |
| `utf16`   | String, UTF-16*           | `"string"`             |

* Note: Strings are automatically null terminated.

#### Example patch

```json
{
  "patch": [
    {
      "title": "Example Game Title",
      "app_titleid": [
        "CUSA00000",
        "CUSA00001"
      ],
      "app_ver": "00.34",
      "app_elf": "eboot.bin",
      "patch_ver": "1.0",
      "name": "Example Name",
      "author": "Example Author",
      "note": "Example Note",
      "patch_list": [
        {
          "type": "bytes",
          "addr": "0x00000000",
          "value": "0102030405060708"
        },
        {
          "type": "utf8",
          "addr": "0x00000000",
          "value": "Hello World"
        }
      ]
    }
  ]
}
```
