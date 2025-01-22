from json import load
import pikepdf as pdf
from typing import Callable, Protocol, runtime_checkable


class Context[T]:
    def __init__(self, enter: Callable[[], T], exit: Callable[[], None]):
        self._enter = enter
        self._exit = exit

    def __enter__(self):
        return self._enter()

    def __exit__(self, exc_type, exc, traceback):
        self._exit()


@runtime_checkable
class SupportsStr(Protocol):
    def __str__(self) -> str: ...


@runtime_checkable
class SupportsBytes(Protocol):
    def __bytes__(self) -> bytes: ...


type Token = pdf.Object | SupportsStr | SupportsBytes


def unparseToken(i: Token):
    if isinstance(i, pdf.Object):
        return i.unparse()
    if isinstance(i, SupportsBytes):
        return bytes(i)
    return str(i).encode()


class Graphics:
    def __init__(self):
        self.cmd = []

    def push_state(self):
        self += ("q",)
        return self

    def pop_state(self):
        self += ("Q",)

    def state(self):
        return Context(self.push_state, self.pop_state)

    def set_gray_fill(self, gray: Token):
        self += (gray, "g")

    def set_gray_stroke(self, gray: Token):
        self += (gray, "G")

    def rectangle(self, x: Token, y: Token, width: Token, height: Token):
        self += (x, y, width, height, "re")

    def fill_non_zero(self):
        self += ("f",)

    def begin_text(self):
        self += ("BT",)
        return self

    def end_text(self):
        self += ("ET",)

    def text(self):
        return Context(self.begin_text, self.end_text)

    def set_font(self, name: pdf.Name, size: Token):
        self += (name, size, "Tf")

    def move_to_next_line_start(
        self,
        offset: tuple[Token, Token] | None = None,
    ):
        if offset is None:
            self += ("T*",)
        else:
            self += (*offset, "Td")

    def show_text(self, text: Token):
        if isinstance(text, str):
            text = pdf.String(text)

        self += (text, "Tj")

    def __iadd__(self, other: tuple[Token, ...]):
        self.cmd.append(b" ".join(unparseToken(i) for i in other))
        return self

    def __bytes__(self):
        return b"\n".join(self.cmd)

    def __str__(self) -> str:
        return bytes(self).decode()


