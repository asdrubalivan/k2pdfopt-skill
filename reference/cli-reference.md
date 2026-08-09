# k2pdfopt CLI reference (auto-generated)

<!-- source_binary: /Users/asdrubalivan/.local/bin/k2pdfopt -->
<!-- source_mtime: 1750712294.5636837 -->

Captured from: `k2pdfopt v2.55 (w/MuPDF,DjVuLibre,OCR) (c) 2023, GPLv3, http://willus.com`

This file is generated directly from the installed k2pdfopt binary's own
help output -- it is the source of truth for exact flag names, current
defaults, and which device profiles this specific build ships with. Do
not hand-edit; SKILL.md regenerates it automatically when
`source_mtime` above no longer matches the resolved binary.

## Device profiles (`-dev ?`)

Prefer an exact alias below over manual `-w`/`-h`/`-dpi` geometry.
If the user's exact device isn't listed, pick the closest resolution
match, or fall back to manual geometry using the device's real panel
spec -- see `decision-guide.md`.

```
Available devices:
    Kindle 1-5 (alias k2): 560 x 735, 167 dpi
        Mark corners=1, Padding (l,t,r,b)=0,0,3,4

    Kindle DX (alias dx): 800 x 1180, 167 dpi
        Mark corners=1, Padding (l,t,r,b)=0,0,0,0

    Kindle Paperwhite (alias kpw): 658 x 889, 212 dpi
        Mark corners=1, Padding (l,t,r,b)=0,0,3,4

    Kindle Paperwhite 2 (alias kp2): 718 x 965, 212 dpi
        Mark corners=1, Padding (l,t,r,b)=0,0,3,4

    Kindle Paperwhite 3 (alias kp3): 1016 x 1364, 300 dpi
        Mark corners=1, Padding (l,t,r,b)=0,0,3,4

    Kindle Voyage/PW3+/Oasis (alias kv): 1016 x 1364, 300 dpi
        Mark corners=1, Padding (l,t,r,b)=0,0,3,4

    Kindle Oasis 2 (alias ko2): 1200 x 1583, 300 dpi
        Mark corners=1, Padding (l,t,r,b)=0,0,3,4

    Pocketbook Basic 2 (alias pb2): 600 x 800, 167 dpi
        Mark corners=1, Padding (l,t,r,b)=0,0,3,4

    Nook Simple Touch (alias nookst): 552 x 725, 167 dpi
        Mark corners=1, Padding (l,t,r,b)=0,0,0,0

    Kobo Touch (alias kbt): 600 x 730, 167 dpi
        Mark corners=1, Padding (l,t,r,b)=0,0,3,4

    Kobo Glo (alias kbg): 758 x 942, 213 dpi
        Mark corners=1, Padding (l,t,r,b)=0,0,3,4

    Kobo Glo HD (alias kghd): 1072 x 1328, 250 dpi
        Mark corners=1, Padding (l,t,r,b)=0,0,3,4

    Kobo Glo HD Full Screen (alias kghdfs): 1072 x 1448, 250 dpi
        Mark corners=1, Padding (l,t,r,b)=0,0,3,4

    Kobo Mini (alias kbm): 600 x 730, 200 dpi
        Mark corners=1, Padding (l,t,r,b)=0,0,3,4

    Kobo Aura (alias kba): 758 x 932, 211 dpi
        Mark corners=1, Padding (l,t,r,b)=0,0,3,4

    Kobo Aura HD (alias kbhd): 1080 x 1320, 250 dpi
        Mark corners=1, Padding (l,t,r,b)=0,0,3,4

    Kobo H2O (alias kbh2o): 1080 x 1309, 265 dpi
        Mark corners=1, Padding (l,t,r,b)=0,0,3,4

    Kobo H2O Full Screen (alias kbh2ofs): 1080 x 1429, 265 dpi
        Mark corners=1, Padding (l,t,r,b)=0,0,3,4

    Kobo Aura One (alias kao): 1404 x 1713, 300 dpi
        Mark corners=0, Padding (l,t,r,b)=0,0,3,4

    Kobo Clara HD (alias koc): 1072 x 1317, 300 dpi
        Mark corners=0, Padding (l,t,r,b)=0,0,3,4

    Kobo Forma (alias kof): 1440 x 1745, 300 dpi
        Mark corners=0, Padding (l,t,r,b)=0,0,3,4

    Kobo Libra H2O (alias kol): 1264 x 1527, 300 dpi
        Mark corners=0, Padding (l,t,r,b)=0,0,3,4

    Nexus 7 (alias nex7): 1187 x 1811, 323 dpi
        Mark corners=1, Padding (l,t,r,b)=0,0,3,4


Press <ENTER> to exit.
```

## Full flag reference (`-?`)

