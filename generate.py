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


18 0 obj
<<
  /JS 43 0 R
  /S /JavaScript
>>
endobj


43 0 obj
<< >>
stream



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
      0.8
    ]
    /BC [
      0 0 0
    ]
  >>
  /Border [ 0 0 1 ]
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
      0.5 0.5 0.5
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
      /HeBo 10 0 R
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
/HeBo 12 Tf
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

# p1 = PIXEL_OBJ.replace("###IDX###", "50 0").replace("###COLOR###","1 0 0").replace("###RECT###", "460 700 480 720")

with open("frames/options.json", "r") as optfile:
    options = load(optfile)
    GRID_WIDTH = int(options["width"])
    GRID_HEIGHT = int(options["height"])
    FPS = int(options["fps"])

PX_SIZE = 16
GRID_OFF_X = 0
GRID_OFF_Y = 0

fields_text = ""
field_indexes = []
obj_idx_ctr = 50


def add_field(field):
    global fields_text, field_indexes, obj_idx_ctr
    fields_text += field
    field_indexes.append(obj_idx_ctr)
    obj_idx_ctr += 1


# Playing field outline
playing_field = PLAYING_FIELD_OBJ
playing_field = playing_field.replace("###IDX###", f"{obj_idx_ctr} 0")
playing_field = playing_field.replace(
    "###RECT###",
    f"{GRID_OFF_X} {GRID_OFF_Y} {GRID_OFF_X+GRID_WIDTH*PX_SIZE} {GRID_OFF_Y+GRID_HEIGHT*PX_SIZE}",
)
add_field(playing_field)

for x in range(GRID_WIDTH):
    for y in range(GRID_HEIGHT):
        # Build object
        pixel = PIXEL_OBJ
        pixel = pixel.replace("###IDX###", f"{obj_idx_ctr} 0")
        c = [0, 0, 0]
        pixel = pixel.replace("###COLOR###", f"{c[0]} {c[1]} {c[2]}")
        pixel = pixel.replace(
            "###RECT###",
            f"{GRID_OFF_X+x*PX_SIZE} {GRID_OFF_Y+y*PX_SIZE} {GRID_OFF_X+x*PX_SIZE+PX_SIZE} {GRID_OFF_Y+y*PX_SIZE+PX_SIZE}",
        )
        pixel = pixel.replace("###X###", f"{x}")
        pixel = pixel.replace("###Y###", f"{y}")

        add_field(pixel)


def add_button(label, name, x, y, width, height, js):
    script = STREAM_OBJ
    script = script.replace("###IDX###", f"{obj_idx_ctr} 0")
    script = script.replace("###CONTENT###", js)
    add_field(script)

    ap_stream = BUTTON_AP_STREAM
    ap_stream = ap_stream.replace("###IDX###", f"{obj_idx_ctr} 0")
    ap_stream = ap_stream.replace("###TEXT###", label)
    ap_stream = ap_stream.replace("###WIDTH###", f"{width}")
    ap_stream = ap_stream.replace("###HEIGHT###", f"{height}")
    add_field(ap_stream)

    button = BUTTON_OBJ
    button = button.replace("###IDX###", f"{obj_idx_ctr} 0")
    button = button.replace("###SCRIPT_IDX###", f"{obj_idx_ctr-2} 0")
    button = button.replace("###AP_IDX###", f"{obj_idx_ctr-1} 0")
    # button = button.replace("###LABEL###", label)
    button = button.replace("###NAME###", name if name else f"B_{obj_idx_ctr}")
    button = button.replace("###RECT###", f"{x} {y} {x + width} {y + height}")
    add_field(button)


def add_text(label, name, x, y, width, height, js):
    script = STREAM_OBJ
    script = script.replace("###IDX###", f"{obj_idx_ctr} 0")
    script = script.replace("###CONTENT###", js)
    add_field(script)

    text = TEXT_OBJ
    text = text.replace("###IDX###", f"{obj_idx_ctr} 0")
    text = text.replace("###SCRIPT_IDX###", f"{obj_idx_ctr-1} 0")
    text = text.replace("###LABEL###", label)
    text = text.replace("###NAME###", name)
    text = text.replace("###RECT###", f"{x} {y} {x + width} {y + height}")
    add_field(text)


add_button(
    "Play",
    "B_play",
    GRID_OFF_X + (GRID_WIDTH * PX_SIZE) // 2 - 50,
    GRID_OFF_Y + (GRID_HEIGHT * PX_SIZE) // 2 - 50,
    100,
    100,
    "onInit();",
)

add_button(
    "Pause/Resume",
    "B_pause_resume",
    GRID_OFF_X,
    GRID_OFF_Y + GRID_HEIGHT * PX_SIZE,
    GRID_WIDTH * PX_SIZE // 2,
    20,
    "onPauseResume();",
)

add_button(
    "Next Frame",
    "B_next_frame",
    GRID_OFF_X + (GRID_WIDTH * PX_SIZE) // 2,
    GRID_OFF_Y + GRID_HEIGHT * PX_SIZE,
    GRID_WIDTH * PX_SIZE // 2,
    20,
    "onNextFrame();",
)

add_text(
    "",
    "T_stat",
    GRID_OFF_X,
    GRID_OFF_Y + GRID_HEIGHT * PX_SIZE + 20,
    GRID_WIDTH * PX_SIZE,
    20,
    "",
)

filled_pdf = PDF_FILE_TEMPLATE.replace("###FIELDS###", fields_text)

with open("js/out/bad.js", "r") as jsfile:
    filled_pdf = filled_pdf.replace(
        "###JAVASCRIPT###",
        "try{" + jsfile.read() + "}catch(error){app.alert(String(error))}",
    )

filled_pdf = filled_pdf.replace(
    "###FIELD_LIST###", " ".join([f"{i} 0 R" for i in field_indexes])
)
filled_pdf = filled_pdf.replace("###GRID_WIDTH###", f"{GRID_WIDTH}")
filled_pdf = filled_pdf.replace("###GRID_HEIGHT###", f"{GRID_HEIGHT}")
filled_pdf = filled_pdf.replace("###FPS###", f"{FPS}")
filled_pdf = filled_pdf.replace(
    "###PAGE_WIDTH###", f"{GRID_WIDTH * PX_SIZE + GRID_OFF_X * 2}"
)
filled_pdf = filled_pdf.replace(
    "###PAGE_HEIGHT###", f"{GRID_HEIGHT * PX_SIZE + GRID_OFF_Y * 2 + 40}"
)

with open("bad.pdf", "w") as pdffile:
    pdffile.write(filled_pdf)
