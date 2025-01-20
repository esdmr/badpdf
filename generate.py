"""
Most of this code originates from PDFtris’s `gengrid.py`.

See: https://github.com/ThomasRinsma/pdftris/blob/0beca0117bb9412e95bfaebf0f84d09fd38620d0/gengrid.py
"""

from json import load


PDF_FILE_TEMPLATE = """
%PDF-1.6

% Root
1 0 obj
<<
  /AcroForm <<
    /Fields [ ###FIELD_LIST### ]
  >>
  /Pages 2 0 R
  /OpenAction 17 0 R
  /Type /Catalog
>>
endobj

2 0 obj
<<
  /Count 1
  /Kids [
    16 0 R
  ]
  /Type /Pages
>>
endobj

%% Annots Page 1 (also used as overall fields list)
21 0 obj
[
  ###FIELD_LIST###
]
endobj

###FIELDS###

%% Page 1
16 0 obj
<<
  /Annots 21 0 R
  /Contents 3 0 R
  /CropBox [
    0.0
    0.0
    ###PAGE_WIDTH###
    ###PAGE_HEIGHT###
  ]
  /MediaBox [
    0.0
    0.0
    ###PAGE_WIDTH###
    ###PAGE_HEIGHT###
  ]
  /Parent 2 0 R
  /Resources <<
  >>
  /Rotate 0
  /Type /Page
>>
endobj

3 0 obj
<< >>
stream
endstream
endobj

17 0 obj
<<
  /JS 42 0 R
  /S /JavaScript
>>
endobj


42 0 obj
<< >>
stream

###JAVASCRIPT###

endstream
endobj

trailer
<<
  /Root 1 0 R
>>

%%EOF
"""

PLAYING_FIELD_OBJ = """
###IDX### obj
<<
  /FT /Btn
  /Ff 1
  /MK <<
    /BG [
      ###COLOR###
    ]
    /BC [
      0 0 0
    ]
  >>
  /Border [ 0 0 0 ]
  /P 16 0 R
  /Rect [
    ###RECT###
  ]
  /Subtype /Widget
  /T (playing_field)
  /Type /Annot
>>
endobj
"""

PIXEL_OBJ = """
###IDX### obj
<<
  /FT /Btn
  /Ff 1
  /MK <<
    /BG [
      ###COLOR###
    ]
    /BC [
      0 0 0
    ]
  >>
  /Border [ 0 0 0 ]
  /P 16 0 R
  /Rect [
    ###RECT###
  ]
  /Subtype /Widget
  /T (P_###X###_###Y###)
  /Type /Annot
>>
endobj
"""

BUTTON_AP_STREAM = """
###IDX### obj
<<
  /BBox [ 0.0 0.0 ###WIDTH### ###HEIGHT### ]
  /FormType 1
  /Matrix [ 1.0 0.0 0.0 1.0 0.0 0.0]
  /Resources <<
    /Font <<
      /Courier 10 0 R
    >>
    /ProcSet [ /PDF /Text ]
  >>
  /Subtype /Form
  /Type /XObject
>>
stream
q
0.75 g
0 0 ###WIDTH### ###HEIGHT### re
f
Q
q
1 1 ###WIDTH### ###HEIGHT### re
W
n
BT
/Courier 12 Tf
0 g
10 8 Td
(###TEXT###) Tj
ET
Q
endstream
endobj
"""

BUTTON_OBJ = """
###IDX### obj
<<
  /A <<
	  /JS ###SCRIPT_IDX### R
	  /S /JavaScript
	>>
  /AP <<
    /N ###AP_IDX### R
  >>
  /F 4
  /FT /Btn
  /Ff 65536
  /MK <<
    /BG [
      0.75
    ]
    /CA (###LABEL###)
  >>
  /P 16 0 R
  /Rect [
    ###RECT###
  ]
  /Subtype /Widget
  /T (###NAME###)
  /Type /Annot
>>
endobj
"""

TEXT_OBJ = """
###IDX### obj
<<
	/AA <<
		/K <<
			/JS ###SCRIPT_IDX### R
			/S /JavaScript
		>>
	>>
	/F 4
	/FT /Tx
	/MK <<
	>>
	/MaxLen 0
	/P 16 0 R
	/Rect [
		###RECT###
	]
	/Subtype /Widget
	/T (###NAME###)
	/V (###LABEL###)
	/Type /Annot
>>
endobj
"""

STREAM_OBJ = """
###IDX### obj
<< >>
stream
###CONTENT###
endstream
endobj
"""


def guard_script(js: str):
    return "try{" + js + "}catch(error){app.alert(String(error))}"


def format(src: str, **kw: str | int | float):
    for k, v in kw.items():
        src = src.replace(f"###{k.upper()}###", str(v))

    return src


def add_field(field: str, **kw: str | int | float):
    global fields_text, field_indexes, obj_idx_ctr

    kw.setdefault("idx", f"{obj_idx_ctr} 0")

    fields_text += format(field, **kw)
    field_indexes.append(obj_idx_ctr)
    obj_idx_ctr += 1

    return str(kw["idx"])


