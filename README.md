# Bad Apple in PDF

An experiment to play [“Bad Apple!!”][bad-apple] in a JavaScript-enabled PDF
viewer. It is tested in Chromium (PDFium) and Firefox (PDF.js). The initial page
load might take a few seconds.

Note that currently, `bad.pdf` uses [PDFtris][pdftris]’s generator which uses
individual pixels. This limits the maximum resolution and frame rate of the
video. Theoretically, switching to [DoomPDF][doompdf]’s generator may improve
these restrictions, since it uses an input box for each row of pixels. Color
depth is not a concern, since the video is (converted to) black and white.

## Requirement

- [UV][uv]
- [GNU Make][make]
- [FFmpeg][ffmpeg]
- POSIX-compatible `/bin/sh`
- [Git][git]

## Building

```sh
git clone esdmr/badpdf --recurse-submodules
cd badpdf
uv sync
make bad.pdf

# Or, to run a preview server
make preview
```

## Development

This involved down scaling the original video and encoding it using
Run-Length Encoding (plus some optional, lossy compression). Then a script
encoded the resulting frame data into base64 and embedded it in a PDF template,
along with the JavaScript code to play it.

The original video is also available at the
[Felixoofed/badapple-frames][badapple-frames] repository, so I added it as a
submodule at `frames/src`.

The bash script over at `frames/create-frames.sh` downscales the video and
lowers the video frame rate using [FFmpeg][ffmpeg] commandline interface. The output goes
into the `frames/out` directory.

The python script over at `frames/process_frames.py` loads each frame and converts
them into black and white. Then, it encodes the run-length of the values.
Finally, it does two lossy compressions on the RLE’d stream.

The first is the “RLE Bleed-0” compression. Its goal is to reduce zero bytes
after a full (255) run-length, by intentionally miscoloring the remaining
non-full byte. This is only done at a certain threshold, as a larger miscolored,
vertical streak might be distracting.

```
rle:      0:512                         1:005 (2 segments)
uint8:    0:255 1:000 0:255 1:000 0:002 1:005 (6 bytes)
bleed-0:  0:255 1:000 0:255             1:007 (4 bytes)
```

The second is the “RLE Ridge” compression. Its goal is to reduce very short
segments, by intentionally miscoloring that segment, thereby combining three
segments together. This will diminish small details, so it is best to keep the
threshold small.

```
rle:   0:355 1:002 0:050             (3 segments)
uint8: 0:255 1:000 0:100 1:001 0:050 (5 bytes)
ridge: 0:255 1:000 0:151             (3 bytes)
```

The final frame data goes to the `frames/out/frames.bin` file. If you run the
preview server, you can see how it will look like at `bad.html`. It is a port of
`index.js` from Acrobat API into Web API.

The python script over at `generate.py` is a modified version of
[PDFtris][pdftris]’s generator. It defines the page width and height in a
separate variable, defines the FPS to be synchronized between FFmpeg and
JavaScript, and defines a button to play and an input box for frame/byte count.
The output goes to `bad.pdf`.

## Related Work

- [PDFTris][pdftris]
- [DoomPDF][doompdf]

[bad-apple]: https://www.youtube.com/watch?v=i41KoE0iMYU
[badapple-frames]: https://github.com/Felixoofed/badapple-frames
[pdftris]: https://github.com/ThomasRinsma/pdftris
[doompdf]: https://github.com/ading2210/doompdf
[uv]: https://docs.astral.sh/uv/
[ffmpeg]: https://www.ffmpeg.org/
[make]: https://www.gnu.org/software/make/
[git]: https://git-scm.com/