```
k2pdfopt v2.55 (w/MuPDF,DjVuLibre,OCR) (c) 2023, GPLv3, http://willus.com
    Compiled Dec 26 2023 with CLang v17.0.6 for OS/X on ARM64.

usage:  k2pdfopt [opts] <input pdf/djvu | folder>

(Or just drag a PDF or DJVU (.djvu) file to this icon.)

Attempts to optimize PDF (or DJVU) files (especially two-column ones) for
display on the Kindle (or other mobile readers/smartphones) by looking for
rectangular regions in the file and re-paginating them without margins and
excess white space.  Works on any PDF or DJVU (.djvu) file, but assumes it
has a mostly-white background.  Native PDF files (not scanned) work best.

If given a folder, k2pdfopt first looks for bitmaps in the folder and if
any are found, converts those bitmaps to a PDF as if they were pages of a
PDF file.  If there are no bitmaps in the folder and if PDF files are in
the folder, then each PDF file will be converted in sequence.

Output files are always .pdf and have _k2opt added to the source name by
default (see -o option to specify alternate output name.)



Press <ENTER> to continue (q to quit).K2PDFOPT environment variable
-----------------------------
You can supply command-line options via the environment variable K2PDFOPT,
for example,

     set K2PDFOPT=-ui- -x -j 0 -m 0.25

Command line options from the command line take precedence over the ones in
the environment variable K2PDFOPT.














Press <ENTER> to continue (q to quit).Command Line Options
--------------------
-?[-] [pattern]   Show [don't show] usage only (no file processing).
                  If pattern is specified, only options with text matching
                  the pattern are shown.  The pattern can use * as a wild
                  card, e.g. -? -col.  Use -?- to turn off usage.
                  Combine with -ui- to get something you can redirect
                  to a file.
-a[-]             Turn on [off] text coloring (use of ANSI color codes) on
                  the screen output.  Default is on.
-ac[-] [<aggressiveness>]  Auto crop.  For books or papers that have dark edges
                  due to copying artifacts, this option will attempt to
                  automatically crop out those dark regions so that k2pdfopt
                  can correctly process the source file.  The <aggressiveness>
                  factor is from 0 to 1.  Higher is more aggressive cropping.
                  Default if not specified is 0.1.  See also -m.
                  Default value is off (-ac-).
                  Note that autocropping does not work on cropped regions
                  created with -cbox.  See -dw for a discussion about this.




Press <ENTER> to continue (q to quit).Command Line Options (cont'd)
-----------------------------
-as[-] [<maxdeg>] Attempt to automatically straighten tilted source pages.
                  Will rotate up to +/-<maxdegrees> degrees if a value is
                  specified, otherwise defaults to 4 degrees max.  Use -1 to
                  turn off. Default is off (-as -1 or -as-).
                  Note that autostraighten does not work on cropped regions.
                  See -dw for a discussion about this.
-author <author>   Set the author metadata / property of the PDF output
                  file(s). Default is to use the author of the source document
                  (-author "").
-bmp[-] <pageno>  Generate [do not generate] a bitmap rendering of converted
                  page number <pageno> and write it to file k2pdfopt_out.png.
                  If this option is used, no other files are written, i.e. the
                  complete conversion is NOT done--ONLY the bitmap file is
                  written.  If -sm is also specified, then the bitmap is of
                  marked source page <pageno>.  If -bmp-, then <pageno> is not
                  necessary.  Default is -bmp-.





Press <ENTER> to continue (q to quit).Command Line Options (cont'd)
-----------------------------
-bp[+|-|--] [m|<inches>] Break [do not break] output pages at end of each input
                  page.  Default is -bp-.  If a numeric value is put after -bp,
                  then rather than breaking the output page at the end of each
                  input page, a gap is inserted of that many inches, e.g.
                  -bp 1 will insert a 1-inch gap between contents of each
                  input page.  Special option -bp+ will break the pages at
                  the green boundaries between region as marked by the -sm
                  option (see -sm).  If bookmark information is available
                  and -toc is specified (on by default) page breaks will be
                  inserted in the converted file at each bookmark unless -bp--
                  is specified.  If "-bp m" is specified, then a page break
                  is inserted after each major (red-box) section.  This can
                  help prevent text selection overlap problems in native output
                  mode.  See also -toc, -bpl.
-bpc <nn>         Set the bits per color plane on the output device to <nn>.
                  The value of <nn> can be 1, 2, 4, or 8.  The default is 4
                  to match the kindle's display capability.  This is ignored
                  if the -jpg option is specified.



Press <ENTER> to continue (q to quit).Command Line Options (cont'd)
-----------------------------
-bpl <srcpagelist>   Insert page break in destination file before each source
                  file page listed in <srcpagelist>.  This has the same format
                  as the -p option.  See also -p, -bp, -toc, -toclist.  Default
                  is no page list.  Example:  -bpl 10,25,50,70,93,117,143.
                  This automatically sets -bp to it's default value (-bp-).
-bpm[<type>] <color>  Set a page break mark type and color.  This option allows
                  you to put colored marks in the PDF file to specify where to
                  break pages or where to avoid page breaks.  <type> is either
                  1 to force a page break or 2 to prevent a page break until
                  next mark.  <color> is an R,G,B triplet, 0-1 for each color
                  component, no spaces.  For example, to break the page
                  wherever the source file has a green dot or short green
                  horizontal line:  -bpm1 0,1,0.  Use <color> = -1 to clear.
                  If you omit the <type>, 1 is assumed.
-c[-]             Output in color [grayscale].  Default is grayscale.






Press <ENTER> to continue (q to quit).Command Line Options (cont'd)
-----------------------------
-cbox[<pagelist>|u|-] <cropbox>  Similar to the -grid option, but allows you to
                  specify exact crop boxes from the source page which will
                  then be processed as major (red-box) regions.  These regions
                  can then become individual output pages or can be processed
                  further (searched for columns, re-flowed, etc.) depending on
                  what other options are selected.  By default, they are
                  processed further, like every other major region.
                  You may specify the -cbox option multiple times to crop out
                  different parts of each source page, each crop being treated
                  as a major region.  See the -mode command.  To have each
                  crop box become a new page in the output file, for example,
                  use -mode crop, e.g.
                      k2pdfopt myfile.pdf -mode crop -cbox 2in,3in
                  <cropbox> has the format <left>,<top>,<width>,<height>
                  where all values are specified from the upper-left corner of
                  the source page, with units, like the -w and -h options,
                  except that the default units for -cbox are inches.  If only
                  <left> and <top> are specified, then <width> and <height>
                  extend to the edge of the page.
                  Example: -cbox 1in,1in,6in,9in (same as -cbox 1,1,6,9).

Press <ENTER> to continue (q to quit).Command Line Options (cont'd)
-----------------------------
                      This specifies a crop box that is 6 x 9 inches and which
                      has an upper left corner which is 1 inch from the left
                      and top of the source page.
                  Use -cbox- to clear all cropboxes, which defaults back to
                  processing every page without any crop boxes.
                  You can use a page list, <pagelist>, to specify on which
                  pages to apply the cropboxes.
                  Examples:
                      -cbox5-51o ... applies the cropbox on pages 5,7,9,...,51.
                                     ('o' = odd.  Use 'e' for even.)
                      -cbox1,2-5,13,15  ... applies the cropbox on pages 1,2,3,
                                            4,5,13, and 15.
                      -cboxc <cropbox> ... applies <cropbox> to the cover image.
                                           (see -ci option.)
                  Be sure not to put a space between -cbox and the page list.
                  Use -cboxu to set a crop box for all unspecified pages.
                  E.g. -cbox1-10 <cbox1> -cboxu <cbox2> will apply <cbox1> to
                  all pages 1 to 10 and <cbox2> to all other pages.
                  The default is no crop boxes (-cbox-).  See also -m, -ac.
                  USAGE NOTE:  Once you specify -cbox at least one time, only

Press <ENTER> to continue (q to quit).Command Line Options (cont'd)
-----------------------------
                  the crop boxes you specify (and any associated page ranges)
                  are processed/converted by k2pdfopt.  No other pages or
                  regions are processed.  So if you want to specify a special
                  cropbox for the first page, for example, but then have all
                  remaining pages treated entirely, you must specify this:
                      -cbox1 ...   -cboxu 0,0
                      (-cboxu 0,0 applies a full-page cropbox to all other
                        pages.  u = unspecified.)
                  The -cbox2- 0,0 will set the cropbox for pages 2 and beyond
                  to the full page size.
                  See also:  -ibox.
-cg <inches>      Minimum column gap width in inches for detecting multiple
                  columns.  Default = 0.1 inches.  Setting this too large
                  will give very poor results for multicolumn files.  See also
                  -cgmax.
-cgmax <inches>   Max allowed gap between columns in inches.  If the gap
                  between two regions exceeds this value, they will not be
                  considered as separate columns.  Default = 1.5.  Use -1 for
                  no limit (disable).  See also -cg.


Press <ENTER> to continue (q to quit).Command Line Options (cont'd)
-----------------------------
-cgr <range>      Set column-gap range, 0 - 1.  This is the horizontal range
                  over which k2pdfopt will search for a column gap, as a
                  fraction of the page width.  E.g. -cgr 0.5 will search
                  from 0.25 to 0.75 of the page width for a column gap.
                  Set this to a small value, e.g. 0.05, to only search for
                  column breaks in the middle of the page.  Default = 0.33.
-ch <inches>      Minimum column height in inches for detecting multiple
                  columns.  Default = 1.5 inches.
-ci[-] <imagefile>   Specify a cover image for the first page of the converted
                  PDF.  <imagefile> can be a bitmap file (png or jpg) or can be
                  a page from a PDF file, e.g. myfile.pdf[34] would use page 34
                  of myfile.pdf.  You can just specify an integer, e.g. -ci 50
                  to use page 50 of the source file being converted as the
                  cover page.  Default is -ci-, which is no cover image.
                  NOTE:  -ci only works with bitmapped output--it does not
                         (yet) work with native PDF output.
-cmax <max>       Set max contrast increase on source pages.  1.0 keeps
                  contrast from being adjusted.  Use a negative value to
                  specify a fixed contrast adjustment.  Def = 2.0.
                  See also -er.

Press <ENTER> to continue (q to quit).Command Line Options (cont'd)
-----------------------------
-col <maxcol>     Set max number of columns.  <maxcol> can be 1, 2, or 4.
                  Default is -col 2.  -col 1 disables column searching.
                  Columns will be displayed left to right unless -r is
                  specified, in which case they will be displayed right
                  to left.  You can use the -go option to override this.
















Press <ENTER> to continue (q to quit).Command Line Options (cont'd)
-----------------------------
-colorbg (or -colorfg) <hexcolor>|<bitmap>[,<hexcolor>|<bitmap>[,...]]
                  Map the color white (background color, for -colorbg) or the
                  color black (text color, for -colorfg) to <hexcolor>,
                  where <hexcolor> is a 6-digit hex RRGGBB representation of a
                  color, e.g. ffffff for all white, 000000 for all black,
                  ff0000 for bright red, etc.  If <hexcolor> is not a grayscale
                  color, the -c (color output) option will be turned on
                  automatically.  This option only works with bitmapped output
                  (not native--see -n).  Grayscale colors between black and
                  white will be linearly interpolated between the specified
                  -colorbg and -colorfg colors.  If the source document has
                  colors, only (mostly) grayscale pixels are affected if ! is
                  put before the color, e.g. -colorbg !ffffd0
                  A bitmap can also be specified, e.g. -colorbg myfile.jpg.
                  In this case, the bitmap gets tiled in as the background.
                  If you specify a comma delimited list of colors (or bitmaps),
                  then consecutive rows of text are colored with the
                  consecutive colors.  This is a possible way to make the
                  rows of text easier to follow, e.g. -colorfg ff0000,00 will
                  color alternate rows of text red and black.

Press <ENTER> to continue (q to quit).Command Line Options (cont'd)
-----------------------------
                  Default is -colorbg "" and -colorfg "" (no mappings).
-comax <range>    Stands for Column Offset Maximum.  The <range> given is as a
                  fraction of the width of a single column, and it specifies
                  how much the column divider can move around and still have
                  the columns considered contiguous.  Set to -1 to revert back
                  to how columns were treated in k2pdfopt v1.34 and before.
                  Default = 0.3.
-crgh <inches>    Set the min height of the blank area that separates regions
                  with different numbers of columns.  Default = 1/72 inch.
-d[-]             Turn on [off] dithering for bpc values < 8.  See -bpc.
                  Default is on.
-ddr[-]           Detect Double Rows.  [Expert mode.]  By default this is on.
                  Use -ddr- to turn off.  This option does extra analysis to
                  try and separate text rows by looking for double and triple
                  rows that may have been missed on the first pass.  This can
                  have the unintended consequence of breaking up figures
                  across pages.




Press <ENTER> to continue (q to quit).Command Line Options (cont'd)
-----------------------------
-de <size>        Defect size in points.  For scanned documents, marks
                  or defects smaller than this size are ignored when bounding
                  rectangular regions.  The period at the end of a sentence is
                  typically over 1 point in size.  The default is 1.0.
-dev <name>       Select device profile (sets width, height, dpi, and corner
                  marking for selected devices).  Currently the selection is
                  limited.  <name> just has to have enough characters to
                  uniquely pick the device.  Use -dev ? to list the devices.
                  Default is -dev kindle2.
-dpi <dpival>     Same as -odpi.
-dr <value>       Display resolution multiplier.  Default = 1.0.  Using a
                  value greater than 1 should improve the resolution of the
                  output file (but will make it larger in file size).
                  E.g. -dr 2 will double the output DPI, the device width
                  (in pixels), and the device height (in pixels).
-ds <factor>      Override the document size with a scale factor.  E.g. if
                  your PDF reader says the PDF file is 17 x 22 inches and
                  it should actually be 8.5 x 11 inches, use -ds 0.5.  Default
                  is 1.0.


Press <ENTER> to continue (q to quit).Command Line Options (cont'd)
-----------------------------
-dw[-] [<fitorder>] De-warp [do not de-warp] pages (uses Leptonica de-warp
                  algorithms).  Default is not to de-warp.  Does not work
                  for native mode output.  Optional <fitorder> specifies the
                  fit order for the dewarping curves.  Can be 2, 3, or 4.
                  Default is 4.
                  [Advanced: You can actually make the fit order a two-digit
                   code.  E.g. -dw 24 will use 4th-order on each row of text
                   but only 2nd-order for columns of displacement (see
                   leptonica dewarpFindVertDisparity() in dewarp2.c)]
                  Note: de-warping, like auto-straighten and auto-crop, is
                  intended for entire pages. It does not work on cropped areas.
                  If you want it to work on cropped areas, you should run
                  k2pdfopt in two passes--first to create selected crop
                  areas (e.g. -mode crop), then to apply dewarping.
-ehl <n>          Same as -evl, except erases horizontal lines instead of
                  vertical lines.  See -evl.  Default is -ehl 0.





Press <ENTER> to continue (q to quit).Command Line Options (cont'd)
-----------------------------
-er <n>           Use erosion filter on source bitmaps.  Makes the text look
                  darker.  A larger value of <n> makes the text thicker/darker.
                  Try -er 1 or -er 2.  Default is 0 (no erosion filtering).
                  Use a negative value for <n> to do the erosion before the
                  constrast adjustment is applied.  Use a positive value to
                  to the erosion after the constrast adjustment is applied.
                  This option may magnify scanning defects, so you might want
                  to combine with the -de (defect removal) option.
                  Has no effect in native mode output. See also -de, -g, -cmax.
-evl <n>          Detects and erases vertical lines in the source document
                  which may be keeping k2pdfopt from correctly separating
                  columns or wrapping text, e.g. column dividers.  If <n> is
                  zero, this is turned off (the default).  If <n> is 1, only
                  free-standing vertical lines are removed.  If <n> is 2,
                  vertical lines are erased even if they are the sides of
                  an enclosed rectangle or figure, for example.





Press <ENTER> to continue (q to quit).Command Line Options (cont'd)
-----------------------------
-f2p <val>        Fit-to-page option.  The quantity <val> controls fitting
                  tall or small contiguous objects (like figures or
                  photographs) to the device screen.  Normally these are fit
                  to the width of the device, but if they are too small or
                  too tall, then if <val>=10, for example, they are allowed
                  to be 10%% wider (if too small) or narrower (if too tall)
                  than the screen in order to fit better.  Use -1 to fit
                  a tall object entirely within the device screen no matter
                  what.  Use -2 as a special case--all "red-boxed" regions
                  (see -sm option) are placed one per page.
                  Use -f2p -3 to fit as many "red-boxed" regions as
                  possible on each page without breaking them across pages.
                  (see -mode concat).
                  Default is -f2p 0.  See also -jf, -fr.
                  Note:  -f2p -2 will automatically also set -vb -2 to
                  exactly preserve the spacing in the red-boxed region.  If
                  you want to compress the vertical spacing in the red-boxed
                  region, use -f2p -2 -vb -1.



Press <ENTER> to continue (q to quit).Command Line Options (cont'd)
-----------------------------
-fc[-]            For multiple column documents, fit [don't fit] columns to
                  the width of the reader screen regardless of -odpi.
                  Default is to fit the columns to the reader.
-fr[-]            Figure rotate--rotates wide-aspect-ratio figures to landscape
                  so that they best fit on the reader page.  Default is not
                  to rotate.  See also -f2p.
-fs <points>[+]   The output document is scaled so that the median font size in
                  the converted file is <points> points.  If the <points> value
                  is followed by a '+', the scaling is adjusted for every
                  source page, otherwise the font size is only adjusted once,
                  based on the median font size for the entire source document.
                  The default is -fs 0, which turns off scaling based on font
                  size.  The use of -fs overrides the -mag setting.
-g <gamma>        Set gamma value of output bitmaps. A value less than 1.0
                  makes the page darker and may make the font more readable.
                  Default is 0.5.  Has no effect with native-mode output.
                  See also -er, -cmax.




Press <ENTER> to continue (q to quit).Command Line Options (cont'd)
-----------------------------
-go <nn>          Grid order.  Override order of processing for a gridded page
                  (see -grid) or for multiple columns.  The following integer
                  codes are used:  1=left-to-right, 2=right-to-left,
                  3=top-to-bottom, 4=bottom-to-top.  So -go 13 will first go
                  left to right, starting at the top row and then working
                  towards the bottom row, row by row.  -go 31 will go top to
                  bottom starting with the left column and then working to the
                  right, column by column.  The default is 31 unless -r is
                  specified, in which case it is 32.  For multiple columns,
                  only 1 or 2 need be specified.











Press <ENTER> to continue (q to quit).Command Line Options (cont'd)
-----------------------------
-grid <C>x<R>[x<O>][+]  Grid the source page into <C> columns by <R> rows with
                  with <O> percent overlap.  No regard will be made for trying
                  to break the page between columns or rows of text.  If a +
                  is specified, the destination page order will go across and
                  then down, otherwise it will go down and then across.  To
                  turn off gridding, specify a zero value for the columns or
                  for the rows.  Default is no gridding.  The default overlap
                  is 2%%.  Example:  -grid 2x2x5.  By default, gridding also
                  sets the following options, which can be overridden by
                  following the grid option with other command options:
                  -n -wrap- -f2p -2 -vb -2 -col 1.  For example, if you want
                  a column search done on each grid piece, you can put this:
                  -grid 2x2 -col 2.  See also -go, -cbox.








Press <ENTER> to continue (q to quit).Command Line Options (cont'd)
-----------------------------
-gs[-][-]         Force use of Ghostscript instead of MuPDF to read PDFs.
                  K2pdfopt has built-in PDF translation (via the MuPDF
                  library) but will try to use Ghostscript if Ghostscript
                  is available and the internal (MuPDF) translation fails
                  (virtually never happens).  You can force Ghostscript to
                  be used with this -gs option.  Use -gs- to use Ghostscript
                  only if MuPDF fails.  Use -gs-- to never use Ghostscript.
                  Download ghostscript at http://www.ghostscript.com.
-gtc <inches>     Threshold value for detecting column gaps (expert mode).
                  Sets how many of the pixels in the column shaft can be
                  non-white (total height of a line crossing the shaft in
                  inches).  See also -gtr.  Default = .005.









Press <ENTER> to continue (q to quit).Command Line Options (cont'd)
-----------------------------
-gtr <inches>     Threshold for detecting gaps between rows (expert mode).
                  This option is commonly adjusted when lines of text in the
                  source file are too close together or slightly overlap and
                  don't have a clean gap between them.  It effectively sets
                  how clean that gap has to be in order for k2pdfopt to
                  consider that there are separate rows of text.  It does
                  this by setting the maximum total black pixels, in inches,
                  on average, that can be in each row of pixels before the gap
                  is no longer considered a gap.  A higher value makes it
                  easier to detect gaps between rows of text.  Too high of a
                  value may inadvertently split figures and other graphics.
                  For documents with nice clean spaces between each row of
                  text, this setting should not need to be adjusted.
                  Default = 0.006.  See also -rsf.
-gtw <inches>     Threshold for detecting word gaps (expert mode).
                  See -gtr.  Default = .0015.





Press <ENTER> to continue (q to quit).Command Line Options (cont'd)
-----------------------------
-h <height>[in|cm|s|t|p|x] Set height of output device in pixels, inches, cm,
                  source page size (s), trimmed source region size (t),
                  pixels (p), or relative to the OCR text layer (x).
                  The default units are pixels (p), and the default value
                  is 735 (the height of the Kindle 2 screen in pixels).
                  Examples:
                      -h 6.5in   Sets the device height to 6.5 in
                                 (using the output dpi to convert to
                                  pixels--see -dpi).
                      -h 1.5s    Sets the device height to 1.5 times the
                                 source page height (same as -h -1.5).
                      -h 1t      Sets the device height to whatever the
                                 trimmed page height is (you can follow
                                 -mode copy with -h 1t to make the output
                                 page height equal to the crop box height.
                      -h 0.5x    Sets the device height to half of the
                                 height of the box exactly surrounding
                                 the OCR text layer on the source page.
                  See also -w, -dpi, -dr.


Press <ENTER> to continue (q to quit).Command Line Options (cont'd)
-----------------------------
-hy[-]            Turn on [off] hyphen detection/elimination when wrapping
                  text.  Default is on.
-i                Echo information about the source file (PDF only).
                  Disables all other processing.
-ibox[<pagelist>|-|u] <cropbox>  Same as -cbox (see -cbox), except that these
                  boxes are ignored by k2pdfopt.  This is done by whiting out
                  the boxes in the source bitmap.  For native output, the
                  area in the -ibox will not affect the parsing of the source
                  file, but it may still be visible in the output file.
                  Default is no iboxes (-ibox-).  See also -cbox.
-idpi <dpi>       Set pixels per inch for input file.  Use a negative value
                  as a multiplier on the output dpi (e.g. -2 will set the
                  input file dpi to twice the output file dpi (see -odpi).
                  Default is -2.0.
-j -1|0|1|2[+/-]  Set output text justification.  0 = left, 1 = center,
                  2 = right.  Add a + to attempt full justification or a -
                  to explicitly turn it off.  The default is -1, which tells
                  k2pdfopt to try and maintain the justification of the
                  document as it is.  See also -wrap.


Press <ENTER> to continue (q to quit).Command Line Options (cont'd)
-----------------------------
-jf 0|1|2 [<inches>]  Set figure (tall region) justification.  If a figure
                  has left or right margins available, this option allows
                  you to set the justification differently than the text.
                  E.g. you can center figures with -jf 1.  If you want to
                  specify a minimum height for figures (e.g. minimum region
                  height where this justification applies), you can tack it
                  on at the end, e.g. -jf 1 1.5 to center any region taller
                  than 1.5 inches.  Default is 0.75 inches for the minimum
                  height and to use the same justification on figures as
                  the rest of the document (-jf -1).  See also -f2p to fit
                  small or tall figures to the page.
-jfc[-|+]         Attempt [do not attempt] to keep figure captions joined
                  with their figures.  If you specify -jfc+, k2pdfopt will
                  also try to detect figure captions in multi-column documents.
                  This is not done by default because k2pdfopt will sometimes
                  (more often than not, in my experience) incorrectly choose
                  the multi-column layout if it is also trying to detect what
                  is a figure caption.  See also -cg, -cgmax, -cgr, -crgh.
                  Default = -jfc.


Press <ENTER> to continue (q to quit).Command Line Options (cont'd)
-----------------------------
-jpg [<quality>]  Use JPEG compression in PDF file with quality level
                  <quality> (def=90).  A lower quality value will make your
                  file smaller.  See also -png. Use of -jpg is incompatible
                  with the -bpc option.
-l <lang>         See -ocrlang.
-lang <lang>      See -ocrlang.
-ls[-][pagelist]  Set output to be in landscape [portrait] mode.  The default
                  is -ls- (portrait).  If an optional pagelist is specified,
                  only those pages are affected--any other pages are done
                  oppositely.  E.g. -ls1,3,5-10 would make source pages 1, 3
                  and 5 through 10 landscape.










Press <ENTER> to continue (q to quit).Command Line Options (cont'd)
-----------------------------
-m[l|t|r|b] <val>[<units>][,<val>[units][,...]]  Set global crop margins for
                  every page.  If more than one value is given (comma-delimited
                  with no spaces in between), the order is left, top, right,
                  bottom, e.g. -m <left>,<top>,<right>,<bottom>.  You can also
                  use the more powerful -cbox option to do this same thing.
                  The default units are inches.  For available units and their
                  descriptions, see -h.
                  Examples:
                      -m 0.5cm
                         Sets all margins to 0.5 cm.
                      -m 0.5cm,1.0cm
                         Sets the left margin to 0.5 cm and all the other
                         margins to 1.0 cm.
                      -m 0.2in,0.5in,0.2in,0.5in
                         Sets the left and right crop margins to
                         0.2 inches and the top and bottom to 0.5 inches.
                      -mt 1cm
                         Sets the top margin to 0.5 cm.
                      -m -0.1x,-0.1x,1.1x,1.1x
                         With the 'x' unit, the behavior is a little

Press <ENTER> to continue (q to quit).Command Line Options (cont'd)
-----------------------------
                         different.  Rather than specifying the widths
                         of each margin, you specify the position of
                         the crop box relative to the OCR text layer
                         in the source file, where 0x,0x,1x,1x would
                         exactly bound the OCR text layer.
                  The default crop margins are 0 inches.
                  [NOTE: The default was 0.25 inches for all margins before
                         v1.65.]
                  See also -cbox and -ac to autocrop scanning artifacts.
-mag <value>      Magnify the converted document (text) size by <value>.
                  Default is -mag 1 (no magnification). See also -fs.
-mc[-]            Mark [don't mark] corners of the output bitmaps with a
                  small dot to prevent the reading device from re-scaling.
                  Default = mark.







Press <ENTER> to continue (q to quit).Command Line Options (cont'd)
-----------------------------
-mode <mode>      Shortcut for setting multiple options at once which
                  determine the basic way in which k2pdfopt will behave.
                  Available modes are:
                      copy   "Copy" mode.  This isn't really intended for
                             use with an e-reader.  It just creates a
                             bitmapped copy of your source document at the
                             exact same dimensions.  This can be useful in
                             order to eliminate any font compatibility
                             issues or if you want to eliminate selectable
                             text (follow with -mode copy with -ocr-).
                             The equivalent settings are -n- -wrap- -col 1
                             -vb -2 -w 1s -h 1s -dpi 150 -rt 0 -c -t- -f2p
                             -2 -m 0 -om 0 -pl 0 -pr 0 -pt 0 -pb 0 -mc-.
                             Use -odpi to select the bitmap resolution.
                             Note 1:  Use -mode copy -n if you want an exact
                                      copy (output in native mode).
                             Note 2:  The default gamma and contrast settings
                                      are not reset by -mode copy.  If you
                                      want a perfect copy, do this:
                                      -mode copy -gamma 1 -s- -cmax 1

Press <ENTER> to continue (q to quit).Command Line Options (cont'd)
-----------------------------
                      fp     "Fit Page" mode.  Also can use -mode fitpage.
                             Fits the entire contents of each source page
                             onto the reader display.  Same as -n -wrap- -col 1
                             -vb -2 -f2p -2 -t.
                      fw     "Fit Width" mode.  Fits the text to the width
                             of the reader in landscape mode without doing any
                             text re-flow.  This is the best way to preserve
                             the original layout of the source document.
                             To fit to the reader width in portrait mode, add
                             -ls- after -mode fw to turn off landscape.
                             The -mode fw option is equivalent to -n -wrap-
                             -col 1 -vb -2 -t -ls.  It was inspired by SoPDF's
                             "fit width" option.  Can also use -mode sopdf
                             or -mode fitwidth
                      2col   "Two-column" mode.  Same as -n -wrap- -col 2
                             -vb -2 -t.  Optimizes for a 2-column scientific
                             article with native PDF output.
                      tm     "Trim margins" mode.  Same as -mode copy, but
                             sets the output to be trimmed to the margins and
                             the width and height of the output to match the

Press <ENTER> to continue (q to quit).Command Line Options (cont'd)
-----------------------------
                             trimmed source pages.  Also uses native mode.
                             Equivalent to -n -wrap- -col 1 -vb -2 -f2p -2 -t
                             -w 1t -h 1t -rt 0 -c -m 0 -om 0 -pl 0 -pr 0 -pt 0
                             -pb 0 -mc-.  Can also use -mode trim.
                      crop   "Crop" mode.  Used with the -cbox option, this
                             puts each cropped area on a separate page,
                             untrimmed, and sizes the page to the cropped
                             region.  Same as -wrap- -col 1 -vb -2 -w 1t -h 1t
                             -t- -rt 0 -c -f2p -2 -m 0 -om 0 -pad 0 -mc- -n
                      concat "Concatenation" mode.  Similar to -mode crop,
                             but keeps the output pages the same size as the
                             source pages and fits as many crop-boxed regions
                             onto each new output page as possible without
                             breaking them across pages.  Equivalent to: -n
                             -wrap- -col 1 -vb -2 -t- -f2p -3 -fc- -w 1s -h 1s
                             -ocr-
                      def    "Default" mode. This is the mode you get if you
                             run k2pdfopt with no customized options.  It is
                             equivalent to -wrap -n- -col 2 -ocr m -vb 1.75
                             -dev k2 -rt auto -c- -t -f2p 0 -m 0 -om 0.02 -ls-

Press <ENTER> to continue (q to quit).Command Line Options (cont'd)
-----------------------------
                  You can modify modes by overriding their options after
                  specifying the mode, e.g. -mode fw -vb -1.



















Press <ENTER> to continue (q to quit).Command Line Options (cont'd)
-----------------------------
-n[-]             Use "native" PDF output format.  NOTE: if you want native
                  PDF output, it's probably best to use a -mode option like
                  -mode fitwidth or -mode 2col, both of which automatically
                  turn on native PDF output and optimize other settings for it.
                  Native PDF output preserves the native source PDF contents,
                  i.e. the output PDF file is not rendered as a sequence of
                  bitmapped pages like in the default k2pdfopt output mode.
                  Instead, the source PDF's native content is used along with
                  additional PDF instructions to translate, scale, and crop
                  the source content.  With native PDF output, if the source
                  file has selectable text, the text remains selectable in
                  the output file.  The output file can also be zoomed
                  without loss of fidelity.  This may also result in a
                  smaller output file (but not always).  By default, native
                  PDF output format is turned off.  See also -mode.
                  NOTES:
                  1. Native PDF output cannot be used with text wrapping
                     on (see -wrap option).  Turning it on will disable
                     text wrapping.
                  2. Native PDF output is not recommended for source

Press <ENTER> to continue (q to quit).Command Line Options (cont'd)
-----------------------------
                     files which are scanned (there is no benefit unless
                     the scanned document includes a layer of OCR text).
                  3. Native PDF output is incompatible with OCR (see -ocr),
                     though OCR is typically not necessary if the native PDF
                     contents are kept.  Turning on native PDF output will
                     disable OCR.
                  4. Native PDF output can only be used with PDF source
                     files (it does not work with DJVU source files).
                  5. Contrast adjust, gamma correction, and sharpening
                     are disabled with native PDF output.
                  6. It is recommended that you use -vb -2 with native PDF
                     output, particularly if you are having difficulty
                     selecting/searching text in the output PDF file.
                  7. This option works well with -mode fw, -mode 2col, or
                     with the -grid option.  It is used by default in those
                     cases.





Press <ENTER> to continue (q to quit).Command Line Options (cont'd)
-----------------------------
-neg[-|+]         Inverse [don't inverse] the output images (white letters
                  on black background, or "night mode").  If -neg+, inverts
                  all graphics no matter what.  If just -neg, attempts to
                  invert text only and not figures.  Default = -neg-.
                  See also -colorbg and -colorfg.
-ng <gap>         Set gap between notes and main text in the output document.
                  The <gap> defaults to inches but can have other units (see
                  -h, for example).  See -nl and -nr for how to turn on notes
                  processing.  Default is -ng 0.2.
-nl[<pages>] [<leftbound>,<rightbound>]











Press <ENTER> to continue (q to quit).Command Line Options (cont'd)
-----------------------------
-nr[<pages>] [<leftbound>,<rightbound>]
                  The source document has notes in the left (-nl) or right
                  (-nr) margins.  Specific pages can be specified for the
                  notes using <pages> (same format as -cbox or -p).  If
                  <leftbound>,<rightbound> are specified, they specify the
                  fraction of the page width where to look for the break
                  between the notes and the main page.  E.g.
                  -nl 0.15,0.25 will look for the boundary between the notes
                  and the text between 15%% and 25%% of the way across the
                  source page.  Use -nl- to turn off all processing of notes
                  in the margins (default).  Default values for <leftbound>
                  and <rightbound> are 0.05 to 0.35 for -nl and 0.65 to 0.95
                  for -nr.
                  Notes in the margins are treated differently than other
                  "columns" of text.   They will be interspersed with the
                  text in the adjacent column of main text.
                  Note that -nr... or -nl... will also set -cg to 0.05.




Press <ENTER> to continue (q to quit).Command Line Options (cont'd)
-----------------------------
-nt <nthreads>    Use <nthreads> parallel threads when OCR-ing a document
                  with the Tesseract OCR engine (GOCR is not thread safe).
                  This may provide a significant processing speed improvement
                  when using Tesseract OCR.  Note that a higher number is not
                  always faster.  You should experiment with your system to
                  find the optimum.  A negative value is interpreted as a
                  percentage of available CPUs.  The default is -50, which
                  tells k2pdfopt to use half of the available CPU threads.
                  Some performances I measured:
                  ----------------------------------------------------------
                                                               OCR Speed
                     O/S           CPU         Nthreads       improvement
                  ----------------------------------------------------------
                  Win 10 x64     Core i5      2 (default)        1.5x
                  Win 10 x64     Core i5          3              1.6x
                  Win 10 x64     Core i5          4              1.8x
                  ----------------------------------------------------------
                  Win 10 x64     Core i7          2              1.8x
                  Win 10 x64     Core i7          3              2.4x
                  Win 10 x64     Core i7      4 (default)        2.5x

Press <ENTER> to continue (q to quit).Command Line Options (cont'd)
-----------------------------
                  Win 10 x64     Core i7          5              2.8x
                  Win 10 x64     Core i7          6              2.7x
                  Win 10 x64     Core i7          7              2.7x
                  Win 10 x64     Core i7          8              2.6x
                  ----------------------------------------------------------
                  Linux x64      Core i5      2 (default)        1.9x
                  Linux x64      Core i5          3              2.6x
                  Linux x64      Core i5          4              2.7x
                  ----------------------------------------------------------
                  Linux x64   Xeon E52690v2       2              1.9x
                  Linux x64   Xeon E52690v2       4              3.5x
                  Linux x64   Xeon E52690v2       6              5.1x
                  Linux x64   Xeon E52690v2       8              6.6x
                  Linux x64   Xeon E52690v2   10 (default)       8.7x
                  Linux x64   Xeon E52690v2      14              9.5x
                  Linux x64   Xeon E52690v2      20             10.2x
                  ----------------------------------------------------------
                  Interestingly, Linux seems to have much better multithreading
                  performance than Windows.  I suspect the OS/X results are
                  similar to the Linux results.

Press <ENTER> to continue (q to quit).Command Line Options (cont'd)
-----------------------------
                  NOTE:  -nt has no effect if you select -ocrd c or -ocrd p.
                         See -ocrd.



















Press <ENTER> to continue (q to quit).Command Line Options (cont'd)
-----------------------------
-o <namefmt>      Set the output file name using <namefmt>.  %s will be
                  replaced with the full name of the source file minus the
                  extension.  %b will be replaced by the base name of the
                  source file minus the extension.  %f will be replaced with
                  the folder name of the source file.  %d will be replaced with
                  the source file count (starting with 1).  The .pdf extension
                  will be appended if you don't specify an extension.
                  E.g. -o out%04d.pdf will result in output files out0001.pdf,
                  out0002.pdf, ... for the converted files.  Def = %s_k2opt
                  -------------------------------------------------------------
                  BITMAP OUTPUT:  For output to bitmaps, you can put -o .png
                  or -o .jpg (see -jpeg for quality setting).
                  -------------------------------------------------------------
                  MORE DETAIL:  If <namefmt> ends in .jpg or .png, the output
                  will be in the JPEG or PNG bitmap format, respectively, one
                  bitmap per page.  If your <namefmt> has no %d in it, then
                  %04d will be appended.  If <namefmt> has only one %d, it will
                  get substituted with the page number.  If it has two %d's,
                  the first will get the file count and the second will get the
                  page number.  Example: if the source PDF is myfile.pdf, then

Press <ENTER> to continue (q to quit).Command Line Options (cont'd)
-----------------------------
                  -o %s%03d.png would create myfile001.png, myfile002.png,
                  etc., for each page of the PDF.



















Press <ENTER> to continue (q to quit).Command Line Options (cont'd)
-----------------------------
-ocr[-] [g|t|m]   Attempt [don't attempt] to use optical character
                  recognition (OCR) in order to embed searchable text into
                  the output PDF document.  If followed by t or g, specifies
                  the ocr engine to use (tesseract or gocr).  If followed by
                  m, and if the PDF document has text in it, then the MuPDF
                  engine is used to extract the text (sort of a virtual OCR).
                  If -ocr is specified with no argument, tesseract is used.
                  If tesseract fails (e.g. no language files found), GOCR
                  is used.  The overall default operation of k2pdfopt is
                  -ocr m.  See also -ocrvis and -ocrhmax.
                  NOTE:  Turning on OCR will disable native PDF output.
                  DISCLAIMER:  The main intent of OCR isn't to improve the
                      visual quality of the text at all--at least not the way
                      k2pdfopt does it.  OCR is most useful on scanned PDFs
                      that don't have selectable text to begin with, but using
                      OCR with k2pdfopt on such documents doesn't change the
                      look of the output PDF file at all.  The OCR text is
                      simply placed invisibly over the scanned text so that
                      you appear to be able to select the scanned text (when,
                      in fact, you are selecting the invisibly placed OCR

Press <ENTER> to continue (q to quit).Command Line Options (cont'd)
-----------------------------
                      text).  So the only time you will even notice the OCR
                      errors is if you try to search for a word and can't find
                      that word because the OCR of that word is incorrect, or
                      if you copy a selection of the OCR text and paste it
                      into something else so that you can actually see it.
-ocrcol <n>       If you are simply processing a PDF to OCR it (e.g. if you
                  are using the -mode copy option) and the source document has
                  multiple columns of text, set this value to the number of
                  columns to process (up to 4).  Default is to use the same
                  value as -col.











Press <ENTER> to continue (q to quit).Command Line Options (cont'd)
-----------------------------
-ocrd w|l|c|p     Set OCR detection type for k2pdfopt and Tesseract.  <type>
                  can be word (w), line (l), columns (c), or page (p).  Default
                  is line.
                  For -ocrd w, k2pdfopt locates each word in the scanned
                  document and passes individual words to Tesseract for
                  OCR conversion.  This was the only type of detection before
                  v2.42 but is not an optimal OCR conversion method when
                  using Tesseract.
                  For -ocrd l, k2pdfopt passes each line of the converted
                  file to Tesseract for conversion.  This typically gives
                  better results than -ocrd w since Tesseract can better
                  determine the text baseline position with a full line.
                  For -ocrd c, k2pdfopt detects each column of the converted
                  file and passes that to Tesseract for conversion.
                  For -ocrd p, k2pdfopt passes the entire output page of text
                  to Tesseract and lets Tesseract parse it for word positions.
                  Tesseract has done considerable code development for
                  detecting words on pages (more than k2pdfopt), so this
                  should also be a reliable way to create the OCR layer.
                  One drawback to -ocrd c or -ocr p is that there is no benefit

Press <ENTER> to continue (q to quit).Command Line Options (cont'd)
-----------------------------
                  to using the OCR multithreading option (see -nt).
-ocrhmax <in>     Set max height for an OCR'd word in inches.  Any graphic
                  exceeding this height will not be processed with the OCR
                  engine.  Default = 1.5.  See -ocr.

















Press <ENTER> to continue (q to quit).Command Line Options (cont'd)
-----------------------------
-ocrlang <lang>|? Select the Tesseract OCR Engine language.  This is the
                  root name of the training data, e.g. -lang eng for English,
                  -ocrlang fra for French, -ocrlang chi_sim for simplified
                  Chinese.  You can also use -l.  The default language is
                  whatever is in your Tesseract trained data folder.  If you
                  have more than one .traineddata file in that folder, the
                  one with the most recent time stamp is used.
                  NOTE 1: As of v2.52, k2pdfopt will download training files
                  from github as needed.  You can append -fast to the training
                  file name to get the fast version, otherwise the best version
                  will be downloaded.  If the default url fails, you can
                  specify the URL (folder name) in the environment variables
                  TESSDATA_URL and TESSDATAFAST_URL, e.g.
                  set TESSDATA_URL=https://raw.githubusercontent.com/tesseract-ocr/tessdata_best/master
                  You will be prompted to approve downloads unless you specify
                  the -y command-line option.
                  NOTE 2: Use -ocrlang ? to see the list of Tesseract language
                  files in your Tesseract data folder and available for
                  download.
                  NOTE 3: Using the -ocrvis t option will not show the OCR text

Press <ENTER> to continue (q to quit).Command Line Options (cont'd)
-----------------------------
                  correctly for any character above unicode value 255 since
                  k2pdfopt does not use any embedded fonts, but the text
                  will convert to the correct Unicode values when copy /
                  pasted.
                  NOTE 4: Tesseract allows the specification of multiple
                  language training files, e.g. -ocrlang eng+fra would
                  specify English as the primary and French as the secondary
                  OCR language.  In practice I have not found this to work
                  very well.  Try multiple languages in different orders.












Press <ENTER> to continue (q to quit).Command Line Options (cont'd)
-----------------------------
-ocrdpi <dpi>     Set the desired dpi of the bitmaps passed to the OCR engine
                  OR set the desired height of a lower case letter (e.g. 'e')
                  in pixels.  If <dpi> is positive, it is interpreted as dpi.
                  If <dpi> is negative, the absolute value is interpreted as
                  a lowercase letter height in pixels.  Any bitmapped text sent
                  to the OCR engine will be downsampled (if too large) so that
                  the appropriate dpi or lowercase letter size is achieved.
                  The default is 300 because I've found this works best
                  empirically for Tesseract v4.0.0 English OCR with font sizes
                  in the range 8 - 15 pts.  Use a lower value if the font size
                  in your document is larger than 15 - 20 pts.  Or use
                  -ocrdpi -24 if you have a wide range of font sizes.
                  Use -ocrdpi 0 to disable any downsampling.
-ocrout[-] <namefmt>  Write [don't write] UTF-8 OCR text output to file
                  <namefmt>.  See the -o option for more about how
                  <namefmt> works.  Default extension is .txt.  Default is
                  no output.




Press <ENTER> to continue (q to quit).Command Line Options (cont'd)
-----------------------------
-ocrsort[-]       When a PDF document has its own OCR/Text layer, this option
                  orders the OCR text layer by its position on the page.  This
                  should not be necessary unless the OCR layer was very poorly
                  generated.  Default is -ocrsort- (off).
-ocrsp[+|-]       When generating the OCR layer, do an entire row of text at
                  once, with spaces between each words.  By default (-ocrsp-),
                  each word is placed separately in the PDF document's OCR
                  layer.  This causes problems with text selection in some
                  readers (for example, individual words cannot be selected).
                  Using -ocrsp- may fix behavior like this, but will result in
                  less accurate word placement since k2pdfopt does not try to
                  exactly match the font used by the document.  Use -ocrsp+
                  to allow more than one space between each word in the row
                  of text in order to optimize the selection position.







Press <ENTER> to continue (q to quit).Command Line Options (cont'd)
-----------------------------
-ocrvbb[-]        Verify OCR bounding boxes.  For PDF files that have a built-
                  in OCR layer, if the resulting text selection does not seem to
                  match the graphical word positions in the document, you can
                  try this option.  It checks the bounding box for each word
                  from the OCR layer against the actual graphical placement of
                  the word in the document and "shrinks" the bounding box to
                  just fit around the word.  This only affects non-native PDF
                  conversions.  Default is -ocrvbb- (turned off).
-ocrvis <s|t|b>   Set OCR visibility flags.  Put 's' to show the source doc,
                  't' to show the OCR text, and/or 'b' to put a box around
                  each word.  Default is -ocrvis s.  To show both the source
                  document and the OCR text overlayed on top:  -ocrvis st.
                  See also -ocr.  See also -ocrlang (the note about -ocrvis t).
-odpi <dpi>       Set pixels per inch of output screen (def=167). See also
                  -dr, -w, -h, -fc.  You can also use -dpi for this.
                  See also -fs, -mag.





Press <ENTER> to continue (q to quit).Command Line Options (cont'd)
-----------------------------
-om[b|l|r|t] <val>[<units>][,<val>[units][,...]]  Set the blank area margins
                  on the output device.  Works very much like the -m option.
                  See -m for more about the syntax.  Default = 0.02 inches.
                  Note that the 's', 't', and 'x' units for -om all behave
                  the same and scale to the device size.  E.g. -om 0.1s will
                  make the device screen margins 0.1 times the device width
                  (for the left and right margins) or height (for the top and
                  bottom margins) of the output device screen.
-ow[-|+] [<mb>]   Set the minimum file size (in MB) where overwriting the
                  file will not be done without prompting.  Set to -1 (or
                  just -ow with no value) to overwrite all files with no
                  prompting.  Set to 0 (or just -ow-) to prompt for any
                  overwritten file.  Def = -ow 10 (any existing file
                  over 10 MB will not be overwritten without prompting).
                  Use the + option (-ow+) to rename the existing file
                  instead of overwriting it.  Existing files will be renamed
                  as follows:
                      file_k2pdfopt.pdf --> file_k2pdfopt_old<nnnn>.pdf
                  See also -y option.


Press <ENTER> to continue (q to quit).Command Line Options (cont'd)
-----------------------------
-p <pagelist>     Specify pages to convert.  <pagelist> must not have any
                  spaces.  E.g. -p 1-3,5,9,10- would do pages 1 through 3,
                  page 5, page 9, and pages 10 through the end.  The letters
                  'e' and 'o' can be used to denote even and odd pages, e.g.
                      -p o,e        Process all odd pages, then all even ones.
                      -p 2-52e,3-33o    Process 2,4,6,...,52,3,5,7,...,33.
                  Overridden by -px option.  See -px.
-pad <padlist>    A shortcut for -pl, -pt, -pr, -pb.  E.g. -pad 15,10,13,20
                  is the same as -pl 15 -pt 10 -pr 13 -pb 20.  Also, using
                  -pad 15 will set all pads to 15, for example.
-p[b|l|r|t] <nn>  Pad [bottom|left|right|top] side of destination bitmap with
                  <nn> rows.  Defaults = 4 (bottom), 0 (left), 3 (right), and
                  0 (top).  Example:  -pb 10.  This is typically only used on
                  certain devices to get the page to come out just right.  For
                  setting margins on the output device, use -om. See also -pad.
-png              (Default) Use PNG compression in PDF file.  See also -jpeg.





Press <ENTER> to continue (q to quit).Command Line Options (cont'd)
-----------------------------
-ppgs[-]          Post process [do not post process] with ghostscript.  This
                  will take the final PDF output and process it using
                  ghostscript's pdfwrite device (assuming ghostscript is
                  available).  A benefit to doing this is that all "invisible"
                  and/or overlapping text regions (outside cropping areas) get
                  completely removed, so that text selection capability is
                  improved.  The actual ghostscript command used is:
                  gs -dSAFER -dBATCH -q -dNOPAUSE -sDEVICE=pdfwrite
                     -dPDFSETTINGS=/prepress -sOutputFile=<outfile>
                     <srcfile>
                  The default is not to post process with ghostscript.
-px <pagelist>    Exclude pages from <pagelist>.  Overrides -p option.  Default
                  is no excluded pages (-px -1).
-r[-]             Right-to-left [left-to-right] page scans.  Default is
                  left to right.  See also -go option.






Press <ENTER> to continue (q to quit).Command Line Options (cont'd)
-----------------------------
-rhmin <points>   Row Height Minimum.  This sets the minimum height that any
                  text row or text-row-like object can be, in points.  If
                  the object is less than this height, it will be ignored
                  in the converted file for the processes of formatting.
                  The default is -1 (which means it is not used).
                  This is an experimental option (as of v2.52).
-rsf <val>        Row Split Figure of merit (expert mode).  After k2pdfopt has
                  looked for gaps between rows of text, it will check to see
                  if there appear to be missed gaps (e.g. if one row is twice
                  the height of all the others).  Increasing this value makes
                  it harder for k2pdfopt to split a row.  Lowering it makes it
                  easier.  Default value = 20.









Press <ENTER> to continue (q to quit).Command Line Options (cont'd)
-----------------------------
-rt <deg>|auto[+]|aep  Rotate source page counterclockwise by <deg> degrees.
                  NOTE: If you're trying to get "landscape" output so that
                  you can turn your reader on its side, use -ls instead of
                  -rt.  The -rt option is intended to be used for when your
                  source PDF is incorrectly rotated--e.g. if you view it on
                  a standard PC reader and it comes up sideways.
                  <deg> can be 90, 180, 270.  Or use "-rt auto" to examine up
                  to 10 pages of each file to determine the orientation used
                  on the entire file (this is the default).  Or use "-rt aep"
                  to auto-detect the rotation of every page.  If you have
                  different pages that are rotated differently from each other
                  within one file, you can use this option to try to auto-
                  rotate each source page.  Use -rt auto+ to turn on auto-
                  detect even in preview mode (otherwise it is off).
                  See also -ls.
-s[-]             Sharpen [don't sharpen] images.  Default is to sharpen.





Press <ENTER> to continue (q to quit).Command Line Options (cont'd)
-----------------------------
-sm[-]            Show [don't show] marked source.  This is a debugging tool
                  where k2pdfopt will mark the source file with the regions it
                  finds on them and the order in which it processes them and
                  save it as <srcfile>_marked.pdf.  Default is not to show
                  marked source.  Red regions are found on the first pass
                  (use -f2p -2 to put each red region on a separate page).
                  Green lines mark vertical regions affected by -vb and -vs.
                  Gray lines mark individual rows of text (top, bottom, and
                  baseline).  Blue boxes show individual words (passed to OCR
                  if -ocr is specified).
-sp[-]            For each file on the command-line, just echo the number
                  of pages--don't process.  Default = off (-sp-).
-t[-]             Trim [don't trim] the white space from around the edges of
                  any output region.  Default is to trim.  Using -t- is not
                  recommended unless you want to exactly duplicate the source
                  document.





Press <ENTER> to continue (q to quit).Command Line Options (cont'd)
-----------------------------
-title <title>    Set the title metadata / property of the PDF output file(s).
                  Default is to use the title of the source document
                  (-title "").  The <title> string will be parsed for
                  special characters that allow you to substitute the file
                  name.  See the -o option for a description of these
                  substitutions.
-to[-]            Text only output.  Remove figures from output.  Figures are
                  determined empirically as any contiguous region taller than
                  0.75 inches (or you can specify this using the -jf option).
                  Use -to- to turn off (default).
-toc[-]           Include [don't include] table of contents / outline /
                  bookmark information in the PDF output if it is available
                  in the source file (works only for PDF source files and
                  only if MuPDF is compiled in).  By default, a new destination
                  page is started at each bookmark location.  Do disable this,
                  see the -bp option.  If -toc- is specified, bookmark
                  information from the source file is ignored.  See also
                  -toclist.  Default is -toc.



Press <ENTER> to continue (q to quit).Command Line Options (cont'd)
-----------------------------
-toclist <pagelist>|<file>  Override the PDF source file's outline information
                  (bookmarks / table of contents) with either a list of source
                  pages or a file describing the table of contents. If you
                  specify a list of pages, e.g. -toclist 5,10,20,40,100
                  then those pages are marked as Chapter 1, 2, etc.,
                  respectively.  If you specify a file name, the file should be
                  a text file formatted like this example:
                      1 Introduction
                      10 Chapter 1
                      +10 Chapter 1, Part A
                      +25 Chapter 1, Part B
                      ++25 Chapter 1, Part B, Subsection 1
                      ++27 Chapter 1, Part B, Subsection 2
                      +30 Chapter 1, Part C
                      50 Chapter 2
                      70 Chapter 3
                  The '+' indicates a sub-level heading (multiple +'s for
                  multiple sub-levels).  The first number on the line is the
                  source page reference number.  The rest of the text on the
                  line is the name of the chapter / subheading.

Press <ENTER> to continue (q to quit).Command Line Options (cont'd)
-----------------------------
                  Note:  This option overrides -toc.  To get a template from
                  an existing PDF file, see the -tocsave option.
-tocsave <file>   If an outline exists in the PDF file (and -toc is specified)
                  write that outline to text file <file> in the format required
                  by -toclist.  See -toc, -toclist.
-ui[-]            User input query turned on [off].  Default = on for linux or
                  if not run from command line in Windows.
-v                Verbose output.
-vb <thresh>      Set gap-size vertical-break threshold between regions that
                  cause them to be treated as separate regions.  E.g. -vb 2
                  will break the document into separate regions anywhere
                  there is a vertical gap that exceeds 2 times the median
                  gap between lines of text.  These separate regions may
                  then be scaled and aligned independently.
                  Special values:  Use -vb -1 to preserve all horizontal
                  alignment and scaling across entire regions (vertical
                  spacing may still be adjusted).  Use -vb -2 to exactly
                  preserve each region (both horizontal alignment and
                  vertical spacing--this is the value used by -mode fw, for
                  example).  The default is -vb 1.75.

Press <ENTER> to continue (q to quit).Command Line Options (cont'd)
-----------------------------
-vls <spacing>    Set vertical line spacing as a fraction of the text size.
                  This can be used to override the line spacing in a document.
                  If 1, then single spacing is used.  2 = double spacing.
                  If negative, then the absolute value acts as the limiting
                  case.  E.g., if you set -vls -1.5, then any the line
                  spacing of the original document is preserved unless it
                  exceeds 1.5 (times single spacing).  Default = -1.2.
                  See also -vs.
-vs <maxgap>      Preserve up to <maxgap> inches of vertical spacing between
                  regions in the document (marked in green when using -sm
                  option).  This value has no effect if you use a negative
                  value for -vb.  The default value is 0.25.
                  See also -vls, -vb.
-w <width>[in|cm|s|t|p] Set width of output device.  Default is 560.  See -h.







Press <ENTER> to continue (q to quit).Command Line Options (cont'd)
-----------------------------
-wrap[-|+]        Enable [disable] text wrapping.  Default = enabled.  If
                  -wrap+, regions of text with lines shorter than the mobile
                  device screen are re-flowed to fit the screen width.  If
                  you use -wrap+, you may want to also specify -fc- so that
                  narrow columns of text are not magnified to fit your device.
                  Text wrapping disables native PDF output (see -n option).
                  See also -ws, -j, -fc, -n.
-ws <spacing>     Set minimum word spacing for line breaking as a fraction of
                  the height of a lowercase 'o'.  Use a larger value to make it
                  harder to break lines.  If negative, automatic word spacing
                  is turned on.  The automatic spacing leans toward breaking
                  long words between letters to be sure to fit text to the
                  device display.  Def = -0.20.  The absolute value of the
                  setting, if negative, is used as a minimum allowed value.
                  If you want k2pdfopt to aggressively break lines (e.g. break
                  apart long words if they don't fit on a line), use a smaller
                  absolute value, e.g. -ws -0.01.  A positive value works as
                  it did in v2.18 and before.  The default value was changed
                  from 0.375 in v2.18 to -0.20 in v2.20.  See also -wrap.


Press <ENTER> to continue (q to quit).Command Line Options (cont'd)
-----------------------------
-wt[+] <thresh>   Any pixels whiter than <thresh> (0-255) are treated
                  as "white".  Setting this lower can help k2pdfopt better
                  process some poorly-quality scanned pages or pages with
                  watermarks.  Note that the pixels which are above <thresh>
                  threshold value and therefore are treated as white are not
                  actually changed to pure white (255) unless the '+' is also
                  included.  Otherwise, this only sets a threshold.
                  The default value for -wt is -1, which tells k2pdfopt to pick
                  the optimum value.  See also -cmax, -colorfg, -colorbg.
-x[-]             Exit [don't exit--wait for <Enter>] after completion.
-y[-]             Assume [don't assume] "yes" to queries, such as whether
                  to overwrite a file.  See also -ow.  Also turns off any
                  warning messages.








Press <ENTER> to continue (q to quit).Press <ENTER> to exit.
```
