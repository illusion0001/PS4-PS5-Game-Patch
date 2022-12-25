# GoldHEN Patch Repository
Patches for PlayStation 4 Games.

## Features
* `.json` support

## Usage

#### Manual Installation (Offline via HDD)
- Download [patch zip](https://github.com/GoldHEN/GoldHEN_Patch_Repository/raw/gh-pages/patch1.zip).
- Copy `patch1.zip` to `/data/GoldHEN/` using an FTP client.
- Open [GoldHEN Cheat Manager](https://github.com/GoldHEN/GoldHEN_Cheat_Manager/releases/latest) and click Update.
- If the patches was installed correctly from Internal HDD, you should see the following message:

<details>
<summary>Screenshot (Click to Expand)</summary>

![](https://user-images.githubusercontent.com/37698908/204118853-8b34d4d5-e213-44a3-95a4-9462d419f2d2.png)

</details>

#### Manual Installation (Offline via USB)

- Download [patch zip](https://github.com/GoldHEN/GoldHEN_Patch_Repository/raw/gh-pages/patch1.zip).
- Copy `patch1.zip` to root of USB drive.
- Open [GoldHEN Cheat Manager](https://github.com/GoldHEN/GoldHEN_Cheat_Manager/releases/latest) and click Update.
- If the patches was installed correctly from USB, you should see the following message:

<details>
<summary>Screenshot (Click to Expand)</summary>

![](https://user-images.githubusercontent.com/37698908/204118861-ae3fa9c1-a429-4bf9-a357-55a8e7e3df77.png)

</details>

#### Easy Installation
- Patches can be configured, install/update via:
  - [GoldHEN Cheat Manager](https://github.com/GoldHEN/GoldHEN_Cheat_Manager/releases/latest)
  - [Itemzflow Game Manager](https://github.com/LightningMods/Itemzflow)
- Run your game.

### Storage
* Use `FTP` to upload patch files to:
  * `/user/data/GoldHEN/patches/json/`
* Naming conversion for app and patch engine to recognize: `(TitleID).{format}`
  * e.g. `CUSA00001.json`
  * e.g. `CUSA03694.json`

## Developing patches

Plugin system and GoldHEN Cheat Manager looks for patches by `(TitleID).{format}`. (this is automatically generated from a python script using `app_titleid` key when downloading/updating)
<br>You may edit the individual file for your Title ID or edit the base file and upload it to your PS4 as `(TitleID).{format}`.

```bash
export PS4_IP=192.168.1.138 # your PS4 ip address
export PS4_FTP_PORT=2121 # your PS4 ftp port (2121 via GoldHEN payload)
# sending base file as CUSA00000.json
curl -T ExampleGame.json ftp://$PS4_IP:$PS4_FTP_PORT/data/GoldHEN/patches/json/CUSA00000.json
# sending CUSA00000.json as CUSA00000.json
curl -T CUSA00000.json ftp://$PS4_IP:$PS4_FTP_PORT/data/GoldHEN/patches/json/CUSA00000.json
```

* Repository naming conversion for single or multiple games: `GameName.{format}` (English names only)
  * e.g. `ExampleGame.json`
  * e.g. `Example Game 2.json`

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
        "EXAMPLE01",
        "EXAMPLE02"
      ],
      "app_ver": "00.34",
      "app_elf": "eboot.bin",
      "patch_ver": "1.0",
      "name": "Example Name",
      "author": "Example Author",
      "note": "Example Note",
      "patch_list": [
        { "comment": "This is a code comment, improves code readability." },
        { "type": "bytes", "addr": "0x00000000", "value": "0102030405060708", "comment": "Code comment at end of line is also supported." },
        { "type": "utf8", "addr": "0x00000000", "value": "Hello World" }
      ]
    }
  ]
}
```
