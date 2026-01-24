# Nordify

Convert images to the Nord palette without artifacts.

<p align="center">
  <img src="assets/before.png" width="49%" />
  <img src="assets/after.png" width="49%" />
</p>

---

## Why?

All other available tools I tried either got the colors wrong, or produced dot-artifacts typical from the Floyd-Steinberg algorithm:

<table>
<tr>
<td align="center" width="33.33%">
  <img src="assets/cmp-original.png" style="width: 100%; max-width: 350px;" />
  <br />
  <em>Original</em>
</td>
<td align="center" width="33.33%">
  <img src="assets/cmp-floyd-steinberg.png" style="width: 100%; max-width: 350px;" />
  <br />
  <em>Floyd–Steinberg</em>
</td>
<td align="center" width="33.33%">
  <img src="assets/cmp-mine.png" style="width: 100%; max-width: 350px;" />
  <br />
  <em>Mine</em>
</td>
</tr>
</table>


## How to Use

I recommend to use the `uv` package manager. Then just clone the repo and run the python script on your image:

```commandline
git clone https://github.com/kikefdezl/nordify.git
cd nordify

uv sync
uv run main.py input.png output.png
```

I recommend default options since they work very well, but you can experiment with other options:
```commandline
--no-expand               Use only original 16 Nord colors
--expansion-factor (num)  Number of interpolated colors (default: 3)
--rgb-distance            Use RGB distance instead of perceptual LAB
```