def add_button(
    label: str,
    name: str | None,
    x: int | float,
    y: int | float,
    width: int | float,
    height: int | float,
    js: str | None,
):
    script_idx = none_script_idx if js is None else add_field(STREAM_OBJ, content=js)

    ap_idx = add_field(BUTTON_AP_STREAM, text=label, width=width, height=height)

    return add_field(
        BUTTON_OBJ,
        script_idx=script_idx,
        ap_idx=ap_idx,
        label=label,
        name=name if name else f"B_{obj_idx_ctr}",
        rect=f"{x} {y} {x + width} {y + height}",
    )


def add_text(
    label: str,
    name: str | None,
    x: int | float,
    y: int | float,
    width: int | float,
    height: int | float,
    js: str | None,
):
    script_idx = none_script_idx if js is None else add_field(STREAM_OBJ, content=js)

    return add_field(
        TEXT_OBJ,
        script_idx=script_idx,
        label=label,
        name=name if name else f"T_{obj_idx_ctr}",
        rect=f"{x} {y} {x + width} {y + height}",
    )


with open("frames/options.json", "r") as f:
    options = load(f)
    IN_ROWS = bool(options["rows"])

with open("frames/ffmpeg.json", "r") as f:
    ffmpeg_options = load(f)
    GRID_WIDTH = int(ffmpeg_options["width"])
    GRID_HEIGHT = int(ffmpeg_options["height"])
    FPS = int(ffmpeg_options["fps"])

if IN_ROWS:
    PX_WIDTH = 10
    PX_HEIGHT = 16
    PX_HEIGHT_OVERLAY = 8
else:
    PX_WIDTH = 16
    PX_HEIGHT = 16
    PX_HEIGHT_OVERLAY = 0

GRID_AREA_WIDTH = GRID_WIDTH * PX_WIDTH
GRID_AREA_HEIGHT = GRID_HEIGHT * (PX_HEIGHT - PX_HEIGHT_OVERLAY) + PX_HEIGHT_OVERLAY
GRID_OFF_X = 0
GRID_OFF_Y = 0

fields_text = ""
field_indexes = []
obj_idx_ctr = 50
none_script_idx = add_field(STREAM_OBJ, content="")


if not IN_ROWS:
    add_field(
        PLAYING_FIELD_OBJ,
        color="1",
        rect=f"{GRID_OFF_X} {GRID_OFF_Y} {GRID_OFF_X+GRID_WIDTH*PX_WIDTH} {GRID_OFF_Y+GRID_HEIGHT*PX_HEIGHT}",
    )

for y in range(GRID_HEIGHT):
    if IN_ROWS:
        add_text(
            "",
            f"R_{y}",
            0,
            GRID_OFF_Y + y * (PX_HEIGHT - PX_HEIGHT_OVERLAY),
            GRID_AREA_WIDTH,
            PX_HEIGHT,
            None
        )
        continue

    for x in range(GRID_WIDTH):
        add_field(
            PIXEL_OBJ,
            color="0",
            rect=f"{GRID_OFF_X+x*PX_WIDTH} {GRID_OFF_Y+y*PX_HEIGHT} {GRID_OFF_X+x*PX_WIDTH+PX_WIDTH} {GRID_OFF_Y+y*PX_HEIGHT+PX_HEIGHT}",
            x=x,
            y=y,
        )


add_button(
    "Play",
    "B_play",
    GRID_OFF_X + GRID_AREA_WIDTH // 2 - 50,
    GRID_OFF_Y + GRID_AREA_HEIGHT // 2 - 50,
    100,
    100,
    guard_script("onInit();"),
)

add_button(
    "Pause/Resume",
    "B_pause_resume",
    GRID_OFF_X,
    GRID_OFF_Y + GRID_AREA_HEIGHT,
    GRID_AREA_WIDTH // 2,
    20,
    guard_script("onPauseResume();"),
)

add_button(
    "Next Frame",
    "B_next_frame",
    GRID_OFF_X + GRID_AREA_WIDTH // 2,
    GRID_OFF_Y + GRID_AREA_HEIGHT,
    GRID_AREA_WIDTH // 2,
    20,
    guard_script("onNextFrame();"),
)

add_text(
    "",
    "T_stat",
    GRID_OFF_X,
    GRID_OFF_Y + GRID_AREA_HEIGHT + 20,
    GRID_AREA_WIDTH,
    20,
    "",
)

with open("js/out/bad.js", "r") as f:
    pdf_js = f.read()

filled_pdf = format(
    PDF_FILE_TEMPLATE,
    fields=fields_text,
    javascript=guard_script(pdf_js),
    field_list=" ".join([f"{i} 0 R" for i in field_indexes]),
    grid_width=GRID_WIDTH,
    grid_height=GRID_HEIGHT,
    fps=FPS,
    page_width=GRID_AREA_WIDTH + GRID_OFF_X * 2,
    page_height=GRID_AREA_HEIGHT + GRID_OFF_Y * 2 + 40,
)

with open("bad.pdf", "w") as f:
    f.write(filled_pdf)