class Document:
    def __init__(self, page_width: int | float, page_height: int | float) -> None:
        self.doc = pdf.Pdf.new()
        self.doc.Root["/AcroForm"] = pdf.Dictionary(Fields=[])
        self.page = self.doc.add_blank_page(page_size=(page_width, page_height))
        self.page["/Annots"] = []

        with open("bw.pfb", "rb") as f:
            bw = f.read()

        self.bw = self.doc.make_indirect(
            pdf.Dictionary(
                Type=pdf.Name("/Font"),
                Subtype=pdf.Name("/Type1"),
                BaseFont=pdf.Name("/BW"),
                FirstChar=ord(" "),
                LastChar=ord("!"),
                Widths=[1000, 1000],
                FontDescriptor=self.doc.make_indirect(
                    pdf.Dictionary(
                        Type=pdf.Name("/FontDescriptor"),
                        FontName=pdf.Name("/BW"),
                        Flags=(1 << 0) | (1 << 6),
                        FontBBox=pdf.Rectangle(0, 0, 1000, 1000),
                        ItalicAngle=0,
                        Ascent=500,
                        Descent=-500,
                        CapHeight=500,
                        StemV=500,
                        FontFile=pdf.Stream(
                            self.doc,
                            bw,
                            Length1=880,
                            Length2=1074,
                            Length3=535,
                        ),
                    )
                ),
            )
        )

        self.page.add_resource(self.bw, pdf.Name("/Font"), pdf.Name("/BW"))

        self.f1 = self.doc.make_indirect(
            pdf.Dictionary(
                Type=pdf.Name("/Font"),
                Subtype=pdf.Name("/Type1"),
                BaseFont=pdf.Name("/Courier"),
            )
        )

        self.page.add_resource(self.f1, pdf.Name("/Font"), pdf.Name("/F1"))

        self.doc.trailer["/Info"] = self.doc.make_indirect(
            pdf.Dictionary(
                Title="bad.pdf",
                Creator="https://github.com/esdmr/badpdf generate.py v2",
                Producer=f"pikepdf v{pdf.__version__}",
                Trapped=pdf.Name("/False"),
            )
        )

    def add_field(self, obj: pdf.Object):
        obj = self.doc.make_indirect(obj)
        self.doc.Root["/AcroForm"]["/Fields"].append(obj)
        self.page["/Annots"].append(obj)
        return obj

    def add_script(self, js: str):
        js = "try{" + js + "}catch(error){app.alert(String(error))}"

        return pdf.Dictionary(
            S=pdf.Name("/JavaScript"),
            JS=pdf.Stream(self.doc, js.encode()),
        )

    def set_open_action(self, js: pdf.Object | None):
        self.doc.Root["/OpenAction"] = js

    def add_button(
        self,
        *,
        label: str,
        name: str,
        rect: pdf.Rectangle,
        js: pdf.Object | None,
    ):
        ap = Graphics()

        with ap.state():
            ap.set_gray_fill(0.75)
            ap.rectangle(0, 0, rect.width, rect.height)
            ap.fill_non_zero()

        with ap.state():
            with ap.text():
                ap.set_font(pdf.Name("/F1"), 12)
                ap.set_gray_fill(0)
                ap.move_to_next_line_start((10, 8))
                ap.show_text(label)

        return self.add_field(
            pdf.Dictionary(
                Type=pdf.Name("/Annot"),
                Subtype=pdf.Name("/Widget"),
                FT=pdf.Name("/Btn"),
                Ff=1 << 16,
                T=name,
                Rect=rect,
                MK=pdf.Dictionary(
                    BG=[0.75],
                    CA=label,
                ),
                AP=pdf.Dictionary(
                    N=pdf.Stream(
                        self.doc,
                        bytes(ap),
                        BBox=pdf.Rectangle(0, 0, rect.width, rect.height),
                        FormType=1,
                        Matrix=pdf.Matrix().as_array(),
                        Resources=pdf.Dictionary(
                            Font=pdf.Dictionary(
                                F1=self.f1,
                            ),
                            ProcSet=[
                                pdf.Name("/PDF"),
                                pdf.Name("/Text"),
                            ],
                        ),
                    ),
                ),
                A=js,
                P=self.page.obj,
            )
        )

    def add_text(
        self,
        *,
        default_value: str,
        name: str | None,
        rect: pdf.Rectangle,
        js: pdf.Object | None,
        font_name: pdf.Name = pdf.Name("/F1"),
        font_obj: pdf.Object | None = None,
    ):
        da = Graphics()
        da.set_gray_fill(0)
        da.set_font(font_name, rect.height)

        ap = Graphics()

        with ap.state():
            with ap.text():
                ap.set_font(font_name, rect.height)
                ap.set_gray_fill(0)
                ap.move_to_next_line_start()
                ap.show_text(default_value)

        return self.add_field(
            pdf.Dictionary(
                Type=pdf.Name("/Annot"),
                Subtype=pdf.Name("/Widget"),
                FT=pdf.Name("/Tx"),
                T=name,
                V=default_value,
                DA=str(da),
                AP=pdf.Dictionary(
                    N=pdf.Stream(
                        self.doc,
                        bytes(ap),
                        BBox=pdf.Rectangle(0, 0, rect.width, rect.height),
                        FormType=1,
                        Matrix=pdf.Matrix().as_array(),
                        Resources=pdf.Dictionary(
                            Font=pdf.Dictionary({str(font_name): font_obj or self.f1}),
                            ProcSet=[
                                pdf.Name("/PDF"),
                                pdf.Name("/Text"),
                            ],
                        ),
                    ),
                ),
                AA=pdf.Dictionary(
                    K=js,
                ),
                Rect=rect,
                P=self.page.obj,
            )
        )

    def add_row(
        self,
        *,
        y: int,
        rect: pdf.Rectangle,
    ):
        return self.add_text(
            default_value="",
            name=f"R_{y}",
            rect=rect,
            font_name=pdf.Name("/BW"),
            font_obj=self.bw,
            js=None,
        )

    def add_playing_field(self, *, color: float, rect: pdf.Rectangle):
        return self.add_field(
            pdf.Dictionary(
                Type=pdf.Name("/Annot"),
                Subtype=pdf.Name("/Widget"),
                FT=pdf.Name("/Btn"),
                Ff=1 << 0,
                T="playing_field",
                Rect=rect,
                MK=pdf.Dictionary(
                    BG=[color],
                ),
                P=self.page.obj,
            )
        )

    def add_pixel(self, *, color: float, rect: pdf.Rectangle, x: int, y: int):
        return self.add_field(
            pdf.Dictionary(
                Type=pdf.Name("/Annot"),
                Subtype=pdf.Name("/Widget"),
                FT=pdf.Name("/Btn"),
                Ff=1 << 0,
                T=f"P_{x}_{y}",
                Rect=rect,
                MK=pdf.Dictionary(
                    BG=[color],
                ),
                P=self.page.obj,
            )
        )


