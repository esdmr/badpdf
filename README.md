# Bad Apple in PDF

An experiment to play [“Bad Apple!!”][bad-apple] in a JavaScript-enabled PDF
viewer. It is tested in Chromium (PDFium) and Firefox (PDF.js). The initial page
load might take a few seconds.

## Download

|                                            Name                                             | Description                                           |
| :-----------------------------------------------------------------------------------------: | :---------------------------------------------------- |
|    [`bad-hc-px.pdf`](https://github.com/esdmr/badpdf/releases/download/v2/bad-hc-px.pdf)    | slower, works on both Firefox and Chromium            |
|    [`bad-hc-rw.pdf`](https://github.com/esdmr/badpdf/releases/download/v2/bad-hc-rw.pdf)    | faster, best viewed in Chromium                       |
| [`bad-orig-res.pdf`](https://github.com/esdmr/badpdf/releases/download/v2/bad-orig-res.pdf) | original resolution, best viewed in Chromium          |
| [`bad-half-res.pdf`](https://github.com/esdmr/badpdf/releases/download/v2/bad-half-res.pdf) | half the original resolution, best viewed in Chromium |

Check the [latest release](https://github.com/esdmr/badpdf/releases/latest) for more.

## Requirement

- [UV][uv]
- [Node.JS][nodejs]
- [FFmpeg][ffmpeg]
- [jq][jq]
- [Git][git]
- [GNU Make][make]
- POSIX-compatible `/bin/sh`

## Building

```sh
git clone esdmr/badpdf --recurse-submodules
cd badpdf
make

# Or, to run a dev server
make dev
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

Optionally, this script reorders the frame data according to a [Generalized
Hilbert Curve][gilbert]. This improves the compression rate of RLE, compared to
the linear scan curve.

The first is the “RLE Ridge” compression. Its goal is to reduce very short
segments, by intentionally miscoloring that segment, thereby combining three
segments together. This will diminish small details, so it is best to keep the
threshold small.

```
rle:   0:355 1:001 0:050 (3 segments, 4 bytes)
ridge: 0:406             (1 segment,  2 bytes)
```
The second is the “RLE Plain” compression. It is very similar to the Ridge
compression, but it only compresses odd number of short segments into one.
Unlike the Ridge compression, it expands small details, so it is best to keep
the threshold small. Since Ridge compression already deals with very small
segments, the threshold should be greater than that of Ridge’s, otherwise Plain
would not do anything.

```
rle:   0:355 1:003 0:002 1:004 0:257 (5 segments, 7 bytes)
plain: 0:355 1:009             0:257 (3 segments, 5 bytes)
```

The final frame data goes to the `frames/out/frames.bin` file. If you run the
preview server, you can see how it will look like outside a PDF sandbox.

The python script over at `generate.py` embeds the font and the JavaScript, and
generates the AcroForm widgets for JavaScript to use for displaying the frame
data. It uses [pikepdf][pikepdf] to generate the PDF, which automatically
compresses the PDF stream data.

The generated PDF may use either pixels (like PDFTris) or rows (like DoomPDF) to
display the data. The rows display is much more performant and is able to
support higher resolution without overwhelming the PDF sandbox and renderer. To
improve the graphical quality of the row display, the generator script embeds a
Type1 font `bw.pfb` to use for the text fields. (Unfortunately, PDF.js does not
support fonts in text fields yet.)

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
[gilbert]: https://github.com/jakubcerveny/gilbert
[nodejs]: https://nodejs.org/
[jq]: https://jqlang.github.io/jq/
[pikepdf]: https://pikepdf.readthedocs.io/
