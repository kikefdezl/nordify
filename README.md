# Nordify

Convert images to the Nord pallette without artifacts.

<p align="center">
  <img src="assets/before.png" width="45%" />
  <img src="assets/after.png" width="45%" />
</p>


---

## Why?

All other available tools I tried either got the colors wrong, or produced dot-artifacts typical from the Floyd-Steinberg algorithm:

<p align="center">
  <figure style="display: inline-block; margin: 0 10px; text-align: center;">
    <img src="assets/cmp-original.png" width="30%" />
    <figcaption>Original</figcaption>
  </figure>

  <figure style="display: inline-block; margin: 0 10px; text-align: center;">
    <img src="assets/cmp-floyd-steinberg.png" width="30%" />
    <figcaption>Floyd–Steinberg</figcaption>
  </figure>

  <figure style="display: inline-block; margin: 0 10px; text-align: center;">
    <img src="assets/cmp-mine.png" width="30%" />
    <figcaption>Mine</figcaption>
  </figure>
</p>


## How to Use

I recommend to use the `uv` package manager. Then just clone the repo and run the python script on your image:

```bash
git clone https://github.com/kikefdezl/nordify.git
cd nordify

uv sync
uv run main.py input.png output.png
```
