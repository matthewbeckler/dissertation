BASE=dissertation

SVGFILES := $(wildcard figures/*.svg)
PDFFILES := $(SVGFILES:.svg=.pdf)

all: figs
	pdflatex ${BASE}.tex
	bibtex ${BASE}
	pdflatex ${BASE}.tex
	echo "--------------------------------------------------------------------------------"
	pdflatex ${BASE}.tex
	rm *.aux

view: all
	evince ${BASE}.pdf

chrome: all
	google-chrome ${BASE}.pdf

figs: $(PDFFILES)

%.pdf: %.svg
	inkscape --file=$< --export-pdf=$@

clean:
	rm -rf *.bbl *.blg *.aux *.log *.loa *~ *.bak ${BASE}.ps ${BASE}.dvi ${BASE}.log ${BASE}.pdf *.bak *.cb *.lof *.toc *.lot ${BASE}.out figures/*.pdf figures/*.png

spell:
	ispell -f ispell.words -t `ls *.tex | grep -v ${BASE}.tex`

todo:
	grep --color=auto -i todo *.tex

notes:
	echo "pdftk ${BASE}.pdf cat x-y output chapter_whatever.pdf"
	echo "detex chap-intro.tex > temp.txt"