def rectangle(x: float, y: float, width: float, height: float):
    return pdf.Rectangle(x, y, x + width, y + height)


with open("frames/options.json", "r") as f:
    options = load(f)
    IN_ROWS = bool(options["rows"])

with open("frames/ffmpeg.json", "r") as f:
    ffmpeg_options = load(f)
    GRID_WIDTH = int(ffmpeg_options["width"])
    GRID_HEIGHT = int(ffmpeg_options["height"])
    FPS = int(ffmpeg_options["fps"])

if IN_ROWS:
    PX_WIDTH = 16
    PX_HEIGHT = 16
    PX_HEIGHT_OVERLAY = 2
else:
    PX_WIDTH = 16
    PX_HEIGHT = 16
    PX_HEIGHT_OVERLAY = 0

GRID_AREA_WIDTH = GRID_WIDTH * PX_WIDTH
GRID_AREA_HEIGHT = GRID_HEIGHT * (PX_HEIGHT - PX_HEIGHT_OVERLAY) + PX_HEIGHT_OVERLAY
GRID_OFF_X = 0
GRID_OFF_Y = 0

doc = Document(GRID_AREA_WIDTH + GRID_OFF_X * 2, GRID_AREA_HEIGHT + GRID_OFF_Y * 2 + 40)

if not IN_ROWS:
    doc.add_playing_field(
        color=1.0,
        rect=rectangle(
            GRID_OFF_X,
            GRID_OFF_Y,
            GRID_WIDTH * PX_WIDTH,
            GRID_HEIGHT * PX_HEIGHT,
        ),
    )

for y in range(GRID_HEIGHT):
    if IN_ROWS:
        doc.add_row(
            y=y,
            rect=rectangle(
                GRID_OFF_X,
                GRID_OFF_Y + y * (PX_HEIGHT - PX_HEIGHT_OVERLAY),
                GRID_AREA_WIDTH,
                PX_HEIGHT,
            ),
        )
        continue

    for x in range(GRID_WIDTH):
        doc.add_pixel(
            color=0.0,
            rect=rectangle(
                GRID_OFF_X + x * PX_WIDTH,
                GRID_OFF_Y + y * PX_HEIGHT,
                PX_WIDTH,
                PX_HEIGHT,
            ),
            x=x,
            y=y,
        )


doc.add_button(
    label="Play",
    name="B_play",
    rect=rectangle(
        GRID_OFF_X + GRID_AREA_WIDTH // 2 - 50,
        GRID_OFF_Y + GRID_AREA_HEIGHT // 2 - 50,
        100,
        100,
    ),
    js=doc.add_script("onInit();"),
)

doc.add_button(
    label="Pause/Resume",
    name="B_pause_resume",
    rect=rectangle(
        GRID_OFF_X,
        GRID_OFF_Y + GRID_AREA_HEIGHT,
        GRID_AREA_WIDTH // 2,
        20,
    ),
    js=doc.add_script("onPauseResume();"),
)

doc.add_button(
    label="Next Frame",
    name="B_next_frame",
    rect=rectangle(
        GRID_OFF_X + GRID_AREA_WIDTH // 2,
        GRID_OFF_Y + GRID_AREA_HEIGHT,
        GRID_AREA_WIDTH // 2,
        20,
    ),
    js=doc.add_script("onNextFrame();"),
)

doc.add_text(
    default_value="",
    name="T_stat",
    rect=rectangle(
        GRID_OFF_X,
        GRID_OFF_Y + GRID_AREA_HEIGHT + 20,
        GRID_AREA_WIDTH,
        20,
    ),
    js=None,
)

with open("js/out/bad.js", "r") as f:
    doc.set_open_action(doc.add_script(f.read()))

doc.doc.save(
    "bad.pdf",
    preserve_pdfa=False,
    object_stream_mode=pdf.ObjectStreamMode(pdf.ObjectStreamMode.generate),
    normalize_content=True,
    deterministic_id=True,
)
